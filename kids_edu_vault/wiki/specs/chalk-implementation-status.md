---
type: spec
title: "Chalk 구현 현황 (2026-09-15 기준)"
status: in-progress
owner: "[[jinyong-shin]]"
created: 2026-09-15
updated: 2026-09-15
raw_path: ".raw/chalk-studio-issues-prs-20260915.md"
base_commit: "04f03d061617e6d88e9f2b68eaa82c9933540aa5"
tags:
  - spec
  - chalk
  - product
  - implementation
related:
  - "[[chalk-pedagogy-gate]]"
  - "[[chalk-studio-architecture]]"
  - "[[chalk-entry-point-20260918]]"
  - "[[chalk]]"
  - "[[chalk-requirements]]"
  - "[[chalk-requirement-coverage-audit]]"
  - "[[requirement-id-index]]"
  - "[[chalk-target-shape-proposal]]"
  - "[[capability-measurement-module]]"
  - "[[hypeproof-studio]]"
  - "[[production-strategy-session-20260919]]"
---

# Chalk 구현 현황 (2026-09-15 기준)

> **무엇이 되어 있는가** (기능 단위). 짝 페이지 둘 — **무엇이 필요한가** → [[chalk-requirements]] · **요구사항 단위로 되어 있나** → [[chalk-requirement-coverage-audit]].
> 원본 `.raw/chalk-studio-issues-prs-20260915.md` (studio 세션, 2026-09-15 · **2차 재검증판**). `jayleekr/hypeproof-studio` 기준 커밋 **`04f03d0`** (main = origin/main, 2026-09-15 20:08 KST, 작업 트리 clean·stash 없음) + `gh issue/pr` 실제 조회 + 운영 `/health` 실측.
> 번호는 전부 `jayleekr/hypeproof-studio` 기준이다.

> [!note] 1차 조사는 clean이었지만 최신은 아니었다 (2026-09-15 재검증)
> 1차 기준 커밋 `4195faa`는 origin/main보다 **9커밋 뒤**였다(ahead 0). fast-forward 후 `04f03d0`.
> 그 9커밋은 전부 #1020·#1049 측정·리뷰 레인이고 **`chalk/`를 건드린 것은 0건**, Chalk 요구사항·테스트·ADR·마이그레이션은 **바이트 동일**, 운영 health도 동일했다. **아래 사실은 그대로 유효하다.**
> 예외 1건: `65a15c7`(#1066)이 **`HC-09`를 신설**했다(HAIN7 폐지) → [[chalk-requirements]] CR-CAP-12. `docs/studio-requirements.md`는 끝에 28줄이 붙었으나 **`REQ-M38`은 불변** — AE-09 UNMET 판정 그대로. 대조 내역 → [[chalk-requirement-coverage-audit]] §최신성

| 조회 항목 | 실측값 |
|---|---|
| `chalk.hypeproof-ai.xyz/health` | `c0.0.0-dev+f5939d9` · env production |
| `api.hypeproof-ai.xyz/v1/health` | `w0.0.0-dev+880a13d` · env production |

## 1. 코드가 어디에 있나

`chalk/`는 **독립 Cloudflare Worker**(`hypeproof-chalk`, 태그 접두사 `c*`)로 배포된다. 저장소 내 디렉토리 하나다.

**살아 있는 화면 10개** — `/`(→`/console`) · `/console` · `/start` · `/issuer` · `/board`(10초 폴링) · `/authoring` · `/manage` · `/sharing` · `/budgets` · `/learn`. 페이지 자체는 공개이고 **페이지가 하는 API 호출이 강사 Bearer를 나른다.**

**Chalk가 직접 답하는 것**은 읽기 API 4종(`/admin/cohorts/:id/state|board|logs|logs/:seat`)뿐이고, 로그 원문 회수는 **operator 전용**이다. 나머지(`/v1/profile`, `/v1/classroom/*`, 강사 쓰기 `/admin/*` 전부)는 Service로 **포워딩**한다.

> [!key-insight] CR-DEF-04가 코드 수준에서 이미 집행되고 있다
> `chalk/src/index.ts` 헤더 주석이 Chalk에 **의도적으로 없는 것**을 명시한다 — 세션/명단/일시정지/취소 상태에 대한 **모든 쓰기**, **모든 토큰 서명**, admin-password 경로, cron.
> 인증 검증은 `chalk/src/shared.ts`가 Service의 `instructor-auth.ts`·`tokens.ts`를 **재수출**하며 구현을 복사하지 않는다. [[chalk-requirements]] CR-DEF-04("Service가 권한·토큰 서명을 소유")는 요구사항이기 전에 이미 구조다.

D1 테이블 3개(`worker/migrations/0002-chalk-authoring.sql`, idempotent): `authoring_drafts`(PK cohort+course, revision CHECK≥1, request_id/hash) · `authoring_versions`(**버전 키는 갱신되지 않음**) · `authoring_independent_courses`(초안 insert와 **같은 D1 batch**). 교실 관리·공유는 마이그레이션 0003.

테스트 자산: `chalk/test/` 10종(보드 임계값·배포 격리·인증 drift lock 포함, 2026-08-22 운영 usage_log **동결 fixture**) · `worker/test/` 3종 · `e2e/` 3종(Chromium → Chalk → 실제 Service → SQLite, 실기 Mac 셸).

> 📇 두 저장소 정본의 **요구사항 ID 767개 전수 인덱스** → [[requirement-id-index]] (코드·원문·정의 위치·구현 상태 한 행씩)

## 1.5 요구사항 단위로 보면

정본 ID **75개** 전수 대조 결과 — **구현 19 / 부분 32 / 미구현 17 / 미확인 7** → [[chalk-requirement-coverage-audit]].

★ **가장 큰 칸은 미구현(22.7%)이 아니라 부분(42.7%)이다.** 상태는 "안 만들었다"가 아니라 **"연결은 했고 계약을 아직 못 지켰다"**다. 그리고 **미구현 17건 중 12건이 #1012·#1015·#1016·#1017 네 개의 열린 실행 단위 이슈 안에 이미 담겨 있다.**

⚠️ 감사가 추가로 드러낸 것 — **`config/traceability.json`에 이 요구사항 ID가 하나도 없다**(노드 89개 전수 조회, 0건 매치). 파일 자신이 *"Bootstrap scope only"*라 적는다. 이슈 **#996**의 사각지대와 같은 종류이며, 그래서 감사 근거는 전부 코드·테스트에서 직접 찾았다.

## 2. 되는 것 — 실행된 검증 근거가 남은 것

| 항목 | 근거 |
|---|---|
| Service 소유 초안/확정버전 API — 소유자·코호트·프로필 범위 검사, revision CAS, 재시도 멱등, 불변 버전 | #705/#706, ADR 0004. `authoring.test.mjs` 19개 PASS + 실제 workerd/D1 PASS |
| `/authoring` 화면 — 가져오기·편집·저장·재열기, **409에서 로컬 편집 보존**, 401/403 음성 대조군, 모바일 5폭 | #712/#716, `e2e/chalk-authoring` PASS |
| **확정 버전의 학생 전달** — course/version/content-digest를 참여 자격에 서명. **초안 수정이 이미 발급된 자격을 바꾸지 않음** | #739/#740 |
| 수업별 **모델 좁히기** + 학생 입력창 전환 (Sonnet/Opus/Haiku 9버전, 대화 문맥·미전송 초안 유지) | #792/#795, ADR 0006 |
| 수업별 **기능 좁히기** — `features:{allowed}` 6키(read·write·shell·subagents·browser·web_search), 카탈로그를 컴파일된 프로필에서 파생 | #809, ADR 0007 + 강사 picker #813 |
| 확정 수업의 **고정 AI 표시 이름** (불가시·bidi·lone surrogate 거절) | #759 |
| 교실 관리 + **자발적 공유·피드백·철회** — 성인 명시 동의, 지정 수신자, 만료 한정, 열람 감사, 학생 확인 | #732/#733 + 실기 브라우저 인수 #742/#743 |
| 라이브 보드 — 명단 전원 렌더, **메타데이터 전용**, 임계값이 서버에 있고 응답에 함께 실림 | #674/#691. 운영 SQL을 실제 SQLite 행에 돌려 대조군이 깨지는지까지 증명 |
| studio-logs **읽기** 경로 — 도착 확인, 명단 diff, operator 전용 원문 회수 | #680/#691. 이 워커에 R2 `put`/`delete`가 **없음**을 drift lock이 단언 |
| 예산 화면 · 수업별 처리 수준(effort) | #856/#866 · #839 |
| 강사 온보딩 `/start` + 배포 시 마이그레이션 0002·0003 순차 적용 | #735/#736 |
| **프로필 비종속 초안 저장** + 검수된 실행 템플릿만 결합 | #1006 IC-01/02 → PR #1027 |

## 3. ⛔ 안 되는 것 — 저장소 원문이 명시적으로 부인하는 것

> [!warning] 관문의 핵심 3개가 전부 `planned` 리터럴이다
> `chalk-authoring.md`: *"Rehearsal evidence, settings pins and activation **remain planned**."*
> 확정 문서는 `rehearsal:not_run`, `activated:false` **리터럴**을 가진다.
> ADR 0004: *"no activation" / "A frozen document is not a successful rehearsal or an active class" / "**Freezing stores an unverified snapshot, not a deployable class**."*

| 항목 | 원문 근거 |
|---|---|
| **리허설 증거** (학생 조건 실행 → 버전 귀속) = `RUN-01`·CR-GATE-08 | `planned` |
| **활성화(activation)** | ADR 0004 "no activation" |
| **설정 핀** (도구·예제·설정 버전 고정) = `ENV-03` | `planned` |
| **리허설 무효화 T-07** / **진행 중 수업의 버전 바인딩 T-08** | `docs/testing/`: "NOT RUN and not implemented by this slice" |
| 학생 Electron 실기 참여 · 공개 배포 증거 | "instructor UI evidence, not student Electron" |
| **내부 기능 요청 큐** = `REQ-01~04` | 지원 요청은 **미제출 GitHub 초안**을 열 뿐. "GitHub request preparation is **not receipt**" |
| **독립 강의 개설 IC-03** | PR #1027이 IC-01/02만 덮음 |
| **운영 레지스트리의 활성 실행 템플릿** | PR #1027: **"배포되는 레지스트리에서 활성화된 템플릿은 0개"** |
| 반 단위 개설 엔드포인트 (IC-B B2) | PR #1037(OPEN): 머지 직후에도 `authoring_openings`는 비어 있음 |
| **AE-09** (조작된 클라이언트에 대한 도구 경계) | REQ-M38: "**AE-09 는 이 경로에서 UNMET 으로 확정한다**" |
| 보드 `failures_*` · `heartbeat` 열 | 운영 반영·좌석 릴리스 전까지 `null`/`unknown`. 거짓 음성 대신 unknown으로 렌더 |
| 자동 강의 생성 · 임의 MCP 설치 · **원격 수정** = `CLS-04` | §첫 구현 경계: "후속이다". ⚠️ 게다가 `classroom-admin.md:55`가 **"학생 파일 원격 수정은 이 계약으로 허용하지 않는다"**고 못 박아 **요구사항끼리 부딪친다** → [[chalk-requirement-coverage-audit]] |
| **단계별 도움 모드** = `EDU-02` | `session-design.ts:106`이 단계 키를 **정확히 5개로 제한** — `help` 키가 main에 아예 없다. 추가 PR #1028은 #1036에 막힘 |
| T-24~46 시나리오 | PR #1024(OPEN): "새 시나리오는 모두 NOT RUN" |
| 세션 로그 삭제 | `chalk/README.md`: "no deletion — explicitly out of scope" |

> [!key-insight] "활성 템플릿 0개"가 근거까지 확인됐다
> [[chalk-target-shape-proposal]]이 *"검수된 실행 템플릿 0개라 독립 강의가 실제로는 안 열린다"*고 판정한 대목이, PR #1027 본문의 **"운영 활성 템플릿 0개이며 활성화는 별도의 관리자 결정"**으로 1차 근거를 얻었다. 코드가 다 들어가도 **관리자 활성화 전에는 열리지 않는다.**

## 4. ⚠️ 배포 부채 — 운영이 main보다 뒤처져 있다

- **Chalk 운영 = `f5939d9`(PR #795, 2026-09-08)**. 이후 main에 머지됐으나 **운영에 없는 `chalk/` 변경 4건**:

| 커밋 | PR | 강사가 못 보는 것 |
|---|---|---|
| `0e3f399` | #813 | 강사 기능 picker |
| `2a29fcb` | #839 | 수업별 처리 수준 |
| `e7a26b1` | #866 | 위임 예산·참가자 이용 |
| `c36b574` | #1027 | 프로필 비종속 초안 + 실행 템플릿 |

- **Service 운영 = `880a13d`, main보다 28커밋 뒤.**
- 배포 경로: `git tag c0.1.0 && git push origin c0.1.0` → `deploy-chalk.yml`. 테스트 → typecheck → `chalk/`만 배포 → `/health`가 태그를 보고하는지 확인 → **Service `/v1/health` 버전이 전후로 동일한지 단언**. 첫 롤아웃 순서는 **Chalk 먼저, 그 다음 Service**(역순이면 `/console`·`/issuer`가 없는 호스트로 리다이렉트).
- ⚠️ **이 지연이 의도된 보류인지 단순 누락인지 `미확인`** — 관련 결정 기록이 없다.
- `.claude/rules/verification.md`의 "설정은 맞는데 동작이 없는" 유형이 그대로 적용된다 — 프로필 → 워커 직렬화 → 클라이언트 정책 **세 계층 중 하나만 끊겨도** 기능이 설정된 것처럼 보이며 죽는다.

## 5. 차단 체인

```
#1028 (도움 방식을 확정 수업에 묶기) ← #1036 (편집기가 화면에 없는 단계 키를 지운다) ← #1005 (같은 step() 줄을 다시 씀)
#1006 IC-03 (수업 개설) ← #1037 (IC-B B1, OPEN) ← #1027 (IC-01/02, 머지)
독립 강의 확정·개설 ← 관리자의 템플릿 활성화 결정 (운영 활성 0개)
보드 failures_* ← 태스크 B 운영 반영 + HPS_ERROR_SIGNAL_FROM
보드 heartbeat  ← 태스크 E가 좌석이 실제 돌리는 Studio 릴리스에 진입
bohee 인증 발급 ← 운영자 인증 복구
#1018 ← #718 환경 대기 (#718 내용 미확인)
```

> [!warning] #1036 — 오늘 강사가 제목만 고쳐도 도움 설정이 사라진다
> `authoring.html`의 `step()`은 id/title/instructions/hint/acceptance만 렌더하고 `content()`가 각 단계를 `[data-field]` 컨트롤로만 재구성한다. **편집기가 렌더하지 않는 단계 키는 저장 시 조용히 삭제된다** — `steps[].help`가 지워져 확정 수업이 도움 제안을 못 싣는다. 실제 브라우저→Chalk→Service→SQLite로 재현된 결함(X2 P1).
> 합의된 수정: `{...original, ...renderedFields}` + *"도움 방식 설정 있음 — 이 화면에서는 편집할 수 없고 저장 시 유지됩니다"* 읽기 전용 표시. **이 화면에 도움 모드 편집 UI는 넣지 않는다.**

## 6. 이슈·PR 전수

### OPEN 이슈 (Chalk 직접)

| # | 무엇 |
|---|---|
| **732** | ADM-01~14 우산. #733/#736/#738/#740/#743 완료 체크. **마지막 "Service/Chalk 배포" 미체크** |
| **805** | 배포 후 health 버전 전파 대기 검증. run 34262370838에서 업로드 성공 직후 health가 이전 버전을 읽어 실패 → **상한 있는 polling** (sleep 후 무조건 성공·검사 제거는 본문이 금지) |
| **1006** `wip` | 기존 기관 프로필에 종속되지 않는 새 강의 개설. **작성 권한과 실행 권한 분리** |
| **1007** | Studio·Chalk 전체 요구사항·실행 작업 발현 (원문 hash + ID 고정) |
| **1036** | `[CH-1]` 편집기 단계 키 소실 결함 (§5) |
| **1068** `wip` | 한국어 LLM 입문 강의를 기존 Studio HTML 미리보기로 전달 — **Chalk 기능 개발에 강의를 막지 않고** 작성 공백을 요구사항으로 기록 |
| **562** | `[NEW-12]` Chalk 세션 파일 import v0 — 남이 만든 세션을 Studio가 읽는다. 의존: **Chalk schema decision** |

### #1007에서 분해된 실행 단위 (전부 OPEN, 테스트 NOT RUN)

| # | 연결된 요구사항 |
|---|---|
| 1008 | EDU-01, EDU-02 (+AE-10/36) — 단계별 도움 선택 ↔ 실제 모델 행동 |
| 1011 | ENV-01~04, ENV-07 (+AE-07/08/09/12/26) — 강사 설정 → 확정 버전 → 학생 실행 바인딩 |
| **1012** | **RUN-01, RUN-02, VER-02** (+AE-11) — 학생 자격 리허설과 버전별 준비 증거 = **관문의 선행 조건** |
| 1013 | CH-05, EDU-03/04/05 (+AE-42/43) — 사람 피드백 → 다음 초안 |
| 1015 | CH-02, CH-03, CH-06, CH-07 — 검수 가능한 초안 생성·재사용 |
| 1016 | REQ-01~04 — 강사 기능 요청과 실제 해결 확인 |
| 1017 | ENV-05, ENV-06 — 미등록 도구 격리 시험·편입 |
| 1018 | WEB-07, WEB-08, WEB-09 — 공개 버전 복구·웹앱 실행 범위 |

#1009·#1010·#1014는 `chalk-authoring.md` ID를 인용하지 않는다 — **Chalk 직접 연관 여부 미확인.**

### Chalk를 경유·소비하는 상위 에픽 (전부 OPEN)

#566(agentic roadmap) · #746(수업별 Agent 경험 — #759/#795/#813의 부모) · #748(기능·권한 계약) · #755(멀티모델) · #800(이용권·예산) · #915(체험·수업 통합) · #919(배포 게이트) · **#1020**(측정 코어 분리, Jay dogfood) · **#1049**(Capability Evidence) · #996·#1026·#1034(추적성·조정) · #555·#565.

### 머지된 PR 15건

#691(Chalk 워커 신설, closes #674·#676·#680·#684) · #704(문서 10개, 전부 NOT RUN) · #706(D1 초안/불변 버전) · #716(`/authoring`) · #733(`/manage`·`/sharing`) · #736(`/start`) · #740(학생 전달) · #743(실기 수정) · #759(AI 표시 이름) · #795(모델 9버전) · #809(기능 좁히기) · #813(강사 picker) · #839(effort) · #866(`/budgets`) · #1027(프로필 비종속 초안).

> [!note] #813이 남긴 운영 교훈 3개
> ① **picker 기본값은 `inherit`** — 그 상태에서는 `features` 블록을 아예 보내지 않는다. 안 그러면 손대지 않은 수업이 **오늘의 grant에 갇힌다**.
> ② **빈 배열은 미설정과 다른 유효한 선택** = "채팅만 하는 수업".
> ③ 강사에게는 **이름**으로 나간다(`subagents` 같은 내부 키 노출 금지). issuer 허용목록 한 줄을 빠뜨리면 강사 화면이 503.
> #809도 같은 종류를 하나 남겼다 — **적용 지점이 둘**이라 게이트에만 넣으면 게이트 테스트를 다 통과하면서 **모든 SDK 좌석에서 무력해진다.**

### 열린 PR 5건

| # | 무엇 | 비고 |
|---|---|---|
| **1005** | 강의 작성 시 수업 설정을 **이름으로** 선택 + ID 자동 생성 | 본문 첫 줄에 **"Chalk를 Studio와 독립된 저장소로 분리해달라"는 사용자 요청**. 이 PR은 분리 실행이 **아니고** 검토 요청. "기존 강의 재열기 시 ID 필요"는 남음 |
| **1024** | 11문서 289개 + 독립 강의 7계약을 **38개 실행 단위**로 연결. 시나리오 미연결 23개를 T-24~46으로 채워 **79/79 → 66개 시나리오** | Closes #1007. **새 시나리오 전부 NOT RUN** |
| **1028** | 단계별 도움 방식(`help:{default,allowed[]}`)을 확정 수업에 묶고 다음 실행에 전달. **거절된 요청은 공급자에 도달하지 않는다** | **#1036에 의해 차단** |
| **1037** | 6개 복제 검사를 하나의 순수 판단(`decideCohort`)으로 통합 | **사용자에게 보이는 기능 없음** |
| 905 | hono 범프 | dependabot |

**#794는 CLOSED·미머지** — #795로 대체됨.

## 7. 닫히지 않은 채 문서화된 경계

- **AE-09 UNMET (agent-sdk 경로)** — 도구가 클라이언트에서 실행되므로 업스트림 `tools` 필터링으로 닫히지 않는다. ADR-0007이 원래 그 필터를 해법으로 적었다가 **2026-09-08에 정정**했다. 이 경로에서 Service가 집행하는 것은 넷뿐(신뢰 게이트·system prompt 교체·모델 clamp·max_tokens/effort 정규화). 오늘의 passthrough를 그대로 단언하는 **음성 대조군**을 상시 테스트로 두어 조용한 변경을 막는다. Service 집행이 필요한 코호트의 유일한 선택지는 **proxy 경로**
- **명단은 누적** — `cohort:sk-biopharm-2026-a:roster`가 2026-09-03 기준 **340개 핸들**(모든 발급 배치 + 프로브). 범위 없는 diff는 317석을 "누락"이라 부르며 전부 잡음. `?seat_prefix=`로 한정하고 `roster_scope`를 읽어야 한다
- **보드의 측정된 거짓 경보** — 출하 임계값을 2026-08-22 01:45–03:00에 리플레이하면 "정상" 9석 중 3석이 경보에 든다(75분에 약 5회). `board-verdict.ts`는 이를 결함이 아니라 **p98 = 612s의 직접 귀결**로 적고, *첫 실제 세션에서 healthy-seat-hour당 alert-minutes가 이 수치를 크게 넘으면 quiet 컷이 실제 교실에 너무 타이트한 것*이라는 감시 기준을 남겼다

## 8. 열린 제품 질문 · 미확인

- **Chalk를 별도 저장소로 분리할 것인가** (#1005). 선행 조건: 확정 강의 전달 형식 + 공통 인증·저장 API 소유권 정리. 현 구조가 Service 코드를 직접 참조(`chalk/src/shared.ts`)하는 것도 분리 계획에서 다뤄야 한다고 적혀 있다. **결정 미확인**
- **작성 권한과 실행 권한의 분리 방식** (#1006) — 강의 작성으로 모델·도구·미성년 정책·예산 권한이 자동 확대되면 안 된다. **설계 미확정**
- **session-design을 완성된 수업 schema로 볼 것인가** (#562 의존 "Chalk schema decision")

> [!contradiction] 저장소 문서가 한 단계 낡았다 — session-design의 소비자
> `chalk-authoring.md`는 *"현재 session-design은 envelope 검증만 있고 **소비자가 없으므로** 완성된 수업 schema로 취급하지 않는다"*고 적었다.
> 그런데 **#740 이후 `/learn` · Studio 수업 패널 · 두 LLM 와이어 경로가 실제 소비자가 되었다.** 문서 갱신 여부 `미확인`. 이것이 [[chalk-requirements]] CR-DEF-08(스키마 소유 확정)의 전제를 바꾼다 — "소비자 없는 envelope"이 아니라 **이미 3곳이 읽는 계약**을 누가 소유할지의 문제다.

- **`MR-02`·`MR-03`이 studio에 없다** — lab `measurement-retirement.md`의 ID이고 studio 전체에 `MR-0*` 0건. 같은 폐지 결정의 studio 대응물은 `HC-09`(#1066)이나 **흡수인지 별개인지 `미확인`**
- **`HC-04`·`HC-05`가 계약과 코드에서 다르게 생겼다** — actor는 `user|policy` 둘뿐(AI 제안·강사 개입 구분 없음), 상태 집합도 계약과 이름·구성이 다르다. 정합 판정 기록 없음 → [[chalk-requirement-coverage-audit]]
- **`ARC-02`("인증을 URL에 넣지 않는다") ↔ `docs/exit/chalk.md`의 `…/console#t=<token>`** — fragment에 토큰이 들어가는 형태이며 정합 판정 기록 없음. 검사 T-22도 미실행
- **#1049의 여섯 역량 확정 여부** — 본문이 *"versioned candidate definitions, open to future revision"*이라 적고, 작업명 "HypeProof Capability Evidence"도 **확정 리브랜드가 아니라고 명시**. 7 AI Native Assets와의 관계 `미확인` → [[six-human-capabilities]]
- **#1068의 "Chalk authoring gaps" 산출물** — `wip`, 아직 없음

### 이 기록이 확인하지 못한 것

`docs/plan/vessel-and-modules.md`·`dag.yaml` 원문 · ADM/DES 개별 요구사항 원문 · PR #1024의 38개 실행 단위 원장 파일 · IC-04~07·IC-T01~05 · T-24~46 개별 시나리오 · #718 · **각 테스트의 최신 실행 결과**(위 PASS는 모두 해당 PR·문서 시점의 기록이며 이 조사에서 테스트를 직접 실행하지 않았다) · #1009/#1010/#1014의 Chalk 연관.

## 부록 — 번호 목록

- **이슈 OPEN**: 555, 562, 565, 566, 732, 746, 748, 755, 800, 805, 886, 915, 919, 996, 1006, 1007, 1008, 1011, 1012, 1013, 1015, 1016, 1017, 1018, 1020, 1026, 1034, 1036, 1049, 1068
- **이슈 CLOSED**: 674, 676, 680, 684, 703, 705, 712, 735, 739, 742, 792, 799, 802, 847, 856
- **PR MERGED**: 691, 704, 706, 716, 733, 736, 740, 743, 759, 795, 809, 813, 839, 866, 1027
- **PR OPEN**: 905, 1005, 1024, 1028, 1037
- **PR CLOSED (미머지)**: 794

## 관련

[[chalk]] · [[chalk-requirements]] · [[chalk-target-shape-proposal]] · [[capability-measurement-module]] · [[hypeproof-studio]] · [[production-strategy-session-20260919]]

관련: [[requirement-id-index]] — 정본 ID 전수 인덱스(계열·번호 구멍·중복·한쪽에만 있는 ID)
