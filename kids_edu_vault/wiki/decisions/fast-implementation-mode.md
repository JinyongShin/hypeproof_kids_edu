---
type: decision
status: active
priority: 2
date: 2026-04-10
owner: "[[jinyong-shin]]"
context: "파일럿 당일 AI 튜터 운영 모드"
tags:
  - decision
  - pilot
  - ai-tutor
created: 2026-04-12
updated: 2026-04-12
---

# AI 튜터: 빠른 구현 모드

## 결정
- 소아병동 파일럿 당일 AI 튜터는 **빠른 구현 모드**로 운영. 아이가 원하는 걸 말하면 AI가 바로 만들어줌.

## 근거
- 소아암 병동 특성: 피로도 제약, 집중 지속 시간 짧음 ([[environ-kukrip-amsenter]]).
- 기다리는 시간 최소화 → 성취감 극대화 필요.
- 8–12세 타이핑 불가 가능성 고려 ([[2026-04-11-call-note]]).

## 대안 및 기각 이유
- 단계별 교육 모드: 아이가 스스로 이해하며 진행 — 피로도·시간 제약에서 불리.

## 영향 범위
- Cline + Gemini 2.5 Flash 프롬프트 설정.
- 게임 스타터 템플릿: 즉시 실행 가능한 상태로 탑재 ([[sans-kids-school-2025]]).

## 관련
- [[pilot-env-design]] · [[gemini-2-5-flash]]
