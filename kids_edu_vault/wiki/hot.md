---
type: meta
title: "Hot Cache"
created: 2026-04-12
updated: 2026-04-13
tags:
  - meta/cache
---

# Hot Cache — 2026-04-13

최근 컨텍스트 스냅샷. 세션 시작 시 가장 먼저 읽을 것.

---

## 현재 상태: 로그인 + 세션 관리 + 게임 저장 구현 완료

### 프로젝트 개요
- 목표: 소아암 병동 어린이(8-12세) AI 코딩 교육 파일럿 (2026-05-05)
- 스택: FastAPI (Python/uv) + Next.js 16 (App Router) + Claude CLI subprocess
- 래퍼: 채팅(WebSocket) + iframe 게임 프리뷰 + 블록별 프롬프트 스캐폴드

### 오늘 완료된 작업 (2026-04-13)

| 기능 | 내용 | 상태 |
|---|---|---|
| 로그인 | `/login` 페이지, 환경변수 자격증명, sessionStorage auth state | ✅ |
| 채팅 세션 관리 | Create/Delete/Switch 사이드바, REST API | ✅ |
| 게임 HTML 파일 저장 | srcdoc → 파일 저장 + URL 서빙, React 재렌더 버그 해결 | ✅ |
| 보안 수정 4건 | 경로 순회 방어, 환경변수 자격증명, WS accept 순서, asyncio.Lock | ✅ |
| 백엔드 테스트 | pytest 29개 통과 | ✅ |
| 프론트엔드 테스트 | Vitest 9개 통과 | ✅ |

### 아키텍처 요약 (최신)

```
아이 브라우저
  └─ Next.js (localhost:3000)
       ├─ /login — 로그인 페이지 (root/0000, 환경변수 기반)
       ├─ SessionSidebar — 세션 목록·생성·삭제
       ├─ ChatPane — WebSocket → /ws/chat/{child_id}?session_id={session_id}
       └─ GamePreview — <iframe src="/games/{child_id}/{session_id}/{game_id}">

FastAPI (localhost:8000)
  ├─ GET/POST/DELETE /sessions/{child_id}
  ├─ GET /games/{child_id}/{session_id}/{game_id}  ← HTML 파일 서빙
  └─ WS /ws/chat/{child_id}?session_id={session_id}
       └─ game 이벤트: HTML 디스크 저장 후 game_url 반환 (html 페이로드 미전송)
```

### 핵심 파일 경로 (신규·변경)
- `src/frontend/app/login/page.tsx` — 로그인 페이지 (신규)
- `src/frontend/components/SessionSidebar.tsx` — 세션 사이드바 (신규)
- `src/frontend/hooks/useChat.ts` — WS + gameUrl state (갱신)
- `src/frontend/components/ChatPane.tsx` — session_id prop + onGameReady (갱신)
- `src/frontend/components/GamePreview.tsx` — srcdoc → src (갱신)
- `src/backend/main.py` — 세션·게임 REST API 추가 (갱신)
- `src/backend/claude_runner.py` — 복합키 SessionStore + _save_game_html (갱신)
- `src/backend/tests/test_auth_session_game.py` — 29개 TDD 테스트 (신규)

### WS 이벤트 프로토콜 변경
```
// 기존
{"type": "game", "html": "<!DOCTYPE..."}
{"type": "done", "hint": "...", "session_id": "..."}

// 변경 후
{"type": "game", "game_url": "http://localhost:8000/games/{child_id}/{session_id}/{game_id}"}
{"type": "done", "hint": "...", "session_id": "...", "game_url": "http://localhost:8000/games/..."}
```

### 환경 변수 (최신)
```
CLAUDE_TIMEOUT=120
CLAUDE_MODEL=sonnet
MOCK_CLAUDE=0
ADMIN_USERNAME=root        # 신규 (기본값 root)
ADMIN_PASSWORD=0000        # 신규 (기본값 0000)
NEXT_PUBLIC_BACKEND_HTTP_URL=http://localhost:8000
```

### 보안 결정 & 주의사항
- 경로 순회 방어: `path.resolve().is_relative_to(base)` 검증 — 게임 파일 서빙 엔드포인트
- 자격증명: `.env.local` 환경변수 이동. 하드코딩 금지
- WebSocket: `accept()` 는 인증 검증 이전에 호출해야 함 (순서 수정 완료)
- 동시 쓰기: `asyncio.Lock` 으로 race condition 방어
- iframe sandbox: `"allow-scripts"` 유지. `allow-same-origin` 추가 금지
- 세션당 최신 게임 10개 보관 (초과 시 오래된 파일 자동 삭제)

### ADR
- [[auth-session-game-persistence]] — status: implemented (2026-04-13)

### 커밋
- `5ee623b` fix(frontend): 재로그인 시 게임 복원 + 로딩 UI 개선
- `2d8693f` fix(frontend): React Strict Mode WS 오류 메시지 오탐 수정
- `2e9f555` feat: 로그인 + 세션 관리 + 게임 HTML 파일 저장

### 다음 단계 — 상품 요구사항 갭 잔여
| 우선순위 | 항목 | 내용 |
|---|---|---|
| P0 | R4 폴백 | Claude 실패 시 기본 게임 자동 삽입 |
| P0 | R9 밝은 UI | 다크 테마 → 밝은 테마, 큰 글씨, 촬영 친화적 |
| P1 | R8 결과물 공유 | 게임 URL QR 공유 (파일 저장은 오늘 완료) |
| P2 | R7 갤러리 | 퍼실리테이터용 전체 작품 뷰 |

- 리허설 (2026-04-26): P0 완료 목표
- 파일럿 (2026-05-05): P1 완료 목표
