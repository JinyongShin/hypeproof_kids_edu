---
type: meta
title: "Hot Cache"
updated: 2026-04-12
tags:
  - meta/hot
---

# Recent Context

## Last Updated
2026-04-12. Pivot 리서치·결정 완료: code-server+cline → chat+preview 래퍼.

## Key Recent Facts
- 파일럿: **2026-05-05 13:30–15:30 · 국립암센터 일산로323 강당 · 40명, 8–12세** ([[environ-kukrip-amsenter]]). 23일 남음.
- 비용 목표: $0.15 미만 / 세션. Q2 OKR: KR1 수강생 5명+ 실습 / KR2 치명 장애 0 / KR3 운영자 가이드 ([[okr-q2-jy]]).
- 기존 스택 ([[pilot-env-design]]): `hypeproof-ai.xyz` + [[caddy]] + [[oauth2-proxy]] + [[code-server]] + [[cline]] + [[gemini-2-5-flash]].
- 운영 모드: [[fast-implementation-mode]] (피로도·타이핑 제약).

## 2026-04-12 Pivot: Chat+Preview 래퍼로 전환 (proposed)

### Why
- 아이가 AI와 대화해서 게임 만드는 데 **IDE UI는 노이즈**. 실제 필요 표면은 "채팅 + 실행되는 게임" 두 pane ([[single-html-runtime]], [[no-debug-philosophy]]).
- 유료화·PIPA·B2B 계약 경로가 VSCode 포크로는 열리지 않음.
- 시장 화이트스페이스: "chat-native, 코드-invisible, kid-first" — Scratch 4.0 AI는 2027+, **12–18개월 기회 창** ([[intel-competitive-landscape-2026]]).

### Decisions (3 proposed, 2026-04-12)
- [[pivot-to-chat-preview-wrapper]] — 기존 [[pilot-env-design]] 부분 supersede.
- [[iframe-sandbox-over-webcontainers]] — iframe+srcdoc만 사용. WebContainers 상용 라이선스 트랩 회피.
- [[parent-gated-signup-first]] — PIPA 만 14세 미만 대응. 부모 이메일 가입 우선, Google OAuth는 14+/교사 한정.

### Recommended Stack (3주 MVP)
- **Frontend**: Next.js App Router
- **Agent**: Claude Agent SDK (`Edit`/`MultiEdit`) — 단 [[gemini-2-5-flash]] 비용 목표 재검토 필요
- **Sandbox**: iframe + `srcdoc` + `sandbox="allow-scripts"` (⚠️ `allow-same-origin` 금지)
- **Auth**: Clerk (또는 Supabase Auth)
- **Billing (추후)**: Stripe (글로벌) + 포트원 (국내 B2B 세금계산서)
- **Monetization**: 아이 무료 + B2B2C 스폰서 결제 (병원 CSR / 소아암재단 / 지자체)

### Research (3 intel)
- [[intel-wrapper-architecture]] · [[intel-auth-billing-compliance]] · [[intel-competitive-landscape-2026]]

## 실행 방향 (JY 내부 결정, 2026-04-12, Jay 확인 전)
- **옵션 C → A 단계 진행**. 초기 C(운영자 하드코드)로 래퍼 착수, **파일럿 당일 A(새 래퍼 정식)로 전환**.
- Jay 피드백에 따라 변경 가능 (특히 B로 철수 가능성 열어둠).

## Subagent 팀 (2026-04-12 빌드 완료, 총 6개)
- **Wiki**: `wiki-ingest`, `wiki-lint`.
- **Dev (신규)**: `architect` → `implementer` → `tester` → `reviewer` — 전원 sonnet, wiki-query 스킬 포함.
- 위임 규칙: `.claude/CLAUDE.md`. 팀 개요·단계별 규칙·표준 흐름: 루트 `CLAUDE.md` "팀 & 워크플로우" 섹션.
- 보류: `debugger`, `docs-writer` (pain 축적 시 후행 추가).
- Smoke test 미실시 — C 진입 시점에 `@architect`부터 가동.

## Active Threads
- **Jay 확인 대기**:
  - 피벗 방향 승인 (C→A 단계 진행) → 브리핑 문서 `2026-04-12-pivot-briefing-jay.md` (프로젝트 루트).
  - 어린이 Google 계정 보유 여부 — 이젠 부모 이메일 플로우로 축소 가능.
- **JY 결정 필요 (피벗 후속)**:
  - 모델: Claude vs Gemini (Agent SDK 전환 = 비용 A/B 필요).
  - MVP 스코프: OAuth·결제 A 단계 포함 여부.
  - C→A 전환 gate: [[pilot-rehearsal-late-april]]에서 A 준비 상태 검증.
- **JY 이번 주 (유지)**: [[pilot-gemini-api-key]], [[pilot-server-domain]].
- **의료진 합의 필요** (유지): ANC 컷오프, 사전 문진, 강당 HVAC. 4/20 전 확정.
- **[[combat-vs-cooperative-framing]]** 후속: 대체 서사·시스템 프롬프트·고지문.
- **성과 지표 재조정**: 완주율·자기효능감·부모 만족도·치명 장애 0.
- **[[pilot-curriculum-adapted]]** 검증: [[pilot-rehearsal-late-april]].
- **Runbook**: [[pilot-day-operation]] stub 생성(2026-04-12, planned) — 리허설 후 확정. 미작성: `deploy-code-server`, `rehearsal-checklist`, `operator-script-per-block`.
- **튜터 사전 오리엔테이션 커리큘럼**.
- **External stakeholders** 페이지 미생성.
