---
type: decision
title: "Track A 주력 / Track B 백업 구조 채택"
created: 2026-04-12
updated: 2026-04-12
status: accepted
priority: 1
tags:
  - decision
  - pilot/execution-env
  - pilot/5-5
related:
  - "[[tracks-a-b]]"
  - "[[pivot-to-chat-preview-wrapper]]"
  - "[[2026-04-12-jay-workshop-structure]]"
  - "[[environ-kukrip-amsenter]]"
deciders:
  - "[[jay-lee]]"
  - "[[jinyong-shin]]"
---

# Track A 주력 / Track B 백업 구조 채택

## 결정

2026-05-05 파일럿에서 **Track A (웹 기반 채팅+프리뷰 래퍼)를 주력**, **Track B (텔레그램 챗봇, OpenClaw 기반)를 백업**으로 운영한다. 커리큘럼은 하나로 통일하고, 실행환경만 스위칭한다.

## 근거

- 국립암센터 강당 200석 확보 + 장비 반입 제한 없음 → 웹 기반 랩탑/태블릿 세팅이 실현 가능.
- Track A는 [[pivot-to-chat-preview-wrapper]] 방향(chat-native, 코드-invisible)과 일치 — 파일럿 상품 검증에 적합.
- Track B(폰+텔레그램)는 장비 부족 시 또는 기술 장애 발생 시 즉시 전환 가능한 안전망.
- 커리큘럼 단일화: 두 환경 모두 같은 학습 흐름 지원 → 교육 일관성 유지.

## 트레이드오프

| | Track A (주력) | Track B (백업) |
|---|---|---|
| 장비 | 랩탑/태블릿 40대 필요 (미확보) | 스마트폰이면 충분 |
| UX | 채팅+프리뷰 → 상품 검증에 최적 | 텔레그램 UI → 제품 차별화 낮음 |
| 기술 복잡도 | 웹 래퍼 개발 필요 | OpenClaw 챗봇 설정만 |
| 리스크 | 장비 확보 실패 시 B로 전환 | 상품 검증 데이터 품질 저하 |

## 미확정 조건

- **랩탑/태블릿 40대 확보**: 대여·병원 보유·참가자 지참 중 조합 미결정. [[jinyong-shin]] 4/26까지 확인 필요.
- 장비 확보 실패 시 B 전환 게이트: 4/26 리허설 시점에 판단.

## 관련 결정

- [[pivot-to-chat-preview-wrapper]] — Track A의 기술 방향 정의.
- [[stack-decision-after-curriculum]] — Track A 세부 스택 확정 시점.
- [[iframe-sandbox-over-webcontainers]] — Track A 샌드박스 기술 선택.
