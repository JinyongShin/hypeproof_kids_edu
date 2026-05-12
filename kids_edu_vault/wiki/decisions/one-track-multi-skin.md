---
type: decision
status: active
priority: 1
date: 2026-05-11
owner: "봉호 태"
context: "3-트랙 구조 채택 후 재검토 — 커리큘럼 코어는 동일하고 대상만 다름을 확인"
supersedes: "[[three-track-structure]]"
tags:
  - decision
  - strategy
  - curriculum
created: 2026-05-11
updated: 2026-05-11
---

# 1트랙 멀티 스킨 구조 채택

## 결정

커리큘럼 구조를 **3-트랙 → 1트랙 멀티 스킨**으로 전환한다.

- **코어 커리큘럼**: 1개 (학습 흐름·단계·타이밍 동일)
- **스킨**: 대상별로 교체 (scaffold 텍스트, AI 페르소나, 사례·컨텍스트)

| 스킨 | 대상 | 스킨 교체 요소 |
|---|---|---|
| 아동 | 초등생 | 쉬운 언어, 창작 중심 컨텍스트, 아동용 페르소나 |
| 성인 | 직장인·전문직 | 직무 사례 컨텍스트, 성인용 페르소나 |
| 혼합 | 아동+성인 | 공통 활동 + 역할 분리 scaffold |

## 근거

- 3-트랙 구조 운영 시 커리큘럼 설계·검증·개선 비용이 3배로 증가
- 실제 학습 흐름(도입→탐색→제작→공유)은 대상과 무관하게 동일
- 달라지는 것은 언어·사례·페르소나뿐 → 스킨 교체로 충분히 커버 가능
- 단일 코어 유지 시 Production Loop가 단순해지고 품질 향상 속도 빨라짐

## 구현 방향

- `scaffoldData.ts`: 스킨별 데이터셋 교체 (skin: "kids" | "adult" | "mixed")
- `TUTOR.md`: 스킨별 페르소나 파일 분리 (`TUTOR_kids.md`, `TUTOR_adult.md`)
- 커리큘럼 스펙 파일: `specs/core/` 로 통합, 스킨별 override는 `specs/skins/`

## 기각된 대안

| 대안 | 기각 이유 |
|---|---|
| 3-트랙 유지 | 커리큘럼 관리 비용 3배, 개선 주기 느려짐 |
| 2-트랙 (아동/성인) | 근본적으로 같은 문제 — 코어가 동일하면 트랙 분리 불필요 |

## 후속 작업

- [ ] `specs/track-a/`, `specs/track-b/` → `specs/core/` + `specs/skins/` 구조로 재편
- [ ] scaffold 스킨 스펙 정의 (skin 파라미터 및 교체 대상 명세)
- [ ] `TUTOR_kids.md`, `TUTOR_adult.md` 분리 작성
- [ ] hot.md 현황 업데이트

## 관련

- [[three-track-structure]] — superseded
- [[production-loop-adoption]]
- [[production-loop]]
