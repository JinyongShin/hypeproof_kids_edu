---
type: decision
status: superseded
superseded_by: "[[one-track-multi-skin]]"
priority: 1
date: 2026-05-05
owner: "봉호 태"
context: "파일럿(2026-05-05) 이후 HypeProof 교육 상품 구조 확정"
tags:
  - decision
  - strategy
  - curriculum
created: 2026-05-05
updated: 2026-05-05
---

# 3-트랙 교육 구조 채택

## 결정

HypeProof 교육 상품을 3개 트랙으로 운영한다.

| 트랙 | 대상 | 설명 |
|---|---|---|
| Track A | 아동 | 기존 파일럿 방향 — AI로 창작하는 어린이 워크샵 |
| Track B | 성인 | 성인 대상 AI 활용/리터러시 교육 |
| Track C | 혼합 | 아동+성인 동시 참여 (예: 부모+자녀, 가족 워크샵) |

## 근거

- 아동 단독 워크샵(Track A)으로 시작했으나 성인 수요 및 혼합 포맷 가능성 확인
- 트랙별로 커리큘럼·scaffold 텍스트·AI 페르소나가 달라짐
- 단일 트랙 운영보다 3-트랙 구조가 상품 확장성과 시장 커버리지 측면에서 유리

## 대안 및 기각 이유

| 대안 | 기각 이유 |
|---|---|
| 아동 단독 운영 유지 | 성인·혼합 수요 대응 불가 |
| 트랙 무분류 | 커리큘럼·scaffold·페르소나 설계 기준이 섞여 혼선 발생 |

## 영향 범위

- **커리큘럼**: 트랙별 별도 설계 필요
- **scaffold 텍스트** (`scaffoldData.ts`): 트랙별 별도 데이터셋
- **AI 페르소나** (`TUTOR.md`): 트랙별 별도 페르소나 파일
- **Production Loop**: 각 트랙이 독립 루프를 순환
- **기술 구현**: 트랙 선택 UI 또는 별도 엔드포인트 필요 여부 검토 필요

## 후속 작업

- [ ] Track A (아동): 파일럿 관찰 기반 v2 설계 시작
- [ ] Track B (성인): 교육 목표·대상 페르소나 정의
- [ ] Track C (혼합): 포맷 및 운영 방식 정의
- [ ] 트랙별 scaffold·페르소나 파일 구조 설계

## 관련

- [[production-loop-adoption]]
- [[production-loop]]
- [[track-a-primary-b-backup]]
