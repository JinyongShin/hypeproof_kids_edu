---
type: meta
title: "Hot Cache"
created: 2026-04-12
updated: 2026-04-12
tags:
  - meta/cache
---

# Hot Cache — 2026-04-12

최근 컨텍스트 스냅샷. 세션 시작 시 가장 먼저 읽을 것.

---

## 현재 상태: MVP 완료 (Unit 1-7 전체)

### 프로젝트 개요
- 목표: 소아암 병동 어린이(8-12세) AI 코딩 교육 파일럿 (2026-05-05)
- 스택: FastAPI (Python/uv) + Next.js 16 (App Router) + Claude CLI subprocess
- 래퍼: 채팅(WebSocket) + iframe 게임 프리뷰 + 블록별 프롬프트 스캐폴드

### 완료된 작업 (2026-04-12)
| Unit | 내용 | 상태 |
|---|---|---|
| 1 | Backend TDD (28개 테스트) | ✅ |
| 2 | Backend 마무리 (.env.example, uvicorn 기동) | ✅ |
| 3 | Frontend Next.js 초기화 | ✅ |
| 4 | 2-pane 레이아웃 + GamePreview (iframe sandbox) | ✅ |
| 5 | ChatPane (WebSocket 스트리밍) | ✅ |
| 6 | PromptScaffold (블록별 예시 문장 카드) | ✅ |
| 7 | 통합 확인 (MOCK_CLAUDE, 세션 독립, 5탭 동시) | ✅ |

### 아키텍처 요약

```
아이 브라우저
  └─ Next.js (localhost:3000)
       ├─ ChatPane — WebSocket → FastAPI (localhost:8000)
       │                              └─ MOCK_CLAUDE=1: 모의 스트리밍
       │                                 MOCK_CLAUDE=0: Claude CLI subprocess
       └─ GamePreview — <iframe srcdoc sandbox="allow-scripts">
```

### 핵심 파일 경로
- `src/backend/main.py` — FastAPI WebSocket 서버
- `src/backend/claude_runner.py` — SessionStore + stream_claude
- `src/backend/tests/test_claude_runner.py` — 28개 TDD 테스트
- `src/backend/personas/TUTOR.md` — AI 튜터 페르소나
- `src/frontend/app/page.tsx` — 루트 페이지 (Suspense 래핑)
- `src/frontend/components/ChatPane.tsx` — 채팅 UI + WS 연동
- `src/frontend/components/GamePreview.tsx` — iframe 게임 프리뷰
- `src/frontend/components/PromptScaffold.tsx` — 예시 문장 카드
- `src/frontend/hooks/useChat.ts` — WS 상태 관리
- `src/frontend/lib/scaffoldData.ts` — 블록별 커리큘럼 데이터

### 검증 결과 (MOCK_CLAUDE=1)
- WS 이벤트 시퀀스: text×N → game → done ✅
- 세션 독립 (child01 vs child02 동시) ✅
- 5탭 동시 접속 ✅
- /admin/reset 엔드포인트 확인 ✅
- 28개 pytest 전체 통과 ✅
- `npm run build` 통과 ✅

### 다음 단계
- 실제 Claude 연동 (MOCK_CLAUDE=0) 테스트
- 리허설 준비 (2026-04-26)
- 파일럿 당일 운영 (2026-05-05)

### 환경 변수
```
CLAUDE_TIMEOUT=120
CLAUDE_MODEL=sonnet
MOCK_CLAUDE=0       # 1로 설정 시 실제 Claude 호출 없이 개발 가능
```

### 주요 결정 & 함정
- iframe `sandbox="allow-scripts"` only — allow-same-origin 엄격 금지
- MOCK_CLAUDE는 import 시점 평가 → monkeypatch는 setenv 아닌 setattr 사용
- uv PATH: `$HOME/.local/bin` → `~/.bashrc`에 추가 필수
- Next.js useSearchParams → 반드시 Suspense boundary 안에서 호출
- pyproject.toml `[build-system]` 제거 — FastAPI app은 distributable package 아님
