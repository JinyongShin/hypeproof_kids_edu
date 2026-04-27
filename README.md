# HypeProof Kids Edu

소아암 병동 어린이(8~12세)를 위한 AI 코딩 교육 파일럿 프로젝트.  
아이들이 AI와 대화하며 직접 게임을 만들고, 그 과정에서 **어떻게 AI에게 말해야 하는지**를 체득한다.

- **파일럿 일정**: 2026-05-05
- **리허설**: 2026-04-26
- **대상**: 소아암 병동 어린이 40명 내외
- **운영**: HypeProof Lab (JY)

---

## 프로젝트 구조

```
hypeproof_kids_edu/
├── src/
│   ├── backend/          # FastAPI 백엔드 (Python/uv)
│   └── frontend/         # Next.js 프론트엔드
├── kids_edu_vault/       # Obsidian 지식베이스 (vault)
├── meeting_notes/        # 주간 미팅 노트 (레거시 위치)
└── CLAUDE.md             # 프로젝트 + vault 전반 규약
```

---

## 아키텍처

```
아이 브라우저 (localhost:3000)
  ├── ChatPane  ──── WebSocket ──── FastAPI (localhost:8000)
  │                                     └── Claude CLI subprocess
  │                                         (stream-json 스트리밍)
  └── GamePreview
        └── <iframe srcdoc sandbox="allow-scripts">
              └── Claude가 생성한 순수 HTML+JS+Canvas 게임
```

아이가 채팅창에 프롬프트를 입력하면 FastAPI가 Claude CLI를 호출하고, 응답 텍스트를 실시간 스트리밍하면서 내부의 HTML 코드 블록을 추출해 iframe에 즉시 실행한다.

---

## 백엔드 (`src/backend/`)

**스택**: Python 3.12+, FastAPI, uvicorn, uv

### 핵심 파일

| 파일 | 역할 |
|---|---|
| `main.py` | FastAPI 앱 — WebSocket + admin 엔드포인트 |
| `claude_runner.py` | Claude CLI subprocess 래퍼, 세션 관리 |
| `personas/TUTOR.md` | AI 튜터 페르소나 (병원 아이 특화) |
| `tests/test_claude_runner.py` | TDD 테스트 28개 |
| `.env.example` | 환경변수 템플릿 |

### API 엔드포인트

| 메서드 | 경로 | 설명 |
|---|---|---|
| `GET` | `/health` | 헬스 체크 |
| `WebSocket` | `/ws/chat/{child_id}` | 어린이별 독립 채팅 스트림 |
| `POST` | `/admin/reset/{child_id}` | 운영자용 세션 리셋 |

### WebSocket 이벤트 프로토콜

**클라이언트 → 서버**
```json
{ "prompt": "별을 모으는 게임 만들어줘" }
```

**서버 → 클라이언트**
```json
{ "type": "text",  "chunk": "..." }           // 스트리밍 텍스트
{ "type": "game",  "html": "<!DOCTYPE..." }   // 실행 가능한 게임 HTML
{ "type": "done",  "hint": "💡 ...", "session_id": "..." }
{ "type": "error", "chunk": "오류 메시지" }
```

### 세션 관리 (`SessionStore`)

`child_id → claude_session_id` 매핑을 `data/sessions.json`에 영구 저장한다. 동일한 아이가 다시 접속하면 이전 대화 맥락(`--resume`)이 이어진다. atomic tmp→rename 방식으로 파일 손상을 방지한다.

### 환경변수

`.env.example`을 `.env`로 복사 후 설정:

```bash
CLAUDE_TIMEOUT=120   # Claude CLI 응답 타임아웃 (초)
CLAUDE_MODEL=sonnet  # 사용할 Claude 모델
MOCK_CLAUDE=0        # 1로 설정 시 실제 Claude 없이 개발 가능
```

### 개발 실행

```bash
cd src/backend
uv sync
MOCK_CLAUDE=1 uv run uvicorn main:app --reload
```

### 테스트

```bash
cd src/backend
uv run pytest -v
```

28개 테스트가 `SessionStore`, `_extract_hint`, HTML 추출 정규식, `reset_session`, `stream_claude` (mock) 전체를 커버한다. 테스트 코드만 읽어도 각 함수의 계약을 파악할 수 있도록 작성되었다.

> `MOCK_CLAUDE`는 모듈 import 시점에 평가되므로 테스트에서 `monkeypatch.setattr(claude_runner, "MOCK_CLAUDE", True)`를 사용한다. `setenv`로는 동작하지 않는다.

---

## 프론트엔드 (`src/frontend/`)

**스택**: Next.js 16 (App Router, Turbopack), TypeScript, Tailwind CSS

### 핵심 파일

| 파일 | 역할 |
|---|---|
| `app/page.tsx` | 루트 페이지 — 2-pane 레이아웃 |
| `components/ChatPane.tsx` | 채팅 UI + WebSocket 연동 |
| `components/GamePreview.tsx` | iframe 게임 프리뷰 |
| `components/PromptScaffold.tsx` | 블록별 예시 문장 카드 |
| `hooks/useChat.ts` | WebSocket 상태 관리 훅 |
| `lib/scaffoldData.ts` | 블록별 커리큘럼 데이터 |

### 화면 구성

```
┌──────────────────────┬────────────────────────────┐
│    채팅 영역 (40%)   │     게임 프리뷰 (60%)      │
│                      │                            │
│  [블록 진행 표시]    │  <iframe srcdoc            │
│  [예시 문장 카드]    │   sandbox="allow-scripts"> │
│                      │                            │
│  [메시지 목록]       │  (게임 없으면 대기 화면)   │
│                      │                            │
│  [입력창 + 전송]     │                            │
└──────────────────────┴────────────────────────────┘
```

### 보안: iframe sandbox

```html
<iframe srcdoc={html} sandbox="allow-scripts" />
```

`allow-same-origin`은 **절대 사용하지 않는다**. 이 속성이 있으면 iframe 내 스크립트가 부모 페이지의 DOM과 localStorage에 접근할 수 있어 XSS 위험이 생긴다.

### 커리큘럼 블록 (`lib/scaffoldData.ts`)

| 블록 | 스킬 | 예시 문장 카드 |
|---|---|---|
| 0 | 묘사하기 | "토끼처럼 생긴 캐릭터 만들어줘" 외 3개 |
| 1 | 구체화 | "왼쪽 오른쪽 화살표로 움직이게 해줘" 외 3개 |
| 2 | 추가 요청 | "거기다 친구 캐릭터도 추가해줘" 외 3개 |
| 3 | 수정 요청 | "별 대신 하트로 바꿔줘" 외 3개 |
| 4 | 자유 조합 | 카드 없음 — 자유 입력 |
| 5 | 언어화 | 카드 없음 — 발표 블록 |

### 개발 실행

```bash
cd src/frontend
npm install
npm run dev      # localhost:3000
```

URL 쿼리 `?child=01`로 어린이 ID를 지정한다. 지정하지 않으면 `guest`로 처리된다.

---

## AI 튜터 페르소나 (`src/backend/personas/TUTOR.md`)

병원 아이들을 위해 특화된 규칙:

- **즉시 만들기** — 설명보다 완성이 먼저. 요청 즉시 게임을 만들어 준다.
- **코드 숨기기** — 코드 블록 설명 금지. 게임만 실행되면 된다.
- **협력형 서사** — 전투·적·죽음 테마 금지. 별 모으기, 꽃 피우기, 친구 찾기만.
- **프롬프팅 피드백** — 응답 끝에 항상 `💡 다음엔 ~라고 해봐!` 한 줄.
- **기술 제약** — 순수 HTML+JS+Canvas만. CDN 금지 (병원 네트워크 외부 차단 대비).

---

## Obsidian 지식베이스 (`kids_edu_vault/`)

프로젝트의 모든 설계 결정, 미팅 기록, 운영 지식이 Obsidian vault로 관리된다.  
Obsidian에서 `kids_edu_vault/` 폴더를 열면 된다.

### Vault 구조

```
kids_edu_vault/
├── wiki/
│   ├── hot.md             # 최근 컨텍스트 캐시 (~500단어, 세션마다 갱신)
│   ├── index.md           # 마스터 카탈로그
│   ├── log.md             # 작업 로그 (추가 전용)
│   ├── overview.md        # 전체 요약
│   ├── decisions/         # 아키텍처 결정 기록 (ADR) 13개
│   ├── specs/             # 설계 문서 3개
│   │   ├── pilot-env-design.md            # 실행환경 설계
│   │   ├── ai-prompting-literacy-input.md # 프롬프팅 커리큘럼
│   │   └── pilot-curriculum-adapted.md    # 병원 적응 커리큘럼
│   ├── components/        # 기술 컴포넌트 6개
│   │   ├── kids-edu-backend.md   # FastAPI 백엔드 문서
│   │   ├── kids-edu-frontend.md  # Next.js 프론트엔드 문서
│   │   ├── code-server.md
│   │   ├── caddy.md
│   │   └── ...
│   ├── comms/             # 미팅 합성 요약 9개
│   ├── stakeholders/      # 팀원·이해관계자 9명
│   ├── deliverables/      # OKR·마일스톤·작업 8개
│   ├── intel/             # 외부 조사·현장 맥락 14개
│   ├── runbooks/          # 당일 운영 절차
│   └── concepts/          # 조직·개발 용어 7개
└── .raw/                  # 원본 소스 드랍존 (수정 금지)
```

### 주요 문서

- `wiki/hot.md` — 세션 시작 시 가장 먼저 읽는 컨텍스트 캐시
- `wiki/decisions/nextjs-fastapi-wrapper-architecture.md` — 이 래퍼를 만들기로 한 결정 근거
- `wiki/decisions/iframe-sandbox-over-webcontainers.md` — iframe sandbox 선택 이유
- `wiki/specs/ai-prompting-literacy-input.md` — 블록별 AI 프롬프팅 커리큘럼
- `wiki/components/kids-edu-backend.md` — 백엔드 기술 문서
- `wiki/components/kids-edu-frontend.md` — 프론트엔드 기술 문서
- `wiki/runbooks/pilot-day-operation.md` — 파일럿 당일 운영 절차

---

## 개발 현황

| 단계 | 내용 | 상태 |
|---|---|---|
| Backend TDD | SessionStore, stream_claude 28개 테스트 | ✅ 완료 |
| Backend 서버 | FastAPI WebSocket + /admin/reset | ✅ 완료 |
| Frontend 초기화 | Next.js 16 App Router + Tailwind | ✅ 완료 |
| 2-pane 레이아웃 | ChatPane 40% + GamePreview 60% | ✅ 완료 |
| WebSocket 스트리밍 | 실시간 채팅 + 게임 HTML 갱신 | ✅ 완료 |
| 프롬프트 스캐폴드 | 블록별 예시 문장 카드 | ✅ 완료 |
| 통합 확인 | MOCK_CLAUDE 전체 흐름, 5탭 동시 | ✅ 완료 |
| 실제 Claude 연동 | MOCK_CLAUDE=0 실환경 테스트 | 진행 예정 |
| 리허설 | 2026-04-26 | 예정 |
| 파일럿 | 2026-05-05 | 예정 |

---

## 빠른 시작

### 백엔드

```bash
cd src/backend
cp .env.example .env          # 환경변수 설정
uv sync
MOCK_CLAUDE=1 uv run uvicorn main:app --reload --port 8000
```

### 프론트엔드

```bash
cd src/frontend
npm install
npm run dev                   # localhost:3000
```

브라우저에서 `http://localhost:3000?child=01` 접속.

### 테스트

```bash
cd src/backend
uv run pytest -v
```

---

## 기술 선택 근거

- **FastAPI + Claude CLI subprocess**: 빠른 스프린트(1주)에서 검증된 CLI 재사용. WebSocket 스트리밍이 HTTP polling보다 아이 경험에 자연스럽다. *(Phase 4 이후 GLM-5/Pollinations로 전환됨, 추후 Gemini + Claude API로 재전환 예정 — 아래 스케일링 섹션 참조)*
- **iframe `srcdoc` + `sandbox="allow-scripts"`**: WebContainers·Docker 대비 설치 없음, 병원 네트워크 외부 차단 무관, XSS 격리.
- **순수 HTML+Canvas 게임**: CDN 의존 없음. 병원 내부망에서도 동작.
- **TDD (backend)**: 테스트가 곧 문서. 나중에 코드를 처음 보는 사람도 `test_claude_runner.py`만 읽으면 동작 파악 가능.
- **uv**: pip 대비 의존성 설치 속도 10x, lock 파일로 재현 가능한 환경.

---

## 배포 & 스케일링

### 현재 배포 (개발·QA)
- 운영자 맥북에 `uvicorn` + `next dev` 직접 실행, 외부 노출은 **Cloudflare Quick Tunnel** 2개.
- 자동 배포: `claude` 안에서 `/pilot-deploy` 슬래시 커맨드 (`.claude/skills/pilot-deploy/SKILL.md`).
- 수동 절차 + 트러블슈팅: [`kids_edu_vault/wiki/runbooks/deployment.md`](kids_edu_vault/wiki/runbooks/deployment.md).

### 파일럿 D-day(2026-05-05) 스케일링 — TODO
40명 동시 부하 대응 계획. 현재 GLM-5 단독으로는 ~5–10명에서 한계. 페이즈별 검증 필요:

- **결정 (ADR)**: [`kids_edu_vault/wiki/decisions/llm-provider-scaling.md`](kids_edu_vault/wiki/decisions/llm-provider-scaling.md)
- **테스트 계획**: [`kids_edu_vault/wiki/specs/llm-scaling-test-plan.md`](kids_edu_vault/wiki/specs/llm-scaling-test-plan.md)

요약:
1. **1차 = Gemini 2.x Flash 4-키 풀** (sticky-by-session 라운드로빈) — 기본 운영 모드
2. **2차 = Claude Sonnet 4.6 API** (prompt caching, 별도 빌링) — 품질·신뢰 폴백
3. **3차·4차 = GLM(현재) → Pollinations** — 코드 그대로 유지
4. **5차 = 정적 폴백 카드 / `game_template.py`** — R4(완성 보장) 안전망

**Claude Max 20x 구독 4개는 풀로 사용하지 않음** — TOS·디버깅·운영 부채 모두 부담. 1개만 dev/QA 전용으로 사용.

페이즈 0~5 (베이스라인 → 단일 키 → 풀 → Claude 옵션 → 체인 통합 → 드레스 리허설) 순서로 진행. 합격 기준: **p95 < 8s @ 40 concurrent + 에러율 < 5%**.

### 정식 운영 권장
- 파일럿 당일은 Cloudflare quick tunnel 대신 **Named Tunnel + 본인 도메인** 권장 (URL 영구 고정).
- 맥 절전 OFF 필수 (`caffeinate -d`).
- SQLite는 40명 동시 처리 가능하지만 D-1 부하테스트로 검증 필요.
