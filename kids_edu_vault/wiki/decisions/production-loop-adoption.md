---
type: decision
status: active
priority: 2
date: 2026-05-05
owner: "봉호 태"
context: "파일럿(2026-05-05) 완료 후 v2 제작 프로세스 정립"
tags:
  - decision
  - process
  - curriculum
created: 2026-05-05
updated: 2026-05-05
---

# Production Loop v1 채택

## 결정

커리큘럼 제작 프로세스를 3단계 루프(인풋→설계 / 설계→기술피드백 / 리허설→반영)로 표준화한다.
파일럿 이후 v2부터 이 루프를 따른다.

## 근거

- 지금까지 커리큘럼 방향이 게임/그림책/타이틀카드 3개가 병존해 구현과 불일치 반복
- 결과물 포맷을 먼저 결정하지 않은 채 설계 시작 → 중간에 방향 전환 비용 발생
- 기술팀(지웅)이 구현할 scaffold 카드 텍스트를 봉호님이 직접 작성하는 흐름이 필요
- 관찰 데이터(아동 산출물·타이밍)를 vault에 적재해 다음 버전에 환류하는 구조 부재

## 대안 및 기각 이유

| 대안 | 기각 이유 |
|---|---|
| 기존 방식 유지 (자유 형식) | 커리큘럼↔구현 불일치 반복, 방향 혼선 |
| 기술팀 주도 설계 | 교육 의도가 구현에 후반 반영되는 구조 → 품질 하락 |

## 영향 범위

- 봉호님: Stage 1 교육 목표 정의 + Stage 2 scaffold 카드 텍스트 직접 작성
- 지웅 팀: Stage 2에서 기술 실현 가능성 체크, Stage 3 이전까지 구현 완료
- AI 어시스턴트: 각 Stage 문서화, vault ingest, 다음 Stage 전환 알림

## 후속 작업

- [ ] Stage 1: 파일럿 관찰 노트 vault ingest
- [ ] Stage 1: v2 교육 목표 + 블록 구조 정의
- [ ] Stage 2: scaffold 카드 텍스트 템플릿 작성

## 관련

- [[production-loop]] — 상세 스펙
- [[stack-decision-after-curriculum]]
- [[game-content-guideline-pending]]
