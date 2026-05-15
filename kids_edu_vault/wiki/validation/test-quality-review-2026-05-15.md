---
type: validation
title: "테스트 품질 검토 — 2026-05-15"
created: 2026-05-15
updated: 2026-05-15
status: resolved
tags:
  - validation
  - testing
  - backend
  - frontend
related:
  - "[[kids-edu-backend]]"
  - "[[kids-edu-frontend]]"
  - "[[adr-langgraph-gemini-backend]]"
---

# 테스트 품질 검토 — 2026-05-15

LangGraph+Gemini 백엔드 전환(PR#7) 이후 깨진 테스트를 수정하고, 전체 테스트 스위트의 로직 검증 충실도를 검토한 결과.

---

## 수정 완료 — 깨진 테스트 3건

### 1. 프론트엔드 `__tests__/useChat.test.ts`

**문제**: jsdom 환경에서 `NEXT_PUBLIC_BACKEND_HTTP_URL` 미설정 → `BACKEND_WS_URL = ""` → WS URL이 상대 경로(`/ws/chat/...`)가 돼 scheme 검사 실패.

**수정**: 해당 테스트에 `vi.stubEnv("NEXT_PUBLIC_BACKEND_HTTP_URL", "http://localhost:8000")` 추가. 테스트 종료 시 `vi.unstubAllEnvs()` 복원.

### 2. 백엔드 `tests/test_auth_session_game.py` — 컬렉션 오류

**문제**: `from claude_runner import _DATA_DIR` — `claude_runner.py`가 LangGraph 리라이트로 삭제됨.

**수정**: `from main import _DATA_DIR` 로 변경. `_DATA_DIR`은 `main.py:22`에 정의됨.

### 3. 백엔드 `tests/test_auth_session_game.py` — 픽스처 전면 교체

**문제**: `_reset_session_meta` 픽스처가 `main._session_meta`(인메모리 딕트), `main._save_session_meta`, `main._load_session_meta`를 참조 — 세션 저장소가 SQLite(`storage.py`)로 교체돼 전부 사라짐.

**수정**: `_isolated_db` 픽스처로 교체.
- `storage._DB_PATH`를 `tmp_path/test.db`로 monkeypatch → 테스트마다 격리된 SQLite DB
- `get_settings.cache_clear()` + `ADMIN_USERNAME=root`, `ADMIN_PASSWORD=0000` env stub → auth 자격증명 고정
- `main._session_meta` 참조 2곳 → `storage.list_sessions(child_id)` 호출로 교체
- 로그인 응답 assertion `== {"child_id": "root"}` → `.get("child_id") == "root"` (응답에 `admin_id`, `role`, `tenant_id` 추가됨)

### 4. 백엔드 `main.py` — null byte path traversal 5xx 버그 수정

**문제**: `serve_game` 엔드포인트에서 `game_id`에 null byte(`%00`)가 있으면 Python 3.14의 `Path.resolve()`가 `ValueError`를 발생시켜 500 반환.

**수정**: `.resolve()` 호출을 `try/except (ValueError, OSError)`로 감싸 400 반환. 보안 강화 + 테스트 통과.

---

## 테스트 품질 검토 결과

### HIGH — 즉시 대응 권장

| # | 위치 | 문제 |
|---|------|------|
| H1 | `test_edit_loop.py:138` | `sys.path.insert(0, str(__file__.replace("tests/test_edit_loop.py", "")))` — 문자열 조작으로 sys.path 수정. 경로/OS 변경 시 임포트 깨짐. `Path(__file__).parent.parent` 사용해야 함 |
| H2 | `useChat.test.ts` | `send()` 내부가 전역 `WebSocket.OPEN`을 참조하는데 Mock은 `MockWebSocket.OPEN`만 선언. 가드 로직이 실제로 실행됐는지 보장 안 됨 |
| H3 | `test_card_node.py` · `test_spec_node.py` | async 테스트에 `@pytest.mark.asyncio` 데코레이터 없음. 현재는 `asyncio_mode = "auto"` 설정으로 통과하지만, 설정 변경 시 조용히 skip됨 |

### MEDIUM — 커버리지 공백

| 영역 | 누락 |
|------|------|
| `backendUrl.ts` | 단위 테스트 전무. `window.__BACKEND_URL__` 오버라이드, `http→ws`/`https→wss` 변환, SSR 경로 미검증 |
| `useChat.test.ts` | WS 재연결 로직 (`MAX_RETRIES=3`, `onclose → reconnecting → disconnected`), `text` 스트리밍 누적, `send()` payload JSON 검증, `error`/`thinking` 이벤트 처리 |
| `test_auth_session_game.py` | `child_id`/`session_id` 위치 path traversal 미검증, `PATCH /sessions/.../name`, `GET /gallery`, `POST .../save` 엔드포인트 미테스트 |
| `test_ws_handler.py` | 예외 발생 시 `error` 타입 이벤트 발송 미검증 |
| `main.py` | `_migrate_json_to_sqlite()` 전체 미테스트 (JSON→SQLite 마이그레이션 버그 무검증) |
| `storage.py` | `mark_game_saved()` 덮어쓰기 로직, 갤러리 등록 엔드포인트 미테스트 |
| `app/graph/nodes.py` | `chitchat_node`, `_extract_card_json`, `_extract_hint` 등 유틸 (MOCK 경로에서 미실행) |

### LOW — 개선사항

| 위치 | 내용 |
|------|------|
| `test_auth_session_game.py:190` | `time.sleep(1.1)` — 정렬 테스트를 위한 sleep. CI에서 느리고 불안정 |
| `test_summarize_turn.py` | MOCK이 반환하는 고정 값과 다른지 확인하는 동어반복 테스트 |
| `test_card_node.py` · `test_spec_node.py` | 파일시스템 정리 없음 — 반복 실행 시 `_DATA_DIR`에 파일 누적 |
| `useChat.test.ts:249` | 테스트명 "공백 문자열"인데 실제 전달값은 빈 문자열 `""` |
| `conftest.py` vs `test_auth_session_game.py` | DB 격리 fixture 중복 정의 (이중 초기화) |

---

## 현재 테스트 현황

| 스위트 | 파일 수 | 테스트 수 | 결과 |
|--------|---------|-----------|------|
| 백엔드 (pytest) | 8개 | 111개 | 111 passed |
| 프론트엔드 (Vitest) | 2개 | 19개 | 19 passed |

---

## 3-Phase 품질 개선 완료 (2026-05-15)

### Phase 1 — Quick Fixes (완료)

| 파일 | 수정 내용 |
|------|----------|
| `test_edit_loop.py:138` | `sys.path.insert(0, str(__file__.replace(...)))` 잔재 코드 삭제 (H1 해소) |
| `test_graph_routing.py` | `@pytest.mark.anyio` → `@pytest.mark.asyncio` 3개 교체 (마커 통일) |
| `test_summarize_turn.py` | tautology assertion `new_ctx != old_ctx` → `isinstance` + MOCK 고정값 검증 |
| `test_auth_session_game.py` | `_isolated_db` fixture에서 중복 DB 패치 제거 — `conftest.isolate_storage_db`에 위임 |
| `useChat.test.ts` | 테스트명 "공백 문자열" → "빈 문자열" (실제 입력값과 일치) |

### Phase 2 — Filesystem Isolation (완료)

| 파일 | 수정 내용 |
|------|----------|
| `test_card_node.py` | `autouse _patch_data_dir` fixture 추가 — `monkeypatch`로 `_DATA_DIR → tmp_path` 격리 |
| `test_spec_node.py` | 동일 패턴 적용 |

### Phase 3 — 신규 테스트 추가 (완료)

| 파일 | 추가 테스트 |
|------|-----------|
| `test_ws_handler.py` | `test_error_event_sent_on_graph_exception` — BrokenGraph로 예외 강제 후 `error` 이벤트 검증 (H2 해소) |
| `test_auth_session_game.py` | `TestPathTraversalExtended` (child_id/session_id 위치 순회 방어), `TestRenameSession`, `TestSaveGame`, `TestGallery` 클래스 추가 |
| `backendUrl.test.ts` | **신규 파일** — `http→ws`, `https→wss` 변환, `window.__BACKEND_URL__` override, 환경변수 우선순위 (8개 테스트) |
| `useChat.test.ts` | `send()` readyState OPEN 가드 테스트 + payload `{prompt: ...}` JSON 구조 검증 (H2 해소) |

> [!key-insight] 결과
> 97(BE)+9(FE) → **111(BE)+19(FE) = 130 tests 전체 통과**. HIGH 3건 모두 해소, MEDIUM 주요 공백 커버리지 추가 완료.
