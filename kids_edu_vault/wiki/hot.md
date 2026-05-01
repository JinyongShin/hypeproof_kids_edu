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

## 현재 상태: LangGraph 백엔드 구현 완료 — 파일럿 D-4 (2026-05-05)

### ✅ 완료된 작업 (2026-05-01)

**LangGraph + Gemini 백엔드 전체 구현** (`feature/langgraph-gemini` 브랜치)
- Claude CLI subprocess 제거 → LangGraph StateGraph 전환 완료
- 8개 노드 구현: classify_intent, generate_card, save_card, generate_spec, edit_spec, validate_and_build, save_game, chitchat
- 게임 편집 루프: edit_spec_node가 current_spec deep-merge 패치 → "더 빠르게 해줘" 정상 동작
- AsyncSqliteSaver 체크포인터로 대화 맥락 영속화
- 64개 테스트 전체 통과 (MOCK_LLM=1 사용)
- Docker Compose 배포: backend/frontend/langfuse/langfuse-db 4개 서비스
- Langfuse 관측성: 트레이스 정상 수집 확인 (langfuse/langfuse:2.95.11 버전 핀 고정)

### 현재 스택
- **백엔드**: FastAPI + LangGraph + Gemini 2.5 Flash (langchain-google-genai)
- **관측성**: Langfuse v2 self-hosted (localhost:3002)
- **배포**: Docker Compose (로컬) / 추후 fly.io VPS

### 다음 단계
- MOCK_LLM=0으로 실제 Gemini 연동 E2E 테스트
- fly.io VPS 배포
- 파일럿 D-day 준비

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
