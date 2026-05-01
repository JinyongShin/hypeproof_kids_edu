---
type: decision
title: "백엔드 LangGraph + Gemini 단일 스택 재작성"
created: 2026-05-01
updated: 2026-05-01
status: accepted
priority: 1
owner: "JY"
context: "파일럿(2026-05-05) 직후 상품화 v1 대비 — Claude CLI subprocess 의존 제거·게임 편집 루프 구현·대화 맥락 영속화"
tags:
  - decision
  - architecture
  - backend
  - langgraph
  - gemini
related:
  - "[[nextjs-fastapi-wrapper-architecture]]"
  - "[[llm-provider-scaling]]"
  - "[[auth-session-game-persistence]]"
  - "[[game-bug-fix-2026-05-01]]"
deciders:
  - "[[jinyong-shin]]"
---

# 백엔드 LangGraph + Gemini 단일 스택 재작성

## 결정

백엔드를 **LangGraph 워크플로우 그래프 + `langchain-google-genai` (Gemini 2.5 Flash) 단일 스택**으로 처음부터 재작성한다. Claude CLI subprocess 의존, GLM/Pollinations 혼용, 게임 편집 불가, 대화 맥락 재시작 소멸 문제를 일괄 해소한다.

## 근거

### 현재 문제

- **Claude CLI subprocess 의존** — 프로세스 관리 불안정, 버전 고정 어려움, 파이프 I/O 오류 재현 불가.
- **GLM (z.ai) + Pollinations 혼용** — Gemini API 크레딧이 이미 확보된 상태([[llm-provider-scaling]])임에도 별도 서드파티 의존.
- **게임 편집 불가** — "더 빠르게 해줘" 요청 시 전체 게임 재생성 → 이전 spec 무시. [[game-bug-fix-2026-05-01]] 에서 임시 패치했으나 근본 해결 아님.
- **대화 맥락 유실** — Claude `--resume` 플래그에 의존. 프로세스 재시작 시 맥락 소멸.

### LangGraph 선택 이유

- 워크플로우를 **선언적 그래프(노드 + 엣지)**로 표현 → 각 노드 독립 테스트 가능.
- `SqliteSaver` 체크포인터로 `thread_id` 기반 대화 상태 영속화 — 재시작 후에도 맥락 복원.
- `edit_spec_node`에서 `current_spec(state)`을 deep-merge 패치 → 게임 편집 루프 native 구현.
- `langchain-google-genai`로 Gemini 2.5 Flash를 LangChain 표준 인터페이스로 사용 — 추후 모델 교체 시 한 줄 변경.

### 재사용 자산

- `game_engine.py` — 순수 Python, LLM 없음. 그대로 재사용.
- WebSocket 프로토콜([[auth-session-game-persistence]] 정의) — 완전 보존. 프론트엔드 변경 없음.
- SQLite DB 파일 경로 및 게임 HTML 파일 저장 구조 — 그대로 유지.

## 그래프 노드 설계

| 노드 | 역할 |
|---|---|
| `classify_intent` | 입력 의도 분류 (카드 생성 / 게임 생성 / 게임 편집 / 잡담) |
| `generate_card` | 캐릭터 카드 생성 |
| `generate_spec` | 게임 spec 신규 생성 |
| `edit_spec` | 기존 spec을 deep-merge 패치로 수정 |
| `validate_and_build` | spec 검증 후 `game_engine.py` 호출 |
| `save_card` | 카드 저장 + WS 이벤트 emit |
| `save_game` | 게임 HTML 저장 + URL 생성 + WS 이벤트 emit |
| `chitchat` | 일반 대화 응답 |

## 대안 및 기각 이유

| 대안 | 기각 이유 |
|---|---|
| Google ADK | Gemini 락인 심함, 추후 Claude/OpenAI 혼용 불가 |
| Claude SDK 직접 사용 | Anthropic 크레딧 미확보, Gemini 크레딧 활용 못 함 |
| 현행 유지 (subprocess + GLM) | 게임 편집 루프 구현 불가, 맥락 영속화 미지원 구조적 한계 |
| FastAPI + 단순 함수 체인 | 상태 관리·분기·폴백 로직이 스파게티화 — 그래프 선언 대비 유지보수 불가 |

## 영향 범위

- **대체**: `src/backend/claude_runner.py` / `src/backend/genai_runner.py` — 삭제 후 `src/backend/graph/` 신규 구현.
- **보존**: `src/backend/game_engine.py`, `src/backend/storage.py`, `src/backend/main.py` (WS 라우팅 레이어만 유지).
- **추가 의존성**: `langchain-google-genai`, `langgraph`, `langgraph-checkpoint-sqlite` (`pyproject.toml`).
- **새 파일**: `src/backend/langgraph.db` (체크포인터 영속화, gitignore 추가 필요).
- **하위 결정 영향**: [[llm-provider-scaling]] 폴백 체인은 `classify_intent` 노드 실패 시 재진입 지점으로 재설계 필요.

## Open Questions

- [ ] `langgraph.db` 파일을 `kids_edu.db`와 같은 경로(`src/backend/data/`)에 둘지, 별도 경로로 분리할지 결정 필요.
- [ ] Gemini 2.5 Flash 무료 티어 RPM이 파일럿 40명 동시 부하에서 충분한지 [[llm-provider-scaling]] 결과와 교차 검증 필요.
- [ ] `edit_spec` 노드의 deep-merge 전략 — shallow merge vs. JSON Merge Patch (RFC 7396) vs. JSON Patch (RFC 6902) 선택은 구현자 판단.
- [ ] `classify_intent` 노드 프롬프트 튜닝 — 잡담/게임편집 경계 케이스 테스트 케이스 필요.

## 구현 현황 (2026-05-01 완료)

feature/langgraph-gemini 브랜치에서 전체 구현 완료.

### 최종 의존성 (pyproject.toml)
- `langfuse>=2.0,<3.0` — Langfuse 서버 v2와의 호환성 (v3 SDK는 OTLP 전용)
- `langchain>=0.2,<1.0` — langfuse v2 CallbackHandler 의존
- `langchain-google-genai>=2.1` — Gemini LLM
- `langgraph>=0.3` — 그래프 엔진 + AsyncSqliteSaver

### 핵심 구현 파일
- `app/graph/state.py` — EduSessionState TypedDict
- `app/graph/nodes.py` — 8개 노드 (classify_intent, generate_card, save_card, generate_spec, edit_spec, validate_and_build, save_game, chitchat)
- `app/graph/edges.py` — 조건부 엣지 3개
- `app/graph/graph.py` — build_graph() + graph_lifespan() async context manager
- `app/llm.py` — get_card/spec/edit/intent_llm() + MOCK_LLM=1 FakeListChatModel
- `ws_handler.py` — astream_events v2 → WebSocket 브릿지 + Langfuse callback 주입

### 테스트
64개 테스트 전체 통과 (`uv run pytest -v`)
- test_graph_routing.py, test_card_node.py, test_spec_node.py, test_edit_loop.py, test_ws_handler.py, test_auth.py

### Langfuse 관측성
- `langfuse.callback.CallbackHandler` (v2 API)
- `LANGFUSE_HOST: http://langfuse:3000` — Docker 내부 서비스명 (docker-compose.yml에서 오버라이드)
- `.env.local`에 `LANGFUSE_ENABLED=true`, `LANGFUSE_PUBLIC_KEY`, `LANGFUSE_SECRET_KEY`, `LANGFUSE_HOST` 설정

## 관련

- [[nextjs-fastapi-wrapper-architecture]]
- [[llm-provider-scaling]]
- [[auth-session-game-persistence]]
- [[game-bug-fix-2026-05-01]]
- [[single-html-runtime]]
