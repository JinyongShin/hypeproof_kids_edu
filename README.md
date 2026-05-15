# HypeProof Kids Edu

소아암 병동 어린이(8~12세)를 위한 AI 코딩 교육 파일럿 프로젝트.  
아이들이 AI와 대화하며 직접 게임을 만들고, 그 과정에서 **어떻게 AI에게 말해야 하는지**를 체득한다.

- **파일럿 일정**: 2026-05-05
- **대상**: 국립암센터 소아암 병동 어린이 40명 내외
- **운영**: HypeProof Lab (JY)

---

## 아키텍처

```
아이 브라우저 (localhost:3000)
  ├── ChatPane  ──── WebSocket ──── FastAPI (localhost:8000)
  │                                     └── LangGraph StateGraph
  │                                           ├── classify_intent
  │                                           ├── generate_card / save_card
  │                                           ├── generate_spec / edit_spec
  │                                           ├── validate_and_build / save_game
  │                                           └── chitchat
  └── GamePreview
        └── <iframe srcdoc sandbox="allow-scripts">
              └── Gemini가 생성한 순수 HTML+JS+Canvas 게임
```

---

## 스택

| 레이어 | 기술 |
|--------|------|
| 백엔드 | Python 3.12, FastAPI, LangGraph, Gemini 2.5 Flash (langchain-google-genai) |
| 프론트엔드 | Next.js (App Router), TypeScript, Tailwind CSS |
| 데이터 | SQLite (kids_edu.db), LangGraph 체크포인터 (langgraph.db) |
| 관측성 | Langfuse v2 self-hosted |
| 배포 | Docker Compose (로컬 / VPS) |

---

## 빠른 시작 — Docker Compose

### 1. 환경변수 설정

```bash
cp src/backend/.env.example src/backend/.env.local
```

`src/backend/.env.local` 편집:

```env
GEMINI_API_KEY=your-gemini-api-key
MOCK_LLM=0                          # 1: 실제 API 호출 없이 개발 가능
BACKEND_BASE_URL=http://localhost:8000
ADMIN_USERNAME=admin
ADMIN_PASSWORD=your-password

# Langfuse (컨테이너 첫 기동 후 localhost:3002에서 발급)
LANGFUSE_ENABLED=true
LANGFUSE_PUBLIC_KEY=pk-lf-...
LANGFUSE_SECRET_KEY=sk-lf-...
LANGFUSE_HOST=http://localhost:3002  # 외부 접근용 (내부는 docker-compose가 자동 오버라이드)
```

### 2. 컨테이너 실행

```bash
docker compose up -d
```

| 서비스 | URL |
|--------|-----|
| 프론트엔드 | http://localhost:3000 |
| 백엔드 API | http://localhost:8000 |
| Langfuse 관측성 | http://localhost:3002 |

### 3. Langfuse 초기 설정 (최초 1회)

1. http://localhost:3002 접속 → 계정 생성
2. 프로젝트 생성 → Settings → API Keys에서 키 발급
3. `.env.local`의 `LANGFUSE_PUBLIC_KEY`, `LANGFUSE_SECRET_KEY` 업데이트
4. `docker compose up -d --build backend` 로 백엔드 재빌드

> **주의**: `docker compose down -v`로 볼륨을 삭제하면 Langfuse 계정과 API 키가 초기화됩니다. 키를 재발급 후 `.env.local`을 업데이트하세요.

### 4. LLM 없이 개발 (MOCK_LLM)

```bash
# docker-compose.override.yml이 자동으로 MOCK_LLM=1 주입
docker compose up -d
```

`docker-compose.override.yml`이 있으면 Gemini API를 호출하지 않고 픽스처 응답을 반환합니다.

---

## 빠른 시작 — 로컬 개발 (Docker 없이)

### 백엔드

```bash
cd src/backend
cp .env.example .env.local   # 환경변수 설정
uv sync
MOCK_LLM=1 uv run uvicorn main:app --reload --port 8000
```

### 프론트엔드

```bash
cd src/frontend
npm install
npm run dev   # localhost:3000
```

---

## 프로젝트 구조

```
hypeproof_kids_edu/
├── src/
│   ├── backend/
│   │   ├── main.py              # FastAPI 앱 — lifespan, WebSocket, 인증
│   │   ├── ws_handler.py        # WebSocket ↔ LangGraph astream_events 브릿지
│   │   ├── storage.py           # SQLite (세션, 카드, 게임, 테넌트, 어드민)
│   │   ├── game_engine.py       # validate_spec() + build_game_with_spec()
│   │   ├── personas/TUTOR.md    # AI 튜터 시스템 프롬프트
│   │   ├── app/
│   │   │   ├── config.py        # Settings (BaseSettings)
│   │   │   ├── llm.py           # LLM 팩토리 (Gemini / MOCK_LLM)
│   │   │   ├── auth.py          # bcrypt 인증 + ensure_default_admin
│   │   │   ├── checkpointer.py  # get_thread_config()
│   │   │   └── graph/
│   │   │       ├── state.py     # EduSessionState TypedDict
│   │   │       ├── nodes.py     # 8개 노드 함수
│   │   │       ├── edges.py     # 조건부 엣지 함수
│   │   │       └── graph.py     # build_graph() + graph_lifespan()
│   │   ├── tests/               # 64개 테스트 (pytest)
│   │   ├── pyproject.toml
│   │   ├── Dockerfile
│   │   └── .env.example
│   └── frontend/
│       ├── app/                 # Next.js App Router
│       ├── components/          # ChatPane, GamePreview 등
│       ├── Dockerfile
│       └── next.config.ts       # output: "standalone"
├── docker-compose.yml           # backend / frontend / langfuse / langfuse-db
├── docker-compose.override.yml  # MOCK_LLM=1 로컬 테스트용
├── kids_edu_vault/              # Obsidian 지식베이스
└── CLAUDE.md                    # 프로젝트 + Claude Code 규약
```

---

## WebSocket 이벤트 프로토콜

**클라이언트 → 서버**
```json
{ "prompt": "별을 모으는 게임 만들어줘" }
```

**서버 → 클라이언트**
```json
{ "type": "text",  "chunk": "..." }
{ "type": "card",  "character": {...}, "card_url": "...", "hint": "💡 ..." }
{ "type": "game",  "html": "<!DOCTYPE...", "game_url": "..." }
{ "type": "done",  "hint": "💡 ..." }
{ "type": "error", "chunk": "오류 메시지" }
```

---

## LangGraph 그래프 흐름

```
START
  └─ classify_intent
        ├─ "card"        → generate_card → save_card ──────────────┐
        ├─ "game_create" → generate_spec → validate_and_build ─┐   │
        ├─ "game_edit"   → edit_code ──────────────────────────┤   │
        │                                              save_game┘   │
        └─ "chitchat"  → chitchat ───────────────────────────────┐  │
                                                                  ↓  ↓
                                                           summarize_turn → END
```

- `edit_code_node`: 현재 게임 HTML 전체를 LLM에 전달 → Pydantic 구조화 출력으로 수정된 HTML 반환. 코드블록 채팅 노출 없음.
- `summarize_turn_node`: 매 턴 종료 시 카드·게임·발화 정보를 200자 이내 한국어로 압축 → `session_context` 필드에 저장. 다음 턴의 모든 LLM 노드가 이 요약을 컨텍스트로 수신.
- `AsyncSqliteSaver`: `data/langgraph.db`에 대화 상태 영속화 → 재시작 후 맥락 복원
- `MOCK_LLM=1`: `FakeListChatModel`로 실제 API 호출 없이 그래프 실행

---

## 테스트

```bash
cd src/backend
uv run pytest -v
```

| 파일 | 커버리지 |
|------|---------|
| `test_graph_routing.py` | intent 분류, 엣지 라우팅 |
| `test_card_node.py` | 카드 JSON 추출, LRU 정리 |
| `test_spec_node.py` | spec 필드 기본값, spawn 제한 |
| `test_edit_loop.py` | HTML 편집 반환, 폴백, char_sprite 보존 |
| `test_summarize_turn.py` | 롤링 요약 생성, 컨텍스트 교체, 노드 주입 |
| `test_ws_handler.py` | WS 이벤트 타입 순서 |
| `test_auth.py` | 테넌트 격리, 어드민 로그인 |

LLM 호출 노드는 `MOCK_LLM=1`로 픽스처 응답 반환 — 실제 API 비용 없음.

---

## 환경변수 전체 목록

| 변수 | 기본값 | 설명 |
|------|--------|------|
| `GEMINI_API_KEY` | (필수) | Google Gemini API 키 |
| `MOCK_LLM` | `0` | `1`로 설정 시 FakeListChatModel 사용 |
| `BACKEND_BASE_URL` | `http://localhost:8000` | 파일 URL 생성용 베이스 URL |
| `ADMIN_USERNAME` | `admin` | 관리자 로그인 ID |
| `ADMIN_PASSWORD` | `admin` | 관리자 로그인 비밀번호 |
| `LANGFUSE_ENABLED` | `false` | Langfuse 관측성 활성화 |
| `LANGFUSE_PUBLIC_KEY` | | Langfuse 프로젝트 공개 키 |
| `LANGFUSE_SECRET_KEY` | | Langfuse 프로젝트 비밀 키 |
| `LANGFUSE_HOST` | `http://localhost:3002` | Langfuse 서버 URL (로컬 접근용) |

---

## AI 튜터 페르소나 (`src/backend/personas/TUTOR.md`)

병원 어린이를 위해 특화된 규칙:

- **즉시 만들기** — 설명보다 완성이 먼저. 요청 즉시 게임/카드를 만든다.
- **코드 숨기기** — 코드 블록·기술 설명 금지. 결과물만 보여준다.
- **협력형 서사** — 전투·적·죽음 테마 금지. 별 모으기, 꽃 피우기, 친구 찾기만.
- **프롬프팅 피드백** — 응답 끝에 항상 `💡 다음엔 ~라고 해봐!` 한 줄.
- **기술 제약** — 순수 HTML+JS+Canvas만. CDN 금지 (병원 네트워크 외부 차단 대비).

---

## Obsidian 지식베이스 (`kids_edu_vault/`)

모든 설계 결정, 미팅 기록, 운영 지식을 Obsidian vault로 관리.  
Obsidian에서 `kids_edu_vault/` 폴더를 열면 된다.

- `wiki/hot.md` — 세션 시작 시 가장 먼저 읽는 컨텍스트 캐시
- `wiki/decisions/` — 아키텍처 결정 기록 (ADR)
- `wiki/specs/` — 기술 명세
- `wiki/runbooks/` — 운영 매뉴얼
- `wiki/components/` — 컴포넌트 문서

---

## 배포

### 현재 (로컬 Docker Compose)
```bash
docker compose up -d
```

### 파일럿 D-day (Cloudflare Quick Tunnel)
```bash
# `/pilot-deploy` 슬래시 커맨드로 자동화
# 또는 kids_edu_vault/wiki/runbooks/deployment.md 수동 절차 참조
```

### 정식 운영 (fly.io VPS) — 준비 중
- `fly.toml` 스텁 존재 (`src/backend/fly.toml`)
- SQLite 볼륨: `fly volumes create kids_edu_data`
- `fly deploy`
