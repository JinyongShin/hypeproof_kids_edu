---
type: meta
scope: edu-11-16
title: "Curriculum Log"
created: 2026-08-08
updated: 2026-09-18
tags:
  - meta/log
  - curriculum
---

# Curriculum Log

`curriculum_wiki/` 변경 이력. 최신 항목이 위. **추가 전용 — 과거 엔트리 수정 금지.**

---

## [2026-09-18] ruling | 조항 4건이 제품 검사가 됐다 — lint 2 첫 구현
- Source: `hypeproof-studio` PR `#1115`(외부 저장소, **이 세션이 직접 확인하지 않음**) + `scratchpad/chalk-scan/gate-check-source-mapping.md`
- 생성: [[ruling-pedagogy-gate-implementation]] (`gaps/`, `type: ingest-ruling`, **`scope: common`** — 두 라인 공통 사안)
- 판정 **`adopt`**: 조항을 바꾸지 않고 채택됐다. **규칙 문서를 제품에 복사하지 않았고** 코드 주석에 조항 ID·경로·짧은 인용까지만 남겼다 → **이 볼트가 여전히 정본이다**
- ⭐ **[[curriculum-schema]] lint 2가 첫 구현체를 얻었다.** 제품의 `step_evidence` 검사와 **대상·방식·수준(경고)까지 일치**한다. 문서의 *"lint 1~12 전부 미구현"* 문장을 정정했다 — 단 **구현은 이 볼트가 아니라 다른 저장소에 있다**
- [[lesson-plan-quality-checklist]] 관문2-2·2-6·2-9가 제품 검사 3종으로 나갔다. 2-9는 **±10분 임계값까지 조항에 있어** 제품이 새로 정할 것이 없었다
- ⛔ **되돌아온 판정 요구 ①** — `prerequisites`의 의미가 미확정인데 **그것이 유일한 실질 차단 검사**다. 자산 의존 관계([[placement-rules]] `requires`) ↔ 학습자 선행지식([[methods-index]] §선택가이드 2단계) 두 후보가 코드 주석에 병기돼 있다. **두 층을 함께 확정해야 한다** — 조항의 의미는 이 볼트가, `session-design`의 `prerequisites` 칸이 무엇을 담는가는 제품(`CH-01` 유래)이 정한다. 어긋나면 관문이 엉뚱한 것을 검사하고, 한쪽 몫으로만 적어 두면 **서로 정했다고 여겨 아무도 안 정한다**
- ⛔ **되돌아온 판정 요구 ②** — **관문1(헌법)을 켜지 못했다.** [[edu-constitution]]이 아동·청소년 전제인데 제품 범위에 **성인 전문직 수업**이 있다. 켜면 성인 수업이 A-4·B-1에 걸리고, 끄면 아동 수업에서 헌법이 작동하지 않는다. **정확도가 아니라 정합성 문제.** `scope`에 성인 라인 값이 없다 — 제품 쪽 `CR-EDU-08`과 같은 사안
- ⚠️ **관문2-4(금지 개입 4계열)는 관문2에서 유일하게 "필수. 없으면 미완성"인데 제품에 필드가 없다.** [[prohibited-moves]]가 설계한 *"강사 매뉴얼은 그 필드에서 자동 생성된다"*가 아직 성립하지 않는다
- 📌 **드러난 것: 검사 대상 인스턴스가 이 볼트에 0건이다.** `activities/`·`assets/`·`curricula/`가 비어 있어 회귀 샘플을 커리큘럼 위키에서 가져올 수 없었고, 제품 데모는 사업 볼트의 `wiki/specs/track-b/` 수업 문서를 원재료로 썼다. **조항은 밖에서 먼저 실행됐고 정본 쪽에는 걸어 볼 부품이 아직 없다**
- 자산 변경: [[curriculum-schema]](lint 절 정정) · [[lesson-plan-quality-checklist]](자동화 절) · [[curriculum-index]](gaps 4→5)

---

## [2026-08-30] intake | 정본 8/10 개정이 이 라인에 준 영향
- Source: `wiki/` 정본 미러 [[hypeproof-mission]] · 대조 분석 [[mission-product-alignment]] (원본: `hypeprooflab/MISSION.md` 개정 2026-08-10)
- 갱신: `curriculum-hot` — "사업 쪽에서 들어온 것" 섹션 추가. 이 라인 문서는 신규 생성 없음
- 들어온 것: **7 Assets 정본 명칭 확정**(검증·위임·반복·주인의식) / [[measurement-axes]]의 5축 논리가 **8축 통일 제안**으로 사업 쪽에 올라감 / 미션 성공 기준이 **"자기 문제를 AI와 함께 풀었는가"**로 변경 / 사용자·구매자 분리 / 증거 제품 라인 신설
- 판정 필요: 이 라인 문서들의 축 명칭을 정본에 맞출 것 · 지도안 목표 서술을 새 성공 기준으로 재검토할 것
- ⚠️ 경계: 정본이 "7가지"를 명시하므로 **8축은 정본 개정 사안**이다. 이 라인이 단독으로 확정할 수 없다. 미결이던 "조직 표준 확장 제안 담당"이 여전히 비어 있고, 이제 그 미결이 정본 개정 담당 문제로 커졌다
- Key insight: 이 라인이 2026-08-08에 "거리 축 부재는 조직 표준의 결손"이라고 적어둔 지적이, 사업 쪽 대조 작업에서 그대로 채택돼 통일 제안의 근거가 됐다. 라인에서 세운 논거가 조직 표준을 움직이는 경로가 실제로 작동한 첫 사례다. 다만 담당이 없어 여전히 문서에만 남아 있다.

## [2026-08-17] rules | scope 값 체계 + 파일명 접두사 정식화
- Pages: `curriculum-schema` (scope 값 체계·접두사 2종·lint 10~12 추가), `curriculum-index`
- 재판정: 28건 → `scope: common` / 작업 파일 라인 분리(`startup-hot`·`startup-log` 신설)
- Key insight: 라인이 하나일 때 붙인 `scope: edu-11-16`이 40건에 그대로 남아 **`edu-constitution`(헌법)조차 형식상 창업·IR 라인에 적용되지 않는 상태**였다. 게이트 문서가 라인 전용으로 잠겨 있으면 게이트가 아니다. 라인을 볼트로 쪼개는 방안도 검토했으나, 두 라인은 `common` 28건을 공유해 결합도가 높다 — 복사하면 두 진실이 생기고 참조하면 이름만 분리다. **라인은 축이지 트리가 아니다.** 경합한 것은 지식이 아니라 작업 상태였으므로 `hot`·`log`만 쪼갰다. `measurement-axes`·`placement-rules` 등 4건은 본문을 읽어야 판정되므로 규칙과 어긋난 상태로 명시해 남겼다.

## [2026-08-08] split | curriculum_wiki 분리 신설
- 이전 위치: `curriculum_wiki/**` (33), `curriculum_wiki/research/ped-*` (10), `wiki/decisions/edu-11-16-*` (4), `_templates/` (4)
- 신설: `curriculum-index`, `curriculum-log`, `curriculum-hot`, 폴더 8종
- 삭제: 오버라이드 3건 + `override-protocol` + `_templates/override`
- Key insight: 위키를 사업 볼트와 지식 볼트로 나눴다. 오버라이드 프로토콜은 "기존 조직 문서와의 관계"를 기록하는 장치였는데, 그 결론(무순위·합성점수 금지·5축)이 이미 헌법과 측정 문서에 흡수되어 있어 삭제해도 지식을 잃지 않는다. 남은 것은 조직 표준 4축 확장 제안 하나이며 사업 볼트 과제로 넘겼다.

## [2026-08-08] asset | 방법론 라이브러리 + 국내 모형 지도
- Pages: `methods/` 15건 (카드 8 + 국내 지도 5 + 선택 가이드 + 근거 기준)
- Key insight: 발견학습 논쟁의 결론은 "발견이냐 설명이냐"가 아니라 "안내가 있느냐"다. 비유도 발견은 명시적 수업보다 나쁘고(d=-0.38) 유도된 발견은 낫다(d=+0.50). 국내 "문제 해결 학습 모형"은 서구 PBL이 아니라 안내된 발견에 가깝다. Builder 트랙은 Problem-Based가 아니라 Project-Based다.

## [2026-08-08] research | L0 사이클 ①·②
- Pages: `research/` 10건
- Key insight: 검증 대상 5건 중 2건 기각, 1건 조건부, 1건이 설계 전제를 뒤집었다. 사이클 ②에서 Lv1 시장 근거를 확보하고 금지 개입 정식화 오류를 발견했다.

## [2026-08-08] scaffold | 자산 레이어 최초 구축
- Pages: 헌법, 금지 개입, 측정 축, 배치 제약, 지도안 규격·작성법·검증, 스키마, 결정 4건
- Key insight: 강의 한 벌을 통짜로 쓰면 재조합이 안 된다. 활동 원자로 쓰고 "강의 한 벌"은 컴파일 인스턴스로 취급한다. 목표는 강의가 아니라 강사가 자기 상황에 맞게 조립할 수 있는 상태다.
