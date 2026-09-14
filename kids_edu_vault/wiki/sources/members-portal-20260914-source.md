---
type: source
title: "Source — HypeProof Members 포털 스냅샷 2026-09-14"
status: summarized
source_type: internal_web
source_date: 2026-09-14
raw_path: ".raw/members/"
raw_files:
  - ".raw/members/how-we-work.md"
  - ".raw/members/studio-features.md"
  - ".raw/members/meetings-2026-09-14.md"
source_url: "https://hypeproof-ai.xyz/members/"
tags:
  - source
  - operating-model
  - product
  - measurement
created: 2026-09-14
updated: 2026-09-14
related:
  - "[[hypeproof-operating-model]]"
  - "[[six-human-capabilities]]"
  - "[[ai-crew-personas]]"
  - "[[capability-measurement-module]]"
  - "[[2026-09-14-weekly-prep]]"
  - "[[roles-kpi-proposal-20260914]]"
---

# Source — HypeProof Members 포털 스냅샷 2026-09-14

> [!note] 입수 경로
> 세 페이지 모두 **멤버 전용(`noindex`, Google/GitHub OAuth 게이트)**이다. 익명 요청은 `NEXT_REDIRECT → /auth/signin`으로 끊긴다.
> 2026-09-14에 JY가 로그인 상태에서 본문을 추출해 `.raw/members/`에 넣었다. **포털은 정본이 아니라 정본을 연결해 보여주는 읽기 창구**이므로(포털 본문이 스스로 그렇게 선언한다), 여기 정리한 것도 미러다.
> 원본 revision: Studio 요구사항 `67b4adf` (jayleekr/hypeproof-studio) · Harness `6476812` · Studio 기능 페이지 기준일 2026-09-11 · Harness 기준일 2026-09-10.

| 파일 | 원 URL | 분량 |
|---|---|---|
| `how-we-work.md` | `/members/how-we-work` | 486줄 |
| `studio-features.md` | `/members/studio/features` | 2,747줄 (요구사항 289개 원문 포함) |
| `meetings-2026-09-14.md` | `/members/meetings/2026-09-14` | 343줄 |

세 페이지는 서로를 명시적으로 참조한다. 9/14 사전자료가 허브이고, How We Work가 R&R 정의, Studio Features가 제품 상태 근거다.

## 무엇이 새로 들어왔나

1. ⭐ **7 Assets → 6 Capabilities 재구성** (2026-09-13 제품 채택) → [[six-human-capabilities]]
2. ⭐ **운영 모델이 문서화됐다** — 6단계 작업 흐름 · 9개 인간 역할 + KPI · RACI 19행 · 주간 루프 · 6원칙 → [[hypeproof-operating-model]]
3. **AI Crew 5 페르소나**와 위임 3등급 → [[ai-crew-personas]]
4. **역량 측정 모듈**이 Studio 밖으로 분리되는 중 (Studio·Claude Code·Codex 공통 코어) → [[capability-measurement-module]]
5. **Studio·Chalk 기능 현황이 요구사항 단위로 공개**됐다 — 289개 요구사항 / 11개 문서
6. **9/14 회의의 핵심 아젠다 = R&R 제안 공유**, 9/16까지 회신 → [[roles-kpi-proposal-20260914]]

## 이 스냅샷이 볼트의 무엇을 닫는가

| 볼트의 미결 | 이 소스의 답 |
|---|---|
| "회의록의 **신제형** = [[jehyeong]] 여부 확증 전" (8/31~9/6 열려 있었음) | ✅ **닫힘.** How We Work가 **"제형 — 홈페이지 만들기 강의 · 교육 구성·현장 진행·고객 후속 관계"**로 명시하고 10/7 강의 담당으로 배정한다 |
| [[chalk]] `status: proposal` ("아이디어 단계") | ✅ **틀렸다.** Chalk는 **현재 기능 3개 + 로드맵 4개**로 요구사항·검증 근거까지 붙어 있다 → [[chalk]] 갱신 |
| 8/31 "최우선 개발 = 어드민/모니터링" | 🟡 Chalk의 "확정 수업 전달하고 현황 보기"가 그 자리다. 다만 **학생 조건 리허설은 `예정`** |
| [[sediment]] 진행 상태 | ⚠️ **9/7~9/14 main 커밋·머지 PR 0건.** 제품 3종 중 유일하게 이번 주 변화 없음 |

## ⚠️ 볼트와 충돌하는 것

> [!contradiction] 7 Assets가 정본 자리에서 내려왔다 (제품 한정)
> 볼트 정본([[hypeproof-mission]] 미러)과 [[hot]]은 **7 Assets(보는 눈·의도·맥락·검증·위임·반복·주인의식)**를 확정 체계로 싣는다.
> 이 소스는 **2026-09-13부로 신규 제품 개발의 기본 모델이 6개 역량**이라고 적는다. 다만 *"7개보다 측정상 우수하거나 정확히 6개가 정답이라는 연구 결론이 나온 것은 아니다"*라고 스스로 단서를 단다.
> → 층이 갈렸다: **대외·미션 서술은 7, 신규 제품 관찰 모델은 6.** [[six-human-capabilities]]에 대조표를 두었다.

> [!contradiction] "AI가 못 하는 건 테이스트와 오너십"과 Taste의 소멸
> 2026-09-06 회의에서 [[jay-lee]]는 **"세븐 에셋도 중요하지만 결국 AI가 제대로 못 하는 건 테이스트와 오너십"**이라 말했다 ([[2026-09-06-weekly-on-hypeproof]] §3).
> 일주일 뒤 채택된 6개 모델에서 **Taste라는 이름은 사라지고 Judgment로 재정의**된다 — "좋은 결과를 알아보는 눈"에서 "**목적과 기준에 따라 대안을 비교하고 선택 이유를 설명하는 행동**"으로. 미감이 아니라 설명 가능한 근거로 옮긴 것이다.
> 이름이 바뀐 것인지 개념이 바뀐 것인지는 판정이 필요하다. 8/31의 **"AI-인간 거리감 8번째 축"** 제안과 창업 라인 **D-3("8번째 Asset 신설 안 함")**도 이 재구성 위에서 다시 읽어야 한다.

> [!contradiction] TJ에게 배정된 역할이 없다
> 9개 인간 역할 표 어디에도 **[[tj]]**가 없다. 9/6 회의에서 미션 덱을 발표하고 스토리텔링 재구성 액션을 받은 사람이다.
> 누락인지 의도인지 미확인. 사전자료는 "**새로운 제품·역할에 대한 제안도 받는다**"고 열어 두었다.

## 인명 대조

| 포털 표기 | 볼트 페이지 | 확신 |
|---|---|---|
| Jay | [[jay-lee]] | ✅ |
| 지웅 | [[jiwoong-kim]] | ✅ |
| 진용 | [[jinyong-shin]] | ✅ |
| 봉호 | [[bongho-tae]] | ✅ |
| 제형 | [[jehyeong]] | ✅ **확증됨** |
| 조민한 | [[minhan-cho]] | ✅ |
| 광현 | [[jesse-kim]] | 🟡 **강한 정황.** 역할(품질·운영 총괄)이 8/31 [[jesse-kim]] 배정과 정확히 일치하고, 9/6 축어록에서 [[jay-lee]]가 "광연"이라 부르자 Jesse Kim이 답한다. 한글 표기 확증 전 |
| — | [[tj]] | ⛔ 표에 없음 |

## 미확인

- **광현**의 한글 표기와 [[jesse-kim]] 동일인 여부 (영문·한글 병기 필요)
- [[tj]] 역할 누락이 의도인지
- ⚠️ **SK 건 입금 미확인** — 딜 원장 사실확인일이 9/5다. [[ir-20260915-pricing-evidence-audit]]의 정산 자물쇠와 직결
- `roadmap.strategy.json`·`deals.yaml`·`ROLES.md`·`traceability.json` 등 **정본 파일 원문 미확보** (GitHub 링크만 확인)
- Studio **공개 배포 상태** — 기능 페이지가 "별도 확인"이라고만 적는다
