# Wiki-Lint 백로그 — 별도 세션 처리 항목

생성: 2026-05-15
상태: 미착수
참조: `wiki/meta/lint-report-2026-05-15.md`

---

## B1. Unlinked Mentions — 9개 엔티티 wikilink 추가

고트래픽 페이지에서 엔티티 이름이 plain text로 등장. 수동 편집 필요.

| 엔티티 | 연결 페이지 | 등장 횟수 | 대상 링크 |
|--------|------------|---------|-----------|
| `SK바이오팜` | hot.md (5), log.md (3), sk-biopharma-meeting (7), sk-biopharma-followup (4), sk-biopharma-pilot (6), adr-hypeproof-studio-v01 (2) | 27+ | `[[sk-biopharma]]` |
| `HypeProof Studio` | hot.md (4), log.md (1), sk-biopharma-pilot (1), adr-hypeproof-studio-v01 (4) | 10+ | `[[hypeproof-studio]]` |
| `비트리` | hot.md (1), sk-biopharma-meeting (2), sk-biopharma-pilot (2) | 5+ | `[[bitree]]` |
| `봉호` | log.md (3) | 3 | `[[bongho-tae]]` |
| `필라멘트리` | log.md (1) | 1 | `[[filamentary]]` |
| `LangGraph` | hot.md (1), log.md (2), adr-langgraph-gemini-backend, langfuse-observability | 4+ | 전용 페이지 없음 → `[[components/langgraph]]` (Phase 1-B에서 생성됨) |
| `Gemini` | hot.md (1), overview (1), log.md (1) | 3 | `[[gemini-2-5-flash]]` |
| `Langfuse` | hot.md (1) | 1 | `[[langfuse-observability]]` |
| `16 Essence` | log.md (1) | 1 | `[[sixteen-essence]]` |

**작업 방식**: 각 파일을 읽고 plain text → `[[link]]` 교체. log.md는 append-only 원칙상 과거 엔트리 수정은 선택적으로 판단.

---

## B2. log.md 아카이브

현재: 558줄. 800줄 초과 시 실행.

**절차**:
1. 2026-04-12 이전 엔트리를 `wiki/log-archive-2026-q1.md`로 이동
2. `log.md` 상단에 `> [!note] 2026-04-12 이전 엔트리는 [[log-archive-2026-q1]] 참조` 추가
3. `index.md`에 `log-archive-2026-q1` 링크 추가

**트리거**: log.md 줄 수 > 800

---

## B3. 빈 Heading 채우기 — 콘텐츠 작성 필요

운영에 실제로 필요한 페이지들. 5/28 dry-run 게이트 전에 채우면 좋음.

| 파일 | 빈 섹션 | 우선순위 |
|------|--------|---------|
| `specs/langfuse-observability.md` | `## 초기 설정 절차`, `## 백엔드 통합`, `## 운영 시 고려사항` | 높음 (prod observability 스펙) |
| `runbooks/pilot-day-operation.md` | `## 절차` | 높음 (당일 운영 runbook) |
| `deliverables/pilot-gemini-api-key.md` | 본문 전체 | 낮음 (완료된 deliverable) |
| `deliverables/pilot-server-domain.md` | 본문 전체 | 낮음 |
| `deliverables/pilot-oauth-setup.md` | 본문 전체 | 낮음 |
| `deliverables/pilot-rehearsal-late-april.md` | 본문 전체 | 낮음 |

**우선 처리**: `langfuse-observability.md`와 `pilot-day-operation.md`는 5/28 dry-run 게이트와 직결.
