# Wiki-Lint 백로그 — 별도 세션 처리 항목

생성: 2026-05-15
상태: **B1·B3 완료 / B2 트리거 대기**
참조: `wiki/meta/lint-report-2026-05-15.md`

---

## B1. Unlinked Mentions — ✅ 완료

### 1차 (2026-05-15, 커밋 8362ef0) — PR 머지 전 처리

| 엔티티 | 처리 파일 | 링크 |
|--------|---------|------|
| `SK바이오팜` | sk-biopharma-pilot(4), hot(4), adr-hypeproof-studio-v01(2), sk-biopharma-meeting(3), sk-biopharma-followup(1), log(2) | `[[sk-biopharma]]` |
| `HypeProof Studio` | hot(1), adr-hypeproof-studio-v01(1), log(1) | `[[hypeproof-studio]]` |
| `비트리` | sk-biopharma-pilot(2), hot(1) | `[[bitree]]` |
| `봉호` | 이미 `봉호([[bongho-tae]])` 형태로 링크됨 — 스킵 | `[[bongho-tae]]` |
| `필라멘트리` | 이미 `[[filamentary]]` 링크됨 — 스킵 | `[[filamentary]]` |
| `16 Essence` | log(1) | `[[sixteen-essence]]` |

### 2차 (2026-05-15, PR#7 머지 후) — ✅ 완료

| 엔티티 | 처리 파일 | 링크 |
|--------|---------|------|
| `LangGraph` | hot(2), log(2) | `[[langgraph]]` (components/langgraph.md — PR#7에서 생성) |
| `Gemini` | hot(1), log(1) | `[[gemini-2-5-flash]]` |
| `Langfuse` | hot(2) | `[[langfuse-observability]]` |

---

## B2. log.md 아카이브 — ⏳ 트리거 대기

현재 줄 수 > 800 초과 시 실행.

**절차**:
1. 2026-04-12 이전 엔트리를 `wiki/log-archive-2026-q1.md`로 이동
2. `log.md` 상단에 `> [!note] 2026-04-12 이전 엔트리는 [[log-archive-2026-q1]] 참조` 추가
3. `index.md`에 `log-archive-2026-q1` 링크 추가

---

## B3. 빈 Heading 채우기 — ✅ 완료 (2026-05-15, 커밋 8362ef0)

| 파일 | 처리 |
|------|------|
| `deliverables/pilot-gemini-api-key.md` | 완료 메모 추가 |
| `deliverables/pilot-server-domain.md` | 완료 + Cloudflare 전환 메모 |
| `deliverables/pilot-oauth-setup.md` | status `delivered`→`in-progress`, SK바이오팜 컨텍스트 반영 |
| `deliverables/pilot-rehearsal-late-april.md` | status `delivered`→`deferred`, 소아암 일정 연기 사유 기록 |
| `specs/langfuse-observability.md` | 탐색 결과 모든 섹션 이미 채워짐 — 스킵 |
| `runbooks/pilot-day-operation.md` | 절차 섹션 존재, Open Questions는 운영 이슈로 별도 관리 — 스킵 |
