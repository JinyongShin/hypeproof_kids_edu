---
type: meta
title: "Hot Cache"
created: 2026-04-12
updated: 2026-05-05
tags:
  - meta/cache
---

# Hot Cache — 2026-05-05

최근 컨텍스트 스냅샷. 세션 시작 시 가장 먼저 읽을 것.

---

## 현재 상태

- **Track A**: 소아암 병동 파일럿 2026-05-05 완료 (국립암센터, 40명). 관찰 결과 미ingest.
- **Track B**: 보아치과 파일럿 2026-05-26 예정. 커리큘럼 v3 + 진행자 스크립트 완성.
- **Track C**: 미착수.

---

## 3-트랙 구조 (2026-05-05 확정)

| 트랙 | 대상 | 상태 | 다음 스텝 |
|---|---|---|---|
| Track A | 아동 | 파일럿 완료 | 관찰 노트 ingest → v2 설계 |
| Track B | 성인 (치과의사) | 5/26 파일럿 준비 중 | 원장님 사례 사전 확인 |
| Track C | 아동+성인 혼합 | 미착수 | A·B 안정 후 시작 |

상세: [[three-track-structure]]

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

- [[three-track-structure]] — 3-트랙 구조 확정 (2026-05-05)
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
