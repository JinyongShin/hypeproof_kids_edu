---
type: decision
title: "교육 원칙 관문을 Service 확정 핸들러에 둔다"
status: accepted
decided: 2026-09-17
owner: "[[jinyong-shin]]"
created: 2026-09-18
updated: 2026-09-18
source_ref: "_worklog/chalk-ops/OPS-LOG.md §4 (외부 경로, 전언)"
tags:
  - decision
  - chalk
  - gate
  - architecture
related:
  - "[[chalk-pedagogy-gate]]"
  - "[[chalk-studio-architecture]]"
  - "[[chalk-requirements]]"
  - "[[chalk]]"
---

# 교육 원칙 관문을 Service 확정 핸들러에 둔다

**결정일 2026-09-17 · 상태 accepted · 구현 완료(PR `#1115` 머지 2026-09-18)**

> [!note] 출처
> 결정 기록은 `_worklog/chalk-ops/OPS-LOG.md` §4에 있으며 **이 세션이 직접 확인하지 않았다**(전언).

## 결정

교육 원칙 관문을 **Service(`worker/`)의 확정(freeze) 핸들러**에 둔다. **Chalk(`chalk/`)가 아니다.**

## 근거

1. **Chalk에 두면 우회된다.** 생성기가 Service에 **직접** 요청할 수 있다. Chalk는 포워딩 표면일 뿐이고(`authoring-forward` 테스트가 *"including reads"*까지 고정한다), 표면에 건 검사는 표면을 건너뛰면 사라진다.
2. **ADR 0004가 이미 규정하고 있었다** — *"내용 검사는 authoring API"*. 새 구조를 도입한 것이 아니라 **기존 규정을 따른 것**이다.
3. **`ARC-01`과 충돌하지 않는다. 반대다.** *"Chalk는 화면·전달, Service는 권한·상태 저장·토큰 서명을 소유한다"* — 내용 검사를 Service에 두는 것이 이 경계와 정합한다.

## 딸린 결정 4건 (같은 날)

| 결정 | 근거 |
|---|---|
| **차단은 한둘만, 나머지는 경고** | 전부 차단이면 **강사가 아무것도 확정하지 못한다** |
| 응답 코드 **422** | 기존 400/403/409와 겹치지 않음 |
| **읽기 시점 재검사 없음** | **교육 원칙은 권한이 아니라 설계 속성**이다. 형제 정책 셋(feature·model·help-mode)은 권한이라 저장·확정·읽기 **세 번** 보지만, 관문은 **확정 1회만** 본다. `readLesson()`은 관문을 부르지 않는다 |
| **증거물 스키마 신설 보류** | `#1036`(저작 화면이 모르는 칸을 저장 시 삭제)을 **먼저** 고쳐야 한다. 순서를 건너뛰면 **칸을 넓힐수록 데이터가 사라진다** |

## 결과

- 확정 시점 검사가 **13 → 14단계**가 됐다. 관문은 9번(형태·완결성)과 11번(모델 subset) 사이.
- 판정은 **확정 시점의 사건**이지 저장된 버전의 속성이 아니다 — `pedagogy`는 `module_json`에 저장되지 않으며 `#1114`의 read-back 테스트가 그 사실을 고정한다.
- 상세는 [[chalk-pedagogy-gate]], 구조는 [[chalk-studio-architecture]].

## 남은 것

- **선행 조건(`lesson_prerequisites`)의 의미가 미확정**인데 그것이 유일한 실질 차단 검사다 → [[ruling-pedagogy-gate-implementation]]
- **관문 판정을 되물을 곳이 없다** — 저장하지 않기로 한 것이 설계이나, "그때 무엇을 통과했나"가 필요해지는 시점이 올지는 판단하지 않았다
- `CR-GATE-04`(*"관문이 판정하는 것은 운영 계약의 준수이고 학습자 역량 해석과 구분한다"*)와 같은 방향이며, **`HC-08` 제약 때문에 역량 기반 합격선은 연구 전에는 세울 수 없다**는 [[chalk-requirements]] §5의 판정이 그대로 유효하다

## 관련

- [[chalk-pedagogy-gate]] · [[chalk-studio-architecture]] · [[chalk-requirements]]
