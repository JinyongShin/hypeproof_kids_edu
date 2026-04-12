---
type: decision
status: proposed
priority: 2
date: 2026-04-12
owner: "JY"
context: "pivot-to-chat-preview-wrapper MVP 착수를 위한 개발 파이프라인 구축"
tags:
  - decision
  - tooling
  - agents
created: 2026-04-12
updated: 2026-04-12
---

# Subagent 팀 구조: Wiki 2 + Dev 4

## 결정
- 프로젝트를 **6개 subagent**로 운영한다. 기존 Wiki 2개(`wiki-ingest`, `wiki-lint`)에 **Dev 4개**(`architect`, `implementer`, `reviewer`, `tester`)를 추가.
- 모든 신규 agent는 `sonnet` 모델, `wiki-query` 스킬 기본 포함.
- 표준 흐름: **architect → implementer → tester → reviewer → (메인 commit) → wiki-ingest/save**.
- 핸드오프는 **파일 경로**로만. 요약 복붙 금지.
- `debugger`·`docs-writer`는 **보류** (pain 축적 시 후행 추가).

## 근거
- 피벗 후 3주 MVP 착수 ([[pivot-to-chat-preview-wrapper]], [[fast-implementation-mode]]) — 설계·구현·테스트·리뷰 파이프라인이 없으면 메인 컨텍스트가 포화된다.
- `build_teams.md` 처방 참고하되 그 자체 경고("과도한 specialist는 자동 위임 신뢰도 저하")도 수용 → 6개 → 4개로 축소.
- 모든 Dev agent는 첫 작업 전 `hot.md` + 루트 `CLAUDE.md` + 지정 ADR Read 강제 — subagent는 fresh context에서 시작하므로 시딩 없으면 피벗·PIPA·iframe 제약을 모른다.
- `sonnet` 기본: architect를 opus로 올릴 여지가 있으나 대부분 ADR은 sonnet으로 충분, 복합 판단은 메인(opus)이 직접 작성하면 비용-품질 균형.

## 대안 및 기각 이유
- **6-agent 풀 세트** (`build_teams.md` 원안에 `debugger`·`docs-writer` 포함): 초기부터 과잉. 자동 위임 혼란 + 유지비 증가. 실제 반복 디버그 병목·문서 수요 누적 관찰 시 추가가 더 건전.
- **2-agent 유지 (Wiki만)**: MVP 구현을 메인이 전부 처리 → 컨텍스트 포화, 리뷰 품질 저하, 테스트 누락 위험.
- **architect = opus 고정**: 비용 낭비. 복합 아키텍처 결정은 sonnet보다 메인(opus)이 직접 작성하는 편이 핸드오프 손실도 없음.
- **병렬 작업 전용 agent 신설**: 불필요. `worktree-parallel` 스킬로 커버.

## 영향 범위
- **생성**: `.claude/agents/{architect,implementer,reviewer,tester}.md`, `.claude/CLAUDE.md` (위임 규칙).
- **수정**: 루트 `CLAUDE.md` — "팀 & 워크플로우" 섹션 추가 (6-agent 표, 스킬 인벤토리, 7단계 규칙, 표준 흐름, 비용 가드레일).
- **운영 규약 변경**:
  - 신규 기능은 architect ADR → implementer → tester → reviewer 순 강제.
  - subagent Bash 스코프: `git push`·`reset --hard`·`rm -rf`·전역 설치 금지 (메인 전용).
  - 시크릿: `.env.local` + `.env.example`, 인라인 금지. reviewer는 PR 전 `rg -i "sk-|api[_-]?key"` 스윕.
  - 주간: 금요일 `@wiki-lint`.
- Supersede: 없음 (기존 결정 뒤집지 않음).

## 후속 작업
- [ ] Smoke test: `@architect`에게 "Next.js 프로젝트 구조 ADR" 초안 지시 → `wiki/decisions/`에 proposed 생성 확인.
- [ ] Smoke test: `@implementer`로 Next.js 스캐폴드 → `package.json` 생성 확인.
- [ ] Smoke test: `@reviewer` iframe sandbox 체크 리포트 반환 확인.
- [ ] Smoke test: `@tester` Vitest 1건 생성 확인.
- [ ] E2E smoke: 소기능 하나로 architect→implementer→tester→reviewer 완주 + 사이클 시간 측정.
- [ ] Jay 승인 후 C 진입 시점에 실전 가동.
- [ ] 1주 운영 후 회고: `debugger`·`docs-writer` 추가 필요성 재평가.

## 관련
- [[pivot-to-chat-preview-wrapper]] · [[fast-implementation-mode]]
- [[iframe-sandbox-over-webcontainers]] · [[parent-gated-signup-first]] (Dev agent가 강제로 따라야 할 제약)
- 구현: `.claude/agents/architect.md` · `.claude/agents/implementer.md` · `.claude/agents/reviewer.md` · `.claude/agents/tester.md` · `.claude/CLAUDE.md`
