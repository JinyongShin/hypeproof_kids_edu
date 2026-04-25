# CLAUDE.md — HypeProof Kids Edu

## 프로젝트 개요
국립암센터 소아암병동 AI 크리에이터 워크샵 (2026.5.5) 및 키즈 에듀케이션 상품 개발.

## 레포 구조

### 루트
- `meeting_notes/` — 회의록, 커리큘럼, 환경 체크리스트, 병원 문의 초안
- `kids_edu_vault/` — **Obsidian Vault (메인)**. 아래 구조 참조
- `src/` — 기술 구현 소스
- `build_teams.md` — 팀 빌드 관련
- `product-requirements-gap-plan.md` — PR과 구현 갭 분석
- `2026-04-12-mvp-dev-plan.md` — MVP 개발 계획

### kids_edu_vault/ (Obsidian Vault)

| 폴더 | 용도 |
|------|------|
| `wiki/intel/` | 경쟁사, 사례 연구, 병원 환경 조사, 연구 문헌 |
| `wiki/specs/` | 기술 명세 |
| `wiki/comms/` | 커뮤니케이션 자료 |
| `wiki/runbooks/` | 운영 매뉴얼 |
| `wiki/meta/` | 메타 문서 |
| `wiki/decisions/` | 의사결정 로그 |
| `wiki/stakeholders/` | 이해관계자 프로필 |
| `wiki/components/` | UI/UX 컴포넌트 |
| `wiki/deliverables/` | 납품물 |
| `wiki/concepts/` | 개념 정의 |
| `_templates/` | Obsidian 템플릿 (concept, meeting, source, runbook, stakeholder, component, deliverable, intel, spec, decision) |
| `.raw/` — 원본 참고 자료 (가공 전) |

## 설치된 Skills (.claude/skills/)

| Skill | 용도 |
|-------|------|
| `wiki` | 위키 페이지 생성/관리 |
| `wiki-query` | 위키 검색 |
| `wiki-ingest` | 외부 소스 ingest |
| `wiki-lint` | 위키 링크/포맷 검증 |
| `obsidian-cli` | Obsidian CLI 연동 |
| `obsidian-markdown` | Obsidian 마크다운 규칙 |
| `obsidian-bases` | Obsidian Bases 템플릿 |
| `save` | 파일 저장 |
| `canvas` / `json-canvas` | 캔버스 작업 |
| `autoresearch` | 자동 리서치 |
| `defuddle` | URL 컨텐츠 추출 |
| `tdd` | 테스트 주도 개발 |
| `worktree-parallel` | git worktree 병렬 작업 |

## Obsidian 마크다운 규칙

- 파일명: `kebab-case.md`
- 위키링크: `[[페이지명]]` 형식 사용
- 프론트매터: YAML 지원
- 태그: `#tag` 형식
- 템플릿: `_templates/` 폴더 참조
- `.raw/` 폴더의 자료는 가공 후 `wiki/` 로 이동

## Slash Commands
- `/wiki` — 새 위키 페이지 생성
- `/save` — 파일 저장
- `/wiki-query` — 위키 검색
- `/wiki-lint` — 링크/포맷 검증
- `/wiki-ingest` — 외부 소스 ingest
