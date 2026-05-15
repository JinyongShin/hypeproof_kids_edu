---
type: decision
title: "ADR: LangGraph + Gemini 백엔드 전환"
status: active
created: 2026-05-01
updated: 2026-05-15
tags:
  - decision
  - adr
  - backend
  - langgraph
  - gemini
---

# ADR: LangGraph + Gemini 2.5 Flash 백엔드 전환

**날짜**: 2026-05-01  
**브랜치**: `feature/langgraph-gemini` → **main 머지 완료 (2026-05-15, PR#7)**  
**상태**: active (merged)

---

## 결정

기존 `genai_runner.py` 단일 LLM 호출 방식을 **LangGraph StateGraph + Gemini 2.5 Flash** 스택으로 전면 교체.

---

## 배경 — 이전 방식의 한계

| 문제 | 내용 |
|------|------|
| 단일 LLM 라우팅 | 모든 인텐트(카드·게임·잡담)를 하나의 프롬프트로 처리 → 복잡도 증가 |
| spec deep-merge | 게임 편집 시 스펙 diff 방식 → 구조적 변경이나 시각 변경 대응 불가 |
| 컨텍스트 소실 | 세션이 길어지면 이전 대화 맥락이 날아감 |
| 테스트 불가 | 모든 LLM 호출이 뭉쳐 있어 단위 테스트 작성 불가 |

---

## 채택한 구조

### 그래프 토폴로지

```
classify_intent
    ├─ game_create → generate_spec → validate_and_build → save_game → summarize_turn
    ├─ game_edit  → edit_code ──────────────────────────→ save_game → summarize_turn
    ├─ card       → generate_card → save_card ──────────────────────→ summarize_turn
    └─ chitchat   → chitchat ──────────────────────────────────────→ summarize_turn
```

### 노드 목록 (`app/graph/nodes.py`)

| 노드 | 역할 | LLM |
|------|------|-----|
| `classify_intent_node` | 인텐트 분류 (4종) | intent_llm (temp=0.1, 64 tokens) |
| `generate_card_node` | 캐릭터/세계 카드 생성 | card_llm (temp=0.7, 2048 tokens) |
| `save_card_node` | 카드 DB 저장 | — |
| `generate_spec_node` | 게임 스펙 JSON 생성 | spec_llm (temp=0.5, 1024 tokens) |
| `edit_code_node` | 게임 HTML 전체 편집 | edit_llm (temp=0.3, **16384 tokens**) |
| `validate_and_build_node` | 스펙 검증 + HTML 빌드 | — |
| `save_game_node` | 게임 HTML DB/파일 저장 | — |
| `chitchat_node` | 자유 대화 | card_llm |
| `summarize_turn_node` | 매 턴 롤링 컨텍스트 요약 (200자) | summary_llm (temp=0.1, 256 tokens) |

### edit_code 핵심 변경점

이전: 스펙 diff → JSON merge → HTML 재조립  
이후: **현재 게임 HTML 전체를 LLM에 전달 + Pydantic 구조화 출력**으로 수정된 HTML 직접 반환.
구조적 변경(새 UI 요소 추가)과 시각 변경(색상·크기) 모두 단일 패스에서 처리.

### 롤링 컨텍스트 (`summarize_turn_node`)

매 턴 종료 시 카드·게임·발화를 200자 이내로 압축 → `EduSessionState.session_context`에 저장.
다음 턴의 모든 LLM 노드에 시스템 프롬프트로 주입됨.

### 상태 스키마 (`app/graph/state.py`)

```python
class EduSessionState(TypedDict):
    messages: Annotated[list, add_messages]  # LangGraph 관리
    session_id: str
    child_id: str
    tenant_id: str          # MVP: "default"
    latest_character: Optional[dict]
    latest_world: Optional[dict]
    current_spec: Optional[dict]
    current_game_html: Optional[str]
    current_game_url: Optional[str]
    intent: Optional[str]   # "card"|"game_create"|"game_edit"|"chitchat"
    card_result: Optional[dict]
    card_url: Optional[str]
    hint: Optional[str]
    session_context: Optional[str]  # 롤링 요약
    token_usage: dict
    error: Optional[str]
```

### 체크포인터 (상태 영속화)

- 프로덕션: `AsyncSqliteSaver` (`data/langgraph.db`)
- 테스트: `MemorySaver` (인메모리)
- `graph_lifespan()` async context manager로 main.py에서 lifespan 관리

---

## LLM 구성 (`app/llm.py`)

모든 모델: `gemini-2.5-flash-preview-04-17`  
역할별로 temperature·max_output_tokens를 분리해 비용/품질 최적화.

```python
get_card_llm()    # temp=0.7, 2048 tokens — 창의적 카드 생성
get_spec_llm()    # temp=0.5, 1024 tokens — 결정론적 스펙 생성
get_edit_llm()    # temp=0.3, 16384 tokens — 전체 HTML 반환
get_summary_llm() # temp=0.1, 256 tokens — 짧고 정확한 요약
get_intent_llm()  # temp=0.1, 64 tokens — 분류 전용
```

`MOCK_LLM=1` 환경변수로 모든 LLM을 `FakeListChatModel`로 대체 → CI/단위테스트 비용 없음.

---

## 테스트 커버리지

`b5551d5` 커밋 기준 68개 pytest 통과 (MOCK_LLM=1):

| 테스트 파일 | 내용 |
|------------|------|
| `test_auth.py` | DB 인증 + env-var fallback |
| `test_card_node.py` | 카드 생성 노드 |
| `test_edit_loop.py` | 게임 편집 루프 |
| `test_graph_routing.py` | 인텐트별 라우팅 |
| `test_spec_node.py` | 스펙 생성 노드 |
| `test_summarize_turn.py` | 롤링 요약 노드 |
| `test_ws_handler.py` | WebSocket 핸들러 |

---

## 결과

- 코드 복잡도 격리: 각 노드 독립 테스트 가능
- 인텐트별 LLM 파라미터 튜닝 가능
- 롤링 컨텍스트로 긴 세션에서도 맥락 유지
- 체크포인터로 서버 재시작 후에도 세션 복원

## PR#7 리뷰 반영 (2026-05-15 머지)

PR 리뷰(ico1036) 3건에서 제기된 항목 중 코드 수정이 필요한 것만 처리. 이미 구현된 것은 코멘트로 확인.

| 항목 | 처리 방식 | 커밋 |
|------|---------|------|
| `nodes.py` `sys.path.insert` 7회 반복 | 모듈 레벨 1회로 통합 | `ad4ca19` |
| `edit_code_node` 실패 시 무음 | `error: "edit_code_failed"` → `save_game_node`에서 "수정을 제대로 못했어" 피드백 | `ad4ca19` |
| `docker-compose.yml` Langfuse 시크릿 하드코딩 | `${VAR:-fallback}` 패턴 + `.env.langfuse.example` 추가 | `ad4ca19` |
| 프론트엔드 `.env.example` 없음 | `src/frontend/.env.example` 신규 추가 | `ad4ca19` |
| `test_auth_session_game.py` 깨진 import | `claude_runner` → `app.graph.nodes` 수정 | `ad4ca19` |

**이미 구현 확인됨 (수정 불필요)**:
- WebSocket 재연결: `hooks/useChat.ts` — 3회 재시도 + `wsStatus` UI 구현됨
- SQLite WAL 모드: `storage.py:95` `PRAGMA journal_mode=WAL` 설정됨
- JWT SECRET_KEY: `app/auth.py` 환경변수 기반 확인됨

**파일럿 후 처리 예정**: Ping/Pong 하트비트, iframe CSP 헤더, 10턴+ rolling summary

---

## 관련 페이지

- [[adr-container-deployment]] — 이 백엔드를 컨테이너로 배포하는 결정
- [[adr-multitenant-schema]] — 멀티테넌트 DB 스키마 결정
- [[langfuse-observability]] — LLM 호출 관측성 설정
