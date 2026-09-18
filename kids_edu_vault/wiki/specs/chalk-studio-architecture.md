---
type: spec
title: "Studio·Chalk·Service 아키텍처와 데이터 흐름"
status: review
owner: "[[jinyong-shin]]"
created: 2026-09-18
updated: 2026-09-18
source_ref: "scratchpad/chalk-scan/studio-architecture-dataflow.md (외부 경로, 전언)"
tags:
  - spec
  - chalk
  - architecture
  - product
related:
  - "[[chalk]]"
  - "[[hypeproof-studio]]"
  - "[[chalk-pedagogy-gate]]"
  - "[[chalk-entry-point-20260918]]"
  - "[[chalk-implementation-status]]"
  - "[[chalk-requirements]]"
---

# Studio·Chalk·Service 아키텍처와 데이터 흐름

> [!note] 출처와 확인 범위
> **전부 `hypeproof-studio` 저장소의 코드·설정에서 확인된 사실이며, 이 세션이 직접 확인하지 않았다.**
> 근거: `scratchpad/chalk-scan/studio-architecture-dataflow.md` (기준 `hypeproof-studio` main `75fe6e4` + PR `#1115`·`#1117`).
> 이 페이지는 **볼트가 갖고 있지 않던 구조 지식**을 기록한다. 인수 기준 원문은 저장소를 읽는다.

## 1. 네 계층

`products.yaml`의 `layers` 선언:

| 코드 | 계층 | 무엇 | 도달 비용 |
|---|---|---|---|
| `v` | app | **Studio 바이너리** (`extensions/hypeproof-chat` 포함) | **재설치** |
| `w` | service | Worker 런타임 (`worker/`) | 즉시, 전원 |
| `c` | surface | **강사 표면** (`chalk/`) | 강사만 |
| `m` | module | 데이터 (커리큘럼·session-design·observation-rubric) | 배포 |

## 2. 소유 경계 — `ARC-01`

> *"Chalk는 **화면·전달**, Service는 **권한·상태 저장·토큰 서명**을 소유한다."*

| | Service (`worker/`) | Chalk (`chalk/`) | Studio (`extensions/`) |
|---|---|---|---|
| 토큰 **서명** | ✅ 유일 | ❌ | ❌ |
| 토큰 **검증** | ✅ | ✅ (Service 것을 re-export) | — |
| KV **쓰기** | ✅ 유일 | ❌ | ❌ |
| D1 **쓰기** | ✅ 유일 | ❌ | ❌ |
| R2 | 읽기·쓰기 | **LIST + GET만** | ❌ |
| cron | ✅ 유일 | ❌ | — |
| admin Basic | ✅ | ❌ (비밀번호를 갖지 않음) | ❌ |

### 코드가 그 경계를 집행한다 — 테스트 4종

| 테스트 | 무엇을 금지하나 |
|---|---|
| `instructor-auth-drift` | **두 번째 구현 금지.** `assert.strictEqual(shared.verify, tokens.verify)` — **함수 객체 동일성**이라 복사본이면 즉사. 토큰 픽스처 10종에 대해 **상태코드가 같고 거부 문구가 바이트 단위로 같아야** 한다 |
| `deploy-isolation` | **두 배포 train 분리.** Chalk에 cron 금지 · `wrangler deploy` 스텝 정확히 1개 · 빌드 태그 패턴이 `^v` (= `c*` 태그가 다른 train을 깨울 수 없다). 반대로 **KV/D1은 같은 id여야 한다 — 공유가 계약이다** |
| `logs-read-path` | Chalk Worker 소스에 R2 `put`/`delete`가 나타나면 실패 |
| `authoring-forward` | *"Chalk must remain a forwarding surface for authoring, **including reads**"* — 저작 로직을 Chalk에 넣으면 깨진다 |

`chalk/src/shared.ts`가 Service 소스로 들어가는 **유일한 창구**이며, 서명 함수(`issue`/`issueIssuer`)를 import하지 않고 KV 헬퍼는 읽기 전용만 가져온다.

### 포워더의 헤더 규칙
- 허용 목록 = Service 자신의 `isIssuerAllowedEndpoint` (**두 번째 목록이 아니다**)
- 헤더 화이트리스트: `Authorization`(Bearer만, Basic 거부) + `Content-Type`
- **`cf-access-authenticated-user-email`은 절대 전달하지 않는다** — Service admin 미들웨어가 신뢰하는 헤더다

## 3. ⭐ Studio ↔ Chalk 는 연결돼 있지 않다

- **Studio 안에서 Chalk로 들어가는 경로가 없다.** `extensions/hypeproof-chat/`에서 chalk 도메인·`/authoring` 문자열 **0건**. **강사는 브라우저로 따로 들어간다.**
- 반대 방향은 있다 — Service가 `/issuer`·`/console`을 **302로 Chalk에 넘긴다**. 302를 쓴 이유가 주석에 있다: fragment(`#t=<issuer token>`)가 브라우저에서 재부착돼 **토큰이 네트워크를 건너지 않는다.**

→ 진입점 논의의 출발점이다. → [[chalk-entry-point-20260918]]

## 4. 확정(freeze) 14단계

`worker/src/routes/authoring.ts`. **`#1115` 이전에는 13단계였고 관문이 9와 10 사이에 들어갔다.**

| # | 검사 | 실패 시 |
|---:|---|---|
| 0 | *(화면)* 클라이언트 선검사 — `title·audience·objective·starter` | 서버에 가지 않음 |
| 1 | `isModuleVersion(version)` | 400 |
| 2 | JSON 파싱 | 400 |
| 3 | `expected_revision` 정수 ≥1 | 400 |
| 4 | `readDraft` + `owns()` | **404** (내용 비공개) |
| 5 | 이미 있는 버전 → scope 확인 후 멱등 반환 | 403 / 409 |
| 6 | `revision` 불일치 | 409 |
| 7 | `!profile_id` | 409 `template_required` |
| 8 | `templateAdmission()` (#1006) | 403 `template_not_reviewed` |
| 9 | **`validateSessionDesign(content, true)`** — 형태·완결성 | 400 |
| **10** | **`checkLessonPedagogy()` ← 관문 (#1115)** | **422 `pedagogy_blocked`** |
| 11 | `validateModelSubset` → `modelBinding` | 403 / 409 |
| 12 | `validateFeatureSubset` → `featureBinding` | 403 |
| 13 | `makeModuleDoc` (sha256) | — |
| 14 | `INSERT ... WHERE revision=?` — **쓸 때 revision 재확인** | 409 |

성공 응답: `{ module, source_revision, rehearsal: "not_run", activated: false, pedagogy }`
→ **확정은 활성화가 아니다.** 응답이 매번 그렇게 말한다.

### 에러 코드 체계 — 사실상 없다
응답은 대부분 `{error: "<한 줄 산문>"}`이고 기계가 읽을 `reason`은 **셋뿐**이다: `template_required` · `template_not_reviewed` · `pedagogy_blocked`.
**화면은 그중 `error` 문자열만 쓴다** — `reason`도 `findings`도 화면에 닿지 않는다.

## 5. 저장되는 것과 저장되지 않는 것

### D1 (`worker/migrations/0002-chalk-authoring.sql`)
| 테이블 | 가변성 |
|---|---|
| `authoring_drafts` | 조건부 UPDATE (owner + revision) |
| `authoring_versions` | **확정본. 불변 — 버전 키는 갱신되지 않는다** |
| `authoring_independent_courses` · `authoring_openings` | #1006 |

### Module 계층
| kind | 저장소 | 비고 |
|---|---|---|
| `curriculum` · `observation-rubric` | **KV** | `:pin`이 유일한 가변 키 |
| `session-design` | **D1** `authoring_versions.module_json` | ADR 0004: *"KV pin은 eventually consistent라 compare-and-swap 편집이 불가"* |

무결성은 `sha256(JSON.stringify(content))` — 주석이 **"인증이 아니라 무결성"**이라고 명시한다.

### 저장되지 않는 것
- **관문 판정** — [[chalk-pedagogy-gate]] §6
- **리허설 증거** — `authoring_versions` 스키마에 칸이 없다. `rehearsal: "not_run"`은 **네 곳에 박힌 하드코딩 리터럴**이다

> [!warning] ⛔ 지우는 경로가 없다
> 코드·마이그레이션 전체에 `DELETE FROM authoring*` / `DROP TABLE` **0건**. 저작 라우터에 `.delete()` 핸들러도 없다.
> ADR 0004가 그렇게 정했다 — *"Preserve the two D1 tables for recovery/export; no deletion is required. **Destructive data cleanup is a separate decision.**"*
> **운영자 권한으로도 제품 API로는 못 지운다.** 사람이 `wrangler d1 execute --remote`로 직접 SQL을 치는 것뿐이다.
> → 이것이 [[chalk-pedagogy-gate]]의 "시연은 프로세스 내부 러너로만" 결정의 근거다. **운영에는 지우개가 없다.**

## 관련

- [[chalk-pedagogy-gate]] · [[chalk-entry-point-20260918]]
- [[chalk-implementation-status]] · [[chalk-requirements]] (`ARC-01`·`ARC-02`)
- [[chalk]] · [[hypeproof-studio]]
