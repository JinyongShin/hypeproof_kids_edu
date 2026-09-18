---
type: spec
status: draft
scope: common
ip_owner: unverified
title: "커리큘럼 자산 프론트매터 스키마"
owner: JY
created: 2026-08-08
updated: 2026-08-17
tags:
  - curriculum
  - schema
---

# 커리큘럼 자산 프론트매터 스키마

컴파일러(L4)의 입력은 산문이 아니라 **프론트매터**다. 아래 필드가 없으면 그 자산은 조합 불가능하며, 강사는 그것을 재사용할 수 없다.

## 공통 필수 필드

모든 `curriculum_wiki/` 노트에 적용.

```yaml
type: method | activity | rubric | guardrail | constraint | spec | asset | track | lesson-plan | ingest-ruling | meta
status: draft | active | quarantine | retired
scope: common | edu-11-16 | startup-ir     # 유효 범위. common = 라인 무관 정본
ip_owner: unverified | hypeproof | partner-<name> | joint | derived-external
created: YYYY-MM-DD
updated: YYYY-MM-DD
tags: [curriculum, ...]
```

## `scope` — 값 체계 (2026-08-17 신설)

| 값 | 뜻 | 접두사 |
|---|---|---|
| **`common`** | **라인 무관.** 라인이 몇 개로 늘어도 이 문서는 하나다 | `m-` `kr-` 또는 없음 |
| `edu-11-16` | 11~16세 라인 전용 | `edu-11-16-` `ped-` |
| `startup-ir` | 고등학생 창업·IR 라인 전용 | `startup-` |

### 왜 `common`이 신설되었는가

`curriculum_wiki/`가 만들어질 때 라인은 **하나뿐이었다.** 그래서 40건 전부에 `scope: edu-11-16`이 붙었다. 두 번째 라인(`startup-ir`)이 생기자 **`edu-constitution`(헌법)조차 형식상 창업 라인에 적용되지 않는 상태**가 드러났다.

**게이트 문서가 라인 전용으로 잠겨 있으면 게이트가 아니다.** 2026-08-17 26건을 `common`으로 재판정했다.

### 판정 기준

> **"두 번째 라인에서도 이 문서를 그대로 읽을 것인가?"**
> 그렇다 → `common` · 아니다 → 라인값

- **헌법·금지개입·근거등급·방법론 카드·지도안 규격은 `common`이다.** 대상 연령이나 상품이 바뀌어도 변하지 않는다
- **연령·시장·상품 근거는 라인값이다.** 특정 연령대 발달 특성, 특정 시장 가격, 특정 트랙 구조
- **`common` 문서를 한 라인의 필요로 고치려 할 때는 멈춘다.** 그건 라인 전용 문서를 새로 만들라는 신호다

⚠️ **`common`은 "모든 라인에 검증됐다"는 뜻이 아니다.** 방법론 카드의 근거는 대부분 특정 연령대 연구에서 왔다. 라인마다 이식 판정이 필요하다는 사실은 그대로다. → [[ruling-startup-ir-asset-alignment]]

## 파일명 — 접두사 체계 (2026-08-17 신설)

파일명은 `kebab-case.md`이며 **볼트 전체에서 고유**해야 한다(위키링크가 파일명 기준이므로 `wiki/`와도 충돌 불가).

접두사는 **`scope`를 파일명에서 눈으로 읽기 위한 것**이다. 프론트매터를 열지 않고도 어느 라인 문서인지 알 수 있어야 한다.

접두사는 두 종류가 있다. **섞어 쓰지 않는다.**

**① 종류 접두사** — 문서의 *성격*을 나타낸다. `scope`를 구속하지 않는다.

| 접두사 | 대상 | 허용 `scope` |
|---|---|---|
| `m-` | 방법론 카드 (국제 문헌 기반) | `common` |
| `kr-` | 국내 수업 모형 지도 | `common` |
| `ped-` | 교수학습·시장 조사 | **`common` 또는 `edu-11-16` 둘 다 가능** |
| `ruling-` | **판정 문서** | 모든 값 |
| `act-` | 활동 원자 | 모든 값 |

**② 라인 접두사** — 문서가 *어느 라인 전용*인지 나타낸다. `scope`와 1:1이다.

| 접두사 | 대응 `scope` |
|---|---|
| `edu-11-16-` | `edu-11-16` |
| `startup-` | `startup-ir` |
| `curriculum-` | `edu-11-16` (작업 파일 `curriculum-hot`·`curriculum-log`. `curriculum-index`·`curriculum-schema`는 `common` 예외) |

**③ 접두사 없음** — 라인·주제를 넘는 **정본**. `scope: common`.
예: `edu-constitution` · `measurement-axes` · `prohibited-moves` · `placement-rules` · `methods-index` · `evidence-standards` · `lesson-plan-authoring-guide`

### ⚠️ 미판정 — 규칙과 어긋난 상태로 남겨둔 2건

접두사가 없어(규칙 ③) `common`이어야 하는데 `scope: edu-11-16`인 문서가 둘 있다. **추측으로 옮기지 않고 판정 대기로 둔다.**

| 문서 | 쟁점 |
|---|---|
| [[measurement-axes]] | 문서가 스스로 "커리큘럼 라인 정본"이라 선언한다. 그런데 창업·IR 라인에는 **집단창의에 대응하는 축이 없다**(대회 배점 45~50점). `common`으로 올려 6번째 축을 넣을지, 라인 전용 측정 문서를 새로 만들지 |
| [[placement-rules]] | 배치 제약 C-1~C-9가 11~16세 회차 구조(110분×2)에 묶여 있는지 확인 필요 |

같은 이유로 `ped-session-format-attention-group-size`(표본 연령)·`ped-premium-private-education-benchmark-kr`(시장 가격대)도 `edu-11-16`에 남겼다. 넷 다 **본문을 읽어야 판정된다.**

⚠️ **`ped-`가 두 `scope`를 허용하는 것은 의도된 타협이다.** 조사 문서는 "이 근거가 어느 라인까지 유효한가"가 사후에 판정된다 — 특정 연령대 표본에서 나온 조사가 알고 보니 라인 무관이거나 그 반대다. 파일명을 바꾸면 위키링크가 전부 깨지므로 **접두사는 고정하고 `scope`만 옮긴다.** 대신 `ped-` 파일은 파일명만으로 라인을 알 수 없으니 `scope`를 확인해야 한다.

### 판정 규칙

- **라인 전용 문서는 라인 접두사를 반드시 붙인다.** 라인이 늘어나면 접두사도 늘어난다
- **`ruling-`이 라인 접두사보다 앞선다.** `ruling-startup-ir-...`가 맞고 `startup-ruling-...`은 틀리다. 판정 문서는 한곳에 모아 보는 것이 우선이기 때문이다
- **접두사 없음은 "정본"의 표시다.** 라인이 아무리 늘어도 이 문서는 하나라는 선언. 새 문서에 접두사를 안 붙이려면 그 근거를 답할 수 있어야 한다
- 접두사는 `scope`와 **모순되면 안 된다**. `startup-` 파일에 `scope: edu-11-16`이 오는 것은 오류다

> ⚠️ **이 규칙은 사후에 만들어졌다.** 2026-08-17 창업·IR 라인 문서 6건 중 1건(`yeep-resource-manifest`)이 접두사를 빠뜨린 것을 발견하고 정식화했다. 관행으로 유지하던 것을 규칙으로 올리지 않으면 반드시 어긋난다.

## `ip_owner` — 값 체계

`ip_owner`는 **누락 금지**. 파트너 IP가 섞인 자산은 제3자 라이선스 패키지에서 기계적으로 제외되어야 한다. → [[edu-11-16-parent-track-ip-boundary]]

| 값 | 뜻 | 라이선스 패키지 |
|---|---|---|
| **`unverified`** | **기본값. 귀속 판정 전** | ⛔ **자동 제외** |
| `hypeproof` | 판정 완료. 법인 단독 소유 | ✅ 포함 |
| `partner-<name>` | 파트너 소유 | ⛔ 제외 (인바운드 계약 범위 내에서만 사용) |
| `joint` | 공동 소유 | ⚠️ 개별 합의 필요 |
| `derived-external` | 외부 저작물 기반 2차적저작물 | ⚠️ 재배포 검토 필요 |

### 왜 `unverified`가 기본값인가

2026-08-08 기준 **48건 전부 `unverified`다.** 이는 미완이 아니라 정직한 상태다.

초기에는 파일을 만들 때마다 습관적으로 `hypeproof`를 넣었으나, **각 파일에 대해 "정말 법인 단독 소유인가"를 판정한 적이 없었다.** 전부 같은 값으로 채워진 필드는 "판정이 끝났다"는 잘못된 인상을 주고, 라이선스 패키지 빌드 시 그것을 믿으면 위험하다.

실제로 판정이 필요한 사례:

| 대상 | 쟁점 |
|---|---|
| `curriculum_wiki/research/ped-*` 10건 | 외부 저작물의 요약·번역. 인용 범위를 넘는 요약이 재배포되면 문제. **`derived-external` 후보** |
| `models/kr-models-*` 4건 | 국내 교육과정 모형 정리. 같은 성격 |
| `models/m-00*` 8건 | Gold Standard PBL 7요소(PBLWorks), 스캐폴딩 3요소 등은 **원저자의 프레임**이다 |
| `.raw` 유래 자산 | 원본은 Jay의 아이데이션 산출물. **개인 vs 법인 귀속이 정리된 적 없다** |

마지막 항목이 특히 그렇다. 회사–창업자 간 IP 귀속 문제이며 **법률 검토 영역**이다. 임의로 `hypeproof`를 적는 것은 추정이다.

### 판정 규칙

- **판정 없이 `hypeproof`로 올리지 않는다.** 판정 근거를 노트 본문 또는 `edu-11-16-parent-track-ip-boundary`에 남긴다
- `partner-<name>`의 `<name>`은 **파트너사가 확정된 뒤** 채운다. 현재 미확정
- `derived-external`은 원저작물 출처를 함께 기록한다
- **`unverified`가 남아 있는 자산은 라이선스 패키지 빌드에서 자동 제외**된다. 이것이 이 값의 안전 기능이다

## activity — 활동 원자

조합의 최소 단위. 30~60분. "차시"보다 작고 "단계"보다 크다.

```yaml
type: activity
id: act-<3자리>                  # 불변. 파일명이 바뀌어도 이 값으로 참조
model: M?                        # 소속 수업모형
principle: []                    # 원리 번호
level: [lv1, lv2]                # 적용 발달구간. 변형은 본문에
duration_min: 45
requires: [act-003, asset-...]   # 선행 자산·활동
forbids: []                      # 동시·인접 배치 금지
evidence: ""                     # 이 활동이 남기는 증거물 1개
axes: [input, load]              # 측정 5축 중 훈련 대상
prohibited_moves: []             # 금지 개입. 강사 매뉴얼로 자동 추출
prep_assets: []                  # 사전 준비 자산
safety: none | attention | protocol   # protocol이면 별도 대응 절차 필수
method: [m-002]                  # 채택 방법론 → curriculum_wiki/methods/
guidance:                        # m-002 요건. 발견형 활동에 필수
  space: ""                      # 탐색 공간을 어떻게 좁히는가
  elicit: ""                     # 설명 유도 발문
  feedback: ""                   # 즉각 피드백 통로
individual_evidence: ""          # 소집단 활동의 개별 산출물 (m-005 요건)
retry: true                      # 재시도 기회 유무 (m-006 요건)
```

### 방법론 파생 필수 필드 (2026-08-08 추가)

방법론 라이브러리 조사에서 도출된 요건. → [[methods-index]]

- **`guidance`** — 발견형 활동(`method`에 m-002 포함)은 3개 하위 필드를 모두 채운다. **하나라도 비면 그 활동은 "안내된 발견"이 아니라 방치**이며, 명시적 수업보다 나쁜 결과를 낸다 (Alfieri et al. 2011: 비유도 발견 d=−0.38)
- **`individual_evidence`** — 소집단 활동은 개별 산출물이 있어야 한다. 없으면 증거가 개인에게 귀속되지 않아 Evidence(Sediment)가 성립하지 않는다
- **`retry`** — 피드백이 발생하는 활동에서 `false`면 그 피드백은 형성평가가 아니다

### 필드 주석

- **`evidence`** — 증거물이 없는 활동은 만들지 않는다. Evidence(Sediment)에 적재될 것이 없으면 그 시간은 상품 가치를 만들지 않는다.
- **`prohibited_moves`** — 이 라인 품질의 핵심 장치. "무엇을 하는가"보다 **"무엇을 하지 않는가"**가 결과를 결정한다. → [[prohibited-moves]]
- **`requires` / `forbids`** — 컴파일러가 배치 유효성을 검증하는 근거. 산문에 숨어 있으면 검증이 안 되고, 라이선스 강사는 산문을 읽지 않는다.
- **`duration_min`** — 회차 총시간에 의존하지 않게 30/45/60 단위로만 쓴다. 회차 포맷이 바뀌어도 자산을 안 건드리기 위함. → [[edu-11-16-session-format]]
- **`safety: protocol`** — 정서적 어려움이 드러날 수 있는 활동. 개별 대응 절차 문서 링크 필수.

## lesson-plan — 지도안

활동 원자를 1차시 분량으로 조립한 결과. 컴파일러의 출력이자 강사의 실행 문서.

```yaml
type: lesson-plan
track: <track-id>
session: <회차>-<차시>
activities: [act-001, act-004]   # 구성 활동
model: [M1]
level: lv1 | lv2
duration_min: 110
evidence: []                     # 이 차시가 남기는 증거물
completion_link: []              # 연결된 수료 요건
```

규격과 작성 순서는 [[lesson-plan-authoring-guide]].

## ingest-ruling — 승격 판정

`.raw/` 원자재를 자산으로 승격할 때 무엇을 왜 바꿨는지 기록. 원본은 `.raw`에 불변으로 남는다.

```yaml
type: ingest-ruling
source: ".raw/<파일명>"
ruling: adopt | transform | reject | defer
grounds: ""
produced: []                     # 이 판정으로 생성된 자산
```

## Lint 규칙

`/wiki-lint` 실행 시 아래를 검사한다.

1. `curriculum_wiki/**` 에 `ip_owner` 누락 → 에러 (프론트매터 기준. 본문 코드블록은 무시)
2. `evidence`가 빈 `activity` → 경고
3. `status: quarantine` 자산이 트랙에 포함됨 → 에러
4. `safety: protocol` 인데 대응 절차 링크 없음 → 에러
5. `method`에 m-002 포함인데 `guidance` 하위 필드 미완 → 에러
6. 소집단 활동인데 `individual_evidence` 비어 있음 → 에러
7. 피드백 활동인데 `retry: false` → 경고
8. `ip_owner`가 정의된 5개 값 외 → 에러
9. **`ip_owner: unverified` → 라이선스 패키지 빌드에서 자동 제외** (경고, 빌드 시 에러)
10. **`scope`가 라인 전용값인데 파일명에 대응 접두사 없음 → 에러**
    (`scope: startup-ir` → `startup-` 또는 `ruling-startup-` / `scope: edu-11-16` → `edu-11-16-`·`ped-`. 접두사 없는 정본 문서는 화이트리스트로 예외 처리)
11. **파일명 접두사와 `scope`가 모순 → 에러** (예: `startup-*.md` 에 `scope: edu-11-16`)
12. 파일명이 볼트 전체(`wiki/` 포함)에서 중복 → 에러 (위키링크 해석 불가)

> 🆕 **2026-09-18 정정 — lint 2는 구현됐다. 단 이 볼트가 아니라 `hypeproof-studio`에서다.** 교육 원칙 관문 검사기(PR `#1115`)의 `step_evidence` 검사가 lint 2와 **대상·방식·수준까지 일치**한다. 조항은 복사되지 않았고 주석에 ID·경로·인용만 남았다 — **이 문서가 여전히 정본이다.** → [[ruling-pedagogy-gate-implementation]]
>
> ⚠️ **나머지 lint 1·3~12는 여전히 미구현이다.** 규칙 10·11이 있었다면 `yeep-resource-manifest` 누락은 커밋 전에 걸렸다. → [[curriculum-hot]] P3

## 관련

- [[edu-constitution]]
- [[lesson-plan-authoring-guide]]
