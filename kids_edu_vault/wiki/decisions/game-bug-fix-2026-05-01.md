---
type: decision
status: resolved
title: "게임 버그 3종 수정 (2026-05-01)"
created: 2026-05-01
tags:
  - bug-fix
  - game-engine
  - chat
  - spec
updated: 2026-05-01
---

# 게임 버그 3종 수정

**날짜**: 2026-05-01  
**브랜치**: `fix/game-bug-3종`  
**Playwright QA**: 통과

---

## Bug 1: HTML 소스코드 채팅 노출

### 원인
GLM-5가 게임 HTML을 응답할 때 `full_text`(HTML 소스 포함)를 그대로 `StreamEvent(type="text")`로 전송.  
`ChatPane.tsx`는 JSON 블록만 제거, bare HTML은 통과.

### 수정
- `src/backend/genai_runner.py` — `_strip_code_for_chat()` 헬퍼 추가.  
  코드 블록(` ``` `) 및 bare `<!DOCTYPE…</html>` 제거 후 yield.
- `src/frontend/components/ChatPane.tsx` — 메시지 렌더 regex:  
  `/```json[\s\S]*?```/gi` → `/```[\s\S]*?```/gi` (모든 코드블록 제거)

---

## Bug 2: 게임 생성 후 캐릭터 카드 소실

### 원인
`GamePreview.tsx`에서 `gameHtml`이 있으면 카드 뷰 전체를 교체해 게임 iframe만 표시.  
세션 전환 전까지 카드 복귀 수단 없음.

### 수정
`src/frontend/components/GamePreview.tsx`에 `showGame: boolean` 상태 추가.
- 새 게임 도착 → `setShowGame(true)` (자동 게임 뷰)
- 세션 전환 → 리셋
- 게임 iframe 하단에 "🎴 카드 보기" 버튼 → `setShowGame(false)`
- 합성/단일 카드 뷰 상단에 "🎮 게임 보기" 버튼 → `setShowGame(true)` (gameHtml 있을 때만)

---

## Bug 3: 게임 수정 시 완전히 새 게임 생성

### 원인
`main.py` spec_prompt에 현재 게임 spec이 없어 LLM이 매번 fresh spec 생성.  
기존 HTML에 `const SPEC = {...};` 형태로 spec이 임베드되어 있으나 미활용.

### 수정 (1차 시도 → 실패)
`storage.list_games()` → 최신 게임 HTML 읽기 → regex로 `const SPEC` 추출 → spec_prompt에 주입.  
**실패 원인**: spec에 `bg_svg`(~1,205자) + `char_sprite`(~684자) SVG가 포함되어 GLM-5 프롬프트 과부하 → `spec JSON 파싱 실패` 폴백.

### 수정 (2차 — 최종)
추출한 spec JSON을 `json.loads()` 후 SVG 필드 제거:
```python
spec_for_prompt.get("world", {}).pop("bg_svg", None)
spec_for_prompt.pop("char_sprite", None)
```
정제된 spec만 주입 → GLM-5 파싱 성공.

### 검증
- 기준 게임: `spawns[0].speed=2.0, rate=0.03`
- "더 빠르게 바꿔줘" 후: `speed=4.0, rate=0.06` (2배 증가 확인)

---

## 수정 파일 요약

| 파일 | 변경 |
|------|------|
| `src/backend/genai_runner.py` | `_strip_code_for_chat()` + text yield 2곳 교체 |
| `src/frontend/components/ChatPane.tsx` | 메시지 렌더 regex 확장 |
| `src/frontend/components/GamePreview.tsx` | `showGame` 토글 + 버튼 2개 |
| `src/backend/main.py` | spec 추출·SVG 제거·주입 블록 |
