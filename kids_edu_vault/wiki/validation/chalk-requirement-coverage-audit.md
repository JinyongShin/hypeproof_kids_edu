---
type: validation
title: "Chalk 요구사항 반영 여부 전수 감사 (2026-09-15)"
status: recorded
owner: "[[jinyong-shin]]"
created: 2026-09-15
updated: 2026-09-15
raw_path: ".raw/chalk-traceability-audit-20260915.md"
base_commit: "04f03d061617e6d88e9f2b68eaa82c9933540aa5"
tags:
  - validation
  - chalk
  - requirements
  - traceability
related:
  - "[[chalk-requirements]]"
  - "[[chalk-implementation-status]]"
  - "[[requirement-id-index]]"
  - "[[chalk]]"
  - "[[chalk-target-shape-proposal]]"
  - "[[capability-measurement-module]]"
---

# Chalk 요구사항 반영 여부 전수 감사 (2026-09-15)

> [[chalk-requirements]]의 `CR-*` 89건이 가리키는 **정본 ID 75개를 studio 저장소에서 하나씩 대조**한 결과. 짝 페이지 [[chalk-implementation-status]]가 *무엇이 되어 있나*를 기능 단위로 적는다면, 이 페이지는 **요구사항 단위로 되어 있나**를 적는다.
> 기준 커밋 **`04f03d0`** (main = origin/main, 2026-09-15 20:08 KST) · `git fetch --all --prune` 직후 · 원본 `.raw/chalk-traceability-audit-20260915.md`
> 판정 규칙: **근거가 있을 때만 `구현됨`**. 근거를 못 찾으면 `미확인`이다 — *없다*가 아니다.

> 📇 두 저장소 정본의 **요구사항 ID 767개 전수 인덱스** → [[requirement-id-index]] (코드·원문·정의 위치·구현 상태 한 행씩)

## 결과

| 상태 | 건수 | 비율 |
|---|---|---|
| **구현됨** — 코드 + 실행된 검사 근거 | **19** | 25.3% |
| **부분** — 일부 구현 + 남은 인수가 문서에 명시 | **32** | 42.7% |
| **미구현** — 문서·이슈가 직접 미구현/NOT RUN이라 적음 | **17** | 22.7% |
| **미확인** — 어느 쪽 근거도 못 찾음 | **7** | 9.3% |
| 합계 | **75** | |

`CR-*` 89건 중 **정본 ID가 `없음`인 22건**(CR-DEF-08 · CR-GATE-01/02/03/04/07/09 · CR-AUTH-11/12 · CR-RUN-10/11/12 · CR-EDU-07/08 · CR-CAP-10/11 · CR-COM-01~06)은 [[chalk-requirements]] 자신이 "제안 단계에서만 존재"로 표시한 항목이라 대조 대상이 아니다.

> [!key-insight] "부분"이 가장 큰 칸이다 — 42.7%
> 미구현(22.7%)보다 부분(42.7%)이 두 배 가깝다. 그리고 부분 32건은 **세 패턴**으로만 나뉜다.
> ① **"기존 것을 연결했고 새 계약은 남았다"** — ADM-02/03/05/06/08/09/10/11/13 아홉 건. `classroom-admin.md`의 구현 범위 표가 행마다 남은 인수를 적고, 문서가 스스로 *"표의 구현 범위는 전체 ADM 합격을 의미하지 않는다"*고 쓴다.
> ② **"API는 됐고 실기·디자인 인수가 부분"** — DES-04/05/07/12. 2026-09-07 Chromium 실행이 DT-01/02/04/06의 **일부**만 덮었고 **DT-03(상태 주입 대조군)은 전체 실행 기록이 없다**.
> ③ **"판정표가 이미 부분이라 적음"** — AB-01/12/13/17 · HC-04/05/06/07 · INT-ACCESS-02.
> **즉 이 제품의 실제 상태는 "안 만들었다"가 아니라 "연결은 했고 계약을 아직 못 지켰다"**다. [[chalk-target-shape-proposal]]의 *"기계는 다 만들었고 부품이 없다"*와 같은 것을 요구사항 단위로 본 그림이다.

## 구현됨 19건 — 무엇이 실제로 서 있나

| 묶음 | ID |
|---|---|
| 권한·경계 | `BASE-01` · `ARC-01` · `ADM-07` · `AB-03` · `AB-04` · `AB-05` · `MU-02` |
| 저작·버전 불변 | `VER-01` · `SAVE-01` · `CH-01` · `CH-04` |
| 전달·교실 | `RUN-03` · `CLS-02` · `CLS-05` · `ADM-14` |
| 역량 계약 | `HC-01` · `HC-02` · `HC-03` · **`HC-09`** |

`HC-01/02/03`은 `worker/src/lib/measurement-core/`가 근거다 — `capability-models.ts`의 `legacy-seven-assets`가 원 키를 유지하고 *"deliberately no conversion table"*·*"values are never re-mapped"*를 코드 주석으로 박아 두었으며, `interpretation.ts`가 `CONVERSION_KEYS`를 `legacy_conversion`으로 **거절**한다. `HC-09`는 PR **#1066**(`65a15c7`) 머지 + `skills/hain7-report/scripts/test_hain7_signal.py`(일반 호출 거부 · `--latest` 거부 · `--legacy-replay` 명시 재생)가 근거다.

> **7→6을 하지 않는다는 원칙이 문장이 아니라 실행되는 코드다.** [[capability-measurement-module]]·[[six-human-capabilities]]의 "이름 통일이 아니라 버전" 판정이 여기서 집행된다.

## 미구현 17건 — 12건은 이미 열린 이슈 안에 있다

| 묶음 | ID | 이슈 |
|---|---|---|
| **리허설·버전 귀속** | `RUN-01` · `RUN-02` · `VER-02` | **#1012** |
| 저작 심화 | `CH-03` · `CH-05` · `CH-06` · `CH-07` (`CH-02`는 부분) | **#1015** |
| 환경 고정·도구 편입 | `ENV-03` · `ENV-05` · `ENV-06` | **#1017** |
| 요청 큐 | `REQ-02` · `REQ-03` · `REQ-04` · `ADM-12` | **#1016** |
| 도움 방식 | `EDU-02` | #1008 → PR #1028 (**#1036에 막힘**) |
| 교실 운영 | `CLS-04` | ⚠️ 계약이 **명시적으로 불허** — 아래 |
| 역량 연구 | `HC-08` | 연구 절차 대기 (CA-T19 미실행) |

**관문의 재료가 정확히 `RUN-01`·`RUN-02`·`VER-02` 세 줄이고, 셋이 한 이슈(#1012)에 있다.** [[chalk-requirements]] CR-GATE-05/08이 이것이다.

`EDU-02`가 왜 미구현인지가 구체적이다 — `session-design.ts:106`이 단계 키를 **정확히 5개**(`id/title/instructions/hint/acceptance`)로 제한하고 있어 **`help` 키 자체가 main에 없다.** 그걸 추가하는 PR #1028이 결함 #1036에 막혀 있다.

> [!contradiction] `CLS-04` — 요구사항끼리 정면으로 부딪친다
> `CR-OPS-05`(=`CLS-04`)는 **"학생 허용 후 강사가 수정하며 변경 이력·복구 지점을 보존한다"**(P1)를 요구한다.
> 그런데 `classroom-admin.md:55`는 **"자동 관찰·학생 파일 원격 수정·아동 동의·전체 세션 보존은 이 계약으로 허용하지 않는다"**고 못 박는다.
> 미구현이 아니라 **다른 요구사항이 금지한 상태**다. [[chalk-target-shape-proposal]] 충돌 1(*"강사 수정은 막지 말고 증거에서 분리"*)이 바로 이 지점이며, 판정 없이 구현으로 갈 수 없다.

## 미확인 7건 — 근거를 못 찾은 것

| ID | 왜 |
|---|---|
| **`ARC-02`** | 검사 T-22가 기기 E2E이고 **실행 기록 없음**. 게다가 `docs/exit/chalk.md`가 강사 링크를 **`…/console#t=<token>`**로 기록한다 — URL fragment에 토큰이 들어가는 형태이며 *"인증을 URL에 넣지 않는다"*와의 정합이 **판정된 기록이 없다** |
| `ENV-07` | 정의만 있고 지원 OS·아키텍처·최소 앱 버전을 실제 명시한 산출물이 없다. T-23 미실행 |
| `RUN-04` | 학생 기기 지원·접속·AI 가용 확인 경로의 근거 없음 |
| `RUN-05` | 환경 오류 시 작업 보존·복구 안내의 Chalk 경로 근거 없음 |
| `EDU-01` | *"실습마다 학생이 직접 판단할 과제를 안내"*의 구현·검사 근거 없음 |
| **`MR-02`·`MR-03`** | **studio 저장소 전체에 `MR-0*` 문자열 0건** — 아래 |

> [!warning] `MR-02`·`MR-03`은 studio에 대응물이 없다
> 두 ID는 lab `products/lab-web/measurement-retirement.md`의 것이고 studio에는 **요구사항 행도 코드도 없다**(`grep -rn -E "\bMR-0[1-9]\b"` → 0건).
> 같은 폐지 결정의 studio 쪽 대응물은 있다 — **`HC-09`(#1066)**가 HAIN7 폐지를 studio 요구사항으로 받았다. 다만 **`MR-02/03`(과거 기록의 7축 정의 유지 · 방법론 판 바이트 보존)이 `HC-09`에 흡수된 것인지 별개로 남는지는 `미확인`**이다. → [[chalk-requirements]] CR-CAP-13

## 대조 중 드러난 사실 3건 — 요구사항 상태와 별개

> [!warning] ① 쓸 수 있는 traceability 매핑이 사실상 없었다
> `config/traceability.json`의 노드 **89개를 전수 조회했고 이 요구사항 ID가 하나도 없다** — `CH-01`·`ADM-02`·`HC-01`·`AB-03`·`MU-02`·`DES-04`·`VER-01` 전부 미매치이고 문서 경로로도 `classroom-admin.md`·`classroom-design.md`는 **0건**이다. 파일의 `coverage` 필드 자신이 *"Bootstrap scope only; unregistered product areas are not claimed covered."*라고 적는다.
> **이 감사의 근거는 전부 요구사항 문서·코드·테스트에서 직접 찾은 것이다.** 열린 이슈 **#996**이 지적한 사각지대와 같은 종류이며, PR #1024가 하려는 일(원문 hash + ID 고정)이 여기에 해당한다.

**② `capability-model-contract.md`의 상태줄이 코드보다 뒤처졌다.** 머리말은 여전히 *"2026-09-08 · 상태: 제안, 측정 구현 전"*이고 본문도 *"새 rubric·점수·저장 schema가 이미 적용됐다는 뜻이 아니다"*라고 적는데, 실제로는 `measurement-core`(#1042/#1043, 2026-09-14)가 `capability_model` 버전·`supersedes`·conversion 거절을 구현했고 `HC-09` 절이 같은 파일 뒤에 붙었다. **`HC-01/02/03`을 `구현됨`으로 판정한 근거는 문서가 아니라 코드와 테스트다.**

**③ `access-intent-fulfillment-2026-09-08.md`의 HC 판정도 뒤처졌다.** *"새 `capability_model_version`·정의/rubric·actor별 interpretation 저장/내보내기는 미구현"*은 2026-09-08 기준이고, #1042 이후 앞의 둘은 구현됐다. 다만 **actor provenance는 여전히 `user`/`policy` 둘뿐이라 `HC-04`는 부분 그대로**다.

> [!contradiction] `HC-04`·`HC-05`가 계약과 코드에서 다르게 생겼다
> **`HC-04`** — 계약은 사람 발화/선택 · AI 제안 · 정책 기본값 · **강사 개입**을 actor provenance로 구분하라고 요구한다. 코드(`legacy-observation.ts:34`)의 actor는 **`"user" | "policy"` 둘뿐**이다. *"AI가 작성한 문장을 학습자 독립 수행 증거로 저장하지 않는다"*와 [[chalk-target-shape-proposal]] 충돌 1의 판정(*강사가 손댄 부분도 독립 수행 증거에서 제외*)이 **지금 저장 스키마로는 표현될 수 없다.**
> **`HC-05`** — 계약은 `provisional / confirmed / needs_review / null`을, 코드는 `observed / unobserved / insufficient_evidence` + `unreviewed / confirmed / disputed / retracted`를 쓴다. *미관찰을 0으로 채우지 않는* 골격은 성립하지만 **이름·구성이 다르고 정합 판정 기록이 없다.**

## 최신성 검증 — 1차 조사는 clean이었지만 최신은 아니었다

| 확인 | 결과 |
|---|---|
| 1차 조사 시 로컬 main | **origin/main보다 9커밋 뒤** (`ahead 0 / behind 9`) |
| working tree · stash | clean · 없음 (1·2차 모두) |
| 그 9커밋이 `chalk/`를 건드렸나 | **0건** (`git log main..origin/main -- chalk/` 빈 결과) |
| Chalk 요구사항·테스트·ADR·마이그레이션 | **바이트 동일** (sha256 일치) |
| `docs/studio-requirements.md` | 끝에 28줄 추가(`REQ-STUDIO-LOCAL-REVIEW`, `REQ-SS1~4`). **`REQ-M38`은 불변** — AE-09 UNMET 판정 그대로 |
| 2026-09-14 이후 머지된 Chalk PR | **0건** (전부 measurement/review 레인) |
| 운영 health | `c0.0.0-dev+f5939d9` · `w0.0.0-dev+880a13d` — **1차와 동일** |

뒤처져 있던 9커밋은 전부 #1020·#1049 측정·리뷰 레인(PR #1048·#1050·#1058·#1059·#1060·#1061·**#1066**·#1067·#1069)이고, **`chalk/` 영향은 없지만 `HC-09` 하나가 이 감사에 들어왔다.**

> **교훈은 볼트 규약이 이미 적어 둔 것과 같다** — *"오래된 체크아웃은 없는 것보다 나쁘다. 확신을 주기 때문이다."* 이번엔 `gh` 조회가 원격에 직접 질의했기 때문에 이슈·PR 사실은 살았고, **뒤처진 것은 로컬 파일을 읽어 만든 사실뿐**이었다.

## 관련

[[chalk-requirements]] · [[chalk-implementation-status]] · [[chalk]] · [[chalk-target-shape-proposal]] · [[capability-measurement-module]] · [[six-human-capabilities]]

관련: [[requirement-id-index]] — 정본 ID 전수 인덱스(계열·번호 구멍·중복·한쪽에만 있는 ID)
