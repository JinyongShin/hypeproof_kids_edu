---
type: session
title: "2026-04-18 UX 개선 5종 구현 + QA"
created: 2026-04-18
updated: 2026-04-18
status: completed
tags:
  - dev/frontend
  - dev/backend
  - qa
related:
  - "[[kids-edu-frontend]]"
  - "[[kids-edu-backend]]"
---

# 2026-04-18 — UX 개선 5종 구현 + QA

파일럿(2026-05-05) 대비 아동 UX 및 병원 네트워크 안정성을 위한 5가지 개선을 구현하고 실제 Claude로 E2E QA를 수행한 세션.

---

## 배경 — 식별된 문제점

현재 구현을 분석해 파악한 5가지 결함:

| # | 문제 | 영향 |
|---|---|---|
| 1 | `iframe src={gameUrl}` — 게임마다 HTTP 요청 | 병원 네트워크 불안정 시 게임 화면 빈 채로 남음 |
| 3 | Python 예외 문자열이 아이에게 그대로 노출 | `TimeoutExpired: Command ['claude'...]` 등 |
| 4 | 블록 버튼에 숫자 `0~5`만 표시 | 아이들이 무엇을 배우는지 알 수 없음 |
| 5 | 최대 120초 대기 중 스피너만 표시 | 아이들 불안 유발 |
| 6 | WS 재연결 중임을 UI에서 알 수 없음 | 퍼실리테이터/아이 혼란 |

---

## 구현 내용

### 개선 1 — iframe `srcdoc` 전환 (네트워크 독립성)

**변경 전**: `<iframe src="http://localhost:8000/games/...">` — 게임 볼 때마다 HTTP GET 발생.

**변경 후**: WebSocket `game` 이벤트에 `game_html` 필드 추가, 프론트에서 `srcDoc={gameHtml}`으로 렌더링.

- `claude_runner.py` — `StreamEvent(type="game", game_url=..., html=html_content)`
- `main.py` — `payload["game_html"] = event.html`
- `useChat.ts` — `gameHtml` 상태 추가, `game_html` 수신 시 설정
- `GamePreview.tsx` — `gameHtml ? { srcDoc: gameHtml } : { src: gameUrl }` 조건부 렌더

**세션 전환 시 폴백**: `gameHtml=""` → `src={gameUrl}` (디스크 파일 서빙). `allow-same-origin` 없음 유지 (보안).

**QA 확인**: `hasSrcdoc: true`, `src: null`, `/games/` HTTP 요청 **0건**.

---

### 개선 3 — 아동 친화적 에러 메시지

`claude_runner.py`에 `_friendly_error(kind)` 헬퍼 추가. 4종 에러 경로 교체:

| 경로 | 기존 | 변경 후 |
|---|---|---|
| `FileNotFoundError` | `"claude CLI를 찾을 수 없습니다."` | `"AI 도우미를 찾을 수 없어. 선생님한테 도움을 요청해봐! 🙏"` |
| `returncode != 0` | `f"claude 실행 오류: {stderr}"` | `"AI가 잠깐 실수했어. 다시 한 번 해볼까? 🔄"` |
| `TimeoutExpired` | `f"응답 시간 초과 ({CLAUDE_TIMEOUT}초)"` | `"AI가 너무 오래 생각했어. 다시 한 번 말해봐! ⏰"` |
| generic `Exception` | `str(e)` | `"뭔가 잘못됐어. 다시 한 번 해볼까? 😅"` |

원본 에러는 `logger.error` / `logger.exception`으로 유지.

---

### 개선 4 — 블록 UI 스킬 이름 표시

`ChatPane.tsx` 블록 버튼: `SCAFFOLD_DATA` import, 숫자→ `"1 묘사하기"` 형태.

- 1-based 표시 (`block + 1`), 내부 값은 0-based 그대로
- `sm:hidden` / `hidden sm:inline` 반응형: 모바일 숫자만, 640px↑ 이름 포함
- `flex-wrap` + `flex-shrink-0`: 6개 버튼 2행 wrap

**QA 확인**: 2행 레이아웃 `1 묘사하기` ~ `6 언어화` 정상 표시.

---

### 개선 5 — 대기 중 중간 피드백 메시지

`ChatPane.tsx`에 `waitingMessage` 상태 + `useEffect` 타이머 추가:

- **15초 후**: `"AI가 열심히 생각하고 있어... 잠깐만 기다려봐! 💭"`
- **40초 후**: `"거의 다 됐어! 조금만 더 기다려봐 🎮"`
- `isLoading` false 시 타이머 취소 + 메시지 초기화

---

### 개선 6 — WS 재연결 상태 배너

`useChat.ts`에 `wsStatus: "connected" | "reconnecting" | "disconnected"` 상태 추가:

- `ws.onopen` → `"connected"` (신규 추가)
- `ws.onmessage` → `"connected"` (retryCount 초기화와 함께)
- `ws.onclose` + 재시도 → `"reconnecting"`
- `ws.onclose` + MAX_RETRIES 초과 → `"disconnected"`

`ChatPane.tsx` 상단에 조건부 배너:
- 황색(`bg-yellow-900/80`): `"연결 중... 잠깐만 기다려봐 🔄"`
- 적색(`bg-red-900/80`): `"서버 연결이 끊겼어. 새로고침 해봐! ⚠️"`

**QA 확인**: WS 강제 종료 시 황색 배너 즉시 등장, 재연결 완료 시 사라짐.

---

## QA 중 발견·수정한 추가 버그 (3건)

### 버그 A — 블록 버튼 5·6 잘림
- **원인**: `flex` 컨테이너 오버플로 + `whitespace-nowrap` 버튼
- **수정**: `flex-wrap` + `flex-shrink-0`

### 버그 B — 힌트 텍스트 말풍선 중복 표시
- **원인**: AI 응답 텍스트에 `💡` 줄이 포함되어 말풍선 + 힌트 버튼에 이중 노출
- **수정**: `msg.text.replace(/\n*💡[^\n]*$/m, "")` — 메시지 렌더 시 마지막 `💡` 줄 제거

### 버그 C — 세션 전환 시 이전 힌트 잔류
- **원인**: `useChat.ts` 세션 전환 effect에 `setHint("")` 누락
- **수정**: 세션 전환 `useEffect` 에 `setHint("")` 추가

---

## 최종 변경 파일

```
src/backend/
  claude_runner.py   — _friendly_error 헬퍼, 에러 4곳, game html 추가, HTML 크기 로그
  main.py            — game_html 직렬화, WS 에러 2곳 교체

src/frontend/
  hooks/useChat.ts          — gameHtml·wsStatus·onopen, setHint 초기화
  components/ChatPane.tsx   — 블록 UI·flex-wrap·대기 피드백·재연결 배너·힌트 중복 제거
  components/GamePreview.tsx — srcDoc 전환
  app/page.tsx              — gameHtml 상태 전파
```

---

## QA 스크린샷 목록

| 파일 | 내용 |
|---|---|
| `qa-01-main-page.png` | 로그인 후 메인 화면 (블록 버튼 스킬명 표시) |
| `qa-03-game-loaded.png` | 토끼 게임 생성 완료 (srcdoc 렌더링) |
| `qa-06-block-wrap-fix.png` | 블록 버튼 2행 wrap 수정 후 |
| `qa-08-hint-dedup.png` | 힌트 중복 제거 후 (말풍선 깔끔) |
| `qa-09-session-switch.png` | 세션 전환 → URL 폴백 확인 |
| `qa-12-reconnect-banner.png` | WS 재연결 황색 배너 |

---

## 남은 사항 (이번 세션 미처리)

- **대기 피드백 E2E 검증**: 실제 15초 이상 소요 응답이 필요해 자동화 미완
- **에러 메시지 E2E 검증**: `CLAUDE_TIMEOUT=1` 환경에서 수동 재현 권장
