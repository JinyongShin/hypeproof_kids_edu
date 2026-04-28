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
- `/pilot-deploy` — 파일럿 환경 배포 자동화 (의존성 설치 + Cloudflare quick tunnel + 서버 기동)

## 배포 구조 (현재)

**아키텍처**: 운영자 맥북 위에서 백엔드(uvicorn) + 프론트(next dev)를 띄우고, 각각 **Cloudflare Quick Tunnel**로 외부 노출. 별도 클라우드 호스팅 없음.

```
인터넷 ──▶ Cloudflare quick tunnel ──▶ 운영자 맥북
            │
            ├─ <fe-tunnel>.trycloudflare.com ──▶ localhost:3000  (next dev)
            └─ <be-tunnel>.trycloudflare.com ──▶ localhost:8000  (uvicorn)
```

| 컴포넌트 | 포트 | 명령 |
|---|---|---|
| FastAPI 백엔드 | 8000 | `uv run uvicorn main:app --host 0.0.0.0 --port 8000` (`src/backend/`) |
| Next.js 프론트 | 3000 | `npm run dev` (`src/frontend/`) |
| BE tunnel | — | `cloudflared tunnel --url http://localhost:8000` |
| FE tunnel | — | `cloudflared tunnel --url http://localhost:3000` |

### 핵심 파일 (gitignore 됨, 환경별 직접 작성)
- `src/backend/.env.local` — `ZAI_API_KEY`, `GEMINI_API_KEY`, `BACKEND_BASE_URL`, `ADMIN_PASSWORD`
- `src/frontend/.env.local` — `NEXT_PUBLIC_BACKEND_HTTP_URL`, `NEXT_PUBLIC_BACKEND_WS_URL`
- `src/frontend/public/_backend.js` — 런타임 백엔드 URL 오버라이드 (Cloudflare 터널 URL을 직접 박음). `_backend.example.js` 참고.

### 배포 절차
1. **자동**: `/pilot-deploy` 스킬 실행 → 모든 단계 자동.
2. **수동**: `kids_edu_vault/wiki/runbooks/deployment.md` 참조.

### 한계 (현재 운영 리스크)
- **Quick tunnel URL은 cloudflared 재시작마다 바뀜** — `_backend.js` / `BACKEND_BASE_URL` 갱신 필요.
- **맥 절전 들어가면 외부 접속 끊김** — 파일럿 당일은 절전 OFF 필수.
- **어카운트리스 정책** — 트래픽 패턴에 따라 Cloudflare가 차단할 수 있음 (40명 동시 접속은 검증 필요).
- **LLM 동시 처리 한계** — 현재 GLM-5 단독으로는 ~5~10명. 40명 부하 대응 전략은 [[llm-provider-scaling]] (ADR) + [[llm-scaling-test-plan]] (페이즈별 테스트).
- **정식 운영용 권장**: Cloudflare Named Tunnel + 본인 도메인. 파일럿 D-day 전에 전환 검토.
