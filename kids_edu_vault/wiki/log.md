---
type: meta
title: "Log"
created: 2026-04-12
updated: 2026-09-15
tags:
  - meta/log
---

# Log

볼트 변경 이력. 최신 항목이 위.

---

## [2026-09-15] spec | 요구사항 ID 전수 인덱스 — 767개 ID, 한 행씩
- Type: spec (신규) · 요청자 [[jay-lee]]: *"lab에 코드 기반으로 요구사항이 정의돼 있으니, 위키에서도 그 코드와 함께 빠짐없이 모든 코드에 해당하는 요구사항을 확인할 수 있게 해달라"*
- Page created: [[requirement-id-index]] (`wiki/specs/`, 약 259KB / 표 행 704개)
- Sources: 🆕 `.raw/lab-requirement-id-inventory-20260915.md` (lab 전수 인벤토리, 625정의 / 546고유 / 62계열) + studio 정본 직접 추출(`04f03d0`) + [[chalk-requirement-coverage-audit]](구현 상태 75건)
- 규칙: **구현 상태·근거는 감사된 ID에만 채우고 나머지는 비웠다.** `—`는 "미구현"이 아니라 **"아직 안 봤다"**임을 페이지 머리에 못 박았다. 원문은 230자에서 문장 경계 절단(아카이브 150자) + **정의 위치 `파일:라인`**을 실어 정확한 인수 기준은 정본에서 읽게 했다
- 총계: **고유 767** = studio 497(요구사항 303 + 행동 계약 190 + 명명 계약 3 + Intent 4 중복 제외) + Intent 21 + lab 546 (교집합 제외 후 합)
- ★ **번호 구멍 0건.** 두 저장소 62계열 전부가 1번부터 최대 번호까지 연속이다 — `XX-01 XX-02 XX-04` 식 누락은 없다
- ⚠️ **중복 정의 진짜 충돌 1건 — `REQ-M30`이 두 개다.** `studio-requirements.md:299`("매칭된 탭을 운전 대상으로 고정", #523)와 `:302`("능력 상실은 보여야 한다 — 무성 폴백 금지", #476)가 **서로 다른 요구사항인데 같은 코드**를 쓴다. `REQ-M` 계열은 행 43 / 최대 번호 42. **개번 판정 필요**
- ⚠️ **같은 내용의 두 벌 79건** — lab `studio-prd/catalog.json` ↔ `requirements.json`. 지금은 원문 불일치 0건이지만 **한쪽만 갱신되면 즉시 갈라진다**
- ★ **미러가 양방향으로 벌어져 있다** — lab 미러는 `hypeproof-studio@2d96413`(9/14) 스냅샷이라 **`HC-09`(HAIN7 폐지)와 `SS-01~14`(9/15 신규 `session-sync.md`)가 없다.** 반대로 **`IC-01~07`(독립 강의 개설 계약)은 lab 미러에만 있고 studio main에는 없다** — 열린 PR #1024·이슈 #1006 안에만 있다. **정본 미러가 아직 머지되지 않은 계약을 이미 담고 있다**
- ⛔ **양쪽 어디에도 정의가 없는데 참조되는 ID 4건** — `MC-07`·`MC-21`·`MC-27`·`MC-34`. `requirements/local-task-review.md`가 *"MC-07, MC-21–25, MC-27–32, MC-34–35의 한정 구현"*이라 적지만 그 ID는 **제안 상태인 #1025 계약**의 것이다. **지금 구현 중인 슬라이스가 읽을 수 없는 코드를 참조한다**
- ⚠️ **Intent 계열이 두 저장소로 쪼개져 있다** — `INT-ACCESS-*`는 lab, `INT-AE-*`·`INT-US-*`는 studio `docs/design/`. 같은 접두사인데 정본 저장소가 다르고 **어디가 Intent의 집인지 판정 기록이 없다**
- 경계 선언: 테스트 시나리오 ID(`T-*`·`AT-*`·`DT-*`·`AE-T*`·`VO-T*`·`US-T*`·`CA-T*`·`EFF-T*`·`MR-T*`), 아카이브 작업 단계(`S-1~320` 등), 운영 레지스트리(`KI-*`·`BUG-*`), 법률·헌법 검토 지적(`A-*`·`Z-*`), 오탐(`GPT-4`·`UTF-8`·`K-12`)은 **건수를 적고 제외**했다 — 빠뜨린 게 아니라 다른 층이라는 것을 페이지에서 확인할 수 있게
- 내 1차 추출에서 **`TUX-A11Y-01~04` 4건과 `TUX-COPY-01`이 빠져 있었다** — lab 인벤토리의 문서별 건수(55)와 대조해 잡았다. ID 정규식이 `A11Y`처럼 **숫자를 품은 접두사 조각**을 못 받던 버그. 교차 대조가 실제로 누락을 잡아냈다
- Pages updated: [[chalk-requirements]] · [[chalk-implementation-status]] · [[chalk-requirement-coverage-audit]] · [[chalk]] · [[specs/_index]] · [[index]] · [[hot]] · [[log]] · `.raw/.manifest.json`

---

## [2026-09-15] ingest | Chalk 3부작 완성 — 전수 감사로 "부분 42.7%"가 드러났다
- Type: re-ingest (1건 갱신 반영) + ingest (1건 신규)
- Sources: `.raw/chalk-requirements-20260915.md`(2차 갱신판 — 이미 직전 ingest에서 반영 완료, 재확인 시 해시 동일) · 🆕 `.raw/chalk-traceability-audit-20260915.md`(studio 세션 전수 감사) · `.raw/chalk-studio-issues-prs-20260915.md`(헤더 3줄 갱신 = 기준 커밋 `4195faa` → `04f03d0`)
- Pages created: [[chalk-requirement-coverage-audit]] (`wiki/validation/`)
- ⭐ **판정: `wiki/validation/`.** 요구사항 페이지도 현황 페이지도 아니다 — *요구사항 단위로 반영됐나*를 묻는 **검증 결과**이고, 세 페이지가 3부작으로 선다: **필요한 것(specs) / 되어 있는 것(specs) / 대조 결과(validation)**
- ★ **가장 큰 칸은 미구현이 아니라 "부분" 42.7%다** (구현 19 · 부분 32 · 미구현 17 · 미확인 7 / 75개). 이 제품의 실제 상태는 *안 만들었다*가 아니라 **"연결은 했고 계약을 아직 못 지켰다"**다 — `classroom-admin.md`의 구현 범위 표가 행마다 남은 인수를 적고 문서가 스스로 *"표의 구현 범위는 전체 ADM 합격을 의미하지 않는다"*고 쓴다. [[chalk-target-shape-proposal]]의 *"기계는 다 만들었고 부품이 없다"*를 요구사항 단위로 본 그림
- ★ **미구현 17건 중 12건이 이미 열린 실행 단위 4개(#1012·#1015·#1016·#1017) 안에 있다.** 관문 재료 세 줄(`RUN-01`·`RUN-02`·`VER-02`)이 전부 **#1012** 하나에 모여 있다 — 관문을 세우는 일이 흩어진 과제가 아니라 **한 이슈**라는 뜻
- ★ **7→6을 하지 않는다는 원칙이 문장이 아니라 코드다** — `measurement-core/capability-models.ts`가 *"deliberately no conversion table"*·*"values are never re-mapped"*를 주석으로 박고 `interpretation.ts`가 `CONVERSION_KEYS`를 `legacy_conversion`으로 거절한다. `HC-01/02/03/09` 모두 `구현됨`. `HC-09`는 PR **#1066** 머지 + `test_hain7_signal.py`가 근거
- ⚠️ **`CLS-04`는 미구현이 아니라 요구사항끼리 부딪친 상태다** — `CLS-04`(학생 허용 후 강사 수정, P1) ↔ `classroom-admin.md:55`("학생 파일 원격 수정은 이 계약으로 허용하지 않는다"). [[chalk-target-shape-proposal]] 충돌 1이 정확히 이 자리이며 **판정 없이 구현으로 갈 수 없다**
- ⚠️ **`HC-04`의 actor가 `user|policy` 둘뿐이다** — AI 제안·강사 개입을 구분하는 칸이 저장 스키마에 없어 *"강사가 손댄 부분도 독립 수행 증거에서 제외"*(CR-CAP-10)가 **지금 스키마로는 표현될 수 없다.** `HC-05`도 상태 집합 이름·구성이 계약과 다르고 정합 판정 기록이 없다
- ⚠️ **쓸 수 있는 traceability 매핑이 없었다** — `config/traceability.json` 노드 89개 전수 조회에 Chalk 요구사항 ID **0건**. 파일 자신이 *"Bootstrap scope only"*라 적는다(이슈 #996의 사각지대). 감사 근거는 전부 요구사항 문서·코드·테스트에서 직접 찾은 것
- ⚠️ **1차 조사는 clean이었지만 최신이 아니었다** — 로컬 main이 origin/main보다 **9커밋 뒤**(ahead 0). fast-forward 후 `04f03d0`. 다만 그 9커밋은 `chalk/`를 0건 건드렸고 Chalk 요구사항·테스트·ADR·마이그레이션은 **바이트 동일**, 운영 health도 동일 → **기존 사실 유효**. 예외 1건이 `HC-09` 신설. 볼트 규약의 *"오래된 체크아웃은 없는 것보다 나쁘다"*가 그대로 적용됐고, 이번엔 `gh`가 원격 직접 질의였기 때문에 이슈·PR 사실만 살았다
- **20% 가설 표기를 전파했다** — [[record-issuance-model]](정본 개념) + [[jeon-sangyeol-meeting-20260916]](**9/16 자리 자료** — 확정 조건처럼 말하지 않도록 경고). 나머지 인용 3건([[jiwoong-kim]]·[[2026-09-14-weekly-on-hypeproof]]·[[park-junghyun]])은 회의 발언 인용이라 원문 그대로 둠
- Pages updated: [[chalk-requirements]](§0 반영 현황 + `CLS-04` 충돌 행 + `HC-04/05` 불일치 + `MR-02/03` 미확인) · [[chalk-implementation-status]](기준 커밋 `04f03d0` + 9커밋 재검증 + §1.5 + 열린 질문 3건) · [[chalk]](전수 감사 분포) · [[record-issuance-model]] · [[jeon-sangyeol-meeting-20260916]] · [[index]] · [[hot]] · [[log]] · `.raw/.manifest.json`

---

## [2026-09-15] ingest | Chalk 짝 문서 2벌 — 요구사항(CR-* 89건)과 구현 현황(4195faa)
- Type: ingest (2 sources, paired)
- Sources: `.raw/chalk-requirements-20260915.md` (lab 세션) · `.raw/chalk-studio-issues-prs-20260915.md` (studio 세션)
- 판정: **`wiki/` 트리.** 지금 굴러가는 제품 실행 맥락이고 3년 뒤 다른 강의를 만들 때 볼 문서가 아니다. `curriculum_wiki/`로 가지 않는다.
- 기존 페이지를 새로 만들지 않고 이어 붙였다 — [[chalk]]·[[chalk-target-shape-proposal]]·[[capability-measurement-module]]·[[2026-09-14-weekly-on-hypeproof]]. 새 페이지는 **성격이 다른 두 벌**(요구사항 정본 정리 / 시점 현황 기록)이라 각각 세웠다.
- Pages created: [[chalk-requirements]] (`CR-*` 89건 / 9묶음, 정본 15문서 매핑, 개념 사전 8항, 근거 지도 11시점) · [[chalk-implementation-status]] (기준 커밋 `4195faa`, 화면 10개·D1 3테이블·테스트 16종, 이슈·PR 전수, 차단 체인 7줄)
- Key insight ①: ⭐ **관문이 필요하다는 합의는 있고, 통과시키는 규칙은 어디에도 없다.** 합격선의 **주체·항목·임계값·재판정 절차·근거 공개 범위가 전부 `미확인`**이다. 그리고 `HC-08`(연구 construct audit를 통과한 정의만 쓴다) 때문에 **역량 기반 합격선은 연구가 끝나기 전에 세울 수 없다** → 지금 세울 수 있는 관문은 역량이 아니라 **계약 준수** 축
- Key insight ②: ⭐ **관문의 재료 3개가 전부 `planned` 리터럴이다** — 리허설 증거·설정 핀·활성화. 확정 문서가 `rehearsal:not_run`·`activated:false`를 **값으로** 들고 있고 ADR 0004가 *"Freezing stores an unverified snapshot, not a deployable class"*라고 적는다. [[chalk-target-shape-proposal]]의 "확정에 내용 검사가 없다"는 판정이 원문으로 확증됐다
- Key insight ③: **머지된 것과 강사가 보는 것이 다르다** — 운영 Chalk `f5939d9`는 main보다 **PR 4건**(#813·#839·#866·#1027), Service는 **28커밋** 뒤. 볼트의 "구현됨(active)" 판정은 main 기준으로 맞지만 운영 기준으로는 아니다. **의도된 보류인지 누락인지 결정 기록이 없다**
- Key insight ④: **CR-DEF-04(Service가 권한·토큰 서명 소유)는 요구사항이기 전에 이미 구조다** — `chalk/src/index.ts` 헤더 주석이 Chalk에 상태 쓰기·토큰 서명이 **없음**을 명시하고 drift lock이 단언한다. 7층 그림의 "브릿지 구현됨"이 정확했다
- 충돌·모순 5건 (§아래 페이지에 `[!contradiction]`으로 기록)
  1. **`status: active` ↔ 라인업 정본 "제안 단계·대외 언급 금지"** — 층이 다르다(코드가 있다 / 팔 수 있다고 말하지 않는다). 대외 문서·IR에서 완료 제품으로 쓰면 정본 위반 → [[chalk-requirements]] §1
  2. **session-design "소비자 없음" ↔ #740 이후 소비자 3곳** (`/learn`·Studio 수업 패널·두 LLM 경로). 저장소 문서가 한 단계 낡았고, 이것이 **스키마 소유 결정의 전제를 바꾼다** → [[chalk-implementation-status]] §8
  3. **여섯 역량의 확정 여부** — #1049 본문은 *"versioned candidate definitions"* + "확정 리브랜드 아님"이라 명시. [[hot]]·[[six-human-capabilities]]의 "2026-09-13 제품 채택"이라는 표현보다 저장소가 더 보수적이다
  4. **요구사항 총건수 3종** — 289(정본 표기) / 296(PR #1024, 12문서) / 284(9-14 JY 직접 추출). 경계 처리 차이. **인용 시 289 + 출처 병기**로 통일
  5. **건수 표기 오류** — 라우터가 "9묶음 66건"이라 했으나 실제 `CR-*`는 **89건**이다(1차 87 → 2차 재검증에서 `HC-09` 반영으로 CR-CAP-12·13 추가). 66은 PR #1024의 시나리오 수(79/79 → 66개 시나리오)와 섞인 것으로 보인다
- 🆕 **ingest 중 원본이 2차 재검증판으로 갱신됐다** — `hypeprooflab@5c0a0859`·`hypeproof-studio@04f03d0` 기준으로 다시 훑어 3건이 들어왔다: **`HC-09` 신설(HAIN7 폐지)** · lab **`measurement-retirement.md`(MR-01~04)** · **9/14 회의 결과부 게시**(확정/가설/미결 구분). 세 건 모두 페이지에 반영. 파생 판정 3개 — ① **파트너 수수료 20%는 가설이며 합의된 딜 조건이 아니다**(결과부 명시, [[record-issuance-model]] 인용 주의) ② **제품 오너는 확정이나 `PRODUCT-LINEUP.md`가 9/11 이후 미갱신** — 정본 표기 갱신이 남은 작업 ③ **저장소 분리는 "사용자 전달 경험을 먼저 정의한 뒤 결정"**으로 순서가 못 박혔다 (PR #1005 요청이 여기 걸린다)
- ⚠️ **CR-CAP-11 표기 두 갈래** — 볼트는 측정 모듈을 「Studio와 **Chalk** 양쪽 임포트」로 기록했는데 lab 회의 결과부는 「Studio·Claude Code·Codex」만 적고 **Chalk를 임포트 대상에 넣지 않았다**(`미확인`). [[capability-measurement-module]]에 기록
- ⚠️ 지금 강사에게 손상을 주는 결함: **#1036** — `/authoring` 편집기가 **화면에 없는 단계 키를 저장 시 조용히 지운다.** 제목만 고쳐도 `steps[].help`가 사라져 확정 수업이 도움 제안을 못 싣는다. PR #1028이 여기 막혀 있다
- Pages updated: [[chalk]](2026-09-15절 신설 + 미결 5건 상태 갱신) · [[chalk-target-shape-proposal]](확증 4건 / 갱신 필요 2건 / 미다룬 축 1건) · [[capability-measurement-module]](#1020·#1049 + HC-08 제약) · [[2026-09-14-weekly-on-hypeproof]](오너 조건의 착수 기록) · [[specs/_index]] · [[index]] · [[hot]] · [[log]] · `.raw/.manifest.json`

---

## [2026-09-15] fix | 9/15 vs 9/16 혼동 해소 — 전상열 미팅은 9/16, 9/15는 덱 기한
- Type: correction (날짜·명명)
- 계기: JY가 *"wiki에 15일 16일 관련 혼동이 있었던 것 같은데?"* — 직전 ingest가 플래그만 걸고 남겨 둔 건.
- 판정: **8/25~9/6 볼트 기록은 틀리지 않았다.** 원문 3회 연속 "9월 15일 IR"이었고(8/25 요약·8/31 요약·9/6 축어록 *"이번 15일 날 9월 15일 날"*), **9/14 회의에서 날짜가 옮겨졌다** — 지웅: *"16일 날 내일 모레 미팅을 하기로 했고요."* 9/14가 월요일이므로 **9/16(수)**.
- ⭐ **날짜만 바뀐 게 아니라 자리의 성격이 바뀌었다** — *"간단히 식사를 하고 그다음에 카페에서 대화를 나누는 (…) 어디 앞에서 스크린 띄우고 발표한 자리는 아니에요."* 그래서 "IR"이라는 이름 자체가 부정확했다. [[jay-lee]]의 "슬라이드 프레임에 갇히지 말 것 · 이미지 · 소셜 캐피탈" 피드백이 이 성격 변화와 같은 것을 가리킨다.
- 두 번째: **9/15는 사라진 날짜가 아니라 다른 마감이 됐다** — [[jiwoong-kim]]의 덱 최종 수정 기한. 9/16은 R&R·KPI 회신 기한([[roles-kpi-proposal-20260914]], 24:00)과 겹친다. **하루에 마감 둘 + 미팅 하나.**
- 부수 오류 1건: `ir-20260915-plan`과 [[weekly-on-hypeproof-20260914-source]]가 9/16을 **"(화)"**로 적었다. 9/16은 **수요일**이다.
- 조치: `wiki/deliverables/ir-20260915-plan.md` → **`jeon-sangyeol-meeting-20260916.md`** 리네임(`aliases`로 구 이름 보존), 인바운드 위키링크 **26개 파일** 치환, `due: 2026-09-16`, [[hot]]·[[index]]·[[deliverables/_index]]·[[2026-09-14-weekly-on-hypeproof]]·[[weekly-on-hypeproof-20260914-source]]·[[jiwoong-kim]]·[[startup-hot]]의 "확정 필요" 플래그 해소.
- ⚠️ 남은 것: `ir-mentor-candidates-20260915` · `why-hypeproof-for-teen-startup-ir-20260915` · `ir-20260915-pricing-evidence-audit` **3건은 파일명에 20260915를 그대로 둔다** — 9/16 미팅이 아니라 *그 미팅용 덱*에 대한 문서이고 리네임 이득이 링크 치환 비용보다 작다. 날짜로 검색할 때 걸릴 수 있다는 점만 기록.
- Pages updated: [[jeon-sangyeol-meeting-20260916]](리네임+정정), [[hot]], [[index]], [[deliverables/_index]], [[2026-09-14-weekly-on-hypeproof]], [[weekly-on-hypeproof-20260914-source]], [[jiwoong-kim]], [[startup-hot]], [[log]] + 링크 치환 18건

---

## [2026-09-14] save | Chalk 완성형 제안 — 관문(gateway)으로 정의
- Type: deliverable
- Location: `wiki/deliverables/chalk-target-shape-proposal.md`
- 산출물: `/Users/jj_home/Git/HypeProof/_worklog/chalk-target-shape-20260914.html` + `-script.md` (**볼트 밖**. 이 저장소는 공개이고 문서에 타임라인·미결·조직 판단이 있어 이동)
- From: 지웅의 주말 과제 3분류 중 ③ 프로덕트에 대한 JY 답변. 멤버 페이지 요구사항 289건 · `curriculum_wiki/` 48건 · Studio Chalk PR 이력(09-05~09-14) 세 출처를 겹쳐 본 결과
- Key insight: ⭐ **서로 참조한 적 없는 두 자료가 8쌍에서 같은 말을 한다.** 특히 `HC-04`("AI가 작성한 문장을 학습자 독립 수행 증거로 저장하지 않는다")와 JY의 대행 금지는 **판단 근거까지 일치** — 누가 썼는지가 증거의 성립 조건. 그러니 교육 원칙은 제품에 *이식*할 게 아니라 **대응표로 맞추면 된다**. `HC-01`이 이름 변경을 금지하므로 통일이 아니라 매핑.
- 두 번째: ⭐ **양쪽이 똑같이 비어 있다.** 제품은 검수된 실행 템플릿 0개라 독립 강의가 안 열리고, JY 자산은 수업 부품 0건·자동 검사 0/12. 두 저장소가 서로 모른 채 **"기계는 다 만들었고 부품이 없다"**는 같은 상태에 도달했다 — *무엇을 부품으로 인정할지를 아무도 정하지 않았다.*
- 세 번째: **Chalk 요구사항 53건의 범위는 "치과의사 대상 홈페이지 수업"이다** (문서 첫 줄). 아동·청소년을 전제한 적이 없으므로 [[edu-constitution]] 2층 분리는 새 구조가 아니라 **현상 기술**이다.
- 네 번째: **확정(freeze)에 내용 검사가 없다는 것을 문서가 스스로 적고 있다** — *"Freezing stores an unverified snapshot, not a deployable class."* 차단 장치 자체는 여럿 있으나(`VER-02` 합격 무효화, `US-14` 승격 차단, fail-closed 기본값) **전부 형식·권한 검사**다.
- 판정: **Chalk는 만드는 도구이기 전에 통과시키는 관문.** [[chalk]]의 기존 "생성기" 정의를 버리지 않고 뒤로 미룬다 — 생성기는 재료가 쌓여야 작동하고 재료는 수업이 돌아야 쌓이므로 **관문 → 수업 축적 → 생성기**. 관문 개념은 [[jinyong-shin]]이 8/31에 말한 게이트웨이 역할을 **확정 시점**이라는 구현 자리에 연결한 것이다.
- ⚠️ 미반영: [[six-human-capabilities]](2026-09-13 제품 채택)를 모르고 `HC-01`의 "일곱 개 고정"만 보고 썼다. **판정 자체는 유효하다** — `HC-02`·`HC-06`이 정확히 그 7→6 전환을 규율하는 조항이므로 "이름 안 바꾸고 새 버전으로"가 실제로 일어난 일이다. 다만 충돌 2 서술이 한 단계 낡았다.
- Pages created: [[chalk-target-shape-proposal]]
- Pages updated: [[index]], [[deliverables/_index]], [[hot]], [[log]]

---

## [2026-09-14] ingest | Weekly on HypeProof 2026-09-14 — "우리가 만들어 놓고 우리도 아무도 안 쓴다"
- Source: `.raw/meeting_notes/Weekly on HypeProof - 2026_09_14 21_53 KST - Notes by Gemini.md` (요약본, 커밋) + `(1)` 스크립트본 1,204줄 (gitignore)
- Summary: [[weekly-on-hypeproof-20260914-source]]
- Pages created: [[2026-09-14-weekly-on-hypeproof]], [[weekly-on-hypeproof-20260914-source]], [[internal-productization]]
- Pages updated: [[sixteen-essence]], [[six-human-capabilities]], [[capability-measurement-module]], [[chalk]], [[sediment]], [[hypeproof-studio]], [[record-issuance-model]], [[roles-kpi-proposal-20260914]], [[jeon-sangyeol-meeting-20260916]], [[dental-fullday-website-workshop]], [[2026-09-14-weekly-prep]], [[tj]], [[jinyong-shin]], [[jiwoong-kim]], [[bongho-tae]], [[minhan-cho]], [[jehyeong]], [[comms/_index]], [[sources/_index]], [[index]], [[hot]], [[log]]
- 계기: 사전자료([[2026-09-14-weekly-prep]])가 *"회의록이 나오면 사전자료는 보존하고 별도로 추가한다"*고 지시한 대로, 실제 회의록을 별도 페이지로 만들었다. **사전자료와 회의록의 온도 차가 이 ingest의 핵심**이다 — 사전자료가 "완료 증거가 없다"로 에둘러 쓴 것을 회의에서는 "아무도 안 쓴다"로 말했다.
- Key insight: ⭐ **[[jay-lee]]가 미국에서 Studio를 직접 결제해 쓰고 내린 진단이 회의 전체를 끌었다.** *"스튜디오를 우리는 지금 아무도 안 쓴다"* · *"체험판을 다 빌드했음에도 그 사람을 통해 우리가 원하는 것을 전달할 수 없었다 — **무엇을 깨닫게 해야 하는지 나조차도 모르겠더라**"* · *"우리는 **바이브 코딩하는 사람들이랑 똑같았어요**"*. 처방이 [[internal-productization]]이다 — **우리가 먼저 쓰고 먼저 측정한다.**
- 두 번째: ⚠️ **[[sixteen-essence]]의 근거가 없다고 저자가 직접 밝혔다.** *"이거 내가 그냥 16개 여기서 주워 와 가지고… 노정석 대표님 유튜브에 나오시는 그 흰머리 아저씨 분, 그분이 생각하는 16개 에셋을 그냥 따온 건데, **철학적으로 과학적으로 논거가 좀 없어 보인다**."* 볼트는 이것을 **"HypeProof Lab의 핵심 교육 IP"**로 기록해 왔다. 양쪽에 `[!contradiction]`을 달았다. **16 → 7 → 6의 궤적이 개수를 줄인 역사가 아니라 근거를 붙여 온 역사**로 다시 읽힌다 — 그래서 아레나 연구 에픽이 [[minhan-cho]]·[[bongho-tae]]에게 어사인됐다.
- 세 번째: ⭐ **[[chalk]]에 오너가 생겼다 — [[jinyong-shin]]이 자청했다.** 그리고 같은 회의 1시간 전 본인이 Chalk에 빠진 축을 지목했다: *"강의를 우리가 아니라 **누군가 한다고 했을 때 그 자격을 어떻게 줄 거냐**는 측정 축이 빠져 있었다. **초크에 게이트 역할을 부여하면** 좋지 않을까."* 8/31 게이트웨이론 → 9/14 측정 모듈 → Chalk 오너십이 한 줄로 이어진다. 조건은 **요구사항 매핑 페이지 트래킹**이고, 다음 Weekly 첫 아젠다다. Jay의 단서도 그대로 남겼다 — *"너는 개발을 할 수 있는데 안 한 거잖아."*
- 네 번째: ⭐ **[[sediment]]가 왜 멈췄는지 밝혀졌다.** *"내가 세디먼트를 만들었던 이유는 사실 그거(내부 제품화)였는데, **나조차도 잊어먹고 있었고, 프로덕트 오너가 지금 아무도 없죠.** 내가 그거를 진용이한테 줬지만… **한번 내 미스지.**"* 직전 ingest가 "설계·대외 제안에는 있는데 구현이 없다"고 적었던 것의 답이다 — **방치가 아니라 목적 상실**이었다. 다만 되살아난 목적의 실행이 [[capability-measurement-module]]이라는 **별개 모듈**로 가고 있어 Sediment와의 관계는 미정리다.
- ✅ **충돌 하나가 해소됐다**: [[tj]] 역할 누락. TJ가 직접 물었고 Jay가 **사과**했다 — *"일부러 그런 건 아니고."* 덧붙인 말이 날카롭다: ***"태진이가 제일 많이 측정이 돼야 된다."*** 브랜드·콘텐츠와 법무·IP를 제외하고 **하고 싶은 역할을 직접 고르라**는 것. 부수로 [[bongho-tae]]가 초안에서 빠졌던 이유도 나왔다 — **"뭘 하고 있는지 리포트가 안 돼서"**. 볼트가 "이동"으로 읽었던 것은 **제외 후 재배치**였다.
- 정정 1건: **"5단계 커리큘럼"은 강의 5개가 아니었다.** [[jay-lee]]: *"다섯 개를 하라고 한 게 아니라 **수강생의 페르소나를 다섯 단계로 정의하라**고 한 거고요."* 그리고 **이탈자 KPI**가 붙었다 — *"그만두는 사람들에 대한 KPI도 있어야 돼. **그때는 AX 케어로 이어져야 된다 — AX 케어는 홈페이지 빌딩**이지."* [[dental-fullday-website-workshop]] 갱신.
- ⚠️ **날짜**: [[jeon-sangyeol]] 대표 미팅이 축어록상 **9/16**이다(*"16일 내일모레"*). 볼트는 8/25부터 `ir-20260915-plan`으로 9/15를 써 왔다. R&R 회신 기한(9/16 24:00)과 같은 날이 된다. ✅ **2026-09-15 해소** → 아래 [2026-09-15] 항목.
- ⚠️ **요약본 오탈자**: Gemini가 채널 파트너 결정을 *"…지향하기로 결정했다"*로 적었으나 같은 문서 제목은 **"도입 보류"**이고 축어록은 *"채널 얘기할 수준은 아직 아니거든"*이다. **"지양"의 오기**.
- ⏰ 기한: **R&R 회신 9/16(수) 24:00** — 역할 수용 여부 + 위클리 보고 양식 의견. [[tj]]는 희망 역할 제안. [[jiwoong-kim]]은 9/15까지 덱 최종 수정(킬러 센텐스·유기적 연결 다이어그램). [[jesse-kim]] 해커톤 초안 금주 말.
- 미확인: Jay가 쓴 **논문급 문서·칼럼** 실물 · **"아레나"**의 의미(⚠️ **R&R의 음성 오인식** 가능성이 높은데 요약본이 "아레나 연구"로 그대로 옮겼다) · 16 Assets 원 출처 인물 · 레포 분리 시점 · 데모데이 12~1월 가능 여부(질의만) · How We Work의 맥락관리 담당이 신제형인지 광현인지(포털 표기와 어긋남)

## [2026-09-14] ingest | HypeProof Members 포털 3페이지 — 7 Assets가 6개로 재구성됐다
- Source: `.raw/members/how-we-work.md` · `studio-features.md` · `meetings-2026-09-14.md` (멤버 전용 OAuth 게이트. JY가 로그인 상태에서 추출)
- Summary: [[members-portal-20260914-source]]
- Pages created: [[six-human-capabilities]], [[hypeproof-operating-model]], [[ai-crew-personas]], [[capability-measurement-module]], [[roles-kpi-proposal-20260914]], [[2026-09-14-weekly-prep]], [[members-portal-20260914-source]]
- Pages updated: [[chalk]], [[hypeproof-studio]], [[sediment]], [[seven-ai-native-assets-original]], [[jehyeong]], [[jesse-kim]], [[jiwoong-kim]], [[jinyong-shin]], [[bongho-tae]], [[minhan-cho]], [[jay-lee]], [[tj]], [[comms/_index]], [[sources/_index]], [[index]], [[hot]], [[log]]
- 계기: 익명 fetch가 `NEXT_REDIRECT → /auth/signin`으로 끊겨 브라우저 경로를 시도했고, 최종적으로 JY가 본문을 `.raw/members/`에 넣었다. **포털은 정본이 아니라 정본을 연결하는 읽기 창구**임을 문서 스스로 선언하므로 여기 정리한 것도 미러다.
- Key insight: ⭐ **7 Assets가 6개 역량으로 재구성됐다** (2026-09-13 제품 채택) → [[six-human-capabilities]]. 산술은 **Intent+Context = Framing** 하나뿐이고 나머지 셋은 이름이 아니라 **관점이 좁혀졌다** — Taste→Judgment(미감 → 설명 가능한 선택 근거), Delegate→Orchestrate(맡기기 → 권한·검토지점 설계), Iterate→Adapt(반복 → 전략 변경). 이유가 우리 볼트의 기존 진단과 정확히 맞물린다: **"몇 번 위임하거나 반복했는지만으로는 역량을 설명할 수 없다."** [[asset-pressure-map]]이 Context·Iterate만 "재정의 필요"로 판정했던 그 자리다. **AI가 흡수 중인 구간이 곧 측정이 무너지는 구간**이라는 읽기가 두 문서에서 독립적으로 나왔다.
- 두 번째: 모델의 진짜 내용은 표가 아니라 **"이것만으로는 부족" 열**이다 — 에이전트 수·도구 호출 수·재시도 횟수·AI의 통과 선언·제출 버튼 클릭. **전부 자동 집계가 가능한 지표이고 전부 기각됐다.** 이것이 [[record-issuance-model]]에 직접 걸린다: 9/6에 [[jiwoong-kim]]이 제시한 대시보드 매트릭(제작자·사용자·이번 주 사용자·마지막 갱신)은 **전부 활동량**이고 여기서 기각된 종류다. 간극을 메우는 물건이 [[capability-measurement-module]]인데 **실사용 0건**이다.
- 세 번째: ⚠️ **[[chalk]]가 `proposal`이 아니었다.** 볼트는 8/31 이후 "아이디어 단계"로 기록해 왔는데, 기능 페이지에 **현재 기능 3개**가 요구사항 원문·검증 기록과 함께 있고 수업 만들기 요구사항만 53개다. `status: active`로 정정. 다만 [[jesse-kim]]이 "크립토나이트"라 부른 **가격 방어 층(품질 게이트·학생 리허설·회고 루프)은 전부 로드맵**이다 — **킥은 아직 안 나왔다.**
- 네 번째: **운영 모델이 처음 문서화됐다** → [[hypeproof-operating-model]]. 6단계 흐름·9역할·RACI 19행·주간 루프·6원칙. 구조의 핵심은 **제품의 논리를 조직에 적용한 것**이다 — 6단계 작업 흐름과 [[six-human-capabilities]]가 같은 뼈대다. 조직 형태는 **기여 기반**이며 "Jay가 사업의 위험과 실행 공백을 맡는다"고 명시한다. ⚠️ 9역할 중 **5개가 Jay**이고 제품 3종 중 2종의 리드가 공석이다.
- 다섯 번째: **[[ai-crew-personas]]** 5종(Scout·Compass·Forge·Lens·Keeper)의 설계 핵심은 능력이 아니라 **월권 차단**이다 — "고객 한 명의 반응을 시장 전체로 확대하지 않는다", "자체 테스트를 고객 성과로 보고하지 않는다", "기준을 낮춰 통과시키지 않는다". **Keeper는 우리 `wiki-lint`+`hot`/`log`와 거의 같은 일**을 한다. 우리가 앞선 것은 `[!contradiction]` 기록 형식이고, 뒤진 것은 **재확인 기한(TTL) 필드가 없다**는 점이다.
- ✅ **미결 하나가 닫혔다**: 8/31부터 열려 있던 **"회의록의 신제형 = [[jehyeong]]인가"**. How We Work가 "제형 — 홈페이지 만들기 강의"로 배정하고 10/7 담당으로 명시한다.
- ⚠️ 충돌 4건을 `[!contradiction]`으로 달았다: ①정본은 여전히 7 Assets ↔ 신규 제품은 6 (**두 층 병존**, 언제 합쳐지는지 미결) ②[[jay-lee]]가 9/6에 "AI가 못 하는 건 **테이스트와 오너십**"이라 한 지 일주일 만에 **Taste가 Judgment로 재정의**됐다 — 가장 인간적이라 지목한 자산이 가장 먼저 조작적 정의로 끌려 나왔다 ③[[chalk]] 상태 오기 ④**[[tj]]에게 배정된 역할이 없다** (9/6에 덱을 발표하고 액션을 받은 사람인데 두 표 모두에 없다)
- ⛔ [[sediment]]: **9/7~9/14 main 커밋·머지 PR 0건.** 그런데 주간 루프 5단계·[[bitree]] 공동 BM 제안·제품 라인업 **세 곳이 Sediment를 전제한다.** 설계와 대외 제안에는 있는데 구현이 멈춰 있고, 볼트·포털·Sediment 중 "팀의 기억"을 누가 맡는지도 미정이다.
- ⏰ 액션: **9/16(수)까지 전원 R&R·KPI 회신** → [[roles-kpi-proposal-20260914]]. 무응답은 수락으로 처리되지 않는다.
- ⚠️ 숫자: **SK 건 입금 미확인**(딜 원장 사실확인일 9/5). [[ir-20260915-pricing-evidence-audit]]의 정산 자물쇠와 직결된다.
- 미확인: **광현**의 한글 표기와 [[jesse-kim]] 동일인 여부(역할·9/6 호명으로 강한 정황) · [[tj]] 누락이 의도인지 · 변호사 채널 담당이 표에서 사라진 이유 · `roadmap.strategy.json`·`deals.yaml`·`ROLES.md` 원문 미확보 · Studio 공개 배포 상태

## [2026-09-14] ingest | Weekly on HypeProof 2026-09-06 — 9/15 덱 리허설과 치과 선회
- Source: `.raw/meeting_notes/Weekly on HypeProof - 2026_09_06 23_04 KST - Notes by Gemini.md` (요약본, 커밋) + 같은 이름의 `(1)` 스크립트본 (954줄, **gitignore·로컬 보관**)
- Summary: [[weekly-on-hypeproof-20260906-source]]
- Pages created: [[2026-09-06-weekly-on-hypeproof]], [[weekly-on-hypeproof-20260906-source]], [[record-issuance-model]], [[dental-website-over-blog]], [[dental-fullday-website-workshop]], [[jeon-sangyeol]]
- Pages updated: [[hypeproof-philosophy]], [[hypeproof-lab-philosophy-source]], [[community-epistemic-layer]], [[jeon-sangyeol-meeting-20260916]], [[bitree]], [[boa-dental]], [[park-junghyun]], [[comms/_index]], [[sources/_index]], [[index]], [[hot]], [[log]]
- 계기: 9/6 회의록이 `.raw/`에 들어와 있었으나 미ingest 상태였다. 같은 날 ingest된 것은 [[hypeproof-lab-philosophy-source|철학 문서]]이지 이 회의가 아니다. 정규 월요일(9/7) 미팅을 **하루 당겨 대체한** 회의다.
- Key insight: **철학 문서의 작성자가 [[jinyong-shin]]이 아니라 [[jay-lee]]다.** 9/6 ingest는 파일 전달자(JY)를 작성자로 기록했는데, 축어록에서 [[jay-lee]]가 "내가 올린 문서", "제가 고민을 한 내용"이라 말하고 [[jinyong-shin]]은 같은 자리에서 독자로 발언한다("오늘 살짝 봤는데 어렵더라고요"). 두 페이지에 `[!contradiction]`으로 달고 정정했다. — **전달 경로를 저작으로 읽지 않는다**는 규칙이 하나 생겼다.
- 두 번째: **[[hot]]의 충돌 3번(제품 3종 명칭)이 절반 닫혔다.** [[jay-lee]]가 말로 정리했다 — 제품 = Studio + Curriculum이고 **"커리큘럼은 [[chalk|초크]]가 되겠죠"**, 커뮤니티는 **소셜 러닝 레이어지 제품이 아니다**([[hyrox-license-model-research-20260515|HYROX]]는 *대회*를 프로덕트화했고 커뮤니티는 그 결과다). [[community-epistemic-layer]]의 기존 읽기가 저자 의도와 일치함이 확인된다. ⛔ 다만 **[[sediment]]는 여전히 이 정리에 없다** — 충돌은 완전히 닫히지 않았다.
- 세 번째: **BM의 이름이 생겼다** → [[record-issuance-model]]. 성과를 약속하면 집단소송 리스크가 열리므로(파산 선례 있음, ⚠️회사명 미확인) **기록을 직접 찍어낸다** — 살아 있는 서비스 + 표준 매트릭 대시보드 + 실명 심사([[jeon-sangyeol]]). 이 대시보드가 [[four-learner-experiences]]의 **경험 D 커버리지 구멍**을 메우는 물건이며 8/31의 "최우선 개발 = 어드민/모니터링"과 같은 것이다. [[jay-lee]]는 여기에 **"실제로 돈을 벌었던 기록"**을 추가 요구했다 — 팀에 앱·게임으로 매출을 내 본 사람이 ⛔ 0명이라는 것도 함께 밝혔다.
- 네 번째: **8/31에 열려 있던 "파트너는 채널인가 공동 BM인가"에 답이 나왔다 — 공동 BM.** [[bitree]]는 AI 에이전트 5종으로 연 10억 매출을 내지만 **프로덕타이제이션이 0**이다(온프레미스 바이브 코딩). 우리가 제품 구조화·운영 노하우를 주고 **프로덕션 엔지니어 리소스**를 받는 교환. 전문직 채널의 종착지가 **AX 케어**라는 전망이 여기 걸린다 — "강의만 할 순 없다, 결국 '해 줘'가 된다." 단 [[jay-lee]]는 "**계약직으로 뽑아서 돌리면 된다**"고도 말해 Bitree 경유가 유일 경로는 아니다.
- 다섯 번째: **치과 라인이 블로그를 버렸다** → [[dental-website-over-blog]]. 판단 기준이 "할 수 있는가"가 아니라 **"우리여야만 하는가"**였다는 점이 중요하다 — 블로그는 성공하면 다음이 마케팅이고 그건 역량 밖이다. 그리고 이 결정은 추론이 아니라 **[[park-junghyun]] 원장에게 직접 물어서** 나왔다. 형태는 **풀데이 오프라인**으로 바뀌었다([[dental-fullday-website-workshop]]) — 2.5시간으로는 퍼블리싱 퀄리티가 안 나오고, 원장들을 5회 불러 모을 수 없기 때문. Cloudflare CLI 배포 자동화는 **[[hypeproof-studio]] 제품화 후보**다.
- 여섯 번째: **타임라인이 처음 숫자로 나왔다 — 2027-01 공개 가정, 남은 3개월.** 9/15 IR 방향성에 프로덕션 내용이 들어가야 한다는 요구가 여기서 파생됐다.
- ⚠️ **깨지는 숫자 5건**을 소스 페이지에 표로 모았다. 특히 TJ 덱의 **HYROX 연매출 "188 빌리언 달러"**는 명백한 오류이고, [[jiwoong-kim]] 덱의 **SK바이오팜 "1회차 800만원 / 21명"**은 볼트 확정 견적 **920만원 / 10가족**([[sk-biopharma-bitree-final-quotation-20260526]])과 어긋난다. [[ir-20260915-pricing-evidence-audit]]의 규칙이 그대로 적용된다.
- 미확인: [[jeon-sangyeol]] 대표의 소속·직함 · 파산 사례 회사명("엠비전"/"엔비전") · [[park-junghyun]] 원장의 정산 법인 표기("오라센트") · [[bitree]] 문 대표 성명 · 치과 정산 예시의 개별 금액(축어록에서 150/152만원이 갈림)

## [2026-09-06] ingest | HypeProof Lab Philosophy (updated) — 정본 후보
- Source: `Hypeproof_Lab_Philosophy_updated.docx` ([[jinyong-shin]] 작성) → `.raw/philosophy/hypeproof-lab-philosophy-updated-2026-09-06.md` (textutil 변환. **바이너리 docx는 커밋하지 않는다** — 공개 저장소)
- Summary: [[hypeproof-lab-philosophy-source]]
- Pages created: [[hypeproof-philosophy]], [[asset-pressure-map]], [[community-epistemic-layer]], [[hypeproof-lab-philosophy-source]]
- Pages updated: [[hypeproof-mission]], [[seven-ai-native-assets-original]], [[four-learner-experiences]], [[mission-product-alignment]], [[hypeproof-lab]], [[chalk]], [[sediment]], [[jesse-kim]], [[concepts/_index]], [[sources/_index]], [[index]], [[hot]], [[log]]
- 계기: 2026-09-05 조사에서 **볼트에 "Philosophy"라는 이름의 정본이 없다**는 것이 확인됐고, 8/31 회의에서 [[jesse-kim]]이 발제한 **AKB(가칭)** 자리가 비어 있었다. 이 문서가 그 첫 후보다. **`status: candidate`로 등록했고 [[hypeproof-mission]]이 계속 이긴다.**
- Key insight: **7 Assets에 「변화 가설」이라는 층이 붙었다.** 명칭·정의는 [[seven-ai-native-assets-original]]과 동일한데, 각 자산에 AI 발전에 따른 방향 판정이 달렸다 — 급증 다섯, **Context·Iterate만 "중립/재정의 필요"**다. Memory·RAG가 Context를, Agent loop가 Iterate를 흡수하는 중이기 때문이다. 그리고 이 둘은 [[four-learner-experiences]]에서 **커버리지가 ✅·🟡로 가장 좋은 B·C**에 대응한다. **되는 구간이 곧 AI가 흡수 중인 구간**이라는 읽기가 가능해진다.
- 두 번째: **퇴화 위험 「높음」이 Intent·Verify·Ownership 셋**인데([[asset-pressure-map]]), 이는 **A와 D**에 대응하는 자산이다. "가장 우리다운 곳이 가장 덜 만들어져 있다"에 **"그리고 가장 빨리 퇴화한다"**가 붙는다.
- 세 번째: **[[minhan-cho]]의 "AI-인간 거리감" 8번째 축 제안에 이론적 근거가 생겼다** — Atrophy & Substitution Hypothesis. Atrophy Risk 축이 곧 그 지표의 조작적 정의 후보다. 다만 창업 라인 **D-3("8번째 Asset 신설하지 않는다", 2026-08-17)**의 전제("7 Assets는 개인의 절차적 역량 체계로 유지")를 이 문서가 열어 두므로, **채택 시 D-3의 근거가 약해진다.** 사업 볼트 단독 판정 금지.
- ⚠️ 충돌 3건을 양쪽 페이지에 `[!contradiction]`으로 달았다: ①조직 정의 "글로벌 사교육 시장에 파는 AI 소프트웨어 회사"(정본, 반론 차단용으로 설계된 문장) ↔ "실험실"(후보, 8/10에 폐기된 연구소 서사로 회귀) ②7 Assets 확정 체계 ↔ 연구 모델 ③제품 3종 [[chalk]]·[[hypeproof-studio]]·[[sediment]] ↔ **Curriculum·Studio·Community**. 셋째가 특히 크다 — Chalk는 커리큘럼 **생성기**라 Curriculum과 1:1이 아니고, **Sediment에 대응하는 층이 후보 문서에 없으며**, 역으로 Community에 대응하는 제품이 볼트에 없다.
- ⛔ 공백: 후보 문서에 **증거 제품 라인·사용자/구매자 분리·두 스트림·구조적 방어·"왜 아이인가"·제3자 강사 0건 리스크**가 없다. 문서가 스스로 *"비즈니스 모델을 설명하는 문서가 아니다"*라 선언하므로 층의 차이지만, **정본 대체용으로 쓰면 사업 골격이 통째로 빠진다.**
- 부수 수확: §18 **자기모순 6개**가 그대로 리뷰 체크리스트다 — "Studio의 성공을 결과물의 화려함이나 제작 속도로만 평가하는 경우", "7 Assets을 검증 가능한 가설이 아니라 브랜드 문구로 고정하는 경우" 등. 9/15 덱이 걸릴 만한 항목이 둘 있다.
- 미확인: 문서 작성일(본문에 날짜 없음) · **AKB의 뜻**(8/31 회의록도 "가칭"으로만 표기) · Chalk·Sediment 미등장이 의도인지 8/31 이전 작성인지 · 8/31 액션 "미션 지향 문서 검토 후 텍스트 피드백"의 대상이 이 문서인지

## [2026-09-05] audit | 9/15 덱 숫자 감사 — 인용 가능한 숫자와 깨지는 숫자
- Pages created: [[ir-20260915-pricing-evidence-audit]]
- Pages updated: [[teen-ai-startup-camp-v0]], [[jeon-sangyeol-meeting-20260916]], [[sk-biopharma-pilot]], [[index]], [[hot]], [[log]]
- 계기: 9/15 피칭 덱 작성 에이전트들에게 위키 원문을 공급하다가, 요약본에서 인용한 숫자 세 건이 원본과 어긋나는 것을 발견했다.
- Key insight: **요약이 원본을 앞지른 사례가 하나 있다.** "평균 160분 리텐션"에 붙은 **"3시간 기준"이 8/25 축어록에 없다** — ingest 단계에서 붙어 세 문서로 전파됐고, 정작 SK바이오팜 수업은 4시간 설계다. 분모에 따라 89%와 67%로 갈리는데, 이 숫자는 [[teen-ai-startup-camp-v0]]이 "가장 강한 제품 효과 증거"로 지목한 것이다. **가장 강한 증거의 분모가 미확인이었다.**
- 두 번째: **기획 검토가가 실적가로 굳어 있었다.** "가족당 40~60만원, 50만원 앵커"는 2026-05-15경 검토값이고, 열흘 뒤 실제 견적은 **가족당 92만원**이다([[sk-biopharma-bitree-final-quotation-20260526]]). [[sk-biopharma-pilot]]이 `[!contradiction]`으로 이미 달아두었으나 후속 문서가 계속 검토가를 인용했다. 부수로 **"시간당 10만→20만"의 단위가 1인 기준**임이 풀렸다 — 92만 ÷ 4h ÷ 2인(부모+자녀 페어) = 11.5만/h. 목표가 환산은 가족당 160만원이다.
- 세 번째: **견적서 안에 대응하지 않는 두 산식이 있다.** 원가 항목(918만)과 정산 제안(920만을 20/20/60 분할)이 서로 매핑되지 않는다 — Bitree 184만은 원가에 없고, 운영지원·교통비는 정산에 없다. 이것이 인력 절감 레버의 귀속을 결정한다: 2인 체제로 가면 인건비 918만 → 366만이지만, **비율 정산이면 절감분이 법인에 오지 않는다.** 게다가 견적서 판매자가 **Bitree Corporation**이고 우리는 계약 주체가 아니어서, "직영 전환"은 채널 선택이 아니라 계약 주체 변경이며 [[hypeproof-mission]]의 법인·IP 과제(시한 8/22 경과)가 선결이다.
- 정리하면 자물쇠 셋에 순서가 있다 — ①2인 체제가 돌아가는가(리허설로 확인) ②절감분이 법인에 귀속되는가(정산 재협상은 지금 가능) ③법인이 계약 주체가 될 수 있는가(②의 직영 경로를 막는다).
- 미확인으로 남긴 것: 160분의 분모([[bongho-tae]]) · 정산 제안의 집행 여부 · 견적서의 "이재원 디렉터"가 [[jay-lee]]인가(볼트에 [[lee-jaewon]] 스텁이 `external`·치과로 따로 있어 동명이인을 못 가른다) · 직영 전환 시 영업 원가
- Note: 이번 감사는 위키 스킬을 Wiki Monkey 런타임에 등록한 직후 첫 작업이다. 규칙으로 남긴 것 — **숫자를 인용할 때는 `.raw/` 원본까지 내려가 분모·단위·시점을 확인한다.**

## [2026-09-03] ingest | Weekly on HypeProof 2026-08-31
- Source: `.raw/meeting_notes/Weekly on HypeProof - 2026_08_31 21_59 KST - Notes by Gemini.md` + 동 `(1).md` 스크립트(1,900여 줄). 회의 1건 / 파일 2개
- Summary: [[weekly-on-hypeproof-20260831-source]] · [[2026-08-31-weekly-on-hypeproof]]
- Pages created: [[weekly-on-hypeproof-20260831-source]], [[2026-08-31-weekly-on-hypeproof]], [[minhan-cho]], [[sales-ownership-by-vertical]], [[studio-subscription-league-model]], [[production-strategy-session-20260919]], [[action-items-20260831]]
- Pages updated: [[four-learner-experiences]](팀 확정), [[chalk]](생성기 정정·게이트웨이론), [[sediment]]("크(?)" 해소), [[jesse-kim]], [[jay-lee]], [[jiwoong-kim]], [[bongho-tae]], [[jehyeong]], [[jeon-sangyeol-meeting-20260916]], [[comms/_index]], [[sources/_index]], [[decisions/_index]], [[deliverables/_index]], [[stakeholders/_index]], [[index]], [[hot]], [[log]]
- Key insight: **[[four-learner-experiences]]의 "팀 확정 전"이 여기서 닫힌다.** 8/30에 혼자 세운 가운데 층을 8/31 회의에서 [[minhan-cho]]가 미션 → 네 경험 → 7 Assets → 제품 3종으로 발표했고 팀이 결정으로 채택했다. 커버리지 판정(A·D가 가장 덜 만들어짐)이 개인 분석에서 **팀이 공유하는 지도**로 승격됐다.
- 두 번째: **[[chalk]]의 자리가 올라갔다.** 강의 생성기에서 **교육관 검증 게이트웨이**로 확장됐고, [[jesse-kim]]이 "크립토나이트는 스튜디오가 아니라 초크"라고 못 박았다 — 시간당 10만 원과 목표 20만 원의 간극을 메우는 자리다. 정본이 이미 "서사의 중심은 Chalk"라 한 것과 회의가 같은 방향으로 움직였다.
- 세 번째: [[sediment]]에 남아 있던 미확인 항목("세디먼트 / 크(?) / Studio")이 **Chalk로 확정**됐다.
- 운영 변화: 세일즈를 라인별로 쪼개 담당을 붙였고([[sales-ownership-by-vertical]]), 수익 모델이 단품 판매에서 **구독+리그**로 옮겨갔다([[studio-subscription-league-model]]). 최우선 개발이 **어드민/모니터링 페이지**로 지목됐는데, 이는 커버리지 ⛔ 인 **경험 D**를 메우는 일이다.
- 열린 것: ⚠️ 성공 사례의 정의 미합의(대회 vs 실매출) · ⚠️ **AI-인간 거리감 지표** 제안이 창업 라인의 "8번째 Asset 신설 안 함"(D-3)과 표면상 충돌 · 파트너십을 채널로 볼지 공동 BM으로 볼지 미정
- Note: 스크립트는 8/25 때와 같은 이유(공개 저장소 PII)로 커밋하지 않는다. 이번에는 삭제 대신 **`.gitignore` 규칙**(`*Notes by Gemini (1).md`)으로 로컬 보관만 한다. 요약본의 초대자 이메일·캘린더 링크는 마스킹 후 커밋. 회의록의 **"신제형"** 표기와 [[jehyeong]]의 동일 인물 여부는 확증 전이다.

## [2026-08-30] synthesis | 미션 → 제품 사이의 층 정리 + 롱텀 문서
- Pages created: [[four-learner-experiences]]
- Pages updated: [[mission-product-alignment]](경험 척추·두 갈래·시간 지평 4구간·팀 공유 문서 포인터), [[hypeproof-business-strategy]](두 갈래 구조), [[concepts/_index]], [[index]], [[hot]], [[curriculum-hot]], [[log]]
- 산출물: `HypeProof/_worklog/why-teen-startup-ir-20260915.html` — 롱텀 문서. 자립적으로 읽히도록 내부 용어와 정본 참조를 전부 풀어 썼고, 8축·신원 취급·라이선스·규제는 제품 트랙으로 내려 뺐다
- Key insight: 미션과 제품 사이가 비어 있어서 프레임이 여섯 개로 흩어져 있었다. **네 가지 학습자 경험(A~D)**이 그 가운데 층이고, 출처는 "AI가 날려도 사람에게 남는 것" 넷을 학습자가 겪는 순서로 다시 놓은 것이다. 이 축을 놓자 커버리지 판정이 방향으로 바뀌었다 — **A와 D가 우리 고유의 자리인데 가장 덜 만들어져 있다.** 그리고 넷과 일곱(7 Assets)은 대체가 아니라 시간축과 능력축의 차이이므로, 대외는 넷 내부는 일곱으로 쓰기로 했다.
- 두 번째 발견: **같은 도구로 초등 3학년과 치과 원장을 모두 돌렸고 바뀐 것은 프로필 파일 하나다.** 확장성을 주장이 아니라 기록으로 말할 수 있는 유일한 증거다. 다만 「업스킬링」은 정본의 「우리가 아닌 것」 첫 줄이라 **전문가 스트림**으로 부른다.
- 경계: A~D는 **팀 확정 전**이다. 확정 여부가 열린 질문 1번이고, 흔들리면 커버리지·로드맵이 전부 다시 그려진다.

## [2026-08-30] save | 8/25 회의록 기반 미션 드리븐 렌즈 보강
- Type: synthesis update
- Location: wiki/questions/why-hypeproof-for-teen-startup-ir-20260915.md
- From: Telegram group discussion after re-reading the 8/25 meeting transcript only
- Key insight: 앞선 질문은 제품 기능 점검에 가까웠다. 8/25 회의록 기준 핵심은 "우리 조직이 뭘 위해 달려가며, 그 미션이 왜 학생 창업교육이라는 첫 시장으로 내려오는가"다. G스택은 why-us가 아니라 참고 자료이고, HypeProof가 맡을 앞단은 문제 정의 -> AI 지시 -> 작동하는 것 제작 -> 반복 개선이다. 9/15 HTML은 기존 미션/제품 실사 문서가 아니라 이 렌즈로 전면 재작성되어야 한다.

## [2026-08-30] save | 왜 HypeProof가 고1~2 창업/IR 교육을 해야 하는가
- Type: synthesis
- Location: wiki/questions/why-hypeproof-for-teen-startup-ir-20260915.md
- From: Telegram group discussion on 9/15 pitching, mission-driven framing, and the weak link between HypeProof mission and student startup/IR education
- Key insight: 9/15의 중심 질문은 "창업 교육을 할 것인가"가 아니라 **"왜 학생 창업/IR 교육을 HypeProof Lab이 해야 하는가"**다. HypeProof는 창업교육 회사가 아니라 AI 시대에 판단하는 인간을 기르는 제품 회사이고, 학생 창업/IR 교육은 그 미션을 가장 빨리 증명할 첫 포맷이다. 제품 차별점은 창업 이론 강의가 아니라 학생의 문제정의·AI 지휘·수정 로그·판단 근거를 Studio 안에 남기고, 이를 대입/이력서용 증거 패키지로 바꾸는 데 있다.

## [2026-08-30] ingest | 정본 8/10 포지셔닝 리셋 + 미션↔제품 정렬 점검
- Sources: `hypeprooflab/MISSION.md`(확정 2026-07-31 · 개정 2026-08-10) · `hypeprooflab/docs/decisions/2026-08-10-positioning-reset.md`
- Summary: [[hypeproof-positioning-reset-20260810]]
- Pages created: [[hypeproof-positioning-reset-20260810]], [[mission-product-alignment]], [[chalk]]
- Pages updated: [[hypeproof-mission]](7/31→8/10 전면 재작성), [[hypeproof-mission-20260731-source]](대체됨 배너), [[hypeproof-lab]], [[hypeproof-business-strategy]], [[mission-driven]], [[sediment]], [[concepts/_index]], [[components/_index]], [[sources/_index]], [[index]], [[hot]], [[log]]
- Key insight: 8/29 작업 전체가 **7/31판 위에서** 이뤄졌다. 로컬 저장소가 855 커밋 뒤처져 있었고 마지막 fetch가 8/2였다. 그 결과 [[hypeproof-mission]]이 `status: canonical`을 달고 폐기된 문장을 싣고 있었다 — 정본을 자처하며 틀린 상태가 가장 나쁘다. 8/10 개정의 핵심은 문장이 아니라 **논증의 축**이다: 방어 논리가 잔여 방어에서 구조적 방어로 뒤집혔고("벤더가 개선할수록 시장이 커진다"), 사용자와 구매자가 분리됐으며, 직접 강의가 매출 사업에서 증명 엔진으로 재정의됐다. 그리고 정본이 **제3자 강사 운영 0건**을 사업 모델의 병목으로 못 박았다.
- Note: **정본 인용 전 `git fetch`를 먼저 한다.** 오래된 체크아웃은 없는 것보다 나쁘다 — 확신을 주기 때문이다. 결정 문서도 같은 교훈을 남겼다: "의미 충돌은 먼저 머지된 쪽이 조용히 이긴다. 어떤 CI 게이트도 이걸 보지 않는다."

## [2026-08-29] ingest | HypeProof Lab MISSION.md (정본) + Weekly 2026-08-25
- Sources: `/Users/jj_home/Git/HypeProof/hypeprooflab/MISSION.md` (별도 레포, 2026-07-31 확정 정본) · `.raw/meeting_notes/Weekly on HypeProof - 2026_08_25 20_58 KST - Notes by Gemini.md` + 동 `(1).md` 스크립트
- Summaries: [[hypeproof-mission-20260731-source]] · [[weekly-on-hypeproof-20260825-source]]
- Pages created: [[hypeproof-mission]], [[hypeproof-mission-20260731-source]], [[2026-08-25-weekly-on-hypeproof]], [[weekly-on-hypeproof-20260825-source]], [[teen-ai-startup-camp-v0]], [[jeon-sangyeol-meeting-20260916]], [[ir-mentor-candidates-20260915]], [[jesse-kim]], [[g-stack]], [[sediment]]
- Pages updated: [[hypeproof-lab]], [[mission-driven]], [[hypeproof-business-strategy]], [[startup-hot]], [[startup-log]], [[concepts/_index]], [[comms/_index]], [[sources/_index]], [[stakeholders/_index]], [[specs/_index]], [[deliverables/_index]], [[intel/_index]], [[components/_index]], [[index]], [[hot]], [[log]]
- Key insight: 미션 정본이 조직 정체성을 **콘텐츠 조직 → AI 제품 조직**으로 정정한다. 강의는 목적이 아니라 제품을 성숙시키고 고객을 얻는 수단이며, 그래서 강의 산출물은 부산물이 아니라 제품 자산이고 IP 귀속이 급하다. 법인·IP·라이선스 최우선 과제는 시한(2026-08-22)을 넘겼다. 8/25 회의는 이 정본과 정확히 같은 방향으로 움직였다 — Jay Lee가 IR을 마켓 드리븐에서 미션 드리븐으로 틀었고, 팀은 롱텀(미션)/숏텀(창업 교육) 2축을 채택했다. 다만 숏텀 축의 사업 가설은 전부 2차 정보이고 G스택 차별점에는 내부 반론이 있다. 현재 가장 단단한 근거는 SK바이오팜 세션의 평균 160분 리텐션 하나다.
- Note: 파일 2개는 별개 회의가 아니라 **한 회의의 요약본 + 스크립트**였고, **스크립트는 2026-08-29 삭제**했다(공개 저장소 PII). 요약본의 초대자 이메일·캘린더 링크도 마스킹 후 커밋. `wiki/` 안에 "IR"이 회사 IR과 학생 IR 두 뜻으로 존재하게 되었으므로 문서 간 이동 시 주의.










## [2026-08-08] split | 커리큘럼 지식을 curriculum_wiki/ 로 분리
- 이동: `wiki/curriculum/**` 전체, `wiki/intel/ped-*` 10건, `wiki/decisions/edu-11-16-*` 4건, `_templates/` 4종 → `curriculum_wiki/`
- 삭제: 오버라이드 3건 + `override-protocol` + `_templates/override`. `wiki/projects/*` 3건의 `has_overrides` 되돌림
- 복원: `hot.md`를 2026-07-11 시점(BOA·SK·Studio 맥락)으로 되돌림
- Key insight: 사업 실행 문서와 커리큘럼 지식은 목적·시간축·독자가 다르다. 한 트리에 두면 hot 캐시가 경합하고 스킬 스키마가 충돌한다. 같은 볼트 안에서 트리를 나눠 위키링크는 유지하되 메타 파일과 규약을 분리했다. 오버라이드 프로토콜은 결론이 이미 헌법·측정 문서에 흡수되어 삭제했고, 남은 조직 표준 4축 확장 제안만 사업 볼트 과제로 남겼다.

## [2026-07-11] ingest | 변호사 전문직 채널 미팅 메모
- Source: `.raw/telegram/2026-07-11-legal-professional-channel-meeting.md`
- Summary: [[legal-professional-channel-meeting-20260711-source]]
- Pages created: [[legal-professional-channel-meeting-20260711-source]], [[2026-07-11-legal-professional-channel-meeting]], [[legal-brief-prep-loop]], [[legal-divorce-brief-prep-consulting]]
- Pages updated: [[hypeproof-business-strategy]], [[sources/_index]], [[comms/_index]], [[concepts/_index]], [[specs/track-b/_index]], [[index]], [[hot]], [[log]]
- Key insight: 변호사 채널의 핵심은 빠른 초안보다 truthworthy한 사실 추출과 준비서면 교정 루프다. 의뢰인의 머릿속 사건을 꺼내고, 하나의 사실에서 여러 해석을 분기하며, 변호사의 pass/fail 감각으로 49%→51%를 넘기는 것이 상품 본체가 될 수 있다. GEO와 "이혼 기각" 니치는 후속 확인 필요로 남긴다.

## [2026-07-06] ingest | 보아치과 AI 홈페이지 실습 큐시트
- Source: `.raw/documents/boa-dental-ai-homepage-cuesheet-20260706.pdf`
- Companion sources: `.raw/documents/boa-dental-ai-homepage-cuesheet-20260706.html`, `.raw/documents/boa-dental-ai-homepage-cuesheet-20260706.txt`
- Summary: [[boa-dental-ai-homepage-cuesheet-20260706]]
- Pages created: [[boa-dental-ai-homepage-cuesheet-20260706]], [[boa-dental-ai-homepage-cuesheet-20260706-spec]]
- Pages updated: [[dental-website-copyclone-v3]], [[boa-dental]], [[hypeproof-studio]], [[sources/_index]], [[specs/track-b/_index]], [[index]], [[hot]], [[log]]
- Key insight: 보아치과 2시간 외부 공유용 큐시트는 발표/해커톤 감성을 빼고, 메인강사가 보아치과 홈페이지를 만드는 화면을 기준으로 같이 따라 만들게 한다. Context Engineering은 URL만 넣은 결과와 자세한 병원 컨텍스트 결과의 차이를 체감시키고, Loop Engineering은 루브릭을 만족할 때까지 검사와 수정을 반복시키는 것을 핵심으로 둔다. 최종 산출물은 홈페이지, 배포 URL, GitHub 저장소, `agent.md`다.

## [2026-06-30] save | 보아치과 랜딩 첫 화면 메시지
- Source: `.raw/telegram/2026-06-30-boa-dental-landing-message.md`
- Summary: [[boa-dental-landing-message-20260630-source]]
- Pages created: [[boa-dental-landing-message-20260630-source]]
- Pages updated: [[dental-website-copyclone-v3]], [[sources/_index]], [[index]], [[hot]], [[log]]
- Key insight: 첫 화면은 실제 배포 홈페이지라는 즉시 결과물과, Claude Code/Codex 등 도구와 무관하게 쓰는 `맥락 설계`·`피드백 감각`을 HypeProof Lab의 실전 반복 훈련으로 체화한다는 메시지를 함께 보여줘야 한다.

## [2026-06-30] ingest | Weekly on HypeProof 2026-06-29
- Source: `.raw/meeting_notes/2026-06-29-weekly-on-hypeproof-gemini.md`
- Summary: [[weekly-on-hypeproof-20260629-source]]
- Pages created: [[weekly-on-hypeproof-20260629-source]], [[2026-06-29-weekly-on-hypeproof]]
- Pages updated: [[boa-dental]], [[dental-website-copyclone-v3]], [[hypeproof-studio]], [[sources/_index]], [[comms/_index]], [[index]], [[hot]], [[log]]
- Key insight: 보아치과 강의의 수강자 아웃풋은 홈페이지 초안/공개 URL/전후 비교/설명 카드/Loop Log이고, HypeProof 고유성은 Studio 로그·7 Assets 체화·레이스/커뮤니티·KOL 채널 전략에 있다.

## [2026-06-27] ingest | 보아치과 AI 홍보 레이스 포스터 v1
- Source: `.raw/documents/boa-dental-ai-promo-race-poster-v1-20260627.pdf`
- Companion source: `.raw/documents/boa-dental-ai-promo-race-poster-v1-20260627.html`
- Summary: [[boa-dental-ai-promo-race-poster-v1-20260627]]
- Pages created: [[boa-dental-ai-promo-race-poster-v1-20260627]], [[boa-dental-ai-promo-race-poster-v1]]
- Pages updated: [[boa-dental]], [[sources/_index]], [[deliverables/_index]], [[specs/track-b/_index]], [[index]], [[hot]], [[log]]
- Key insight: 보아치과 포스터 v1의 외부 정본 흐름은 초반 설명과 재료 정리 이후 원장님이 직접 문구·구성·톤을 깎아 최종 홈페이지 초안으로 평가받는 구조다.

## [2026-06-27] correction/save | 보아치과 클로징 — 홍보 자유도 중심 정정
- Type: curriculum correction
- Pages updated: [[dental-website-copyclone-v3]], [[specs/track-b/_index]], [[hot]], `exports/boa-dental-design-rationale.html/.pdf`
- From: Telegram (Jiwoong Kim). 보아치과 원장 강의의 클로징과 레슨은 부모/아이 강의와 달라야 하며, 핵심은 원장님이 자기 치과 홍보를 본인이 원하는 대로 할 수 있는 자유도를 얻는 것이라는 정정.
- Key insight: 의료광고 검증은 필수 가드레일이지만 클로징의 주인공은 검증 자체가 아니다. 보아치과판의 두 중심 기술은 AI에게 내 병원을 제대로 질문/설명하는 Context Engineering과 첫 결과를 원하는 홍보 방향으로 계속 고쳐가는 Feedback Loop다.

## [2026-06-22] correction/save | 보아치과 v3 — v2의 HypeProof DNA 누락 정정
- Type: curriculum correction
- Created: [[dental-website-copyclone-v3]] (md), `exports/dental-website-copyclone-v3.html/.pdf`
- Pages updated: [[specs/track-b/_index]], [[hot]], [[log]]
- From: Telegram (Jiwoong Kim). v2가 봉호 코어·7에셋 행동신호·와우포인트·boaclinic급 결과물을 하나도 안 박은 generic draft라는 정당한 지적.
- Key insight: v3는 (1)봉호 5블록+AI지휘관 서사+핵심 장면(AI가 다르게 만듦→질문 고침)을 본체로, (2)7에셋을 Q&A 아닌 행동신호 관찰표로, (3)오프닝 와우포인트 라이브 데모, (4)결과물 수준을 boaclinic.com급(네이버예약·카카오·SNS 연동 + Cloudflare Pages 안정 배포)으로 고정. v2는 deprecated.

## [2026-06-21] ingest/save | 보아치과 v2 카피클론 + 주인님 확정 우선순위
- Type: curriculum/spec + priority correction
- Created: [[dental-website-copyclone-v2]] (md), `exports/dental-website-copyclone-v2.html`
- Pages updated: [[specs/track-b/_index]], [[hot]], [[log]]
- From: Telegram (Jiwoong Kim). AI의 임의 P0~P3 우선순위는 할루시네이션으로 기각. 정본 우선순위 = 1) 보아치과 커리큘럼을 웹사이트 카피 방향으로 전환(핵심가치 복사·껍데기만 교체) 2) HypeProof Studio 기술 운행 가능성 체크.
- Key insight: v1(detail-v1)의 핵심가치(요리교실·공개URL·7Assets·검증·자기병원전환)는 유지, 출발점만 "빈 샘플 생성"→"실재 사이트 정답지 클론(구조만 차용·콘텐츠 데모 교체, 도용금지)"으로 교체. Studio 운행의 P0 블로커는 이미지 맥락주입 UI + 멀티턴 연속성.

## [2026-06-08] save | HypeProof Studio 메타게임 은유
- Type: concept/spec update
- Pages updated: [[sk-biopharma-bongho-curriculum-v2]], [[hypeproof-studio-game-skillpack-v1]], [[hot]], [[log]]
- From: 봉호 태님 Telegram insight: “HypeProof Studio라는 커다란 게임기 안에서 게임을 만드는 게임을 한다.”
- Key insight: Studio는 AI 코딩툴이 아니라 메타게임 OS다. 7 Assets는 내부 매핑으로 두고, 아이에게는 퀘스트/뱃지/레벨업/출시 보상으로 경험되게 한다.

## [2026-06-08] correction | 7 Assets 평가 프레임 금지
- Type: correction
- Pages updated: [[sk-biopharma-bongho-curriculum-v2]], [[hypeproof-studio-game-skillpack-v1]], [[hot]], [[log]]
- From: Telegram correction that framing 7 Assets as scoring/rubric risks overriding 봉호 커리큘럼.
- Key insight: 봉호 커리큘럼 우선. 7 Assets는 아이에게 점수로 노출하지 않고, Studio가 과정 흔적을 보존한 뒤 관찰 기록/성장 코멘트로만 번역한다. 0/1/2 루브릭은 봉호님 확인 전까지 사용하지 않는다.

## [2026-06-08] save | SK바이오팜 봉호 커리큘럼 v2 재작성
- Type: curriculum/spec
- Created: [[sk-biopharma-bongho-curriculum-v2]]
- Pages updated: [[hypeproof-studio-game-skillpack-v1]], [[specs/_index]], [[index]], [[hot]], [[log]]
- From: Telegram correction that 봉호 커리큘럼 must be treated as the product core, not as a partial reference.
- Key insight: SK바이오팜 수업은 HypeProof Studio 수업이 아니라, 봉호 커리큘럼을 HypeProof Studio로 구현한 가족 AI 게임 창작 수업이다.

## [2026-06-08] decision/save | SK바이오팜 봉호 커리큘럼 구현 + Game Skill Pack
- Type: spec/decision
- Created: [[hypeproof-studio-game-skillpack-v1]]
- Pages updated: [[sk-biopharma-curriculum-detail-v1]], [[hypeproof-studio]], [[specs/_index]], [[index]], [[hot]], [[log]]
- From: Telegram decision that SK바이오팜 게임 만들기 수업은 HypeProof Studio로 해야 하며, 게임 제작 특화 스킬·룰·프롬프트를 사전 탑재해야 한다.
- Key insight: 봉호 커리큘럼을 구현하는 Studio는 범용 코딩툴 대체물이 아니라 아이/가족 수업의 완성률·안전성·리포트 데이터 수집을 보장하는 guided education OS다.

## [2026-06-08] save | 커리큘럼 상세 v1 2종 — SK바이오팜 / 보아치과
- Type: curriculum/spec
- Created: [[sk-biopharma-curriculum-detail-v1]], [[dental-website-workshop-detail-v1]]
- Pages updated: [[sk-biopharma-pilot]], [[dental-homepage-seminar-v1]], [[specs/_index]], [[specs/track-b/_index]], [[index]], [[hot]], [[log]]
- From: Telegram discussion on prioritizing SK바이오팜 커리큘럼 상세 v1 and 보아치과 웹사이트 만들기 상세 v1 based on existing vault materials.
- Key insight: SK바이오팜은 봉호 커리큘럼을 본체로 HypeProof Studio에서 구현하는 7 Assets Family AI Creation Lab으로, 보아치과는 Claude Code 중심 실전 홈페이지 제작 + HypeProof Studio 스킬팩 제품화 경로로 분리하는 것이 현재 최선이다.

## [2026-06-08] ingest | SK바이오팜 일정/대상자 내부 설문 결과
- Source: `.raw/images/sk-biopharma-schedule-survey-20260608.md`
- Summary: [[sk-biopharma-schedule-survey-20260608]]
- Pages created: [[sk-biopharma-schedule-survey-20260608]], [[kim-jinhyuk]]
- Pages updated: [[sk-biopharma-pilot]], [[sk-biopharma]], [[sources/_index]], [[stakeholders/_index]], [[index]], [[hot]], [[log]]
- Key insight: SK바이오팜 파일럿 수요가 20가족/23자녀/2회차/7~8월 토요일 선호로 구체화되어, 분반 의견·2회차 견적·커리큘럼 자료·가능 일정 회신이 다음 병목이 되었다.

## [2026-06-07] ingest | 세미나 기획 의견 정리 — 치과 AI 홈페이지 만들기
- Source: `.raw/articles/dental-homepage-seminar-feedback-20260607.html`
- Summary: [[dental-homepage-seminar-feedback-20260607]]
- Pages created: [[dental-homepage-seminar-feedback-20260607]], [[dental-homepage-seminar-v1]], [[boa-dental]], [[park-junghyun]], [[lee-jaewon]], [[gabia]], [[cafe24]], [[claude-code]], [[vercel]], [[cloudflare]], [[hypeproof-ai-xyz]]
- Pages updated: [[sources/_index]], [[specs/track-b/_index]], [[stakeholders/_index]], [[components/_index]], [[index]], [[hot]], [[log]]
- Key insight: 치과 홈페이지 세미나는 자유 제작보다 샘플을 그대로 따라 만드는 요리교실식 완주 경험과 실제 배포 URL 확보가 핵심이다.
- Correction: 주인님 정정에 따라 이 소스는 [[boa-dental]] 이후 피드백으로 표시한다.

## 2026-06-01 ingest | 7 AI Native Assets 측정 구조 원본
- Source: `.raw/articles/7assets-measurement-review-original-20260523.html`
- Summary: [[7assets-measurement-review-original-20260523]]
- Pages created: [[seven-ai-native-assets-original]]
- Pages updated: [[seven-ai-native-assets-sk-strategy]], [[sk-biopharma-pilot]]
- Key insight: 7 Assets는 Q&A 답변이 아니라 과정 신호로 측정해야 하는 절차적 역량이다.

---
type: meta
title: "Log"
created: 2026-04-12
updated: 2026-04-19
tags:
  - meta/log
---

## [2026-06-01] save | 7 AI Native Assets — SK바이오팜 전략 업데이트
- Type: concept
- Location: wiki/concepts/seven-ai-native-assets-sk-strategy.md
- From: SK바이오팜 최종 견적서와 Bitree 제안서 비교, 7 Assets 중심 상품 전략 업데이트
- Key insight: 7 Assets는 세일즈용 포장이 아니라 외부 고객 인터페이스이며, 16 Essence는 내부 scoring rubric으로 유지한다.


## [2026-06-01] ingest | SK바이오팜 Bitree 최종 견적서
- Source: `.raw/images/sk-biopharma-bitree-final-quotation-20260526.md`
- Summary: [[sk-biopharma-bitree-final-quotation-20260526]]
- Pages updated: [[sk-biopharma-pilot]], [[index]], [[hot]]
- Key insight: 최종 견적은 4시간/10가족 기준 VAT 포함 10,120,000원으로, 기존 40~60만원/가족 검토가보다 높은 프리미엄/high-touch 운영 가격이다.


# Log

추가 전용. 새 엔트리는 **최상단**에 삽입. 과거 엔트리 수정 금지.

---

## 2026-05-15 | sync | HYROX 브랜치 wiki 구조 동기화 (upstream/main 기준)
- 브랜치: sync-hyrox-to-upstream-wiki-structure-20260515
- 작업: upstream/main 병합, projects/ 파일명 kebab-case 변환, [[projects/_index]] 보강, [[index]]/[[hot]] 갱신
- Pages updated: [[index]], [[hot]], [[intel/_index]], [[hypeproof-hyrox-framework-v1]]
- Key insight: HYROX 문서(프레임워크/세션/라이센스/측정/SK바이오팜 분석)를 upstream vault 구조에 편입. HTML artifact는 wiki 페이지로 등록하지 않고 [[hypeproof-hyrox-framework-v1]] frontmatter related로만 참조.

---

## 2026-05-15 | validation | 테스트 품질 3-Phase 개선 완료

- 수정: Phase1(sys.path 삭제, anyio→asyncio, tautology assertion 수정, fixture 중복 제거, 테스트명 수정) / Phase2(test_card_node·test_spec_node _DATA_DIR monkeypatch 격리) / Phase3(error 이벤트, 갤러리/rename/save 엔드포인트, backendUrl.ts 단위 테스트, send() 가드+payload 검증)
- Pages updated: [[test-quality-review-2026-05-15]], [[hot]], [[index]]
- Key insight: 97(BE)+9(FE) → 111(BE)+19(FE) = 130 tests 전체 통과. HIGH 3건(sys.path 잔재, send() 가드 미검증, asyncio 마커 누락) 모두 해소. `backendUrl.test.ts` 신규 생성으로 프론트 테스트 파일 2개로 확장.

---

## 2026-05-15 | validation | 테스트 수정 + 전체 테스트 품질 검토

- 수정: `test_auth_session_game.py` (claude_runner 임포트 → main, `_session_meta` → SQLite, 픽스처 전면 교체), `useChat.test.ts` (WS scheme env stub), `main.py` (null byte path traversal 400 처리)
- Pages created: [[test-quality-review-2026-05-15]]
- Pages updated: [[kids-edu-backend]], [[log]], [[hot]], [[index]]
- Key insight: LangGraph 리라이트로 세션 저장소가 인메모리 딕트 → SQLite로 바뀌면서 테스트 픽스처가 통째로 무효화됐음. 동시에 `main.py`의 null byte path traversal 방어 구멍(Python 3.14 ValueError 미처리)이 발견돼 수정됨. 테스트 품질 검토 결과 97/9 전체 통과하나 HIGH 3건·MEDIUM 다수 공백 확인.

---

## 2026-05-15 | pr-merge | PR#7 feature/langgraph-gemini → main 머지 + 리뷰 반영
- PR: https://github.com/JinyongShin/hypeproof_kids_edu/pull/7
- Pages updated: [[adr-langgraph-gemini-backend]]
- Key insight: [[langgraph]]+[[gemini-2-5-flash]] 백엔드 전환 PR이 리뷰 후 main에 머지됨. `edit_code_node` 실패 피드백 추가(사용자 경험), `sys.path` 반복 패턴 정리(코드 품질), Langfuse 시크릿 외부 주입(보안). 파일럿 후 처리 항목(Ping/Pong, CSP, rolling summary)은 별도 이슈로 추적 예정.

---

## 2026-05-15 | ingest | 국립암센터 행사 사전 확인 요청 초안
- Source: `.raw/meeting_notes/2026-04-21-hospital-inquiry-draft.md`
- Pages created: [[2026-04-21-hospital-inquiry-draft]]
- Pages updated: [[comms/_index]], [[index]]
- Key insight: 파일럿 당일 운영의 9개 핵심 체크포인트 (허가·감염관리·장비·콘텐츠 등)가 한 문서에 정리됨. [[game-content-guideline-pending]] 및 [[case-pediatric-onc-infection-control]] 과 직결.

---

## 2026-05-14 | vault-migration | 볼트 구조 정렬 — 스킬 철학 일치
- 작업: wiki/wiki-ingest/wiki-query/wiki-lint 스킬 철학과 볼트 구조 갭 해소
- Phase 0: git commit + tag (`vault-pre-migration-2026-05-14`) + 파일시스템 백업
- Phase 1: [[sources/_index]] · [[questions/_index]] 신규 폴더 생성
- Phase 2: `HypeProof-business-strategy.md` 루트→[[hypeproof-business-strategy]] (concepts/) 이동 + frontmatter 추가, 중복 파일 삭제
- Phase 3: dead link 4개 stub 생성 — [[adr-langgraph-gemini-backend]] · [[adr-container-deployment]] · [[adr-multitenant-schema]] · [[langfuse-observability]]
- Phase 4: orphan 파일 39개 → [[index]] 등록 (Validation·Projects·Assets·Sources·Questions 섹션 신설, Decisions·Specs·Runbooks·Components·Concepts·Comms 섹션 확장)
- Phase 5: frontmatter 보완 — projects/ 3개·runbooks/ 1개·comms/ 1개 frontmatter 추가, _index.md 13개 `status: navigational` 추가, validation/ 6개 `status: archive` + `updated` 추가
- Phase 6: vault CLAUDE.md 구조 문서 갱신 — 5개 폴더 추가, kebab-case 컨벤션 명시, 스킬 관리 폴더 주의사항 추가
- Key insight: sources/와 questions/가 없으면 wiki-ingest·wiki-query의 지식 누적 루프가 단절됨

---

## 2026-05-14 — JY 액션 리스트 저장 + LangGraph E2E 완료 기록

- Type: save / status update
- Created: [[jy-action-list-2026-05-14]]
- Updated: [[hot]]
- Key insight: [[langgraph]] MOCK_LLM=0 E2E 테스트 완료 확인. fly.io 배포만 남음. [[sk-biopharma]] 파일럿 critical path: 제안서 초안 → Freelancer 채용 → Studio v0.1 빌드.

---

## 2026-05-14 — 배치 ingest 3종 (SK바이오팜 5/12 미팅 × 2 + 5/14 후속)

- Source: `meeting_notes/2026-05-12.md`, `meeting_notes/20260512_meeting.md` (동일 내용), `meeting_notes/2026-05-14.md`
- Type: batch ingest
- Created: [[2026-05-12-sk-biopharma-meeting]], [[2026-05-14-sk-biopharma-followup]], [[sk-biopharma]], [[bitree]], [[oh-sungeun]], [[sixteen-essence]], [[hypeproof-studio]], [[adr-hypeproof-studio-v01]], [[sk-biopharma-pilot]]
- Updated: [[index]], [[hot]]
- Key insight: HypeProof Lab이 [[sk-biopharma]] 임직원 가족 대상 AI 게임 창작 교육 파일럿을 추진 중. 자체 IDE "[[hypeproof-studio]]" (VS Code fork) 개발 결정. 5/28 dry-run이 Go/No-go 게이트. [[sixteen-essence]] 프레임워크를 교육 IP의 핵심으로 구조화.
- 주의: 2026-05-12.md와 20260512_meeting.md는 동일 내용 — 단일 comms 페이지로 통합.

---

## 2026-04-21 — 병원 측 확인 질문 초안 작성

- Type: 작업 기록
- 산출물: `meeting_notes/2026-04-21-hospital-inquiry-draft.md`
- 내용: 소아암 환아 교육 선례 조사 기반 + 운영 미확정 사항을 병원 측에 확인하는 질문 초안 (9개 섹션, 행사허가·연령·참가기준·감염관리·공간·기기·보호자·콘텐츠·진행인력)
- 상태: 팀 공유 완료, 검토 의견 대기 중
- Updated: [[hot]] (JY 현장 상황 정리 태스크 In Progress로 갱신)

---

## 2026-04-21 — 배치 ingest 3종 (wizard-curriculum / asap / meeting-briefing)

- Source: `.raw/wizard-curriculum-20260420.md`, `.raw/2026-04-21-asap.md`, `.raw/2026-04-20-meeting-briefing.md`
- Type: batch ingest
- Created: [[2026-04-20-wizard-curriculum]], [[2026-04-21-asap-action-items]], [[2026-04-20-meeting-briefing]], [[curriculum-wizard-v1]], [[filamentary]], [[vibe-coding]]
- Updated: [[pilot-curriculum-adapted]] (3-way 커리큘럼 방향 contradiction 추가), [[pilot-5-5-milestones]] (4/24 필라멘트리 전달 마일스톤 추가), [[pilot-day-operation]] (wizard curriculum 참조 + open questions 확장), [[comms/_index]], [[stakeholders/_index]], [[index]], [[hot]]

### 핵심 내용

- **커리큘럼 방향 3종 병존**: HTML게임([[pilot-curriculum-adapted]]) vs 그림책([[2026-04-19-curriculum-v0.3]]) vs 게임타이틀카드([[curriculum-wizard-v1]]). 확정 필요.
- **마감 2026-04-24**: BH+지웅 커리큘럼 + JY 현장상황 → [[filamentary]] 부대표 전달.
- **신규 이해관계자**: [[filamentary]] — 현장 교육 협력 기관, 커리큘럼 피드백 파트너.
- **교육 철학**: [[vibe-coding]] 개념 등장 (자연어로 AI를 지휘해 창작물 생성), 16가지 AI 덕목.
- **인력 갭**: 브리핑 권장 6~7명 vs 현 계획 5명 → 1~2명 부족 가능성.

---

## 2026-04-19 — 커리큘럼 v0.3 ingest (2026-04-19-curriculum-v0.3.html)

- Source: `.raw/2026-04-19-curriculum-v0.3.html`
- Type: ingest
- Created: [[2026-04-19-curriculum-v0.3]] (comms), [[curriculum-v0.3]] (deliverable)
- Updated: [[pilot-5-5-milestones]] (커리큘럼 초안 Done 처리), [[pilot-curriculum-adapted]] (v0.3 cross-ref callout 추가), [[deliverables/_index]] (Curriculum 섹션 추가), [[comms/_index]] (v0.3 등록), [[index]] (Comms 9, Deliverables 11, Recent Sources 추가), [[hot]] (커리큘럼 v0.3 컨텍스트로 갱신)

### 핵심 내용
- 봉호([[bongho-tae]])·지웅([[jiwoong-kim]]) 공동 작성. 4/19 마감 목표 달성.
- 코어 골: "내가 존재하는 세계가 있다" — 소아암 병동 어린이가 처음 통제하는 창작 세계.
- 6블록 2시간 구성 (오프닝→캐릭터→세계→꾸미기→발표회→수료식).
- 결과물 형식: **그림책** (표지 + 이름 삽입 이야기 + "지은이: OOO"). 기존 [[pilot-curriculum-adapted]] 게임 HTML 중심과 상이.
- AI 호출 포인트 3종: 캐릭터 카드 생성 / 이름 삽입 이야기 / 표지 이미지.
- 안전 체계 4종: R4(완성보장) / R6(콘텐츠) / R5(에러) / 퍼실리테이터 원칙.
- 다음 게이트: 2026-04-21 Jay·JY 커리큘럼 리뷰 → [[stack-decision-after-curriculum]] 스택 결정.

### 구현 주의사항
- v0.3 커리큘럼의 AI 호출 3종(캐릭터 카드, 이야기, 표지 이미지)은 현재 백엔드 미구현.
- R4 완성보장 폴백도 P0 미충족 상태 — 4/21 후 [[subagent-team-structure]] 작업 범위 재산정 필요.

---

## 2026-04-18 — 0417-call.md ingest: Jay–JY 통화 (2026-04-17)

- Source: `0417-call.md` (원본 날짜 4/18 표기 → 실제 통화일 **2026-04-17**로 정정)
- Type: ingest
- Created: [[2026-04-17-jay-jinyong-call]] (comms), [[jay]] (stakeholder 별칭), [[2026-05-05-pilot]] (deliverable)
- Updated: [[index]] (Stakeholders 10, Comms 8, Deliverables 10, Recent Sources 추가)

### 핵심 내용
- Jay가 HypeProof 사업 구조 브리핑: 교육 트랙 (라이센스 인증 모델) + AX 전환 트랙 (SI/서비스 이원화).
- 세일즈 파이프라인 이미 확보 — 프로덕트가 "필터" 역할. JY → 사업 구조 러프 초안 → 지웅 엔지니어링 디테일.
- 파일럿 개발 현황 공유: 채팅+게임 프레임 완성, 커리큘럼 미완 (봉호 4/19 목표).
- 소아암 환자 게임 콘텐츠 주의: 적/체력 깎임 요소 치료 철학 충돌 가능 → 국립암센터 사전 확인 필요 (JY 액션).
- 4/21 월요일 미팅 확인: 지웅·봉호·정우 참석 확정.

---

## 2026-04-18 — UX 개선 5종 구현 + QA (E2E, 실제 Claude)

- Type: session
- Location: wiki/meta/session-2026-04-18-ux-improvements.md
- 개선 1: iframe `srcdoc` 전환 — `game_html` 필드 WS 전송, 네트워크 독립적 렌더링
- 개선 3: 아동 친화적 에러 메시지 — `_friendly_error()` 헬퍼 4곳 적용
- 개선 4: 블록 버튼 스킬 이름 표시 — `SCAFFOLD_DATA` 사용, 1-based, `flex-wrap`
- 개선 5: 대기 중 중간 피드백 메시지 — 15초/40초 타이머
- 개선 6: WS 재연결 상태 배너 — 황색/적색 조건부 배너
- QA 버그 수정 3건: 블록 버튼 5·6 잘림, 힌트 중복 표시, 세션 전환 시 힌트 잔류
- 커밋: db1df5d

---

## 2026-04-17 — SQLite 마이그레이션 + 세션 버그 수정 + WS 재연결

### 백엔드
- `storage.py` 신규: SQLite DB (`kids_edu.db`), sessions/messages/games/FTS5 테이블
- JSON 파일 → SQLite 자동 마이그레이션 (서버 시작 1회, flag 파일로 멱등성 보장)
- 세션 이름: "대화 N" 기본값 → 첫 메시지 앞 15자 자동 갱신
- `PATCH /sessions/{child_id}/{session_id}/name` 수동 이름 변경 엔드포인트 추가
- WebSocket: user 메시지 스트리밍 전 저장, assistant 메시지 done 시점 저장, 연결 해제 시 부분 저장
- 말풍선 버그 수정: `original_prompt` 를 DB 저장 (주입 전), Claude에는 게임 파일 경로 주입
- 게임 수정/신규 분기: "수정 요청이면 Read 도구로, 새 게임이면 무시하고 새로 만들어"
- `from pathlib import Path` 누락 → NameError → WebSocket 크래시 수정
- Claude subprocess `cwd=tempfile.gettempdir()` + `--add-dir` 로 프로젝트 컨텍스트 격리
- `TUTOR.md` 게임 코딩 규칙 추가: Canvas 고정 480×480, `roundRect()` 금지, try-catch 게임 루프

### 프론트엔드
- `useChat.ts`: sessionId 변경 시 `isLoading`·`gameUrl` 리셋, WS 자동 재연결 (최대 3회)
- `page.tsx`: `activeSessionId` 변경 시 `last_game_url` fresh fetch, `sessionRefreshToken` 추가
- `SessionSidebar.tsx`: `name` 필드 표시, `refreshToken` prop으로 게임 생성 후 re-fetch

---

## 2026-04-17 — 0412 워크샵 구조 문서 확인 + Jay 공유 내용 정리

### 확인
- `0412.md` (프로젝트 루트) 내용 검토 → 볼트 이미 완전 반영됨 (중복 ingest 불필요)
- 기존 `2026-04-12-jay-workshop-structure.md` + `pilot-5-5-milestones.md` 가 최신 기준

### JY → Jay 공유 내용 (4/17 기준)
- Track A 개발 진행 중 (채팅 히스토리, 게임 복원, 로딩 UI 완료)
- **4/21 스택 결정 미팅 전 선행 조건**: BH 커리큘럼 초안 4/19 수령 확인 (Jay 독촉)
- **Jay 액션 필요**: 랩탑/태블릿 40대 확보 방향 결정 (4/21 이전)
- **Jay 액션 필요**: 자원봉사자 퍼실리테이터 섭외 여부 결정

### 다음 게이트
- 2026-04-19: BH 커리큘럼 초안 + Ryan 와우 포인트 설계 마감
- 2026-04-21: Jay ↔ JY 스택 확정 미팅

---

## 2026-04-14 — 채팅 히스토리 저장/복원 + Windows UTF-8 버그 수정

### 구현
- **채팅 히스토리 저장**: `done` 이벤트 시 `data/messages/{child_id}/{session_id}.json` 에 user+assistant pair 저장. atomic write, 경로 순회 방어 적용.
- **복원 API**: `GET /sessions/{child_id}/{session_id}/messages` 엔드포인트 추가.
- **프론트엔드**: `useChat.ts` sessionId 변경 감지 시 자동 히스토리 로드.
- **세션 삭제 연동**: `delete_session` 호출 시 messages 파일도 함께 삭제.

### 버그 수정 (f59b5e4) — Windows CP949 인코딩
- `_append_messages`, `_save_session_meta`, `SessionStore._save` 의 `write_text()` 3곳에 `encoding='utf-8'` 누락 → 한국어 깨짐 + HTTP 500 오류 발생.
- `_load_messages` 에 `UnicodeDecodeError` 예외 처리 추가.

### E2E 검증
- 메시지 전송 → 로그아웃 → 재로그인 → 세션 클릭 → 히스토리 복원 전 구간 확인 완료.

### 커밋
- `f59b5e4` fix(backend): Windows CP949 인코딩 버그 수정
- `40e585d` feat: 채팅 히스토리 백엔드 저장/복원
- `5ee623b` fix(frontend): 재로그인 시 게임 복원 + 로딩 UI
- `2d8693f` fix(frontend): React Strict Mode WS 오류 오탐 수정

---

## 2026-04-13 — 채팅 히스토리 백엔드 저장/복원

### 구현
- **백엔드**: `done` 이벤트 시 `data/messages/{child_id}/{session_id}.json` 에 user+assistant pair 저장 (atomic write, 경로 순회 방어). `GET /sessions/{child_id}/{session_id}/messages` 엔드포인트 추가. `delete_session` 시 메시지 파일도 함께 삭제.
- **프론트엔드**: 세션 전환 시 `GET /sessions/.../messages` 호출 → 메시지 목록 즉시 복원. React state에만 존재하던 기존 구조 탈피.

### 커밋
- `40e585d` feat: 채팅 히스토리 백엔드 저장/복원

---

## 2026-04-13 — 재로그인 게임 복원 + 로딩 UI 개선

### 수정
- **게임 복원**: 세션 전환 시 `last_game_url`을 `onSessionChange` 콜백으로 전달, `setGameUrl(lastGameUrl)`로 즉시 복원. 기존엔 `setGameUrl("")`로 강제 초기화하던 버그.
- **로딩 UI**: 전송 후 AI 첫 응답 전 구간에 `●●●` bounce dots 버블 표시. GamePreview에 `isLoading` prop 추가, 게임 없을 때 스피너, 게임 있을 때 반투명 오버레이+스피너.

### 커밋
- `5ee623b` fix(frontend): 재로그인 시 게임 복원 + 로딩 UI 개선

---

## 2026-04-13 — React Strict Mode WS 오탐 버그 수정 + Playwright MCP 설정

### 수정
- **useChat.ts**: `intentionallyClosed` 플래그 추가. React Strict Mode에서 effect 2회 실행 시 첫 번째 WS cleanup이 연결 수립 전 `onerror`를 트리거하던 문제 해결.
- **.mcp.json**: Windows 환경에서 `npx` 실행 시 `cmd /c` 래퍼 누락 문제 수정. Playwright·context7·sequential-thinking 모두 적용.

### 확인 (Playwright MCP)
- `localhost:3000` → `/login` 자동 리다이렉트 정상
- root/0000 로그인 → 메인 앱 진입, 세션 사이드바 표시 정상
- WS 연결 에러 메시지 제거 확인

### 커밋
- `2d8693f` fix(frontend): React Strict Mode WS 오류 메시지 오탐 수정

---

## 2026-04-13 — 로그인 + 채팅 세션 관리 + 게임 HTML 파일 저장

### 구현된 기능
- **로그인**: `/login` 페이지 신규. `ADMIN_USERNAME`/`ADMIN_PASSWORD` 환경변수 기반 검증. sessionStorage auth state. 미인증 시 `/login` 리다이렉트.
- **채팅 세션 관리**: `SessionSidebar` 신규. `{child_id}_{YYYYMMDD_HHmmss}` 형식 `session_id`. REST API `GET/POST/DELETE /sessions/{child_id}`. 세션 전환 시 마지막 게임 URL 복원.
- **게임 HTML 파일 저장**: `srcdoc` → 파일 저장 + `/games/{child_id}/{session_id}/{game_id}` URL 서빙. React 재렌더 시 게임 중단 버그 해결. 세션당 최신 10개 보관.

### 보안 수정
- 경로 순회 공격 방어: `path.resolve().is_relative_to(base)` 검증
- 하드코딩 자격증명 → 환경변수 이동
- WebSocket `accept()` 순서 수정
- `asyncio.Lock` 동시쓰기 race condition 방어

### 테스트
- 백엔드 pytest: 29개 통과 (`src/backend/tests/test_auth_session_game.py`)
- 프론트엔드 Vitest: 9개 통과 (`src/frontend/__tests__/useChat.test.ts`)

### ADR
- [[auth-session-game-persistence]] — status: proposed → implemented

### 커밋
- `2e9f555` feat: 로그인 + 세션 관리 + 게임 HTML 파일 저장

---

## 2026-04-13 — 클릭 즉시 전송 UI

- Type: decision
- Location: wiki/decisions/click-to-send-ui.md
- From: PromptScaffold 카드 + 힌트 클릭 시 textarea 거치지 않고 즉시 채팅 전송
- 변경 파일: `src/frontend/components/ChatPane.tsx` (handleQuickSend 추가, hint `<p>` → `<button>`)

---

## 2026-04-13 — 모바일 스와이프 네비게이션

- Type: decision
- Location: wiki/decisions/mobile-swipe-navigation.md
- From: 모바일에서 채팅창이 너무 작아지는 문제 → 스와이프 전환 UX 구현
- 변경 파일: `hooks/useSwipe.ts` (신규), `app/layout.tsx`, `app/page.tsx`

---

## 2026-04-12 (16) — 상품 요구사항 인제스트 + 갭 분석

### 내용
- `meeting_notes/production_requirements.md` (R1-R9) 수신
- 현재 구현 대비 갭 분석 완료
- ❌ 미충족: R4(폴백), R7(갤러리), R8(공유), R9(밝은 UI)
- 🔶 부분: R2(타이핑 최소화 — 원클릭 전송 검토 필요)
- ✅ 충족: R1, R3, R5, R6

### 생성 파일
- `kids_edu_vault/wiki/specs/product-requirements.md` — R1-R9 요구사항 + 현황 태그
- `product-requirements-gap-plan.md` (프로젝트 루트) — 갭 해소 구현 계획 (P0/P1/P2)

---

## 2026-04-12 (15) — Unit 7 완료: MVP 통합 확인

### 검증 항목 (MOCK_CLAUDE=1)
- WS 이벤트 시퀀스 (text×N → game → done): PASS
- 세션 독립 (child01 vs child02 동시 접속): PASS
- 5탭 동시 접속 (child01-05): PASS
- /admin/reset 엔드포인트: PASS (mock 세션 미저장으로 false 반환 — 정상)
- `uv run pytest -v` 28개 전체: PASS
- `npm run build` Turbopack 컴파일: PASS

### 볼트 업데이트
- `hot.md` 전면 갱신 (MVP 완료 스냅샷)
- `specs/ai-prompting-literacy-input.md` status → implemented

### 커밋
- `feat: MVP 통합 확인 완료`

---

## 2026-04-12 (14) — Frontend Unit 6 완료: 프롬프트 스캐폴딩 카드

### 완료 내용
- `scaffoldData.ts`: 블록 0-5 교육 목표·스킬·예시 문장 데이터 (이 파일만 봐도 커리큘럼 구조 파악 가능)
- `PromptScaffold.tsx`: 블록별 클릭형 예시 문장 카드 UI
- `ChatPane.tsx` 통합: 카드 클릭 → 입력창 자동 채워짐
- 블록 4(자유 조합)·5(언어화)는 카드 미표시 (자유 입력 유도)
- `npm run build` 통과 확인

### 커밋
- `feat(frontend): 블록별 프롬프트 스캐폴딩 카드`

---

## 2026-04-12 (12) — Frontend Unit 4 완료: 2-pane 레이아웃 + GamePreview

### 완료 내용
- `GamePreview.tsx`: srcdoc + sandbox="allow-scripts" iframe
- `page.tsx`: 채팅 40% | 게임 60% 분할 레이아웃, 임시 테스트 버튼
- `wiki/components/kids-edu-frontend.md` 신규 생성
- 빌드 통과 확인

### 다음 Unit
- Unit 5: ChatPane (WebSocket + 스트리밍)

---

## 2026-04-12 (11) — Frontend Unit 3 완료: Next.js 초기화

### 완료 내용
- `src/frontend/` create-next-app@16 초기화 (TypeScript + App Router + Tailwind)
- 보일러플레이트 정리 (page.tsx, layout.tsx, globals.css)
- 빌드 통과 확인

### 다음 Unit
- Unit 4: 2-pane 레이아웃 + GamePreview (iframe sandbox)

---

## 2026-04-12 (10) — Backend Unit 2 완료: 서버 기동 확인 + 볼트 문서화

### 완료 내용
- `.env.example` 추가 (CLAUDE_TIMEOUT, CLAUDE_MODEL, MOCK_CLAUDE)
- `/health` 응답 확인 완료
- `.gitignore` 수정 (`.env.example` 추적 가능하도록)
- `wiki/components/kids-edu-backend.md` 신규 생성

### 다음 Unit
- Unit 3: Next.js 프론트엔드 초기화

---

## 2026-04-12 (9) — Backend TDD Unit 1 완료: 28/28 테스트 통과

### 완료 내용
- `src/backend/` 초기 구현: `main.py`(FastAPI WebSocket), `claude_runner.py`(subprocess + SessionStore), `personas/TUTOR.md`(W3+W4)
- TDD 테스트 28개 작성·통과: SessionStore(10), _extract_hint(5), _HTML_RE(5), reset_session(2), stream_claude mock(6)
- `pyproject.toml` dev 의존성 추가 (pytest, pytest-asyncio)
- 발견한 패턴: `MOCK_CLAUDE` 같은 모듈 레벨 상수는 `monkeypatch.setattr(module, 'VAR', val)`로 패치해야 함

### 다음 Unit
- Unit 2: `.env.example` 작성 + 서버 기동 확인 → backend 볼트 컴포넌트 페이지

---

## 2026-04-12 (8) — MVP 개발 계획 확정: FastAPI + CLI subprocess + AI 프롬프팅 리터러시

### Why
- 어린이 인터페이스에서 Claude를 어떻게 호출할지 결정. Claude Agent SDK vs CLI subprocess 검토.
- 4/21 스택 결정 게이트 후 4/26 리허설까지 5일밖에 없어 `sanshome_bot/claude_runner.py` 재활용이 유일한 현실적 선택.
- "AI로 게임 만들기" + "AI에게 잘 시키는 법 체득" 두 교육 목표 병행 필요성 확인 → 커리큘럼 + 제품 동시 설계.

### 결정
- 백엔드: FastAPI (Python) + `claude -p --output-format stream-json` CLI subprocess.
- 프론트: Next.js — 채팅 pane + 게임 preview iframe + 프롬프트 스캐폴딩 카드.
- 블록별 프롬프팅 스킬 매핑 (묘사→구체화→추가→수정→자유→언어화) 커리큘럼에 반영 요청.

### 파일 변경
- 갱신: `2026-04-12-mvp-dev-plan.md` — FastAPI 스택으로 전면 업데이트
- 생성: `wiki/specs/ai-prompting-literacy-input.md` — BH 커리큘럼 인풋 spec
- 생성: `wiki/decisions/nextjs-fastapi-wrapper-architecture.md` — 아키텍처 ADR

---

## 2026-04-12 (7) — Subagent 팀 빌드: Dev 4 추가 (architect / implementer / reviewer / tester)

### Why
- 피벗 후 3주 MVP 착수를 위해 개발 파이프라인(설계→구현→테스트→리뷰) 에이전트가 필요. 기존 wiki-ingest/wiki-lint 2개로는 지식측만 커버.
- `build_teams.md` 처방(6개)에서 `debugger`·`docs-writer`는 보류 — pain 축적 시 후행 추가. 과도한 specialist는 자동 위임 신뢰도 저하.

### 팀 구성 (총 6개)
- **Wiki**: `wiki-ingest`, `wiki-lint` (기존)
- **Dev** (신규): `architect`, `implementer`, `reviewer`, `tester` — 전원 `sonnet`, 각 `wiki-query` 스킬 포함.

### 파일 변경
- 생성: `.claude/agents/{architect,implementer,reviewer,tester}.md`
- 생성: `.claude/CLAUDE.md` — 위임 규칙·핸드오프·Bash 스코프·시크릿·주간 루프.
- 수정: 루트 `CLAUDE.md` — "팀 & 워크플로우" 섹션 추가 (6-agent 표, 스킬 인벤토리, 7단계 규칙 표, 표준 흐름 다이어그램, 비용 가드레일).

### 운영 규약 (요지)
- 컨텍스트 시딩: 모든 subagent 첫 작업 전 `hot.md` + 루트 `CLAUDE.md` + 지정 ADR 경로 Read.
- 핸드오프 = 파일 경로 (요약 복붙 금지).
- Bash: `git push`·`reset --hard`·`rm -rf`·전역 설치는 메인만.
- 표준 흐름: architect → implementer → tester → reviewer → (메인 commit) → wiki-ingest/save.

### Open
- Smoke test 미실시 — MVP 착수(=Jay 승인 후 C 진입) 시점에 `@architect`부터 실전 가동 예정.

### Related
- ADR: [[subagent-team-structure]] (proposed, 2026-04-12).
- [[pivot-to-chat-preview-wrapper]], [[fast-implementation-mode]].

---

## 2026-04-12 (6) — JY 내부 결정: 옵션 C→A 단계 진행

- **초기 C**(래퍼 MVP + 운영자 하드코드 계정)로 래퍼 착수, **최종 파일럿 당일은 A**(새 래퍼 정식)로 전환하는 단계 진행안 채택.
- 근거: 파일럿 자체가 "chat-native, 코드-invisible" 포지셔닝 검증이므로 아이 앞에 차별화 UX가 서야 데이터 의미. C에서 멈추면 피드백과 제품 방향 괴리.
- **상태**: JY 내부 결정. Jay 확인 전 — 브리핑 문서 `pivot-briefing-jay.md` 회신 시 변경 가능 (특히 타임라인 리스크 크면 B 철수).
- Updated: [[pivot-to-chat-preview-wrapper]] (현재 실행 방향 섹션 추가), [[hot]], `2026-04-12-pivot-briefing-jay.md`.
- New gate: [[pilot-rehearsal-late-april]]에서 A 준비 상태 검증.

---

## 2026-04-12 (5) — Pivot: code-server+cline → chat+preview 래퍼 리서치·결정

### Context
- 논의: 아이가 AI와 채팅으로 게임을 만드는 데 코드를 볼 이유가 없다 → VSCode 포크(code-server+cline) 구조가 최선이 아니라고 판단.
- 방향: 커스텀 웹 래퍼(좌 채팅 / 우 라이브 프리뷰) + OAuth + 향후 유료화.

### Research filed (3 intel pages)
- [[intel-wrapper-architecture]] — Claude Agent SDK, iframe+srcdoc 샌드박스, Next.js App Router, 코드 숨김 UX 선례.
- [[intel-auth-billing-compliance]] — Clerk/Supabase/NextAuth 비교, Stripe + 포트원 이원화, PIPA 만 14세 미만 트랩.
- [[intel-competitive-landscape-2026]] — bolt/Lovable/v0/Replit/Scratch/엔트리/Khanmigo 비교, 무주공산 3개 파악.

### Decisions (3 proposed)
- [[pivot-to-chat-preview-wrapper]] — 스택 피벗 (기존 [[pilot-env-design]] 부분 supersede).
- [[iframe-sandbox-over-webcontainers]] — 프리뷰 샌드박스 기술 선택 (WebContainers 상용 라이선스 트랩 회피).
- [[parent-gated-signup-first]] — PIPA 대응, 부모 이메일 가입 우선.

### Key findings
- **WebContainers는 상용 라이선스 필요** — bolt.new 모방 트랩. iframe+srcdoc만으로 충분 (p5/canvas엔 Node 불필요).
- **Google OAuth를 아동 주 경로로 삼으면 PIPA 위반 리스크** — 엘리스·코드잇 키즈·구름EDU 전부 부모 계정+자녀 서브프로필 방식.
- **"Chat-native, 코드-invisible, kid-first" 포지셔닝은 무주공산** — Scratch 4.0 AI는 2027+ → 12–18개월 기회 창.
- Claude Agent SDK 전환 시 기존 [[gemini-2-5-flash]] 비용 목표($0.15/세션) 재검토 필요.

### Updated
- [[intel/_index]] — Competitive·Technical References 섹션 채움.
- [[decisions/_index]] — Pending에 3건 추가.
- [[index]] — Decisions(10)·Intel(14) 카운트 갱신.
- [[hot]] — 덮어씀.

### Briefing
- 프로젝트 루트 `2026-04-12-pivot-briefing-jay.md` 작성 — Jay 전달용.

### Follow-up (Jay·JY 결정 필요)
- 모델: Claude vs Gemini (Agent SDK 전환 비용 영향).
- 파일럿 당일 실행 스택: 새 래퍼 vs 기존 code-server (23일 남음).
- MVP 스코프: OAuth·결제를 파일럿 전/후 어디에 둘지.
- 어린이 Google 계정 보유 여부 → 가입 플로우 확정 (기존 blocker 유지).

---

## 2026-04-12 (4) — autoresearch: 소아암 환아 대상 코딩·AI 교육 선례

### Rounds
- 2 rounds, 10 WebSearch, 10 WebFetch (1개 실패: MDPI 403, 1개 unparseable: 한국 KCI PDF).

### Sources filed (9)
- [[case-sickle-cell-coding-study]] — Journal of Intelligence 2026, code.org 11세션 EF 전이 (direct analog).
- [[case-stjude-educational-challenges]] — St. Jude Together 임상 가이드.
- [[case-starlight-therapeutic-gaming]] — Starlight Foundation program description.
- [[case-techquity-pediatric-oncology]] — Pediatric Blood & Cancer 2025 AI+VR 형평성.
- [[case-hospital-pedagogy-framework]] — Hospital pedagogy 3모드/5메커니즘 (Am. J. Tech & Applied 2026).
- [[case-pediatric-onc-infection-control]] — PMC peer-reviewed 감염관리.
- [[case-korean-hospital-schools]] — 국내 4개 어린이 공공전문진료센터 (KCI 2026, partial).
- [[case-academic-continuity-peds-onc]] — Psychosocial Standards (PMC5198902).
- [[case-oep-socioecological-program]] — 호주 OEP 평가 (Continuity in Education).

### Synthesis
- [[research-peds-onc-coding-ed]] — 파일럿 적용 함의 정리.

### Key finding
**우리 파일럿 형식(40명 소아암 환아 단일 90분 AI 코딩 이벤트)의 peer-reviewed 직접 선례는 없음.** 인접 영역 증거는 충분 — 파일럿 설계 4가지 변경([[no-debug-philosophy]] / [[ai-persona-workflows]] / [[single-html-runtime]] / [[combat-vs-cooperative-framing]])은 St. Jude accommodations + Starlight narrative standards와 구조적으로 일치. EF 전이 주장은 증거 부족 → 성과 지표를 **경험·완주율·자기효능감**으로 재정렬 필요.

### Follow-up actions
- ANC 컷오프·사전 문진 양식 의료진 합의.
- 감염관리 프로토콜을 [[pilot-operator-guide]]에 런북 형태 편입.
- 튜터 사전 오리엔테이션 커리큘럼 초안.
- 국립암센터 내부 병원학교 존재 여부 확인.

---

## 2026-04-12 (3) — sans-kids-school-2025 ingest + 병동 재설계 페이지 생성

### Source
- `sans-kids-school-2025/` (2025-08-03 SANS Kids VibeCoding 워크숍 v1.1.2) 검토 및 md 자료 `.raw/sans-kids-2025/`로 복사.
- 복사 범위: `README.md`, `CLAUDE.md`, `CHANGELOG.md`, `workflows/workflow-{1..5}/cursor-rules.md`, `educational-scenarios/*.md`, `workshop-materials/{lecture_script,facilitator-checklist,emergency-troubleshooting,expected-questions,age-based-optimization,workflow-comparison-analysis}.md`, `evaluation/workflow-evaluation-criteria.md`. HTML·이미지·릴리즈 바이너리·setup 스크립트는 제외.

### Created (5 pages)
- Concepts (3): [[no-debug-philosophy]], [[ai-persona-workflows]], [[single-html-runtime]] — Pedagogy 섹션 신설.
- Decisions (1, proposed): [[combat-vs-cooperative-framing]] — 병동 파일럿 서사 전투형→협력형 채택.
- Specs (1, draft): [[pilot-curriculum-adapted]] — 4h → 90분 6블록 재설계.

### Updated
- [[components/sans-kids-school-2025]] — 버전·저자·아키텍처·교수법·병동 변경점 4가지 반영.
- [[concepts/_index]], [[decisions/_index]], [[specs/_index]] — 신규 페이지 등록.
- [[index]] — Decisions/Specs/Concepts 카운트 및 Recent Sources 갱신.
- [[hot]] — 덮어씀.

### 핵심 인사이트
- 원본 워크숍의 전투 서사·Cursor 설치형 배포는 병동에 부적합 → 서사 교체 + [[code-server]] 브라우저형으로 재구성.
- 5종 AI 페르소나 중 W3(속도) + W4(스토리) 합성이 병동에 가장 적합. W3는 [[fast-implementation-mode]]의 원형.
- 원본 자산의 핵심 재활용 포인트는 "게임 템플릿 파일"보다 **교수법 패턴**(no-debug, 30-second rule, 즉시 실행 루프)임.

---

## 2026-04-12 (2) — 개발 문서 관리 확장 + meeting_notes ingest

### Structure
- 볼트 구조 확장: `specs/`, `components/`, `runbooks/`, `concepts/` 4개 도메인 추가.
- 템플릿 4종 추가: `component.md`, `spec.md`, `runbook.md`, `concept.md`.
- 프로젝트 루트 `CLAUDE.md` 및 볼트 `CLAUDE.md` 갱신 예정.

### Ingested (meeting_notes/ 기준)
- Stakeholders (6): [[jay-lee]], [[jinyong-shin]], [[jiwoong-kim]], [[tj]], [[bongho-tae]], [[kiwon-nam]].
- Comms (6): [[2026-01-05-meeting]], [[2026-01-12-meeting]], [[2026-01-19-meeting]], [[2026-01-26-meeting]], [[2026-02-09-meeting]], [[2026-04-11-call-note]].
- Decisions (6): [[regular-meeting-monday-930]], [[discord-for-comms]], [[podcast-format-host-panels-guest]], [[markdown-for-knowledge-share]], [[ai-onboarding-role]], [[fast-implementation-mode]].
- Deliverables (8): [[okr-q2-jy]] + 7개 pilot 작업.
- Components (6): [[code-server]], [[oauth2-proxy]], [[caddy]], [[cline]], [[gemini-2-5-flash]], [[sans-kids-school-2025]].
- Concepts (5): [[hypeproof-lab]], [[mission-driven]], [[tracks-a-b]], [[fundamental-content-teams]], [[ai-native-workflow]].
- Specs (1): [[pilot-env-design]].
- Intel (1): [[environ-kukrip-amsenter]].

### Index/cache
- [[index]] 전면 재작성 — 전체 카탈로그 반영.
- [[hot]] 갱신 — 최근 파일럿 컨텍스트 중심으로 덮어씀.

---

## 2026-04-12 (1) — Scaffold
- Scaffold: `kids_edu_vault/` Mode C (Business/Project) 구조 생성.
- 생성: `index.md`, `log.md`, `hot.md`, `overview.md`.
- 생성: `stakeholders/`, `decisions/`, `deliverables/`, `intel/`, `comms/` 각 `_index.md`.
- 생성: `_templates/` (stakeholder, decision, deliverable, intel, meeting, source).
- 생성: vault 루트 `CLAUDE.md`.
- 2026-05-21 — Added [[dental-supersearch-curriculum-v4]] and [[dental-supersearch-engine-workshop-v2]]: dental supersearch hackathon curriculum combining HYROX-style “원장님을 이겨라” with FDE/SaaS-style internal knowledge capture.## [2026-05-21] spec | 치과 지식 슈퍼서치엔진 v4
- Pages: [[dental-supersearch-curriculum-v4]] · [[dental-supersearch-engine-workshop-v2]]
- v3의 "원장님은 5분, 직원이 주인공" 구조를 유지하면서 산출물을 검색 웹앱 + 원장 검증 로그 + 병원 내부 검색 규칙으로 전환. "원장님을 이겨라" 게임 장치와 7 Assets를 검색스킬 제작 루프로 엮음
- Note: 2026-08-30 hot 캐시 정리 시 log 기록이 없어 이관함
