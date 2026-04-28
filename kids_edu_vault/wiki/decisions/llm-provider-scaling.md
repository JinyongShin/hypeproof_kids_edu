---
type: decision
title: "LLM 공급자 스케일링 전략 — 40명 동시 부하 대응"
created: 2026-04-28
updated: 2026-04-28
status: proposed
priority: 0
tags:
  - decision
  - pilot/5-5
  - infra/llm
related:
  - "[[llm-scaling-test-plan]]"
  - "[[pivot-to-chat-preview-wrapper]]"
  - "[[load-test]]"
deciders:
  - "[[jinyong-shin]]"
---

# LLM 공급자 스케일링 전략

## 결정

파일럿 당일 40명 동시 사용자를 처리하기 위해 **Gemini API 4-키 풀을 1차 공급자**로 채택하고, **Claude API 키를 품질 폴백 / 안전망**으로, **GLM-5(현재) → Pollinations**를 추가 폴백으로 둔다. **Claude Max 20x 구독 4개는 풀로 사용하지 않고 1개만 dev/QA 용도로 사용**하며 나머지 3개는 Cold backup.

## 배경

- 현재 텍스트 LLM = `genai_runner.py`의 GLM-5 (z.ai) 1차 + Pollinations 폴백.
- 실측: GLM 응답 27~38초 (`[[qa-checklist-results]]`), 동시 처리 5~10명에서 큐 폭발 우려.
- 운영 자원: ① Gemini API 키 4개, ② Claude Max 20x 어카운트 4개, ③ GLM 구독 1개.
- D-day 부하: **40명 × 5턴 × ~6K 토큰 = ~1.4M 토큰 / 2시간 30분.**

## 근거

### 왜 Gemini 4-키 풀이 1차인가
- **API 키 멀티는 공급자 의도된 패턴**. RPM 한도 명시·표준 풀링.
- Gemini 2.x Flash latency 1~3초 (GLM 30초 대비 10배 빠름).
- 무료 티어 RPM 15/key × 4 = 60 RPM concurrent → 40명 워크샵 여유.
- TOS 명확 — 멀티테넌트 / 자동화 허용.

### 왜 Claude Max 20x ×4를 풀로 안 쓰는가
- **TOS 회색지대**: 구독은 개인 사용 전제. 4개 동시 어뷰즈 탐지 시 4개 동시 잠김 (같은 결제수단·IP·디바이스 지문).
- **Concurrent 보장 없음**: 4×개인 ≠ 4×concurrent.
- **OAuth 4컨텍스트 운영 부담**: token refresh, 세션 격리, 디버깅 비용.
- **단일 실패점**: 한 어카운트 throttle 시 전체 풀 신뢰도 동시에 깨짐.
- → **품질 옵션 / 폴백 / dev** 용도로만 사용.

### 왜 폴백 체인을 이중삼중으로 두는가
- 워크샵 2시간 30분 동안 **어떤 한 공급자도 무중단 보장 못 함**.
- R4(완성 보장) 요구사항: 아이가 빈손으로 나가는 케이스 0%.
- 폴백 통과 검증을 D-1에 강제로 트리거해서 검증.

## 폴백 체인 (운영 시)

```
1차: Gemini 2.x Flash (4-key round-robin, sticky-by-session)
2차: Claude API (Sonnet 4.6, prompt caching) — API 키 별도 발급
3차: GLM-5 (z.ai, 현재 코드 유지)
4차: Pollinations (현재 코드 유지)
5차: 정적 폴백 카드 / `game_template.py` 기본 빌드 — 이미 구현
```

## 안 할 것 (안티패턴)

- ❌ Max 20x × 4를 hot pool로 묶기 — 어뷰즈 탐지 + 디버깅 지옥.
- ❌ 4개 공급자를 동시에 통합 후 부하 테스트 — 어디가 깨졌는지 분리 불가.
- ❌ 측정 없이 최적화 — 베이스라인 없이는 "나아졌다" 검증 불가.
- ❌ D-day까지 부하 검증 미루기 — 발견-수정-재검증 사이클이 최소 1일.

## 위임 / 책임

- 구현: [[implementer]] (`genai_runner.py`에 분기 + 4-키 풀 + 자동 폴백)
- 부하 테스트: `src/backend/load_test.py` 확장 (40 concurrent + 폴백 트리거 시나리오)
- 결과 기록: [[load-test]] 페이지 갱신
- 의사결정 게이트: 페이즈 1 결과 → 단일 키로 충분하면 페이즈 2 스킵

## 실행 — `[[llm-scaling-test-plan]]` 참조

페이즈 0~5 단계별 테스트 계획. 합격 기준: **p95 latency < 8초 + 에러율 < 5% @ 40 concurrent**.

## 회수 조건 (Rollback)

- 페이즈 4 폴백 체인 통합 검증 실패 시 → 1차를 GLM(현재)으로 되돌리고 인원 축소 재협상 (`[[filamentary]]` 사전 통보).
- D-1 드레스 리허설에서 신규 공급자 통합 미완 시 → 현재 GLM 단일 구성 + 인원 30명 이하로 축소 백업안 발동.

## 영향

- 추가 비용: API 키 발급 시 deposit ~$5, 파일럿 1회 실비용 $1~3 예상.
- 코드 변경 범위: `genai_runner.py` 단일 파일 + `pyproject.toml` SDK 추가 + `.env.example` 키 추가.
- 운영 절차: `[[deployment]]` runbook + `pilot-deploy` 스킬에 `ANTHROPIC_API_KEY` / `GEMINI_API_KEY` 4개 prompt 추가.

## 다음 액션 (Post-PR)

- [ ] `ANTHROPIC_API_KEY` 발급 (`console.anthropic.com`)
- [ ] Gemini API 4키 키 정보 정리 (각 키의 RPM tier 확인)
- [ ] 페이즈 0~1 실행 (베이스라인 + Gemini 단일 키 부하)
- [ ] 결과에 따라 [[llm-scaling-test-plan]] 다음 페이즈 진행
