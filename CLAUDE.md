# HypeProof Kids Edu — Obsidian Vault

Purpose: HypeProof 유료 파일럿(2026-05-05, 소아암 병동 어린이 대상 AI 코딩 교육) 실행환경 설계·운영을 위한 지식베이스.
Owner: JY (신진용)
Project root: `D:\HypeProofLab\hypeproof_kids_edu\`
**Vault root (Obsidian)**: `D:\HypeProofLab\hypeproof_kids_edu\kids_edu_vault\`

> 앞으로 모든 wiki/.raw/노트 생성은 `kids_edu_vault/` 안에서 한다. 프로젝트 루트에 있는 기존 md 파일들은 입력·참조용 자료이며, 필요 시 `kids_edu_vault/.raw/` 로 복사하여 ingest한다(원본은 그대로 둠).

---

## 폴더 구조와 용도

### 프로젝트 루트 (`hypeproof_kids_edu/`)
| 경로 | 용도 | 컨벤션 |
|---|---|---|
| `kids_edu_vault/` | **Obsidian vault 루트**. wiki/, .raw/ 등 모든 지식 자산이 여기 들어간다. | Obsidian에서 이 폴더를 열 것. 아래 Vault 구조 참조. |
| `meeting_notes/` | 주간/특별 미팅 노트, OKR 기록 (레거시 위치) | 파일명: `YYYY-MM-DD-<주제>.md` 또는 기존 Gemini 생성 포맷 유지. 과거 기록은 수정 금지. 향후 신규 미팅 노트는 vault 내부에 작성 권장. |
| `pilot-env-design-draft.md` | 파일럿 실행환경 설계 초안 (입력 자료) | JY 담당 기술 브리핑. ingest 대상. |
| `build_teams.md` | subagent 팀 설계 지시서 | 실행 시 `.claude/agents/` 생성 트리거. |
| `obsidian_settings.md` | 초기 설치 스크립트 | 이미 실행됨. 보관용. |
| `CLAUDE.md` | 이 파일. 프로젝트 + vault 전반 규약. | — |
| `.claude/skills/` | 프로젝트 스킬 (kepano + claude-obsidian) | 수정 금지, 업스트림 재설치로 갱신. |
| `.claude/commands/` | 슬래시 커맨드 정의 | `/wiki`, `/save`, `/canvas`, `/autoresearch` |
| `.claude/agents/` | 위임용 subagent | `wiki-ingest`, `wiki-lint` |
| `.claude/rules/` | 프로젝트 규칙 (예: `uv.md`) | 파이썬 의존성은 `uv` 전용. |

### Vault 내부 (`kids_edu_vault/`) — scaffold 완료
| 경로 | 용도 |
|---|---|
| `kids_edu_vault/.raw/` | 원본 소스 (immutable). ingest 전 드랍존. 수정 금지. Obsidian에서 숨김(dot prefix). |
| `kids_edu_vault/wiki/` | LLM이 관리하는 지식베이스. 아래 레이어 참조. |
| `kids_edu_vault/_templates/` | 노트 타입별 템플릿 10종. |
| `kids_edu_vault/.obsidian/` | Obsidian 볼트 설정·스니펫·플러그인. |

### Wiki 레이어 (`kids_edu_vault/wiki/`) — Mode C 확장판 (회의 + 개발)

```
kids_edu_vault/wiki/
├── index.md            # 마스터 카탈로그 (ingest마다 갱신)
├── log.md              # 추가 전용 (새 로그는 최상단)
├── hot.md              # ~500단어 최근 컨텍스트 캐시
├── overview.md         # 전체 요약
├── stakeholders/       # 사람·조직 (+ _index.md)
├── comms/              # 미팅·스레드 합성 요약 (+ _index.md)
├── decisions/          # 단일 결정 ADR (+ _index.md)
├── deliverables/       # OKR·작업·마일스톤 (+ _index.md)
├── specs/              # 복합 설계 문서 (+ _index.md)
├── components/         # 기술 스택 컴포넌트별 (+ _index.md)
├── runbooks/           # 배포·당일 운영 절차 (+ _index.md)
├── concepts/           # 조직/개발 용어·프레임워크 (+ _index.md)
└── intel/              # 외부 조사·현장 맥락 (+ _index.md)
```

---

## 설치된 Skills (14개)

### Obsidian/Wiki 운영
- `wiki` — 루트 스킬. 볼트 scaffold, 하위 스킬 라우팅, hot cache 관리. 트리거: "set up wiki", `/wiki`.
- `wiki-ingest` — `.raw/`의 소스를 읽어 엔티티·컨셉 페이지 생성/갱신. 트리거: "ingest [filename]".
- `wiki-query` — 볼트 기반 질의응답. hot→index→page 순 읽기. 트리거: "what do you know about X".
- `wiki-lint` — 고아 페이지·끊긴 링크·오래된 주장 점검, Dataview 대시보드 갱신.
- `save` — 현재 대화/인사이트를 구조화된 노트로 보관. 트리거: `/save`.
- `autoresearch` — 주제 입력받아 반복 검색·요약·wiki 파일링. 트리거: `/autoresearch [topic]`.
- `canvas` — `.canvas` 파일에 이미지/텍스트/PDF/위키 페이지 배치. 트리거: `/canvas`.

### Obsidian 문법/도구
- `obsidian-markdown` — Obsidian Flavored Markdown 정답지. 노트 작성 시 필수 참조.
- `obsidian-bases` — `.base` 파일(노트 DB 뷰) 작성.
- `obsidian-cli` — Obsidian CLI로 볼트 조작·플러그인 개발.
- `json-canvas` — `.canvas` JSON 스키마 직접 편집.
- `defuddle` — 웹 페이지에서 본문만 추출(광고·네비 제거)하여 ingest 전 토큰 절감.

### 개발 워크플로우
- `tdd` — Kent Beck TDD / Tidy First. Red-Green-Refactor.
- `worktree-parallel` — 독립 작업을 git worktree로 병렬 진행.

---

## 팀 & 워크플로우

이 프로젝트는 **지식 관리(Wiki) 2 + 개발(Dev) 4** = 총 6개 subagent로 운영된다.
세부 위임 규칙은 `.claude/CLAUDE.md` 참조. 본 섹션은 한눈에 보는 지도.

### Subagent 팀

| Agent | 역할 | Model | 핵심 스킬 | 트리거 |
|---|---|---|---|---|
| `wiki-ingest` | 소스 일괄 ingest → wiki 페이지 생성·갱신 | sonnet | wiki-ingest, obsidian-markdown, defuddle | "ingest [파일]", `.raw/` 드랍 후 |
| `wiki-lint` | 볼트 헬스체크 (고아·끊긴 링크·frontmatter) | sonnet | wiki-lint | 주간 점검, `/wiki-lint` |
| `architect` | 기능·아키텍처 설계, ADR 작성 | sonnet | obsidian-markdown, wiki, simplify, wiki-query | 새 기능·리팩터 착수 시 |
| `implementer` | Next.js / Agent SDK 코드 구현 | sonnet | claude-api, tdd, worktree-parallel, wiki-query | architect ADR 승인 후 |
| `reviewer` | 보안·성능·품질·시크릿·PIPA 리뷰 (read-only) | sonnet | simplify, wiki-query | 커밋·PR 전 필수 |
| `tester` | Vitest/Playwright 테스트 작성·실행 | sonnet | tdd, wiki-query | implementer 산출물에 대해 |

### 스킬 인벤토리 (컨텍스트별)

- **Wiki 운영**: `wiki`, `wiki-ingest`, `wiki-query`, `wiki-lint`, `save`, `autoresearch`, `canvas`
- **Obsidian 문법·도구**: `obsidian-markdown`, `obsidian-bases`, `obsidian-cli`, `json-canvas`, `defuddle`
- **개발**: `claude-api`, `tdd`, `worktree-parallel`, `simplify`
- **하네스**: `update-config`, `keybindings-help`, `loop`, `schedule`

### 단계별 규칙 (매 기능·변경마다)

| 단계 | 담당 | 필수 행위 | 산출물 |
|---|---|---|---|
| 1. Design | `architect` (또는 메인) | ADR 작성 (`_templates/decision.md`), `status: proposed` | `wiki/decisions/<slug>.md` |
| 2. Implement | `implementer` | architect ADR 경로를 컨텍스트로 받음. `.env.local` 사용, 시크릿 인라인 금지 | 코드 파일 + `.env.example` 갱신 |
| 3. Test | `tester` | 기본 후행 모드, 지시 시 TDD 모드. Python은 `uv run pytest` | 테스트 파일 |
| 4. Review | `reviewer` | iframe sandbox escape, 시크릿 누출, PIPA 경로, server/client 경계 점검 (read-only) | 리뷰 리포트 |
| 5. Commit | 메인 | `git push` 등 되돌릴 수 없는 작업은 메인만. subagent는 `git add`/`commit`까지 | 커밋 |
| 6. Archive | `wiki-ingest` 또는 `save` | 결정·학습을 볼트에 반영, `hot.md` 갱신 | wiki 업데이트 |
| 7. Weekly | `wiki-lint` | 금요일 볼트 점검 | lint 리포트 |

### 공통 규약

- **컨텍스트 시딩**: 모든 subagent는 첫 작업 전 `kids_edu_vault/wiki/hot.md` + 이 파일 + 호출자가 지정한 ADR/파일 경로 Read.
- **핸드오프 = 파일 경로**: 요약 복붙 금지. architect→implementer→tester→reviewer 전체가 파일 경로로 연결.
- **이전 결정 조회**: `wiki-query` 스킬 직접 호출. 별도 agent 호출 금지.
- **Bash 스코프**: `git push`, `reset --hard`, `rm -rf`, 전역 설치는 subagent 금지 — 메인만 실행.
- **병행 작업**: 독립 기능 2개 이상이면 `worktree-parallel` 스킬로 worktree 분기 후 worktree별 implementer.

### 표준 흐름

```
새 기능 요청
    ↓
[architect] → wiki/decisions/<slug>.md (proposed)
    ↓ (ADR 경로 전달)
[implementer] → 코드 + .env.example
    ↓ (파일 경로 전달)
[tester] → 테스트 파일
    ↓ (변경 파일 목록 전달)
[reviewer] → 리뷰 리포트
    ↓ (issue 있으면 implementer 재호출, 리포트 경로 전달)
메인 → git commit (로컬까지)
    ↓
[wiki-ingest] or save → 볼트 반영, hot.md 갱신
```

### 모델 비용 가드레일

- 대부분은 `sonnet`. architect도 `sonnet` 기본 — 복합 아키텍처 판단이 필요한 결정만 메인(opus)이 직접 작성.
- 새 agent 추가 전 질문: "기존 6개에 녹지 않는 이유를 한 줄로 답할 수 있는가?" 답할 수 없으면 만들지 말 것. 과도한 specialist는 자동 위임 신뢰도를 떨어뜨린다.

---

## Obsidian 마크다운 규칙 (필수 준수)

### Frontmatter (YAML)
```yaml
---
type: concept            # concept | entity | source | question | meta | ...
title: "Note Title"      # 특수문자 있으면 따옴표
created: 2026-04-12      # YYYY-MM-DD (ISO datetime 금지)
updated: 2026-04-12
status: developing
tags:
  - research
  - ai/obsidian          # 중첩 태그 허용 (/ 구분)
related:
  - "[[Other Note]]"     # YAML 안의 wikilink는 반드시 따옴표
sources:
  - "[[source-page]]"
---
```

- 평탄한 YAML만 사용. 객체 중첩 금지.
- 리스트는 `- item`. 인라인 `[a, b, c]` 금지.
- 날짜는 `YYYY-MM-DD`만.

### Wikilink 원칙 ([[페이지명]])
- 내부 링크는 **항상** `[[파일명]]` 사용. `[텍스트](path.md)` 금지.
- 확장자·경로 생략. 파일명이 유일하면 그대로. 충돌 시 `[[폴더/파일명]]`.
- 별칭: `[[Note Name|표시 텍스트]]`.
- 섹션/블록: `[[Note#Heading]]`, `[[Note#^block-id]]`.
- 임베드는 `![[...]]` (이미지·PDF·노트 섹션). 이미지 크기: `![[img.png|300]]`.
- **YAML 프론트매터 안의 wikilink는 반드시 따옴표로 감쌀 것**.

### Callout·강조
- 콜아웃: `> [!note] 제목` / `> [!warning]` / `> [!contradiction]` 등. 콜아웃 본문 안에 `##` 금지, HTML 금지.
- 하이라이트 `==text==`, 태그 `#parent/child` (본문) / `- parent/child` (YAML, `#` 없이).
- 수식 `$inline$`, `$$block$$`. Mermaid 코드블록 네이티브 지원.

### 하지 말 것
- `.raw/`의 원본 수정.
- `wiki/log.md`의 과거 엔트리 편집(추가 전용, 새 항목은 파일 최상단).
- `[링크](파일.md)` 스타일의 내부 링크.
- ISO datetime(`2026-04-08T00:00:00Z`)을 프론트매터에 사용.
- 인라인 태그 리스트 `tags: [a, b]` 형식.

---

## 운영 플로우

모든 경로는 vault 루트 `kids_edu_vault/` 기준.

1. 소스 수집: `kids_edu_vault/.raw/`에 원본 드랍 → `/wiki ingest <파일>`
2. 노트 작성: `obsidian-markdown` 규칙 준수, wikilink 우선. 파일은 `kids_edu_vault/wiki/` 하위에 생성.
3. 질문: `/wiki-query` 또는 "what do you know about X" — `kids_edu_vault/wiki/hot.md` 먼저.
4. 세션 종료 시: `kids_edu_vault/wiki/hot.md`와 `wiki/log.md` 갱신.
5. 정기 점검: `/wiki-lint` 로 깨진 링크·고아 페이지 제거.
6. 대화 보존 가치 있는 인사이트는 `/save`.

크로스 프로젝트 참조: 다른 프로젝트의 CLAUDE.md에서 `D:\HypeProofLab\hypeproof_kids_edu\kids_edu_vault\` 를 가리키고 `wiki/hot.md` → `wiki/index.md` → 개별 페이지 순으로 읽도록 지시.

---

## 규칙 (rules)

- 파이썬 의존성: `uv` 전용 (`.claude/rules/uv.md`). `pip`·`poetry` 금지.
- 오늘 날짜 기준으로 상대 날짜("이번 주", "다음 주") 노트 작성 시 절대 날짜로 변환.
