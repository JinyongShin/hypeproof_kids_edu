---
type: meta
title: "Hot Cache"
created: 2026-04-12
updated: 2026-05-14
tags:
  - meta/cache
---

# Hot Cache — 2026-05-14

최근 컨텍스트 스냅샷. 세션 시작 시 가장 먼저 읽을 것.

---

## 현재 상태: SK바이오팜 파일럿 진입 + HypeProof Studio 개발 시작

### 가장 최근 작업 (2026-05-14)

**SK바이오팜 × 비트리 5/12 미팅 후속 ingest 완료**
- SK바이오팜 임직원 가족 대상 AI 게임 창작 교육 파일럿 기획 확정
- 대상: 약 15~20가족, 6~7월 토요일 Biweekly, SK바이오팜 10층 내부 카페
- 수업 단위: 4시간 × 2그룹/일

**HypeProof Studio v0.1 개발 결정 (ADR 작성 완료)**
- VS Code fork + 자체 chat panel (Track A / Track B 병렬)
- 5/28~30 dry-run이 Go/No-go 게이트
- Plan B: Cline + Proxy, Studio 8월 데뷔

---

## 주요 임박 마일스톤

| 기한 | 내용 |
|---|---|
| 2026-05-15~30 | HypeProof Studio v0.1 빌드 |
| 2026-05-28~30 | 운영진 자녀 dry-run (4시간) — **게이트** |
| 2026-05-말 | SK바이오팜 수요조사용 제안서 제출 |
| 2026-06-01 | Studio v0.1 release + 가족 안내 메일 |
| 2026-06 (2~3주) | SK바이오팜 1회차 |

---

## 핵심 페이지 (신규)

- [[2026-05-12-sk-biopharma-meeting]] — 5/12 미팅 전체 내용
- [[2026-05-14-sk-biopharma-followup]] — 제품 결정·일정·비용
- [[sk-biopharma]] · [[bitree]] · [[oh-sungeun]] — 이해관계자
- [[hypeproof-studio]] — VS Code fork 자체 IDE
- [[adr-hypeproof-studio-v01]] — Studio 개발 결정 ADR
- [[sixteen-essence]] — HypeProof 교육 IP 핵심 프레임워크
- [[sk-biopharma-pilot]] — 파일럿 마일스톤 트래킹

---

## LangGraph 백엔드 상태 (2026-05-14 기준)

- `feature/langgraph-gemini` 브랜치에서 LangGraph + Gemini 2.5 Flash 구현 완료
- 64개 테스트 통과 (MOCK_LLM=1)
- ✅ **MOCK_LLM=0 E2E 테스트 완료** (2026-05-14)
- 다음: fly.io VPS 배포

---

## 스택 요약

| 레이어 | 기술 |
|---|---|
| 백엔드 | FastAPI + LangGraph + Gemini 2.5 Flash |
| 프론트 | Next.js (App Router) |
| 관측성 | Langfuse v2 self-hosted |
| 교육 도구 | HypeProof Studio v0.1 (예정) / Cline (Plan B) |

---

## 핵심 파일 경로

- `src/backend/genai_runner.py` — `_strip_code_for_chat()`, `generate_card()`
- `src/backend/main.py` — spec 추출·주입 로직 (~490번째 줄)
- `src/frontend/components/ChatPane.tsx`
- `src/frontend/components/GamePreview.tsx`
