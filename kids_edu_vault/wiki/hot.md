---
type: meta
title: "Hot Cache"
created: 2026-04-12
updated: 2026-09-14
tags:
  - meta/cache
---

# Hot Cache — 2026-09-14

세션 시작 시 가장 먼저 읽는 캐시. **500단어 이내로 유지하고 작업이 끝날 때 덮어쓴다.** 이력은 [[log]], 목록은 [[index]].

---

## 정본 (미션 층은 변동 없음)

- `MISSION.md` = **확정 7/31 · 개정 2026-08-10**. 미러 [[hypeproof-mission]], 근거 [[hypeproof-positioning-reset-20260810]]
- 성공 기준: **사용자가 자기 문제를 AI와 함께 풀었는가** / 사업 정의: **글로벌 사교육 시장에 파는 AI 소프트웨어 회사**

## ⭐ 7 Assets가 6개 역량으로 재구성됐다 (2026-09-13 제품 채택)

[[six-human-capabilities]] — **정본 교체가 아니다. 두 층이 병존한다.**

```
대외·미션 서술 = 7 Assets (정본 유지)
신규 제품 관찰 = 6 Capabilities
```

- **Intent+Context → Framing** · Taste → **Judgment** · Delegate → **Orchestrate** · Iterate → **Adapt** · Verify·Ownership은 경계 구체화. 산술은 Framing 하나뿐, 나머지는 **관점이 좁혀졌다**
- 이유는 **관찰 가능성**: "몇 번 위임하거나 반복했는지만으로는 역량을 설명할 수 없다" → [[asset-pressure-map]]과 같은 진단
- ★ **모델의 핵심은 "이것만으로는 부족" 열**이다 — 에이전트 수·도구 호출 수·재시도 횟수·AI의 통과 선언·제출 클릭. **자동 집계 가능한 지표가 전부 기각됐다.** [[record-issuance-model]]의 대시보드 매트릭이 정확히 여기 걸린다
- ⚠️ [[jay-lee]]가 9/6에 "AI가 못 하는 건 **테이스트와 오너십**"이라 한 지 1주 만에 Taste가 Judgment로 재정의됐다
- 판정 필요: **8번째 축(AI-인간 거리감)** 제안과 **D-3("8번째 Asset 신설 안 함")** — 7→6은 신설이 아니라 통합이라 D-3의 전제가 흔들렸다

## ⭐ 운영 모델이 문서화됐다

[[hypeproof-operating-model]] · [[ai-crew-personas]] · 소스 [[members-portal-20260914-source]]

- 6단계 흐름(철학·미션→Intent→요구사항→설계·위임→구현·검증→증거·학습) · **RACI 19행** · 주간 루프(월 Weekly → 화 회의록 분해→이슈 · ETA 필수) · 6원칙
- **기여 기반 운영** — 상근 조직 아님. "Jay가 사업의 위험과 실행 공백을 맡는다"
- AI Crew 5종의 설계 핵심은 능력이 아니라 **월권 차단**. **Keeper = 우리 `wiki-lint`+`hot`/`log`와 같은 일** (우리가 앞선 것: `[!contradiction]` 형식 / 뒤진 것: **재확인 기한 TTL 필드 없음**)
- ⚠️ **9역할 중 5개가 Jay.** [[chalk]]·[[sediment]] 제품 리드 공석·공모 중

## ⏰ 9/16(수)까지 전원 R&R·KPI 회신

[[roles-kpi-proposal-20260914]] — **제안이지 합의가 아니다. 무응답은 수락으로 처리되지 않는다.**

- [[jiwoong-kim]] **Studio 제품 리드로 승격** · [[jinyong-shin]] 개발 · [[bongho-tae]] 교육·연구(변호사 세일즈에서 이동) · [[jesse-kim]] 품질·운영(제품 총괄에서 축소) · [[jehyeong]] 홈페이지 강의 · [[minhan-cho]] 법무·IP
- ⛔ **[[tj]] 배정 없음** · ⛔ **변호사 채널 담당이 표에서 사라졌다**

## 제품 상태 (2026-09-14)

| | 현재 | 로드맵 | 비고 |
|---|---|---|---|
| [[hypeproof-studio]] | 6 | 7 | 체험판 **'내 삶에 AI 더하기'**. ⚠️ 공개 배포 상태 "별도 확인" |
| [[chalk]] | **3** | 4 | ✅ `proposal` → `active` **정정.** 단 가격 방어 층(게이트·리허설·회고)은 전부 로드맵 — **킥은 아직 없다** |
| [[sediment]] | — | — | ⛔ **9/7~9/14 커밋 0.** 그런데 주간 루프·[[bitree]] 제안·라인업 **세 곳이 전제한다** |

[[capability-measurement-module]] — 코어·기록 계층 머지, **실사용 0건.** 첫 사용자 [[jay-lee]]. 289개 요구사항 / 11개 문서 공개.

## ⚠️ 숫자 — 인용 전 원본 확인

- 🆕 **SK 건 입금 미확인** (딜 원장 사실확인일 9/5) → [[ir-20260915-pricing-evidence-audit]]의 정산 자물쇠와 직결
- 9/6 리허설분 5건 → [[weekly-on-hypeproof-20260906-source]]. **HYROX "188 빌리언 달러"** 오류 · **SK "1회차 800만원" ↔ 확정 견적 920만원**
- 9/5 감사분 3건 → **160분의 분모 미확인** · **가족당 50만원은 검토가, 실제 92만원** · **견적서 판매자가 Bitree**

> **규칙**: 숫자를 인용하기 전 `.raw/` 원본까지 내려가 분모·단위·시점을 확인한다.

## 지금 급한 것

1. ⏰ **9/16(수) R&R 회신** + [[jiwoong-kim]] 창업교육 제안
2. **9/15 IR (D-1)** — 빈칸 5개 → [[ir-20260915-plan]]
3. **9/19(금) 밤샘 프로덕션 세션** → [[production-strategy-session-20260919]]
4. **10/7(수) 치과 워크숍** → [[dental-fullday-website-workshop]]
5. ⛔ **법인·IP 귀속**(시한 8/22 경과, [[minhan-cho]] 역할의 첫 과제) · ⛔ 제3자 강사 0건 · ⛔ 학습자 신원

## 열린 질문

- **7과 6은 언제 합쳐지는가.** 커리큘럼 라인(`curriculum_wiki/rules/`)이 7 기준이다 — **사업 볼트 단독 판정 금지**
- **볼트·포털·[[sediment]] 중 "팀의 기억"은 누구 몫인가** — 셋 다 자처하는데 정해지지 않았다
- ⚠️ 성공 사례의 정의 미합의 · 측정 규격 분열(4/5/7축에 **6축 추가**)
- 전문직 채널에서 [[bitree]] 몫 · 🕯️ [[hypeproof-philosophy]] 승격 여부
- **광현** = [[jesse-kim]] 표기 확증 (역할·9/6 호명으로 강한 정황)

## 운영 규칙

> **정본 인용 전 `git fetch`.** · 회의 **축어록은 커밋하지 않는다** (`.gitignore`: `*Notes by Gemini (1).md`)
> **문서 전달자를 작성자로 기록하지 않는다.** ([[hypeproof-philosophy]] 오귀속, 9/14 정정 — 작성자는 [[jay-lee]])
> **기록이 없다고 미실행으로 단정하지 않는다.** *확인 필요*와 *확인된 0*은 다르다 (포털 운영 원칙)

## 자주 여는 곳

[[hypeproof-mission]] · [[six-human-capabilities]] · [[hypeproof-operating-model]] · [[roles-kpi-proposal-20260914]] · [[2026-09-14-weekly-prep]] · [[2026-09-06-weekly-on-hypeproof]] · [[chalk]] · [[ir-20260915-plan]]
