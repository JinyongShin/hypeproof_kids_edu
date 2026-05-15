---
type: meta
title: "Hot Cache"
created: 2026-04-12
updated: 2026-05-15
tags:
  - meta/cache
---

# Hot Cache — 2026-05-15

최근 컨텍스트 스냅샷. 세션 시작 시 가장 먼저 읽을 것.

---

## 현재 상태: SK바이오팜 파일럿 진입 + HypeProof Studio 개발 시작

### 가장 최근 작업 (2026-05-15)

**테스트 품질 3-Phase 개선 완료**
- Phase1: sys.path 잔재 삭제, anyio→asyncio 마커, tautology assertion 수정, fixture 중복 제거, 테스트명 수정
- Phase2: `test_card_node.py`·`test_spec_node.py` `_DATA_DIR` monkeypatch 파일시스템 격리
- Phase3: error 이벤트 테스트, 갤러리/rename/save 엔드포인트 커버리지, `backendUrl.test.ts` 신규(8개), `send()` 가드+payload 검증
- 현재 테스트: **111 BE + 19 FE = 130 tests 전체 통과**
- 상세: [[test-quality-review-2026-05-15]] (status: resolved)

**PR#7 `feature/langgraph-gemini` → main 머지 완료 (동일 세션)**
- ico1036 리뷰 3건 반영 + 이미 구현된 항목 코멘트 확인 처리
- 수정: `edit_code_node` 실패 피드백, `sys.path.insert` 7회→1회, [[langfuse-observability]] 시크릿 외부 주입, `.env.example` 추가
- main 현재 커밋: `75159ee`, 워크트리 및 `feature/langgraph-gemini` 브랜치 정리 완료

**[[sk-biopharma]] × [[bitree]] 파일럿 확정 (2026-05-14)**
- 대상: 약 15~20가족, 6~7월 토요일 Biweekly, [[sk-biopharma]] 10층 내부 카페
- 수업 단위: 4시간 × 2그룹/일

**HypeProof Studio v0.1 개발 결정**
- VS Code fork + 자체 chat panel (Track A / Track B 병렬)
- 5/28~30 dry-run이 Go/No-go 게이트

---

## 주요 임박 마일스톤

| 기한 | 내용 |
|---|---|
| 2026-05-15~30 | HypeProof Studio v0.1 빌드 |
| 2026-05-28~30 | 운영진 자녀 dry-run (4시간) — **게이트** |
| 2026-05-말 | [[sk-biopharma]] 수요조사용 제안서 제출 |
| 2026-06-01 | Studio v0.1 release + 가족 안내 메일 |
| 2026-06 (2~3주) | [[sk-biopharma]] 1회차 |

---

## 핵심 페이지

- [[test-quality-review-2026-05-15]] — 테스트 품질 검토 결과 (방금 생성)
- [[kids-edu-backend]] — 백엔드 컴포넌트 (LangGraph 구조 반영 업데이트)
- [[2026-05-12-sk-biopharma-meeting]] · [[2026-05-14-sk-biopharma-followup]]
- [[sk-biopharma]] · [[bitree]] · [[oh-sungeun]]
- [[hypeproof-studio]] · [[adr-hypeproof-studio-v01]] · [[sixteen-essence]]
- [[sk-biopharma-pilot]]

---

## 스택 요약

| 레이어 | 기술 |
|---|---|
| 백엔드 | FastAPI + [[langgraph]] + [[gemini-2-5-flash]] + SQLite |
| 프론트 | Next.js (App Router) |
| 관측성 | [[langfuse-observability]] v2 self-hosted |
| 교육 도구 | [[hypeproof-studio]] v0.1 (예정) / Cline (Plan B) |
| 테스트 | pytest 111개 (백엔드) · Vitest 19개 (프론트, 파일 2개) — 전체 통과 |
