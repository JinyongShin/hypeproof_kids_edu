# Wiki-Lint 백로그 — 별도 세션 처리 항목

생성: 2026-05-15
상태: 일부 완료
참조: `wiki/meta/lint-report-2026-05-15.md`

---

## B1. Unlinked Mentions — wikilink 추가

### ✅ 완료 (2026-05-15, 커밋 8362ef0)

| 엔티티 | 처리된 파일 | 대상 링크 |
|--------|-----------|-----------|
| `SK바이오팜` | sk-biopharma-pilot(4), hot(4), adr-hypeproof-studio-v01(2), sk-biopharma-meeting(3), sk-biopharma-followup(1), log(2) | `[[sk-biopharma]]` |
| `HypeProof Studio` | hot(1), adr-hypeproof-studio-v01(1), log(1) | `[[hypeproof-studio]]` |
| `비트리` | sk-biopharma-pilot(2), hot(1) | `[[bitree]]` |
| `봉호` | log.md — 이미 `봉호([[bongho-tae]])` 형태로 링크됨, 처리 불필요 | `[[bongho-tae]]` |
| `필라멘트리` | log.md — 이미 `[[filamentary]]` 링크됨, 처리 불필요 | `[[filamentary]]` |
| `16 Essence` | log(1) | `[[sixteen-essence]]` |

### ⏳ PR 머지 후 처리

| 엔티티 | 대상 링크 | 사유 |
|--------|---------|------|
| `LangGraph` | `[[adr-langgraph-gemini-backend]]` | feature/langgraph-gemini PR 머지 대기 |
| `Gemini` | `[[gemini-2-5-flash]]` | 동일 |
| `Langfuse` | `[[langfuse-observability]]` | 동일 |

**대상 파일**: hot.md, log.md, adr-langgraph-gemini-backend, langfuse-observability

---

## B2. log.md 아카이브

현재: 558줄. **트리거 미충족 (800줄 초과 시 실행).**

**절차**:
1. 2026-04-12 이전 엔트리를 `wiki/log-archive-2026-q1.md`로 이동
2. `log.md` 상단에 `> [!note] 2026-04-12 이전 엔트리는 [[log-archive-2026-q1]] 참조` 추가
3. `index.md`에 `log-archive-2026-q1` 링크 추가

**트리거**: log.md 줄 수 > 800

---

## B3. 빈 Heading 채우기 — 상태 갱신

### ✅ 완료 (2026-05-15, 커밋 8362ef0)

| 파일 | 처리 내용 |
|------|---------|
| `deliverables/pilot-gemini-api-key.md` | 진행현황 "미시작" → "완료" 메모 |
| `deliverables/pilot-server-domain.md` | 진행현황 "미시작" → "완료 + Cloudflare 전환" 메모 |
| `deliverables/pilot-oauth-setup.md` | status `delivered` → `in-progress`, SK바이오팜 컨텍스트 반영 |
| `deliverables/pilot-rehearsal-late-april.md` | status `delivered` → `deferred`, 소아암 일정 연기 사유 기록 |

### ✅ 스킵 (이미 완료)

| 파일 | 사유 |
|------|------|
| `specs/langfuse-observability.md` | 탐색 결과 모든 섹션 이미 채워짐 |
| `runbooks/pilot-day-operation.md` | 절차 섹션 존재, Open Questions는 운영 이슈로 별도 관리 |
