---
type: component
title: "Kids Edu Frontend"
created: 2026-04-12
updated: 2026-04-12
status: active
tags:
  - component
  - frontend
  - nextjs
  - pilot/2026-05-05
related:
  - "[[nextjs-fastapi-wrapper-architecture]]"
  - "[[iframe-sandbox-over-webcontainers]]"
  - "[[kids-edu-backend]]"
  - "[[ai-prompting-literacy-input]]"
---

# Kids Edu Frontend

## 역할
Next.js App Router 기반 어린이 코딩 교육 인터페이스.
좌측 채팅 pane에서 AI와 대화 → 우측 iframe에서 게임 즉시 실행.

## 위치
`hypeproof_kids_edu/src/frontend/`

## 실행
```bash
npm run dev   # 개발 서버 localhost:3000
npm run build # 빌드 확인
```

## 레이아웃

```
┌──────────────────┬──────────────────────┐
│  ChatPane  (40%) │  GamePreview  (60%)  │
│  메시지 목록     │  <iframe srcdoc=...  │
│  프롬프트 카드   │  sandbox="allow-     │
│  입력창          │  scripts">           │
└──────────────────┴──────────────────────┘
```

## 컴포넌트

### GamePreview (`components/GamePreview.tsx`)
- `html: string` prop → `iframe srcdoc` 주입
- `sandbox="allow-scripts"` 만 허용 (`allow-same-origin` 금지)
- html 빈 문자열이면 대기 화면 표시

### ChatPane (`components/ChatPane.tsx`)
- `useChat` 훅으로 WebSocket 연결 + 메시지 상태 관리
- 백엔드 `/ws/chat/{child_id}` 로 연결
- `child_id`: URL 쿼리 파라미터 `?child=01`
- 스트리밍 텍스트 표시 + game 이벤트 시 GamePreview 갱신

### PromptScaffold (`components/PromptScaffold.tsx`)
- 현재 블록(0~4)에 맞는 예시 문장 카드
- 카드 클릭 → 입력창 자동 채우기
- 데이터: `lib/scaffoldData.ts`

## 훅

### useChat (`hooks/useChat.ts`)
```typescript
function useChat(childId: string): {
  messages: Message[]
  gameHtml: string
  hint: string
  isLoading: boolean
  send: (prompt: string) => void
}
```

WebSocket 이벤트 처리:
- `text` → 메시지 스트리밍 누적
- `game` → gameHtml 상태 업데이트
- `done` → isLoading=false, hint 표시
- `error` → 에러 메시지
