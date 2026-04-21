# Subagent Delegation — HypeProof Kids Edu

이 프로젝트는 두 종류의 agent 팀을 운용한다. 전체 팀 구성·단계별 규칙·워크플로우 다이어그램은 **프로젝트 루트 `CLAUDE.md`의 "팀 & 워크플로우" 섹션**에서 한눈에 볼 수 있다. 본 파일은 세부 위임 규칙만 정의한다.

## 팀

**지식 관리 (Wiki)**
- `wiki-ingest` — `.raw/` 소스 일괄 ingest → wiki 페이지 생성·갱신
- `wiki-lint` — 볼트 헬스체크, 고아 페이지·끊긴 링크 점검

**개발 (Dev)**
- `architect` — 기능·아키텍처 설계, ADR 작성 (wiki/decisions/)
- `implementer` — Next.js / Agent SDK 코드 구현
- `reviewer` — 커밋·PR 전 보안·성능·품질 리뷰 (필수, read-only)
- `tester` — Vitest/Playwright 테스트 작성·실행

## 위임 규칙

- **새 기능 설계** → @architect 먼저 (ADR 초안이 나와야 implementer 진입)
- **코드 구현** → @implementer (architect의 wiki/decisions/ 페이지 경로를 컨텍스트로 전달)
- **테스트 작성** → @tester (implementer 산출물 경로 전달)
- **코드 리뷰** → @reviewer (커밋·PR 전 필수, proactive)
- **소스 ingest** → @wiki-ingest
- **볼트 점검** → @wiki-lint (금요일 주간 루틴)

메인 대화는 오케스트레이션에 집중. 세부 탐색·구현은 subagent로 context 격리.

## 핸드오프 프로토콜

- 모든 subagent는 첫 작업 전 다음 3개를 Read:
  1. `kids_edu_vault/wiki/hot.md`
  2. `D:\HypeProofLab\hypeproof_kids_edu\CLAUDE.md`
  3. 호출자가 지정한 ADR / 변경 파일 경로
- agent 간 핸드오프는 **파일 경로**로. 요약 복붙은 정보 소실 — 경로 전달.
- reviewer 블로킹 이슈 발생 시: 메인이 implementer 재호출. 리뷰 리포트 경로를 컨텍스트로 전달.
- 이전 결정 조회는 `wiki-query` 스킬 직접 호출 (별도 agent 호출 금지).

## 오케스트레이션 패턴

- **순차 (default)**: architect → implementer → tester → reviewer.
- **병렬 (분기)**: 독립 기능 2개 이상 → `worktree-parallel` 스킬로 worktree 분기, worktree별 implementer.
- **반복 (reviewer 피드백)**: 메인이 "이 리포트를 읽고 해당 파일만 수정하라"로 implementer 재호출.
- **중단 (blocker)**: tester 실패 또는 reviewer CRITICAL → 메인에 에스컬레이션, 다음 단계 자동 진행 금지.

## Bash 스코프 (implementer · tester)

**금지 (메인만 실행)**
- `git push`, `git push --force`, `git reset --hard`
- `rm -rf`, `sudo`, `npm i -g`
- 되돌릴 수 없는 마이그레이션

**허용**
- 로컬 파일 편집, `pnpm` / `npm` / `pnpm dlx` (local)
- `uv run ...`
- `git add`, `git commit` (메시지 확정 후), `git status` / `diff` / `log`

## 시크릿 취급

- API 키 인라인 금지. `.env.local` (gitignored) 사용, `.env.example`에 키 이름만 placeholder.
- reviewer는 PR 전 `rg -i "sk-|api[_-]?key"` 스윕 필수.

## 주간 루프

- 세션 종료 시 메인이 `save` 스킬 또는 `@wiki-ingest` 호출로 볼트 반영.
- 매주 금요일 `@wiki-lint` 점검.

## 새 agent 추가 전 체크

"기존 6개에 녹지 않는 이유를 한 줄로 답할 수 있는가?" 답할 수 없으면 만들지 말 것. 과도한 specialist는 자동 위임 신뢰도를 떨어뜨린다.
