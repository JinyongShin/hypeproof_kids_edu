---
type: spec
title: "LLM 스케일링 — 페이즈별 테스트 계획"
created: 2026-04-28
updated: 2026-04-28
status: draft
priority: 0
tags:
  - spec
  - pilot/5-5
  - infra/llm
  - load-test
related:
  - "[[llm-provider-scaling]]"
  - "[[load-test]]"
---

# LLM 스케일링 — 페이즈별 테스트 계획

상위 결정: [[llm-provider-scaling]]. 이 문서는 그 결정을 검증하는 **페이즈 0~5 실행 매뉴얼**.

## 합격 기준 (모든 페이즈 공통)

| 메트릭 | 목표 |
|---|---|
| p50 latency | < 4초 |
| p95 latency | < 8초 |
| 에러율 (5xx + timeout) | < 5% |
| 폴백 체인 트리거 시 사용자 체감 중단 | 0회 |
| TOS 경고 / throttle 알림 | 0회 |

`src/backend/load_test.py`를 확장해서 **동시 40명 × 5턴 × 30초 간격** 시나리오를 실행. 출력 = JSON 메트릭 + [[load-test]] 페이지 자동 업데이트.

## 페이즈 순서 — Cheapest first, signal-richest first

### Phase 0 — 베이스라인 (현재 GLM, 30분)

**목적**: "아무것도 안 했을 때" 객관 데이터 확보. 이후 모든 비교의 기준.

**실행**
```bash
cd src/backend
uv run python load_test.py --provider glm --concurrent 5,10,20,40 --turns 5 --interval 30
```

**기록**: 첫 실패 동시 사용자 수, p95 latency, 에러 패턴. [[load-test#phase-0]] 섹션에 표로.

**의미**: 여기서 GLM이 의외로 견디면 추가 작업 우선순위 재산정. 안 견디면 페이즈 1 즉시.

---

### Phase 1 — Gemini 단일 키, 40 concurrent (1시간)

**목적**: **여기서 끝날 가능성이 가장 높다.** 1키로 40명이 통과하면 풀링 불필요.

**선행 작업**
1. `pyproject.toml`에 `google-genai` 추가 → `uv sync`
2. `genai_runner.py`에 `_gemini_chat()` 1차 함수 추가 (단일 키)
3. `.env.example`에 `GEMINI_API_KEY` 추가

**실행**
```bash
uv run python load_test.py --provider gemini --concurrent 40 --turns 5
```

**합격**: p95 < 8s, 에러 < 5%, 429(rate limit) 발생 0건.
**불합격 (429 발생)**: 페이즈 2 진행.
**불합격 (latency 폭발)**: 모델 변경 (Flash → Flash-Lite) 또는 프롬프트 길이 축소 검토.

---

### Phase 2 — Gemini 4-키 라운드로빈 풀 (1시간)

**목적**: 페이즈 1이 RPM에서 막혔을 때만 진행.

**구현 요점**
- 키 풀 자료구조: 환경변수 `GEMINI_API_KEYS`(콤마 구분 4개) → 리스트로 파싱.
- **Sticky by session_id**: 같은 child의 연속 호출은 같은 키 → prompt caching 활용 + 디버깅 단순화.
- `hash(session_id) % len(keys)` 단순 분배.
- 429 받으면 다음 키로 즉시 재시도 (3회 시도 후 다음 폴백).
- 키별 RPM 카운터 in-memory (리셋 1분).

**실행**
```bash
GEMINI_API_KEYS=key1,key2,key3,key4 uv run python load_test.py --provider gemini-pool --concurrent 40
```

**합격 기준 동일.**

---

### Phase 3 — Claude Max 20x 단일 어카운트 (옵셔널, 2시간)

**진행 조건**: 페이즈 1 또는 2가 통과한 뒤 "품질 폴백" 옵션을 만들고 싶을 때만.

**중요**: **Max 어카운트 4개 중 메인 1개를 절대 쓰지 말 것.** 망쳐도 되는 어카운트 1개로 시도. 어뷰즈 탐지 시 그 어카운트만 잃기.

**선행 작업**
1. `pyproject.toml`에 `claude-agent-sdk` 추가
2. `genai_runner.py`에 `_claude_subscription_chat()` 추가 (Agent SDK 경로)
3. `.env.example`에 `ANTHROPIC_AUTH_MODE=subscription` 옵션 추가

**실행**
```bash
ANTHROPIC_AUTH_MODE=subscription uv run python load_test.py --provider claude --concurrent 40
```

**관찰 포인트**
- 429 / TOS 경고 발생 여부
- p95 latency (Claude는 1~5초 예상)
- OAuth refresh 안정성 (5시간 윈도우 경계)

**결과별 분기**
- 무사 통과 → Claude를 품질 폴백으로 채택 (`"멋진 카드 만들어줘"` 같은 명시 옵션).
- throttle / 경고 → **Max는 dev/QA 전용**으로 강등. 운영 미사용.

---

### Phase 4 — 폴백 체인 통합 (1시간)

**목적**: 단일 공급자 결과를 종합해 폴백 체인을 코드로 구현 + 검증.

**구현**
```python
# genai_runner.py
async def generate_card(prompt, child_id, session_id):
    for provider in CHAIN:  # ["gemini", "claude_api", "glm", "pollinations"]
        try:
            async for event in provider.stream(prompt, ...):
                yield event
            return
        except (RateLimitError, ProviderError) as e:
            logger.warning("provider %s failed: %s, falling back", provider.name, e)
            continue
    yield static_fallback_card()  # 정적 폴백 (R4)
```

**검증 방법** — failover를 일부러 트리거:
1. 1차 키를 잘못된 값으로 교체 → 2차로 넘어가는지
2. 2차도 잘못된 값 → 3차로
3. 사용자 체감 latency 측정 (1차 실패 → 2차 응답까지 < 5초 목표)

**합격**: 모든 fallover가 자동 + 사용자 체감 중단 없음.

---

### Phase 5 — 드레스 리허설 (D-1, 90분)

**목적**: 실제 워크샵 시나리오 그대로 40명 시뮬. **여기서 처음 발견되는 버그는 D-day에 못 고친다.**

**시나리오** (각 시뮬 사용자)
1. 로그인 (`child_NN`)
2. 캐릭터 카드 생성 (3종 다른 프롬프트 중 랜덤)
3. 세계 카드 생성 (4종 중 랜덤)
4. 게임 생성 ("이 캐릭터로 게임 만들어줘")
5. 저장 클릭
6. 갤러리 페이지 로드

**실행**
```bash
uv run python load_test.py --scenario full-workshop --users 40 --duration 30m
```

**합격 기준**
- 모든 사용자가 6단계 모두 완료 (timeout 0건)
- 갤러리에 40개 게임 모두 등록됨
- 운영자 화면(사이드바·갤러리 버튼·저장 상태)이 의도대로 작동
- 5분간 모니터링하며 백엔드 로그 에러 0건

**불합격**: 발견 버그 우선순위 분류 → 24시간 내 수정 → 재실행.

## 결과 기록

각 페이즈 완료 후 [[load-test]] 페이지에 다음 형식으로 추가:

```
## Phase N (YYYY-MM-DD)
- 환경: provider=X, concurrent=Y, turns=Z
- p50: 1.2s / p95: 3.4s / max: 8.1s
- 에러율: 2.1% (timeout 1건, 429 0건)
- 결정: 합격 / 불합격 + 다음 액션
- raw 데이터: `data/load-test/phase-N-YYYYMMDD.json`
```

## 일정 (제안)

```
Day 0 (오늘):     Phase 0 + Phase 1 코드 통합 (구현)
Day 1:            Phase 1 부하 측정 + 결과 기록
Day 2:            Phase 2 (필요시) + Phase 3 (옵션)
Day 3:            Phase 4 폴백 체인 + 자동 failover 검증
Day 4 (D-1):      Phase 5 드레스 리허설
Day 5 (D-day):    파일럿 실행
```

## 책임

- 구현: [[implementer]]
- 측정 / 결과 기록: [[implementer]] + [[reviewer]] (메트릭 검증)
- 게이트 의사결정: [[jinyong-shin]]

## 의존

- ANTHROPIC_API_KEY 발급 (페이즈 4 실행 전)
- Gemini API 키 4개 정보 정리 (페이즈 1 실행 전)
- `load_test.py` 확장 (현재는 단일 시나리오만) — Day 0 필수
