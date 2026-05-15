---
type: runbook
status: planned
audience: operator
last_verified: 2026-04-12
tags:
  - runbook
  - pilot
  - 2026-05-05
created: 2026-04-12
updated: 2026-04-12
---

# Pilot Day Operation — 2026-05-05

> **Status: planned** — [[pilot-rehearsal-late-april]] 후 실제 절차 확정.
>
> 현재 커리큘럼 설계는 [[curriculum-wizard-v1]] (게임 타이틀 카드 방식, 4/20 JY) 참조.
> 커리큘럼 방향 최종 확정 전 ([[2026-04-21-asap-action-items]])에는 본 runbook의 세션 섹션이 변경될 수 있음.

## 목적
- 2026-05-05 13:30–15:30, 국립암센터 일산로323 강당에서 40명(8–12세)을 대상으로 HypeProof 유료 파일럿을 **사고 0·완주율 최대화**로 진행하기 위한 당일 운영 절차.

## 선행 조건 (D-day 이전)
- [ ] **의료진 합의** 확보 (4/20 전) — ANC 컷오프, 사전 문진표, 강당 HVAC 사양. ([[case-pediatric-onc-infection-control]])
- [ ] [[pilot-rehearsal-late-april]] 완료 + A 준비 상태 검증 (C→A 전환 gate).
- [ ] 래퍼 MVP 가동 (실행환경: [[pivot-to-chat-preview-wrapper]]).
- [ ] [[pilot-gemini-api-key]] / [[pilot-server-domain]] / OAuth 셋업 완료 ([[pilot-oauth-setup]]).
- [ ] [[pilot-curriculum-adapted]] 블록별 운영자 스크립트 확정 ([[pilot-operator-guide]]).
- [ ] 튜터 사전 오리엔테이션 완료.
- [ ] 참석자 사전 문진 완료 + 발열 체크 프로토콜 인쇄.
- [ ] 1인 1기기 배정표, 70% 에탄올 와이프, 수술마스크 40+α 수량 준비.

## 절차

### 09:00–12:00 — 사전 점검 (setup)
1. 강당 HVAC 가동 확인 / 필요 시 HEPA 이동식 배치.
2. 입구 손소독 스테이션 + 운영자 구두 안내 스크립트 배치.
3. 기기(40+α) 배포·로그인 상태 확인, 와이프 완료.
4. 네트워크·래퍼·AI 응답 지연 smoke test (운영자 하드코드 또는 정식 계정).
5. 백업 시나리오(네트워크 장애·AI API 장애·개별 기기 장애) 동작 확인.

### 13:00–13:30 — 입장
1. 입구 발열 체크 + 문진 확인. 증상 있으면 **입장 불가**, 개별 대체안(Zoom) 안내.
2. 전원 수술마스크 착용, 손소독, 1인 1기기 배정.
3. 보호자 오리엔테이션 (10분).

### 13:30–15:30 — 세션 (블록별, 상세는 [[pilot-operator-guide]])
1. 오프닝 / AI와 대화하기 / 게임 만들기 / 공유 / 클로징.
2. 블록간 기기 와이프 (±5분 버퍼).
3. 튜터 1:N 라운드 점검, 완주 곤란 아동 에스컬레이션.

### 15:30–16:30 — 철수 + 디브리프
1. 기기 회수·와이프·충전.
2. 어린이/보호자 만족도 설문 ([[okr-q2-jy]] KR3 근거자료).
3. 운영자·튜터 핫워시 30분 (무엇이 됐나 / 무엇이 무너졌나 / 내일 뭐 바꿀까).

## 검증
- [ ] **치명 장애 0** ([[okr-q2-jy]] KR2).
- [ ] 수강생 5명+ 게임 완성 후 공유까지 완료 (KR1).
- [ ] 감염관리 프로토콜 100% 준수 (손소독·마스크·와이프·문진).
- [ ] 보호자 만족도 / 완주율 / 자기효능감 지표 수집.

## 롤백 / 장애 대응
- **AI API 장애**: 사전 준비된 오프라인 게임 템플릿으로 전환 ([[pilot-game-starter-template]]).
- **네트워크 장애**: 테더링 백업 / 오프라인 스타터로 블록 스킵.
- **개별 기기 장애**: 예비기 즉시 교체, 로그인 상태 복구.
- **아동 증상 발현**: 의료진 인계, 세션 종료 없이 개별 분리.
- **운영자 스크립트 붕괴**: 튜터가 "AI와 대화" 포맷으로 개별 대응.

## 관련
- Runbook: rehearsal-checklist (예정) (예정), deploy-code-server (예정) (예정, C 단계 한정).
- Spec: [[pilot-env-design]] · [[pilot-curriculum-adapted]].
- Intel: [[environ-kukrip-amsenter]] · [[case-pediatric-onc-infection-control]] · [[case-korean-hospital-schools]].
- Deliverable: [[pilot-operator-guide]] · [[pilot-rehearsal-late-april]] · [[okr-q2-jy]].
- Decision: [[pivot-to-chat-preview-wrapper]] · [[fast-implementation-mode]] · [[combat-vs-cooperative-framing]].

## Open Questions
- [ ] ANC 컷오프 수치 확정 (의료진).
- [ ] 강당 HVAC 공기순환 시간당 횟수 실측 (환경팀).
- [ ] C→A 전환 최종 시점: 리허설 직후 vs 당일 아침.
- [ ] 발열/증상 아동 대체안: Zoom 참여 vs 녹화본 후송 vs 개별 방문.
- [ ] 병원 측 40명 집단 집합 허가 (면역저하 환자 감안) — 사전 승인 필수.
- [ ] 동아일보 취재: 병원 홍보팀 경유 보호자 서면 동의 방법 확인.
- [ ] 기기 40대 준비 주체 확정 (병원 / 행사팀 / 개인).
- [ ] 대상 연령대 확정 (0~18세 중 타이핑 가능 연령 기준).
- [ ] 진행자 5명 vs 브리핑 권장 6~7명 인력 충원 방안.
