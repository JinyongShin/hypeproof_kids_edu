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

**볼트 구조 정렬 완료 + .raw 정비**
- wiki/wiki-ingest/wiki-query/wiki-lint 스킬 철학과 볼트 구조 갭 해소
- `sources/`, `questions/` 폴더 신설, dead link 4개 복구, orphan 39개 index 등록
- meeting_notes/ 전체 `.raw/meeting_notes/`로 복사 완료
- 미ingest 파일 `2026-04-21-hospital-inquiry-draft.md` ingest 완료

**SK바이오팜 × 비트리 파일럿 확정 (2026-05-14)**
- 대상: 약 15~20가족, 6~7월 토요일 Biweekly, SK바이오팜 10층 내부 카페
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
| 2026-05-말 | SK바이오팜 수요조사용 제안서 제출 |
| 2026-06-01 | Studio v0.1 release + 가족 안내 메일 |
| 2026-06 (2~3주) | SK바이오팜 1회차 |

---

## 핵심 페이지

- [[2026-04-21-hospital-inquiry-draft]] — 국립암센터 사전 확인 요청 초안 (방금 ingest)
- [[2026-05-12-sk-biopharma-meeting]] · [[2026-05-14-sk-biopharma-followup]]
- [[sk-biopharma]] · [[bitree]] · [[oh-sungeun]]
- [[hypeproof-studio]] · [[adr-hypeproof-studio-v01]] · [[sixteen-essence]]
- [[sk-biopharma-pilot]]

---

## 스택 요약

| 레이어 | 기술 |
|---|---|
| 백엔드 | FastAPI + LangGraph + Gemini 2.5 Flash |
| 프론트 | Next.js (App Router) |
| 관측성 | Langfuse v2 self-hosted |
| 교육 도구 | HypeProof Studio v0.1 (예정) / Cline (Plan B) |
