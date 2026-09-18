---
type: spec
title: "Chalk 교육 원칙 관문 — 검사기 v0"
status: implemented
owner: "[[jinyong-shin]]"
created: 2026-09-18
updated: 2026-09-18
source_ref: "scratchpad/chalk-scan/ 조사 보고 6건 + _worklog/chalk-ops/OPS-LOG.md (외부 경로)"
tags:
  - spec
  - chalk
  - gate
  - pedagogy
  - product
related:
  - "[[chalk]]"
  - "[[chalk-requirements]]"
  - "[[chalk-implementation-status]]"
  - "[[chalk-studio-architecture]]"
  - "[[pedagogy-gate-at-service-freeze]]"
  - "[[chalk-entry-point-20260918]]"
  - "[[chalk-target-shape-proposal]]"
  - "[[ruling-pedagogy-gate-implementation]]"
  - "[[chalk-ci-coverage-census]]"
---

# Chalk 교육 원칙 관문 — 검사기 v0

> **`CR-GATE-03`("검사는 형식·권한에 더해 **내용 검사**를 포함해야 한다")이 처음으로 코드가 됐다.**
> [[chalk-requirements]] §5가 *"관문이 필요하다는 합의는 있고, 관문을 통과시키는 규칙은 어디에도 없다"*로 못 박았던 공백의 **첫 조각**이다. 전부가 아니라 조각이다 — 합격선의 주체·재판정·근거 공개는 여전히 `미확인`.

> [!note] 출처와 확인 범위
> 이 페이지의 구현 사실은 **`hypeproof-studio` 저장소**에서 온 것이며 **이 세션이 직접 확인하지 않았다**(전언 + 조사 보고 경유).
> 근거 문서: `scratchpad/chalk-scan/studio-architecture-dataflow.md` · `studio-gate-placement.md` · `_worklog/chalk-ops/OPS-LOG.md` §4.
> 기준: `hypeproof-studio` main `75fe6e4` + PR `#1115`. **인수 기준 원문은 저장소를 읽는다.**

## 1. 무엇이 머지됐나

| 항목 | 값 |
|---|---|
| PR | **`#1115` 머지됨 (2026-09-18 13:55Z)** |
| 이슈 | `#1114` **닫힘** |
| 구현 위치 | `worker/src/lib/lesson-pedagogy.ts` (순수 함수) + `worker/src/routes/authoring.ts` freeze 핸들러 |
| 호출 지점 | 확정(freeze) **1회만** |
| 차단 응답 | **`422`** + `reason: pedagogy_blocked` |
| 테스트 | 19/19 통과 |

**확정 시점 검사가 13단계 → 14단계가 됐다.** 관문은 9번(형태·완결성)과 10번(모델 subset) 사이에 들어갔다. 전체 순서는 [[chalk-studio-architecture]] §확정 14단계.

성공 응답은 여전히 `{ module, source_revision, rehearsal: "not_run", activated: false, pedagogy }`다 — **확정은 활성화가 아니다.**

## 2. 검사 4종과 조항 출처

조항 매핑은 [[ruling-pedagogy-gate-implementation]]에서 판정한 것이 그대로 코드 주석에 들어갔다.

| 검사 | 수준 | 정본 조항 | 대응 강도 |
|---|---|---|---|
| `step_acceptance` 완료 기준 | fail | `design/lesson-plan-quality-checklist.md` **관문2-2** | ⚠️ **파생** — 원 조항은 차시 단위, 검사는 단계 단위 |
| `lesson_prerequisites` 선행 조건 | **fail (차단)** | ⚠️ **미확정** — 두 후보 병기 | 판정 대기 → §5 |
| `step_evidence` 증거물 | warn | `rules/curriculum-schema.md` **lint 2** | ✅ **완전 일치** (대상·방식·수준까지) |
| `duration_consistency` 시간 정합 | skip | `design/lesson-plan-quality-checklist.md` **관문2-9** (±10분) | ✅ 임계값까지 조항에 있음 |

> [!key-insight] 완료 기준 검사는 freeze 경로에서 도달 불가다 — 그리고 그게 정상이다
> 9번 `validateSessionDesign(content, true)`가 `title`·`audience`·`objective`·`starter`·각 step의 `title`·`instructions`·**`acceptance`**를 공백 불가로 이미 요구한다. 그래서 **`acceptance`가 빈 수업은 9번에서 `400`으로 먼저 막혀 관문에 도달하지 못한다.**
> 그런데도 구현해 둔 이유는 **그 함수가 freeze 전용이 아니기** 때문이다 — 초안 검사·`program.json` 설계 검사·CI 검사기가 같은 규칙을 재사용한다.
>
> 반대로 9번이 **요구하지 않는** 것이 `prerequisites`와 step의 `hint`다. → **선행 조건만 빈 수업이 관문까지 도달하는 유일한 모양**이고, 그래서 실질 차단은 `lesson_prerequisites` 하나가 진다.

## 3. 결정 6건 (2026-09-17~18)

출처: `_worklog/chalk-ops/OPS-LOG.md` §4. **확정된 결정이다.**

| 날짜 | 결정 | 근거 |
|---|---|---|
| 09-17 | **관문을 Service의 확정 핸들러에 둔다. Chalk가 아니다** | Chalk에 두면 **우회된다**(생성기가 Service에 직접 요청). ADR 0004가 *"내용 검사는 authoring API"*로 이미 규정 → [[pedagogy-gate-at-service-freeze]] |
| 09-17 | **차단은 한둘만, 나머지는 경고** | 전부 차단이면 **강사가 아무것도 확정하지 못한다** |
| 09-17 | 응답 코드 **422** | 기존 400/403/409와 겹치지 않음 |
| 09-17 | **증거물 스키마 신설 보류** | `#1036`(저작 화면이 모르는 칸을 저장 시 삭제)을 **먼저** 고쳐야 한다. 순서를 건너뛰면 **칸을 넓힐수록 데이터가 사라진다** |
| 09-17 | **읽기 시점 재검사 없음** | 교육 원칙은 **권한이 아니라 설계 속성**이다 |
| 09-18 | 시연은 **프로세스 내부 러너로만** | 격리가 설정이 아니라 **구조**. 운영에는 **확정본을 지우는 경로가 없다** |
| 09-18 | 데모 자료에 **`demo-` 접두사 + `[데모]` 제목** 강제, 테스트가 고정 | 봉투 바깥 고지는 content만 복사하면 따라가지 않는다 |

> [!key-insight] "권한이 아니라 설계 속성" — 이 한 줄이 관문의 성격을 정한다
> 형제 정책 셋(`lesson-feature-policy` #748 · `lesson-model-policy` #795 · `lesson-help-mode` #1008)은 같은 자리·같은 모양이지만 **권한**을 다룬다 — 좁히기만 가능하고 **저장·확정·읽기 세 번** 검사한다.
> 관문은 권한을 주거나 뺏지 않고 **확정 1회만** 본다. 그래서 `readLesson()`은 관문을 부르지 않는다.
> `CR-GATE-04`(*"관문이 판정하는 것은 운영 계약의 준수이고 학습자 역량 해석과 구분한다"*)와 같은 방향이다.

## 4. 데모 픽스처 4종

시연 대상. 상세 원문 추출은 조사 보고 `demo-source-dental-field.md`·`demo-source-sk.md`.

| # | 자료 | 기대 판정 |
|---|---|---|
| 1 | SK 진행표 | ✅ 통과 |
| 2 | 치과 **정식본** | ✅ 통과 |
| 3 | **치과 현장 진행표** ([[boa-dental-ai-homepage-cuesheet-20260706-spec]]) | 🔴 **차단** |
| 4 | 고친 판 | ✅ 재통과 |

3번이 차단되는 이유는 부실해서가 아니다. `status: active` 정본이고 분 단위 타임테이블·사전 준비물·산출물 4종을 다 갖췄는데도 **7개 구간 전부 완료 기준·선행 조건·강사 금지가 없다.** → *"실행 가능한 문서"와 "검사 가능한 문서"가 다르다*는 것이 시연의 논점.

> [!warning] 데모 설계 제약 2건
> ① 큐시트의 상위 커리큘럼 [[dental-website-copyclone-v3]]는 **"HYROX 레이스" 프레임**이라 헌법 B-1(순위·리더보드 금지)에 걸린다. 성인 라인 적용 여부가 미판정이므로 **큐시트만 태우고 상위 커리큘럼은 태우지 않는다.**
> ② 치과 회차는 **실측 입력 0건**이다. 산출물 4종은 *설계상 만들기로 한 것*이며 실적으로 쓰면 근거 없는 주장이 된다. lab 운영 문서가 직접 적는다 — *"`sample: true`를 `false`로 바꾸는 것은 수정이 아니라 위조다"* (`hypeprooflab/products/workshop-result-report/engagements/dental-2026-07-29/README.md:18`, **이 세션이 직접 확인하지 않음**).

## 5. 미결 — 관문을 더 열려면 먼저 풀어야 할 것

| # | 막힌 것 | 열쇠 | 상태 |
|---|---|---|---|
| 1 | **선행 조건의 의미** | **두 층을 함께 확정** — 조항(볼트) + 필드 내용(제품) | **유일한 실질 차단 검사인데 두 층이 다 비어 있다.** 아래 참조 → [[ruling-pedagogy-gate-implementation]] §4① |
| 2 | 시간 정합 (`duration_consistency`) | `steps[].duration_min` 필드 | 스키마 신설 필요 |
| 3 | 증거물 **양성** 판정 (관문2-1 "제3자가 볼 수 있는 물건") | `steps[].evidence` | **`#1036` 선행** (결정으로 보류) |
| 4 | 헌법(관문1) 계열 7건 | `session.scope` 같은 **명시적 층 구분 값** | `CR-EDU-08` 판정 필요. 정확도가 아니라 **정합성** 문제 |
| 5 | 금지 개입 4계열 (관문2-4, 유일한 "필수. 없으면 미완성") | `steps[].prohibited_moves[]` | `CR-EDU-07`이 이미 요구 |

> [!key-insight] 선행 조건은 **두 층이고 한쪽만 정하면 아무도 안 정한 것이 된다**
> | 층 | 질문 | 정하는 쪽 |
> |---|---|---|
> | **조항** | 관문2-6의 "선행 조건"이 활동 사이의 의존인가 학습자 선행지식인가 | **커리큘럼 볼트** |
> | **제품 필드** | `session-design`의 `prerequisites`에 **강사가 무엇을 적게 할 것인가** | **제품** |
>
> **제품 필드는 볼트가 만든 것이 아니다** — 요구사항 `CH-01`(*"대상·시간·목표·**선수 조건**을 저장하고 재편집한다"*, `CR-AUTH-01`, **구현됨**)에서 왔다.
> 볼트가 "조항은 활동 의존을 뜻한다"고 정해도 **필드가 학습자 선행지식을 담고 있으면 관문은 엉뚱한 것을 검사하게 된다.** 지금 검사가 **"비었나"만 보기 때문에 어긋남이 드러나지 않을 뿐**이고, 내용을 보기 시작하면 갈라진다. **둘을 함께 확정한다.**

> [!warning] 지금 관문1을 켜면 성인 수업이 아동 조항에 걸린다
> 커리큘럼 헌법은 아동·청소년 전제인데 studio 범위에는 **성인 전문직 수업**(치과)이 있다. `CR-EDU-08`("교육 원칙을 공통층/대상별층 2층으로 분리")이 **⚠️판단 필요**로 남아 있는 한 켤 수 없다.
> 커리큘럼 위키는 이미 `scope: common | edu-11-16 | startup-ir`로 그 분리를 해 뒀으나 **성인 전문직 라인 값이 없다.**

## 6. 관측된 한계

- **관문 판정(`pedagogy`)이 저장되지 않는다.** 확정 응답에 실려 나갈 뿐 `module_json`에 들어가지 않으며, `#1114`의 read-back 대조 테스트가 **그 사실을 주석과 함께 고정**한다 — 빠뜨린 필드가 아니라 설계다. 판정은 **확정 시점의 사건**이지 저장된 버전의 속성이 아니다. → *"그때 무엇을 통과했나"를 되물을 곳이 없다.*
- **화면이 판정을 못 보여 준다.** `authoring.html`의 `call()`이 `j.error` 문자열만 쓰므로 `reason`도 `findings`도 화면에 닿지 않는다. 판정과 "무엇을 채우면 열리는가"를 띄우는 브랜치가 있으나 **아직 미머지**(`feat/chalk-pedagogy-verdict-ui`, 커밋 `4c74217`, 이슈 미발행).
- **규칙 술어가 코드에 있다.** 정본은 이 저장소의 커리큘럼 위키이고 주석에 조항 ID·경로·짧은 인용만 남겼다. 장기적으로는 외부 정본에서 읽는 구조(엔진/데이터 분리)로 가야 하며, 모양은 `worker/scripts/cohort-harness/`의 `validate.py`/`rules.yaml`에 이미 있다. 단 **그 mini-YAML 파서가 list-of-maps를 지원하지 않아 규칙 표는 JSON이어야 한다.**

> [!warning] 🆕 2026-09-19 — **관문 코드가 브라우저 검사의 사각지대에 있다**
> `worker/src/lib/lesson-pedagogy.ts`가 `dental-reference.yml`의 `paths` 필터에 **없다.** 그 시험이 실제로 지나는 파일인데도 그렇다.
> → **관문만 고치는 PR은 브라우저 저작 시험이 아예 돌지 않는다.** `#1115`가 걸리지 않고 지나간 것은 그 PR이 `authoring.ts`도 함께 고쳤기 때문 — **운이었다.**
> 같은 작업에서 **손으로 배선하는 쪽의 시험 하나를 깨뜨렸고 검사는 초록이었다. 열흘 뒤 우연히 발견됐다.**
> 원인·전수·수정 우선순위 → [[chalk-ci-coverage-census]] (목록에 파일 추가만 하면 되고 **비용 0**)

## 7. 추적

- `config/requirement-work.json` — 관문은 실행 단위 `lesson-pedagogy-gate`(#1114)이며 `BASE-04`·`CH-04`·`VER-01`을 진다. **포괄 검증 #732에만 걸려 있던 49개를 실행 단위로 쪼갠 첫 사례.**
- ⚠️ **작업 41개 전부 `verification_inputs`가 비어 있다** — 비어 있으면 그 덩어리는 `fulfilled`가 될 수 없다. 즉 **완료를 증명할 근거 칸이 하나도 안 채워져 있다.** 데모 픽스처(#1116)의 제자리가 바로 이 칸이다.
- ⚠️ `config/traceability.json`에 **Chalk 계열 implementation 스테이지 노드가 없다** (REQ·DES·TEST는 있고 IMP가 없다). [[chalk-requirement-coverage-audit]]이 보고한 "Chalk 요구사항 ID 0건"과 같은 부채.

## 관련

- [[pedagogy-gate-at-service-freeze]] — 배치 결정
- [[chalk-studio-architecture]] — 확정 14단계·소유 경계·저장 구조
- [[chalk-entry-point-20260918]] — 진입점 미결
- [[ruling-pedagogy-gate-implementation]] — 커리큘럼 조항 쪽 판정
- [[chalk-requirements]] §B 관문 `CR-GATE-01~09` · §5 합격선 공백
- [[chalk-implementation-status]] · [[chalk-requirement-coverage-audit]]
