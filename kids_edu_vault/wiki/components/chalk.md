---
type: component
title: "Chalk"
status: proposal
tags:
  - component
  - product
  - internal
created: 2026-08-30
updated: 2026-09-03
related:
  - "[[hypeproof-mission]]"
  - "[[hypeproof-studio]]"
  - "[[sediment]]"
  - "[[mission-product-alignment]]"
---

# Chalk

> **강사용 제품.** Studio가 수업을 돌린다면 Chalk는 **수업을 만든다.**
> 상태: **제안 단계(proposal-stage)** — 정본이 "명시적 미결을 달아 그렇게 보여야 한다"고 규정한다.

## 제품 3종 안에서의 자리

```
Chalk  ──만든다──▶  수업 설계 파일  ──돌린다──▶  Studio
                          │
                          └──증거를 쌓는다──▶  Sediment
```

**셋을 잇는 공유 인터페이스가 「수업 설계 파일」이다.** 이 스키마를 누가 소유하고 어디까지 잠그는지가 제품 세 개의 경계를 결정한다 → [[mission-product-alignment]]

## 2026-08-31 회의에서 정정·확장된 것

> [!key-insight] 저장소가 아니라 생성기다
> [[jinyong-shin]]: "강의 계획만 들어 있는 게 초크가 아니라, **우리가 전달하고자 하는 바와 누구를 대상으로 어떤 강의를 할 것인가를 입력했을 때 그 강의안을 만들어 주는 프레임워크**가 초크다."
> 초크 안에 든 것은 강의가 아니라 **강의를 만들 재료와 우리의 방향성**이다. 강사가 바뀌어도 일관된 교육 품질이 나오는 근거이며, **강의 2인 체제**(메인 1 + 보조 1) 최적화의 전제이기도 하다.

**게이트웨이 역할이 추가됐다.** 누군가 Chalk로 강의를 만들었을 때, 그것이 **HypeProof 기준에 부합하는지 검증하고 외부 교육 활용을 열어 주는 관문**이 되어야 한다 ([[jinyong-shin]]).
"초크로 만들었으면 HypeProof의 교육관에 맞는 교육일 것이다"를 보증하는 제품. 회의에서 논의된 **표준화된 인증 체계**의 기술적 근거다.

[[jesse-kim]]: **"저의 크립토나이트는 스튜디오가 아니라 초크가 돼야 한다. 결국 우리의 킥은 초크가 돼야 강남이든 어디든 시간당 20만 원을 받을 수 있다."**
→ 현재 단가 10만 원 / 목표 20만 원의 간극을 메우는 자리에 Chalk를 놓은 것이다 ([[2026-08-31-weekly-on-hypeproof]]).

> [!contradiction] Philosophy 문서의 "Curriculum"과 같지 않다 (2026-09-06)
> [[hypeproof-philosophy]]는 제품 3종을 **Curriculum · Studio · Community**로 쓰고 Chalk를 언급하지 않는다.
> Chalk는 커리큘럼을 **만드는 생성기이자 게이트웨이**이지 커리큘럼 자체가 아니므로 1:1 대응이 아니다. 명칭 통일 판정 필요 → [[hypeproof-lab-philosophy-source]] 충돌 3.
> 다만 그 문서의 Curriculum 설계 단위 `Asset → Behavioral Indicator → Exercise → Feedback → Reflection → Assessment`는 **Chalk가 생성해야 할 산출물 규격의 후보**다.

## 무엇을 만드나

`주제 → 수업 설계 파일 → 보드·설명 카드 → 참가자 프롬프트 → 진행·대비 멘트 → 강사 스크립트 → Studio 코호트 설정`

## 상업 표면

| 표면 | 라이선스 단위 |
|---|---|
| 강사 워크스페이스 | 강사 / 월 |
| 클래스 키트 | 클래스 / 코호트 |
| 기관 라이선스 | 조직 / 기간 |
| **파트너 저작 라이선스** | 파트너 / 기간 — 자격 있는 전문가가 Chalk 호환 수업 IP를 만들 수 있게 |
| 인증 강사 키트 | 지정 강사 / 기간 |

> **파트너 저작 라이선스가 이미 사업모델에 있다.** 그래서 강사 저작 개방은 방향의 문제가 아니라 **순서의 문제**다.

## 미결 (정본이 명시한 것)

- 저장소 위치
- 제품 오너
- 성인 대상 첫 시험 단계
- **스키마 소유** ← 가장 시급
- 계약 범위

## 왜 중요한가

정본은 **서사의 중심을 Chalk, 실행의 순서를 Studio 먼저**로 정했다(결정 2026-08-10). 그리고 사업 병목을 이렇게 못 박는다:

> 우리는 아직 교육자에게 팔아본 적이 없다 — **제3자 강사가 운영한 회차 0건.**
> 공급 모델 전체가 이 미검증 위에 서 있고, 그래서 **Chalk 성숙도가 서사의 병목인 동시에 사업 모델의 병목**이다.

## 관련

- [[hypeproof-mission]] · [[hypeproof-studio]] · [[sediment]] · [[mission-product-alignment]]
- [[2026-08-31-weekly-on-hypeproof]] · [[four-learner-experiences]]
