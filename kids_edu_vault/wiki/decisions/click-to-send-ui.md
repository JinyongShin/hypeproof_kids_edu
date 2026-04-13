---
type: decision
title: "클릭 즉시 전송 UI"
created: 2026-04-13
updated: 2026-04-13
decision_date: 2026-04-13
status: active
tags:
  - frontend
  - ux
  - chat
related:
  - "[[mobile-swipe-navigation]]"
  - "[[kids-edu-backend]]"
---

# 클릭 즉시 전송 UI

## 결정

`PromptScaffold` 카드와 `💡` 힌트를 클릭하면 textarea 입력 없이 바로 채팅이 전송된다.

## 배경

기존 동작:
- PromptScaffold 카드 클릭 → textarea에 텍스트 삽입만 됨. 사용자가 Enter/버튼을 따로 눌러야 전송.
- 힌트(`💡 다음엔 "..."라고 해봐!`) → 클릭 불가능한 `<p>` 텍스트.

아이들(8-12세, 소아암 병동)에게 두 번 클릭하는 마찰은 불필요하다.

## 구현

변경 파일: `src/frontend/components/ChatPane.tsx` 1개.

### 1. `handleQuickSend` 추가

```typescript
const handleQuickSend = (text: string) => {
  if (!text.trim() || isLoading) return;
  send(text.trim());
};
```

`setInput` 없이 바로 `send()` 호출 → textarea 깜빡임 없음.

### 2. PromptScaffold onSelect 교체

```diff
- <PromptScaffold currentBlock={currentBlock} onSelect={setInput} />
+ <PromptScaffold currentBlock={currentBlock} onSelect={handleQuickSend} />
```

### 3. 힌트 버튼화

```tsx
{hint && (() => {
  const match = hint.match(/"([^"]+)"/);
  const sendText = match ? match[1] : hint.replace(/^💡\s*/, "").trim();
  return (
    <button
      onClick={() => handleQuickSend(sendText)}
      disabled={isLoading}
      className="mx-auto block rounded-full border border-indigo-700 px-3 py-1 text-center text-xs text-indigo-400 hover:bg-indigo-950 disabled:opacity-50"
    >
      {hint}
    </button>
  );
})()}
```

- 따옴표(`"..."`) 안 텍스트 추출 후 전송.
- 따옴표 없으면 `💡` 제거 후 전체 텍스트 fallback.
- `isLoading` 중 `disabled` 처리.
