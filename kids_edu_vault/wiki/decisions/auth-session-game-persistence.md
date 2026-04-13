---
type: decision
status: proposed
priority: 1
date: 2026-04-13
owner: "JY"
context: "파일럿 MVP 이후 — 다중 아동 세션 관리·게임 파일 영구 저장·로그인 식별 필요"
tags:
  - decision
  - pilot/feature
  - auth
  - session
  - game-persistence
created: 2026-04-13
updated: 2026-04-13
related:
  - "[[pivot-to-chat-preview-wrapper]]"
  - "[[iframe-sandbox-over-webcontainers]]"
  - "[[nextjs-fastapi-wrapper-architecture]]"
  - "[[product-requirements]]"
---

# 로그인 · 채팅 세션 관리 · 게임 HTML 파일 저장 (통합 ADR)

## 결정

세 가지 기능을 하나의 배포 단위로 구현한다.

1. **하드코딩 로그인** — 앱 진입 시 로그인 화면 표시. `root / 0000` 계정 검증. 성공 시 `child_id = "root"` 를 sessionStorage + React state 에 보관.
2. **채팅 세션 Create / Delete / Switch** — `{child_id}_{timestamp}` 형식 `session_id` 로 다중 세션 관리. 사이드패널 목록 + 새 세션·삭제 버튼. 세션 전환 시 마지막 게임 URL 복원.
3. **게임 HTML 파일 저장 + URL 서빙** — `game` 이벤트 발생 시 `src/backend/data/games/{child_id}/{session_id}/{game_id}.html` 로 디스크 저장. `GET /games/{child_id}/{session_id}/{game_id}` 로 서빙. 프론트엔드 `<iframe srcDoc>` → `<iframe src={gameUrl}>` 전환.

## 근거

- 병동 환경에서 여러 아이가 탭·세션을 전환하며 쓰므로 세션 구분이 필수. ([[product-requirements]] R8)
- 게임 URL이 있어야 QR 공유·갤러리뷰([[product-requirements]] R7, R8)가 가능. srcdoc 은 URL 을 가질 수 없음.
- JWT/쿠키는 병동 테스트 환경에서 설정 복잡도를 높이므로 테스트용 하드코딩 + sessionStorage 로 충분. ([[track-a-primary-b-backup]])
- `allow-same-origin` 금지 원칙([[iframe-sandbox-over-webcontainers]])은 `src=` 전환 후에도 유지 — localhost URL 이어도 sandbox 속성 유지.

## 대안 및 기각 이유

| 대안 | 기각 이유 |
|---|---|
| JWT + 쿠키 인증 | 병동 테스트용으로 과도. 파일럿 이후 정식 출시 시 도입 예정 |
| srcdoc 유지 + blob URL | 세션 전환 후 복원 불가. blob URL 은 탭/새로고침 시 소멸 |
| DB (SQLite 등) 세션 저장 | 단순 JSON 파일이면 충분. 외부 의존성 추가 금지 원칙 적용 |
| URL 쿼리파라미터 방식 child_id | 현재 방식 유지. 로그인 후 state 로 덮어씀 — URL 은 그대로 두어 하위 호환 |

## 영향 범위

### 변경 파일 목록 및 내용

#### 백엔드

**`src/backend/main.py`**
- `GET /sessions/{child_id}` — child_id 의 session 목록 반환. SessionStore 에서 읽음.
- `POST /sessions/{child_id}` — 새 세션 생성. `session_id = f"{child_id}_{int(time.time()*1000)}"`. SessionStore 에 빈 항목으로 등록 후 반환.
- `DELETE /sessions/{child_id}/{session_id}` — 해당 세션의 claude session_id 제거 + sessions.json 에서 삭제.
- `GET /games/{child_id}/{session_id}/{game_id}` — `data/games/{child_id}/{session_id}/{game_id}.html` 파일을 `text/html` 로 서빙. 없으면 404.
- `StaticFiles` mount 대신 직접 파일 읽기 엔드포인트 사용 (sandbox 우회 방지).
- 기존 `/ws/chat/{child_id}` 경로 **변경 없음**. WebSocket 연결 시 추가 파라미터 `session_id` 를 쿼리스트링으로 수신: `/ws/chat/{child_id}?session_id={session_id}`.

**`src/backend/claude_runner.py`**
- `stream_claude(prompt, child_id, session_id)` 시그니처 변경 — 세 번째 인자 추가.
- SessionStore 의 키를 `child_id` 단독 → `f"{child_id}:{session_id}"` 복합키로 변경.
  - `get`, `__setitem__`, `__delitem__`, `__contains__` 모두 복합키 기반으로 교체.
- `game` 이벤트 발생 시 (`html_match` 성공 시) `_save_game_html` 내부 함수 호출:
  - 경로: `_DATA_DIR / "games" / child_id / session_id / f"{game_id}.html"`
  - `game_id = str(int(time.time() * 1000))`
  - 디렉터리 `mkdir(parents=True, exist_ok=True)` 후 파일 기록.
  - `StreamEvent` 에 `game_id: str = ""` 필드 추가. `game` 이벤트 시 `game_id` 포함 yield.
- Mock 모드도 동일하게 `game_id` 포함 (`"mock-game-{timestamp}"`).

**`src/backend/data/sessions.json`**
- 스키마 변경: `{ "child_id:session_id": "claude_session_id" }`. 기존 `{ "child_id": "claude_session_id" }` 와 호환 불가 → 기동 시 old-format 자동 감지 후 비워서 재초기화 (경고 로그 출력).

#### 프론트엔드

**`src/frontend/app/login/page.tsx` (신규)**
- 로그인 폼 컴포넌트. `username` + `password` 입력.
- 검증: `username === "root" && password === "0000"` — 성공 시 `sessionStorage.setItem("child_id", "root")` + `router.push("/")`.
- 실패 시 "아이디 또는 비밀번호가 틀렸어요" 인라인 에러.
- 이미 로그인돼 있으면 (`sessionStorage.getItem("child_id")`) `/` 로 즉시 redirect.

**`src/frontend/app/page.tsx`**
- `useSearchParams` 로 `child` 파라미터 읽는 로직 제거.
- 대신 `sessionStorage.getItem("child_id")` 로 `childId` 획득.
- 없으면 `router.replace("/login")` 으로 redirect.
- `activeSessionId` state 추가 (초기값: `sessionStorage.getItem("active_session_id") ?? ""`).
- `gameUrl` state 추가 (초기값 `""`). `gameHtml` state 제거 — URL 기반으로 교체.
- `onGameReady(gameUrl: string)` 콜백을 `ChatPane` 에 전달. 기존 `onGameHtmlChange` 대체.
- 사이드패널 (`SessionSidebar`) 렌더링 추가: 왼쪽 고정 폭 또는 슬라이드-아웃. 모바일에서는 햄버거 버튼으로 토글.
- 로그아웃 버튼: 헤더 우상단. 클릭 시 `sessionStorage.clear()` + `router.replace("/login")`.

**`src/frontend/components/SessionSidebar.tsx` (신규)**
- Props: `childId`, `activeSessionId`, `onSessionChange(sessionId: string)`, `onLogout()`.
- 마운트 시 `GET /sessions/{childId}` 호출 → 세션 목록 표시.
- "새 세션" 버튼: `POST /sessions/{childId}` → 응답 `session_id` 로 목록 갱신 + `onSessionChange` 호출.
- 세션 항목 클릭: `onSessionChange(sessionId)` 호출.
- 세션 삭제 버튼 (각 항목 우측): `DELETE /sessions/{childId}/{sessionId}` → 목록에서 제거.
  - 활성 세션 삭제 시 남은 목록 중 첫 번째로 자동 전환. 목록 비면 새 세션 자동 생성.
- 세션 이름 표시: `session_id` 의 timestamp 부분을 `HH:mm` 으로 파싱해 표시 (`{childId} 세션 HH:mm`).

**`src/frontend/components/GamePreview.tsx`**
- Props 변경: `html: string` → `gameUrl: string`.
- 빈 문자열이면 기존과 동일한 대기 화면.
- `<iframe srcDoc={html}>` → `<iframe src={gameUrl}>`.
- sandbox 속성 `"allow-scripts"` 유지. `allow-same-origin` 추가 금지.

**`src/frontend/components/ChatPane.tsx`**
- Props 변경: `onGameHtmlChange` → `onGameReady(gameUrl: string)`.
- `session_id` prop 추가 (string). `useChat` 훅에 전달.
- `useChat` 에서 반환하는 `gameUrl` 을 `onGameReady` 로 전달.

**`src/frontend/hooks/useChat.ts`**
- 시그니처: `useChat(childId: string, sessionId: string): UseChatReturn`.
- WS URL 변경: `/ws/chat/${childId}?session_id=${sessionId}`.
- `sessionId` 변경 시 기존 WebSocket 닫고 재연결 (`useEffect` deps 에 `sessionId` 추가).
- `gameHtml` state 제거. `gameUrl` state 추가.
- `game` 이벤트 수신 시: `data.game_url` (백엔드가 내려주는 절대 URL) 을 `gameUrl` 에 저장.
  - 백엔드 `done` 이벤트에 `game_url` 필드 추가 (아래 WS 프로토콜 변경 참조).
- `UseChatReturn` 에 `gameUrl: string` 추가, `gameHtml` 제거.

#### WS 이벤트 프로토콜 변경

```
// 기존
{"type": "game", "html": "<!DOCTYPE..."}
{"type": "done", "hint": "...", "session_id": "..."}

// 변경 후
{"type": "game", "game_url": "http://localhost:8000/games/{child_id}/{session_id}/{game_id}"}
{"type": "done", "hint": "...", "session_id": "...", "game_url": "http://localhost:8000/games/..."}
```

html 페이로드는 WS 를 통해 프론트엔드로 전송하지 않음. 파일로 저장 후 URL 만 내려보냄.

#### 환경 변수

**`.env.example` 추가**
```
BACKEND_BASE_URL=http://localhost:8000
```

**`src/frontend/` `.env.local` 추가**
```
NEXT_PUBLIC_BACKEND_HTTP_URL=http://localhost:8000
```

`useChat.ts` 에서 `game_url` 구성 시 백엔드가 완성된 URL 을 내려주므로 프론트는 조합 불필요.

## Open Questions

- [ ] 세션 목록 UI — 사이드바(왼쪽 고정) vs 드롭다운(헤더 내)? 모바일 레이아웃과의 충돌 검토 필요. 구현자 판단.
- [ ] `sessions.json` 의 claude session 복합키 변경으로 기존 실행 중인 인스턴스의 세션이 초기화됨 — 파일럿 전 배포 순서 주의. 세션 마이그레이션은 별도 ADR 불필요(일회성).
- [ ] 게임 HTML 파일 보존 기간 정책 미정 — 파일럿 종료 후 수동 정리 가정. 자동 만료 로직은 이 ADR 범위 밖.
- [ ] `/ws/chat/{child_id}?session_id=` 쿼리스트링이 없는 기존 연결 처리 — `session_id` 없으면 WS 400 으로 거부할지, 아니면 임시 `{child_id}_default` 세션으로 폴백할지 구현자 결정.

## 관련

- [[pivot-to-chat-preview-wrapper]]
- [[iframe-sandbox-over-webcontainers]]
- [[nextjs-fastapi-wrapper-architecture]]
- [[product-requirements]]
- [[track-a-primary-b-backup]]
- [[mobile-swipe-navigation]]
