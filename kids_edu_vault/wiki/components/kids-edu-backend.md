---
type: component
title: "Kids Edu Backend"
created: 2026-04-12
updated: 2026-05-15
status: active
tags:
  - component
  - backend
  - fastapi
  - langgraph
  - pilot/2026-05-05
related:
  - "[[nextjs-fastapi-wrapper-architecture]]"
  - "[[adr-langgraph-gemini-backend]]"
  - "[[iframe-sandbox-over-webcontainers]]"
  - "[[ai-prompting-literacy-input]]"
---

# Kids Edu Backend

## 역할
FastAPI + LangGraph 기반 백엔드. 어린이의 채팅 입력을 받아 LangGraph StateGraph(Gemini 2.5 Flash)로 처리하고, 스트리밍 응답(텍스트 + 게임 HTML + 카드)을 WebSocket으로 실시간 전달. → [[adr-langgraph-gemini-backend]] 참조.

## 위치
`hypeproof_kids_edu/src/backend/`

## 실행
```bash
# 개발 (Mock LLM 모드)
MOCK_LLM=1 uv run uvicorn main:app --reload

# 실제 Gemini 연동
uv run uvicorn main:app --reload
```

## 주요 엔드포인트

| 경로 | 방식 | 설명 |
|---|---|---|
| `/health` | GET | 서버 상태 확인 |
| `/auth/login` | POST | 인증 (DB 우선, env-var 폴백) |
| `/sessions/{child_id}` | GET/POST | 세션 목록/생성 |
| `/sessions/{child_id}/{session_id}` | DELETE | 세션 삭제 |
| `/sessions/{child_id}/{session_id}/name` | PATCH | 세션 이름 변경 |
| `/sessions/{child_id}/{session_id}/messages` | GET | 채팅 히스토리 |
| `/games/{child_id}/{session_id}/{game_id}` | GET | 게임 HTML 파일 서빙 |
| `/games/{child_id}/{session_id}/{game_id}/save` | POST | 갤러리 등록 |
| `/gallery` | GET | 런칭쇼 갤러리 목록 |
| `/ws/chat/{child_id}` | WebSocket | 채팅 스트리밍 |

## 핵심 모듈

| 파일 | 역할 |
|------|------|
| `main.py` | FastAPI 앱 + 엔드포인트 |
| `storage.py` | SQLite 저장소 레이어 (sessions/messages/games/cards) |
| `ws_handler.py` | WebSocket 핸들러 |
| `app/graph/` | LangGraph StateGraph 정의 |
| `app/graph/nodes.py` | 개별 노드 구현 (classify, spec, card, game, edit, chitchat) |
| `app/auth.py` | bcrypt 인증 (DB + env-var 폴백) |
| `app/config.py` | pydantic-settings 환경 설정 |

## 데이터 저장소

SQLite (`data/kids_edu.db`). 테이블: `sessions`, `messages`, `games`, `cards`, `admins`, `tenants`, `token_log`.

> [!note] 구 JSON 파일 마이그레이션
> `session_meta.json` + `sessions.json` + `messages/` → SQLite. `_migrate_json_to_sqlite()` (`main.py:36`) 가 서버 기동 시 1회 실행. 미테스트 상태([[test-quality-review-2026-05-15]] MEDIUM 항목).

## 환경변수 (.env.local)

| 키 | 기본값 | 설명 |
|---|---|---|
| `GEMINI_API_KEY` | — | Gemini API 키 |
| `MOCK_LLM` | false | true이면 LLM 호출 없이 mock 응답 |
| `ADMIN_USERNAME` | admin | 관리자 아이디 |
| `ADMIN_PASSWORD` | admin | 관리자 비밀번호 |
| `BACKEND_BASE_URL` | http://localhost:8000 | 자기 자신 URL (게임 파일 URL 생성용) |

## 테스트

```bash
uv run pytest -v   # 97개 전체 통과 (2026-05-15 기준)
```

| 테스트 파일 | 커버 범위 |
|-------------|-----------|
| `test_auth.py` | bcrypt 해시/검증, DB·env-var 인증 경로 |
| `test_auth_session_game.py` | 엔드포인트 통합 (login/session CRUD/game 서빙/path traversal) |
| `test_card_node.py` | generate_card_node, save_card_node |
| `test_spec_node.py` | generate_spec_node → validate_and_build_node → save_game_node |
| `test_edit_loop.py` | edit_code_node, save_game_node |
| `test_graph_routing.py` | 라우팅 엣지 함수 단위 테스트 |
| `test_summarize_turn.py` | summarize_turn_node |
| `test_ws_handler.py` | WebSocket 이벤트 흐름 (card/game/done) |

> [!note] 테스트 품질 이슈
> [[test-quality-review-2026-05-15]] 참조. HIGH: `test_edit_loop.py` sys.path 문자열 조작. MEDIUM: 갤러리/save 엔드포인트 미테스트, `_migrate_json_to_sqlite` 미테스트.

## 보안 제약
- `serve_game` 엔드포인트: `Path.resolve()`로 경로 순회 방어 + null byte `ValueError` 400 반환 처리 (2026-05-15 수정)
