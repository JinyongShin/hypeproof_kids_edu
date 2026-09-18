---
type: meta
scope: common
title: "Curriculum Index"
created: 2026-08-08
updated: 2026-08-08
tags:
  - meta/index
  - curriculum
---

# Curriculum Index — 커리큘럼 지식 위키

`curriculum_wiki/`의 마스터 카탈로그. 문서 추가 시 이 파일을 갱신한다.

> **이 트리는 무엇인가**: 커리큘럼과 강의를 만들기 위한 **지식을 축적하고, 그 지식으로 만든 커리큘럼을 축적하는 곳**.
> 사업·기술·제품 문서는 `wiki/`에 있다. 용도 구분은 `kids_edu_vault/CLAUDE.md` 참조.

## 두 라인 — 지식은 공유, 작업 상태는 분리

이 트리에는 **라인이 둘** 있다. 라인은 **`scope` 필드로 구분되며 폴더를 나누지 않는다.**

| 라인 | `scope` | 접두사 | 작업 파일 |
|---|---|---|---|
| 11~16세 AI 교육 | `edu-11-16` | `edu-11-16-` `ped-` | [[curriculum-hot]] · [[curriculum-log]] |
| 고등학생 창업·IR | `startup-ir` | `startup-` | [[startup-hot]] · [[startup-log]] |
| **공유 자산** | **`common`** | `m-` `kr-` 또는 없음 | (라인 로그에 기록) |

> **왜 폴더를 안 나누는가**: 두 라인은 `scope: common` 26건(헌법·방법론 카드·지도안 규격·근거 등급)을 공유한다. 복사하면 두 진실이 생기고 참조하면 이름만 분리다. **라인은 축이지 트리가 아니다.** 경합하던 것은 지식이 아니라 작업 상태였으므로 `hot`·`log`만 쪼갰다. → 값·접두사 규칙은 [[curriculum-schema]]

## 축적 구조

```
지식        methods/ · research/ · gaps/
  ↓
게이트·규칙  rules/ · design/
  ↓
부품        activities/ · assets/
  ↓
산출물      curricula/          ← 완성된 트랙·지도안이 여기 쌓인다
```

## methods/ — 교수학습 방법론 (15) · `scope: common`

- [[methods-index]] — **선택 가이드**. 목표 → 선행지식 → 제약 3단계
- [[evidence-standards]] — 근거 등급 기준. 효과크기 서열화 금지

**방법론 카드 8종**
- [[m-explicit-instruction]] (A) · [[m-guided-discovery]] (A) · [[m-cognitive-apprenticeship]] (B) · [[m-problem-based-learning]] (B) · [[m-cooperative-learning]] (A) · [[m-formative-feedback]] (A) · [[m-poe]] (B) · [[m-project-based-learning]] (B)

**국내 모형 지도 5종** (등급 D — 소통·정렬 도구, 효과 근거로 미사용)
- [[kr-instructional-models-map]] (진입점) · [[kr-models-korean]] · [[kr-models-science]] · [[kr-models-social-moral-math]] · [[kr-models-cooperative]]

## research/ — 조사·근거 (17)

**창업·IR 라인** (`scope: startup-ir`) — 고등학생 대상. 기존 11~16세 라인과 **별개 라인**
- [[startup-minor-legal-boundary-kr]] — 법적 상한. **민법 제8조 영업 허락**이 지렛대
- [[startup-youth-competition-kr]] — 청소년 창업경진대회 심사 배점(**벤치마크**). 아이템 30점 / 과정 70점
- [[startup-modoo-project-kr]] — 모두의 창업(중기부, **벤치마크**). 실제 IR 3단계 + **대필 형사조항**
- [[startup-ir-deck-structures]] — Sequoia · YC · **PSST** 3계보. 산출물 규격 후보
- [[startup-yeep-benchmark-kr]] — 국가가 **무료로 이미 제공하는 것**. 우리 하한선
- [[startup-yeep-deep-read-kr]] — **정독**. 8단계 모형 / AI는 주제일 뿐 / 성실한 실패 / 평가 체계의 빈칸
- [[startup-yeep-resource-manifest]] — YEEP 자료실 전수 목록·재수집 방법 (203건)

**L0 사이클 ① 기존 주장 출처 검증**
- [[ped-adolescent-cognitive-development-verification]] — 형식적 조작기 **기각** / 자기평가 정확도 지지
- [[ped-youth-ai-chatbot-statistics-verification]] — 94.4% **조건부** / "5명 중 1명 매일" **기각**
- [[ped-llm-minor-age-policy-20260808]] — 모델 연령 정책. **Lv1 계정 전제가 뒤집힘**

**L0 사이클 ② 교수법·시장**
- [[ped-korea-elementary-ai-usage-2026]] — **Lv1 시장 근거**
- [[ped-scaffolding-fading-srl]] — 금지 개입 정식화 근거
- [[ped-backward-design-ubd]] — 지도안 작성 순서 근거
- [[ped-session-format-attention-group-size]] — 회차 포맷·정원
- [[ped-ai-literacy-standards-kr-intl]] — 국내·UNESCO 성취기준
- [[ped-cognitive-acceleration-case]] — CASE, 가장 가까운 선례
- [[ped-premium-private-education-benchmark-kr]] — 가격 벤치마크

## rules/ — 게이트·규칙 (9)

- [[edu-constitution]] — **절대 하지 않는 것 11조.** 참고 지침이 아니라 게이트
- [[prohibited-moves]] — 강사 금지 개입 4계열
- [[placement-rules]] — 배치 제약 C-1~C-9
- [[measurement-axes]] — 측정 5축 × 3수준
- [[curriculum-schema]] — 프론트매터 스키마 + **`scope` 값 체계** + **파일명 접두사** + lint 12개
- [[edu-11-16-track-architecture]] — 상품별 독립 완결 트랙
- [[edu-11-16-session-format]] — 회차 포맷 (`provisional`)
- [[edu-11-16-evidence-capture]] — 관찰 기록 수집 주체
- [[edu-11-16-parent-track-ip-boundary]] — 파트너 IP 경계, `ip_owner` 판정

## design/ — 지도안 설계 (2)

- [[lesson-plan-authoring-guide]] — 작성 순서·12절 규격·강사 자유도
- [[lesson-plan-quality-checklist]] — 3관문 검증

## gaps/ — 미해결 (5)

- 🆕 [[ruling-pedagogy-gate-implementation]] (`common`) — **조항 4건이 제품 검사로 구현됐다.** lint 2가 첫 구현체를 얻었다. 되돌아온 판정 요구 2건 — `prerequisites`의 의미 · 성인 라인 `scope` 값
- [[edu-11-16-research-plan]] — 조사 계획·진행 상황·미조사 목록
- [[ruling-profile-based-differentiation]] — `.raw` 승격 판정
- [[ruling-startup-ir-asset-alignment]] — 창업·IR 라인 자산 승계 판정. **7 Assets 전면 / No-Debug 미승계**
- [[ruling-startup-ir-target-and-scope]] — 창업·IR 목표·채널·진입 구간. **국가 대회는 목표가 아니라 참고 자료**

## activities/ · assets/ · curricula/ — 아직 비어 있음

- [[activities-index]] — 활동 원자 (30~60분 단위)
- [[assets-index]] — 사전 생성 데이터셋·카드덱·워크북
- [[curricula-index]] — **완성된 트랙·지도안**

## 관련

- 11~16세 라인: [[curriculum-hot]] · [[curriculum-log]]
- 창업·IR 라인: [[startup-hot]] · [[startup-log]]
- `wiki/index.md` — 사업·기술·제품 문서
