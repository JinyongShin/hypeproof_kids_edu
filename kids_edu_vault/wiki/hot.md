---
type: meta
title: "Hot Cache"
updated: 2026-04-12
tags:
  - meta/hot
---

# Recent Context

## Last Updated
2026-04-12 (Session 8). MVP 개발 계획 확정: FastAPI + CLI subprocess + AI 프롬프팅 리터러시 레이어.

## Key Recent Facts
- 파일럿: **2026-05-05 13:30–15:30 · 국립암센터 일산로323 강당 · 40명, 8–12세** ([[environ-kukrip-amsenter]]). 23일 남음.
- 비용 목표: $0.15 미만 / 세션. Q2 OKR: KR1 수강생 5명+ 실습 / KR2 치명 장애 0 / KR3 운영자 가이드 ([[okr-q2-jy]]).
- 운영 모드: [[fast-implementation-mode]] (피로도·타이핑 제약).
- Track A(웹 래퍼, 주력) / Track B(텔레그램, 백업) — 커리큘럼 단일 ([[track-a-primary-b-backup]]).

## 현재 스택 (2026-04-12 확정)

**교육 목표 2개 병행:**
1. AI와 함께 게임 만들기 (창작 경험)
2. AI에게 잘 시키는 법 체득 ([[ai-prompting-literacy-input]])

**아키텍처** ([[nextjs-fastapi-wrapper-architecture]]):
```
[ Next.js 프론트 ] ←WebSocket→ [ FastAPI 백엔드 ]
  채팅 + iframe preview              ↓
  프롬프트 스캐폴딩 카드      claude -p --stream-json
                               --allowedTools Read,Write,Glob
                               --resume [child_session_id]
```

- sanshome_bot/claude_runner.py 재활용 (빠른 구현)
- iframe srcdoc sandbox="allow-scripts" ([[iframe-sandbox-over-webcontainers]])
- Bash 툴 제거 (아동 보안)

## AI 프롬프팅 스킬 — 블록별 매핑

| 블록 | 스킬 |
|---|---|
| Block 0 | 묘사하기 |
| Block 1 | 구체화 |
| Block 2 | 추가 요청 |
| Block 3 | 수정 요청 |
| Block 4 | 자유 조합 |
| Block 5 | 언어화 (어떻게 말했는지 설명) |

UI: 블록별 프롬프트 스캐폴딩 카드 + "잘 됐던 말들" 히스토리 패널.
Claude 응답 끝: "💡 다음엔 ~라고 해봐!" 1줄.

## 마일스톤 (JY 담당)

| 날짜 | 마감 |
|---|---|
| **4/19** | BH에게 [[ai-prompting-literacy-input]] 전달 |
| **4/21** | 커리큘럼 리뷰 → 스택 최종 확정 ([[stack-decision-after-curriculum]]) |
| **4/26** | 리허설 가능 상태 (FastAPI + Next.js 연동 완료) |
| **4/30** | 드라이런 |
| **5/5** | 파일럿 당일 |

## Active Threads

- **Jay 확인 대기**: 피벗 방향 승인 (`2026-04-12-pivot-briefing-jay.md`).
- **BH 전달 필요 (4/18까지)**: [[ai-prompting-literacy-input]] spec.
- **JY 구현 Phase 1 (~ 4/21)**: `wrapper/` Next.js 스캐폴드 + `backend/` FastAPI 초기화.
- **JY 구현 Phase 2 (4/21~4/26)**: Claude 스트리밍 → iframe 게임 실행 → 세션 → 스캐폴딩 UI.
- **의료진 합의 필요**: ANC 컷오프, 사전 문진, 강당 HVAC. 4/20 전 확정.
- **랩탑/태블릿 40대 확보**: 4/26까지 ([[pilot-5-5-milestones]]).

## Subagent 팀 (2026-04-12 빌드 완료, 총 6개)
- **Wiki**: `wiki-ingest`, `wiki-lint`.
- **Dev**: `architect` → `implementer` → `tester` → `reviewer` — 전원 sonnet.
- 위임 규칙: `.claude/CLAUDE.md`. 팀 개요: 루트 `CLAUDE.md`.
