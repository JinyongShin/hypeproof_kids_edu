---
type: meta
title: "Hot Cache"
created: 2026-04-12
updated: 2026-05-01
tags:
  - meta/cache
---

# Hot Cache — 2026-05-01

최근 컨텍스트 스냅샷. 세션 시작 시 가장 먼저 읽을 것.

---

## 현재 상태: 파일럿 D-4 — 2026-05-05 워크샵

### ✅ 오늘 완료 (2026-05-01)

**게임 버그 3종 수정** → `fix/game-bug-3종` 브랜치 커밋
- Bug 1: 게임 수정 시 HTML 소스코드 채팅 노출 → 수정 완료
- Bug 2: 게임 생성 후 캐릭터 카드 소실 → 🎴/🎮 토글 추가
- Bug 3: 게임 수정 요청 시 새 게임 생성 → spec 주입으로 수정

상세: [[game-bug-fix-2026-05-01]]

---

## 프로젝트 개요

- 목표: 소아암 병동 어린이 AI 창작 워크샵 파일럿 (2026-05-05, 국립암센터, 40명)
- 스택: FastAPI (Python/uv) + Next.js (App Router) + GLM-5 (z.ai)
- 래퍼: 채팅(WebSocket) + iframe 게임 프리뷰 + 블록별 프롬프트 스캐폴드

---

## 완료된 개발 작업 (최신순)

| 기능 | 상태 | 날짜 |
|---|---|---|
| 게임 버그 3종 수정 (소스코드 노출·카드 소실·spec 유실) | ✅ | 2026-05-01 |
| spec composition 게임 엔진 (enumeration → 부품 조합) | ✅ | 2026-04-30 |
| Playwright MCP 연동 (chromium) | ✅ | 2026-05-01 |
| UX 개선 (iframe srcDoc·에러메시지·블록버튼·대기피드백·WS배너) | ✅ | 2026-04-18 |
| SQLite 마이그레이션 + 게임 파일시스템 저장 | ✅ | |
| 세션 이름 자동 할당 + 세션 전환 버그 3종 수정 | ✅ | |

---

## 핵심 ADR

- [[stack-decision-after-curriculum]] — 커리큘럼 확정 후 스택 결정
- [[auth-session-game-persistence]] — status: implemented
- [[track-a-primary-b-backup]] — Track A 주력
- [[game-bug-fix-2026-05-01]] — 게임 버그 3종 수정 기록

### 핵심 파일 경로

- `src/backend/genai_runner.py` — `_strip_code_for_chat()`, `generate_card()`
- `src/backend/main.py` — spec 추출·주입 로직 (~490번째 줄)
- `src/frontend/components/ChatPane.tsx` — 메시지 렌더 regex
- `src/frontend/components/GamePreview.tsx` — `showGame` 토글
- `src/backend/storage.py` / `src/frontend/hooks/useChat.ts`
