---
type: validation
title: "자동 검사 커버리지 전수 — 무엇이 PR에서 실제로 도는가"
status: summarized
owner: "[[jinyong-shin]]"
created: 2026-09-19
updated: 2026-09-19
source_ref: "scratchpad/chalk-scan/ci-coverage-census.md · 기준 hypeproof-studio main ce95747 (외부 저장소, 이 세션이 직접 확인하지 않음)"
tags:
  - validation
  - chalk
  - ci
  - testing
  - product
related:
  - "[[chalk-pedagogy-gate]]"
  - "[[chalk-implementation-status]]"
  - "[[chalk-requirement-coverage-audit]]"
  - "[[verification-discipline]]"
  - "[[chalk]]"
---

# 자동 검사 커버리지 전수

> [!note] 출처와 확인 범위
> **`hypeproof-studio` 저장소 조사이며 이 세션이 직접 확인하지 않았다**(조사 보고 경유).
> 기준 **main `ce95747`** — 열린 PR의 변경은 제외. 조사 원본 `scratchpad/chalk-scan/ci-coverage-census.md`.
> 세션 **둘이 서로 안 보고 독립적으로 재서 숫자가 일치**했다(스크립트 기준 / 테스트 파일 기준).

## 0. ⭐ 남겨야 할 것은 숫자가 아니라 이 문장이다

> [!key-insight] 같은 저장소에 시험 배선 규약이 **두 벌**이다
> 한쪽은 **폴더를 통째로 집어** 새 파일이 저절로 들어간다 — **누락 0**.
> 다른 쪽은 **이름을 하나씩 손으로 적는다** — 빠뜨리면 **조용히 안 돈다**.
>
> **그리고 파일을 만드는 사람은 자기가 어느 쪽에 있는지 모른다.**

구멍은 **결과**이고 규약이 두 벌인 것이 **원인**이다. 아래 숫자는 그 원인이 만든 자국이다.

- 글롭 방식: `extensions/hypeproof-chat`의 `npm test`가 `for f in test/*.smoke.mjs`로 돈다. 새 테스트를 넣었더니 **아무 배선 없이 93개 중 하나로 들어갔다. 고아 0.**
- 손으로 적는 방식: `worker`·`e2e`. 빠뜨리면 아무 신호가 없다.

## 1. 사실

| 항목 | 값 |
|---|---|
| PR 이벤트에 반응하는 워크플로 | **22개 중 7개** |
| 그중 **브라우저로 화면을 모는 층** | **둘뿐** (`dental-reference.yml`·`start-page.yml`) — **둘 다 `paths` 필터로 걸러진다** |
| 시험 묶음(`test`/`test:*`/`demo:*`) 중 PR 검사 경로에 없는 것 | **59개 중 28개** |
| 서버 쪽 시험 파일 중 실행 체인 밖 | **67개 중 9개** — 그중 **6개는 아무 데서도 안 돈다** |

단위 층(`pr-ci.yml`)은 `paths` 필터가 없어 **무엇을 고치든 돈다.** 구멍은 브라우저 층에만 있다.

`tests/rehearsal`은 **10개 전부** 안 돈다.

## 2. 구멍이 둘이고, 뒤쪽이 더 위험하다

### 구멍 ① 목록에 없다
워크플로가 부르는 스크립트 목록에서 빠져 있다. 실패 모양이 다시 둘로 갈린다:

- **배선 누락 (5개)** — `npm run test:costs:d1` 같은 스크립트가 `package.json`에 **멀쩡히 있는데 아무도 부르지 않는다.** → *만든 사람은 "테스트 있음"으로 알고 있을 것이다.*
- **고아 파일 (1개)** — `scrub-secrets.test.mjs`는 **스크립트조차 없다.** 파일 헤더 주석에 실행법이 적힌 것이 전부.

> `scrub-secrets`는 **코치 출력의 자격증명 유출을 막는 가드의 유일한 테스트**다(epic #431). 손으로 돌리면 **통과한다** — 지금 깨져 있다는 뜻이 아니라 **깨져도 아무도 모른다**는 뜻이다.

### 구멍 ② 경로가 안 맞는다 — **더 위험하다**

**"워크플로에 적혀 있다"와 "내 PR에서 돈다"가 다르다.**

`dental-reference.yml`이 부르는 시험은 저작·수업 전달 경로를 브라우저로 모는데, **그 시험이 실제로 지나는 파일 상당수가 `paths` 필터에 없다.**

| 파일 | `paths`에 | 시험이 지나나 |
|---|---|---|
| `worker/src/routes/authoring.ts` | ✅ | 지남 |
| `worker/src/lib/session-design.ts` · `lesson-delivery.ts` | ✅ | 지남 |
| `chalk/**` · `e2e/chalk-authoring/**` | ✅ | 지남 |
| **`worker/src/lib/lesson-pedagogy.ts`** | ❌ **없음** | **지남 (확정 경로의 관문)** |
| `lesson-feature-policy.ts` · `lesson-model-policy.ts` · `lesson-help-mode.ts` | ❌ | 지남 |
| `worker/src/lib/modules.ts` · `routes/admin.ts` | ❌ | 지남 |
| `worker/test/harness/dental-authoring.mjs` | ❌ | **러너 자신이 쓰는 하네스** |

> [!warning] ⛔ 관문만 고치는 변경은 브라우저 시험이 아예 돌지 않는다
> **`lesson-pedagogy.ts`만 고치는 PR은 `dental-reference`가 트리거되지 않는다.**
> [[chalk-pedagogy-gate]]의 `#1115`가 걸리지 않고 지나간 것은 **그 PR이 `authoring.ts`도 함께 고쳤기 때문 — 운이었다.**
> **목록에 있어도 경로가 안 맞으면 평생 안 돈다.**

## 3. 실제 피해 둘

1. **관문을 넣으면서 손으로 적는 쪽의 시험을 깨뜨렸다.** 검사는 초록이었고 머지될 때 아무도 몰랐다. **열흘 뒤 우연히 발견됐다.**
2. **위 §2 구멍 ②** — 같은 관문 코드가 경로 목록에 없어서, 관문만 고치는 변경은 브라우저 시험을 한 번도 태우지 못한다.

## 4. ⚠️ 이 표는 **하한선**이다

조사 원본이 자기 방법의 한계를 6개 적어 두었다. 가장 중요한 것:

> **`continue-on-error`를 확인하지 않았다. 도는 것과 막는 것은 다르다** — 실패해도 통과시키는 스텝이 있으면 **"돈다"가 "지킨다"를 뜻하지 않는다.**

그 밖에 — 쉘 스크립트 안쪽 한 겹까지만 추적 · 합성 액션 미집계 · `matrix` 분기 · `if:`로 꺼지는 스텝 · **`e2e`·`chalk`·`packages/measurement`는 파일 기준으로 세지 않았다**(거기에도 고아가 있을 수 있다).

> **"안 돈다"로 적힌 것은 안 돌 가능성이 높지만, "돈다"로 적힌 것이 실제로 막아 주는지는 별개다.**

## 5. ⬜ 미결 — 답을 지어내지 않는다

### 두 규약 중 어느 쪽으로 통일할 것인가

| 선택 | 얻는 것 | 잃는 것 |
|---|---|---|
| **글롭(통째로 집기)** | **고아가 없어진다** | **실기기·실제 SDK처럼 실행 조건이 다른 시험까지 끌어들인다** |
| 손으로 적기 (현행) | 실행 조건을 고를 수 있다 | 빠뜨리면 조용히 안 돈다 |

**판단이 필요한 자리다.** 위클리 제안서 §10 "위클리 뒤 개발 쪽에서 정할 것"에 올라갔다.

### 그 밖에 판정하지 못한 것 (원본 §4)

| 항목 | 왜 모르나 |
|---|---|
| `tests/rehearsal` 10개를 CI에 넣어야 하는가 | 운영 리허설(실제 토큰·게이트웨이)로 **보이지만** README·스크립트 본문을 읽지 않았다 |
| `e2e`의 `:mac`·`:sdk`·`:live-sdk`가 정말 CI 불가인가 | **이름에서 추정**했을 뿐 실행 요건 미확인 |
| `worker`의 `:d1` 여섯 중 셋만 넣은 것이 의도인가 누락인가 | 셋은 ADR 0004 등에 "explicit PR CI step"으로 적혀 있으나 나머지는 그런 기록을 찾지 않았다 |
| 각 워크플로의 `paths`가 **의도적으로 좁은가** | §2의 빠진 파일들이 "안 넣기로 한 것"인지 "잊은 것"인지 판정할 근거가 없다 |
| `extension / smoke`가 **필수 컨텍스트인가** | 확인 시도가 **403**(토큰 권한 밖인지 ruleset 이동인지 단정 못 함). **글롭으로 자동 진입해도 그 잡이 필수가 아니면 빨개져도 머지를 안 막는다.** ⚠️ **GitHub API 한도 소진 중이라 지금 확인 불가** |

## 6. 값이 큰 순서 (고치지 않았다 — 판단용)

| # | 항목 | 비용 |
|---:|---|---|
| 1 | **`dental-reference.yml`의 `paths`에 빠진 파일 추가** | **0** (새 잡·새 설치 없음). 목록 수정 한 번 |
| 2 | `test:chalk-simple` | 1초. 이미 진행 중 |
| 3 | **`scrub-secrets.test.mjs` 배선** | 스크립트 한 줄 + 체인 한 줄. **값 대비 비용이 가장 낮다** |
| 4 | `worker`의 `:d1` 다섯 | 판정 선행(§5) |
| 5 | `e2e`·`chalk`도 파일 기준으로 세기 | 30분 |
| 6 | `tests/rehearsal` 10개 | 성격 판정 선행(§5) |
| 7 | `continue-on-error` 전수 | "돈다 ≠ 막는다" 확인. 표의 신뢰도를 올린다 |

## 관련

- [[verification-discipline]] — 이 조사가 남긴 검증 규범 3개
- [[chalk-pedagogy-gate]] — §2 구멍 ②가 직접 걸리는 자리
- [[chalk-implementation-status]] · [[chalk-requirement-coverage-audit]] · [[chalk]]
