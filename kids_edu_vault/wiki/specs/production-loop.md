---
type: spec
status: active
owner: "봉호 태"
target_date: 2026-06-01
tags:
  - spec
  - process
  - curriculum
created: 2026-05-05
updated: 2026-05-05
---

# 커리큘럼 제작 루프 (Production Loop v1)

## 목적

커리큘럼 설계 → HypeProof asset 생산 → 실전 투입 → 데이터 환류의 반복 구조를 정의한다.
파일럿 이후 v2 개발부터 적용.

---

## HypeProof Assets 정의

| Asset | 파일 / 위치 | 설명 |
|---|---|---|
| **scaffold 카드 텍스트** | `src/frontend/lib/scaffoldData.ts` | 블록별로 아이에게 보여주는 예시 문장 버튼 |
| **AI 페르소나** | `src/backend/personas/TUTOR.md` | LLM의 말투·출력 형식·블록 감지 규칙 |
| **캐릭터/세계/타이틀 카드** | SQLite `cards` 테이블 | 아동이 실시간 생성하는 JSON+SVG 카드 |
| **HTML5 게임** | 파일시스템 + SQLite `games` 테이블 | 아동이 실시간 생성하는 플레이어블 게임 |

> 캐릭터/세계/타이틀 카드 + HTML5 게임은 **아동 산출물** — 설계 대상이 아니라 관찰 대상.
> scaffold 텍스트 + AI 페르소나가 **설계·수정 대상 assets**.

---

## 루프 구조

```
인풋 → 설계 (Stage 1)
   ↓
설계 → 기술팀 피드백 (Stage 2)   ← scaffold 텍스트 + 페르소나 생산
   ↓
리허설 → 반영 (Stage 3)           ← scaffold + 페르소나 투입, 아동 산출물 관찰
   ↓
   └─→ Stage 1 (다음 버전)
```

---

## Stage 1 — 인풋 → 설계

**Asset 역할**: 참조 전용 — 기존 scaffold 텍스트·페르소나의 갭 분석

### 입력 데이터

| 데이터 | 출처 | 형식 |
|---|---|---|
| 파일럿 관찰 노트 | 진행자 현장 메모 | `wiki/comms/YYYY-MM-DD-pilot-obs.md` |
| 아동 산출물 샘플 | Stage 3 수집 (`cards`, `games` 테이블 덤프) | JSON / 스크린샷 |
| 블록별 소요 시간 | Stage 3 타이밍 기록 | `wiki/validation/YYYY-MM-DD-timing.md` |
| scaffold 텍스트 현황 | `scaffoldData.ts` 현재 버전 | TypeScript |
| AI 페르소나 현황 | `TUTOR.md` 현재 버전 | Markdown |
| decisions/ 로그 | 이전 의사결정 근거 | `wiki/decisions/` |

### 출력

- 교육 목표 + 블록 구조 정의 (다음 버전)
- scaffold 텍스트 갭 분석: 어떤 예시 문장이 안 통했는가
- 페르소나 갭 분석: LLM이 어떤 상황에서 틀린 반응을 했는가
- 결과물 포맷 확정 (단일 선택)

---

## Stage 2 — 설계 → 기술팀 피드백

**Asset 역할**: scaffold 텍스트 + AI 페르소나 **생산** (핵심 단계)

### 입력 데이터

| 데이터 | 출처 |
|---|---|
| Stage 1 교육 목표 + 블록 구조 | 봉호님 확정 문서 |
| scaffold 갭 분석 결과 | Stage 1 출력 |
| 페르소나 갭 분석 결과 | Stage 1 출력 |

### 생산되는 Assets

| Asset | 담당 | 저장 위치 |
|---|---|---|
| **scaffold 카드 텍스트 (신규/수정)** | 봉호님 초안 작성 | `wiki/specs/scaffold-cards-vN.md` → 기술팀이 `scaffoldData.ts` 에 반영 |
| **AI 페르소나 수정안** | 봉호님 초안 작성 | `wiki/specs/tutor-persona-vN.md` → 기술팀이 `TUTOR.md` 에 반영 |
| 진행자 스크립트 | 봉호님 초안 | `wiki/deliverables/facilitator-script-vN.md` |
| 어린이 가이드 | 봉호님 초안 | `wiki/deliverables/kids-guide-vN.md` |
| 기술 실현 가능성 메모 | 지웅 팀 검토 | `wiki/decisions/tech-feasibility-vN.md` |

### 완료 기준

- [ ] scaffold 텍스트: 봉호님 초안 → 지웅 팀 `scaffoldData.ts` 반영
- [ ] AI 페르소나: 봉호님 초안 → 지웅 팀 `TUTOR.md` 반영
- [ ] 커리큘럼 ↔ scaffold ↔ 페르소나 3자 일치 확인
- [ ] 결과물 포맷 단일화 (복수 병존 금지)

---

## Stage 3 — 리허설 → 반영

**Asset 역할**: scaffold + 페르소나 실전 투입, 아동 산출물(cards/games) 관찰

### 수집 데이터

| 데이터 | 측정 방법 | 저장 위치 |
|---|---|---|
| 블록별 소요 시간 | 스톱워치 / 진행자 메모 | `wiki/validation/YYYY-MM-DD-timing.md` |
| 아동 산출물 샘플 | `cards`·`games` 테이블 덤프 or 스크린샷 | `wiki/validation/YYYY-MM-DD-outputs.md` |
| scaffold 사용률 | 어떤 예시 문장 버튼이 눌렸는가 | 관찰 메모 or 클릭 로그 |
| LLM 이상 반응 | 페르소나 규칙 위반 케이스 | 관찰 메모 |
| 진행자 현장 메모 | 스크립트 이탈·즉흥 수정 | `wiki/comms/YYYY-MM-DD-pilot-obs.md` |
| 아동 반응 | 표정·발화·이탈 행동 | 관찰 메모에 포함 |

### vault ingest → Stage 1 환류

- 아동 산출물 + 관찰 메모 → `wiki/validation/` 적재
- 다음 Stage 1의 **scaffold 갭 분석** + **페르소나 갭 분석** 인풋이 됨

---

## 한 줄 요약

| Stage | Scaffold 카드 텍스트 | AI 페르소나 | 아동 산출물(cards/games) |
|---|---|---|---|
| 1. 인풋→설계 | 갭 분석 (읽기) | 갭 분석 (읽기) | 관찰 인풋 |
| 2. 설계→기술피드백 | **생산** (봉호님 초안) | **생산** (봉호님 초안) | 해당 없음 |
| 3. 리허설→반영 | 투입·사용률 관찰 | 투입·이상반응 관찰 | **생성·수집** |

---

## 관련

- [[production-loop-adoption]]
- [[stack-decision-after-curriculum]]
- [[game-content-guideline-pending]]
- `src/frontend/lib/scaffoldData.ts`
- `src/backend/personas/TUTOR.md`
