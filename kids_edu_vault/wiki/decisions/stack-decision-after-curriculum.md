---
type: decision
title: "스택 최종 결정을 커리큘럼 확정(4/21) 이후로 미룸"
created: 2026-04-12
updated: 2026-04-12
status: accepted
priority: 2
tags:
  - decision
  - pilot/execution-env
  - pilot/5-5
related:
  - "[[track-a-primary-b-backup]]"
  - "[[pivot-to-chat-preview-wrapper]]"
  - "[[bongho-tae]]"
  - "[[jinyong-shin]]"
  - "[[2026-04-12-jay-workshop-structure]]"
deciders:
  - "[[jay-lee]]"
  - "[[jinyong-shin]]"
---

# 스택 최종 결정을 커리큘럼 확정(4/21) 이후로 미룸

## 결정

Track A 실행환경의 **세부 기술 스택 최종 결정을 2026-04-21 커리큘럼 리뷰 완료 후로 연기**한다. JY는 4/26 리허설 가능 상태를 목표로 구현하되, 스택 선택의 최종 확정은 커리큘럼이 나온 뒤 진행한다.

## 근거

- "커리큘럼이 도구를 결정한다. 도구가 커리큘럼을 결정하지 않는다." (Jay, 2026-04-12)
- BH 커리큘럼([[bongho-tae]] 마감 4/19)에 따라 필요한 인터랙션 패턴·블록 구조가 달라질 수 있음.
- [[pivot-to-chat-preview-wrapper]]는 방향(chat+preview)을 확정했지만, 세부 프레임워크·모델 선택(Claude vs Gemini 등)은 커리큘럼 의존적.

## 게이트

| 날짜 | 이벤트 | 산출물 |
|---|---|---|
| 4/19 | BH 커리큘럼 초안 완성 | 블록별 활동·완성 기준 |
| 4/21 | Jay + JY 커리큘럼 리뷰 | **스택 최종 결정** |
| 4/26 | JY 리허설 가능 상태 납품 | Track A 작동 래퍼 |

## 현재 잠정 방향 (확정 전)

- Frontend: Next.js App Router
- Sandbox: iframe + srcdoc + `sandbox="allow-scripts"` ([[iframe-sandbox-over-webcontainers]])
- Agent: Claude Agent SDK 또는 Gemini 2.5 Flash 재검토 필요
- Auth: [[parent-gated-signup-first]] 방침 준수 (Clerk 또는 Supabase Auth)

## 관련

- [[bongho-tae]] — 커리큘럼 설계 담당 (4/19 마감).
- [[pilot-rehearsal-late-april]] — 스택 확정 후 리허설 게이트.
