---
type: meta
title: "Hot Cache"
created: 2026-04-12
updated: 2026-05-11
tags:
  - meta/cache
---

# Hot Cache — 2026-05-11

최근 컨텍스트 스냅샷. 세션 시작 시 가장 먼저 읽을 것.

---

## 커리큘럼 구조: 1트랙 멀티 스킨 (2026-05-11 전환)

> 3-트랙 구조 폐기 → **코어 1개 + 스킨 교체** 방식으로 전환.
> 상세: [[one-track-multi-skin]]

| 스킨 | 대상 | 상태 |
|---|---|---|
| 아동 | 초등생 | 5/5 파일럿 완료. 관찰 노트 ingest 필요 |
| 성인 (치과의사) | 직장인·전문직 | 5/26 보아치과 파일럿 준비 중 |
| 혼합 | 아동+성인 | 미착수 |

---

## 현재 우선순위

1. **5/26 보아치과 파일럿** — 치과의사 스킨 v3 + 진행자 스크립트 완성 상태. 원장님 AI 사례 1개 사전 확인 필요.
2. **아동 파일럿 관찰 노트 ingest** — 코어 v2 설계를 위한 선행 작업.
3. **스킨 구조 설계** — `specs/core/` + `specs/skins/` 파일 구조 재편, scaffold·페르소나 스킨 분리.

---

## Track B — 치과의사 워크샵 현황

- 커리큘럼: `specs/track-b/치과의사-curriculum-v3.md` ← **확정 버전**
- 진행자 스크립트: `specs/track-b/facilitator-script-dental-v3.md`
- v1·v2는 참고용으로 `specs/track-b/` 에 보관
- 관찰 데이터 준비: `validation/track-b/` (5/26 파일럿 후 적재 예정)

**5/26 전 필수 확인**: 원장님이 실제로 쓰는 AI 사례 1개 (블록 1용)

---

## Track A — 아동 워크샵 현황

- 커리큘럼: `specs/track-a/`
- 스택: FastAPI (Python/uv) + Next.js (App Router) + GLM-5 (z.ai)
- 핵심 assets: `src/frontend/lib/scaffoldData.ts`, `src/backend/personas/TUTOR.md`
- 파일럿 완료 → Production Loop Stage 1 진입 대기 (관찰 노트 ingest 필요)

---

## 제작 프로세스 (Production Loop)

파일럿 이후 모든 트랙에 적용. 상세: [[production-loop]]

- Stage 1 (인풋→설계): 관찰 노트 ingest + 교육 목표 정의
- Stage 2 (설계→기술피드백): scaffold·페르소나 봉호님 직접 작성
- Stage 3 (리허설→반영): 산출물·타이밍 수집 → vault 환류

---

## 핵심 ADR

- [[one-track-multi-skin]] — 1트랙 멀티 스킨 구조 채택 (2026-05-11) ← **현행**
- [[three-track-structure]] — 3-트랙 구조 (superseded)
- [[production-loop-adoption]] — 3단계 제작 루프 채택 (2026-05-05)
- [[stack-decision-after-curriculum]] — 커리큘럼 확정 후 스택 결정
- [[auth-session-game-persistence]] — status: implemented
- [[game-bug-fix-2026-05-01]] — 게임 버그 3종 수정 기록

---

## 핵심 파일 경로 (Track A 기술)

- `src/backend/genai_runner.py` — `_strip_code_for_chat()`, `generate_card()`
- `src/backend/main.py` — spec 추출·주입 로직 (~490번째 줄)
- `src/frontend/components/ChatPane.tsx` — 메시지 렌더 regex
- `src/frontend/components/GamePreview.tsx` — `showGame` 토글
- `src/backend/storage.py` / `src/frontend/hooks/useChat.ts`
