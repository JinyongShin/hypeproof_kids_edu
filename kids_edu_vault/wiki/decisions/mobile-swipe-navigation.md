---
type: decision
title: "모바일 스와이프 네비게이션"
created: 2026-04-13
updated: 2026-04-13
decision_date: 2026-04-13
status: active
tags:
  - frontend
  - mobile
  - ux
related:
  - "[[nextjs-fastapi-wrapper-architecture]]"
  - "[[pivot-to-chat-preview-wrapper]]"
  - "[[kids-edu-backend]]"
---

# 모바일 스와이프 네비게이션

## 결정

모바일(< 768px)에서 채팅 pane과 게임 pane을 수평 스와이프로 전환한다.  
데스크탑(≥ 768px)의 기존 2-pane 레이아웃은 그대로 유지한다.

## 배경

기존 레이아웃은 `flex w-2/5` + `flex-1` 고정 분할로, 모바일에서 채팅창이 40%로 축소되어 입력하기 어렵다. 파일럿 현장(병원 병동)에서 태블릿·스마트폰 접속 가능성이 있어 개선이 필요하다.

## 구현 방식: 200% 슬라이딩 트랙

```
모바일(overflow-hidden 컨테이너):
┌────────────────────────────────────────┐  ← 화면(100vw)
│  [  Chat Pane (w=50%)  ][  Game (50%)  ]  ← 트랙(w=200%)
└────────────────────────────────────────┘
  translateX(0)   → 채팅 표시
  translateX(-50%) → 게임 표시
```

- 외부 라이브러리 없음 — 순수 React + Tailwind CSS
- 컴포넌트 이중 마운트 없음 → WebSocket 단일 연결 유지
- CSS transition으로 300ms 슬라이드 애니메이션

## 변경된 파일

| 파일 | 변경 내용 |
|------|----------|
| `src/frontend/hooks/useSwipe.ts` | 신규. touchstart/end delta로 좌/우 스와이프 감지 |
| `src/frontend/app/layout.tsx` | `viewport` 메타 추가 (`width=device-width, initialScale=1`) |
| `src/frontend/app/page.tsx` | `activePane` state + useSwipe 연결 + 슬라이딩 레이아웃 |

### useSwipe 훅 인터페이스

```ts
useSwipe({
  onSwipeLeft: () => setActivePane('game'),   // 채팅 → 게임
  onSwipeRight: () => setActivePane('chat'),  // 게임 → 채팅
  threshold: 50,  // px (기본값)
})
```

### Tailwind 클래스 동작

| 상황 | 트랙 너비 | 각 pane 너비 | transform |
|------|----------|-------------|-----------|
| 모바일 + chat | 200vw | 100vw each | 0 |
| 모바일 + game | 200vw | 100vw each | -100vw |
| 데스크탑 | 100% (`md:w-full`) | 40% + flex-1 | 0 (`md:translate-x-0`) |

## 모바일 UX 상세

- 스와이프 방향: 채팅에서 **왼쪽** → 게임 / 게임에서 **오른쪽** → 채팅
- 하단 도트 인디케이터 (`md:hidden`): 현재 pane을 인디고 색으로 표시
- viewport 메타 미설정 시 터치 좌표 비정상 → `layout.tsx`에 Viewport export 추가 필수

## 변경하지 않은 파일

- `ChatPane.tsx`, `GamePreview.tsx`, `hooks/useChat.ts` — 변경 없음
