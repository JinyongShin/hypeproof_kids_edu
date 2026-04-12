---
type: comms
title: "팀 공유 브리핑: 소아암 환아 AI 코딩 파일럿 근거 요약"
created: 2026-04-12
updated: 2026-04-12
status: shareable
audience: team
tags:
  - comms
  - briefing
  - pilot
  - research/synthesis
related:
  - "[[research-peds-onc-coding-ed]]"
  - "[[pilot-curriculum-adapted]]"
  - "[[pilot-env-design]]"
  - "[[pilot-operator-guide]]"
  - "[[okr-q2-jy]]"
---

# 팀 공유 브리핑 — 2026-05-05 소아암 환아 AI 코딩 파일럿 근거 요약

> **목적**: 5월 5일 국립암센터 강당 파일럿(8–12세 40명, 90분 6블록)의 설계 선택을 외부 문헌·기관 권고와 대조해 정리. **팀원·의료진·보호자 대상 설명 공용 자료**로 사용.
>
> **한 줄 결론**: *우리 파일럿 형식(소아암 환아 대상 대규모 단일 회차 AI 코딩 이벤트)의 직접 선례는 공개 문헌에 없음. 다만 인접 영역의 peer-reviewed 증거를 조합하면 교수법·운영·감염관리·피로 대응 전 영역이 근거 기반으로 설계 가능.*

---

## 1. TL;DR

- **무엇을 할 수 있다고 주장해도 되나**: "경험·정서·주의 분산·자기효능감". **EF 전이나 학습성과는 주장 금지** (우리는 90분 단회성, 해당 증거는 11세션 5–6주 투여 기반).
- **무엇이 필수인가**: 손 위생 + 구두 안내, 사전 증상 문진·발열 체크, ANC 컷오프 의료진 합의, 1인 1기기 + 와이프, 전원 수술마스크, ≥12 ACH 환기 확인.
- **우리가 지금 하는 일이 왜 가치 있나**: Pediatric Blood & Cancer 2025의 "Techquity" 프레임(AI + 몰입형 tech로 소아·AYA 종양학 형평성 격차 해소)에 **정확히 들어맞음**. 국내 문헌 기준으로는 소아암 환아 대상 AI 코딩 교육 **최초 사례 가능성** → publishable.

---

## 2. 파일럿 개요

| 항목 | 값 |
|---|---|
| 일시 | 2026-05-05, 13:30–15:30 (90분 실수업) |
| 장소 | 국립암센터 강당 |
| 대상 | 소아암 환아 8–12세, 최대 40명 |
| 형식 | 6블록 × 블록당 ≤15분, 블록 사이 마이크로 휴식 |
| 기술 스택 | `hypeproof-ai.xyz` 단일 URL → Caddy → OAuth2 proxy (Google 화이트리스트) → code-server → Cline → Gemini 2.5 Flash |
| 핵심 교수 제약 | No-debug · AI-as-scribe · Single-HTML runtime · 협력형 서사 |
| OKR 지표 | KR1 5명+ 로그인·완주 · KR2 치명 장애 0건 |

---

## 3. 근거 기반 설계 — 영역별 요약

### 3.1 교수법 (Pedagogy)

| 근거 | 출처 | 우리 설계에의 함의 |
|---|---|---|
| Code.org 기반 코딩이 인지 손상 아동(IQ 71–82, EF 결손)에게 **100% 완주율 + 전이 효과** | Sickle Cell 연구, *Journal of Intelligence* 2026 (peer-reviewed) | 코딩 자체는 우리 모집단에 **실현 가능**. 단 해당 연구는 **11세션 × 5–6주** — 우리 90분 단회성으로는 전이 주장 불가. |
| 소아암 환아 공통 인지 제약: 주의·처리속도·피로 · 표준 편의: **스크라이브 / 연장 시간 / 조용한 공간 / 자주 체크인 / 예고 없는 지명 금지** | St. Jude Together (clinical guide) | 우리 4가지 병동 맞춤 변경 — **no-debug, AI-persona workflows, single-HTML runtime, 협력형 프레이밍** — 은 **모두 St. Jude 편의 권고와 구조적으로 일치**. |
| 부모가 가치 있다고 꼽은 것: "학교는 중요하다는 메시지" + "치료로부터의 주의 분산" · 기술 제공만으로는 0 — **운영 설계가 병목** | OEP 평가 (Continuity in Education, peer-reviewed) | 우리 효과 주장은 **"경험·정서·주의 분산"**으로 고정. WebEx 실패 사례는 "도메인만 열어두면 쓰일 것" 가정의 **반례** — 파일럿 후 접근 경로·부모 오리엔테이션이 없으면 사장된다. |

### 3.2 세션 길이 / 피로 관리

- 미국 기준 **병원 내 수업 시간은 보통 하루 1시간** (St. Jude 관행).
- 우리 **90분 = 6블록 × ≤15분**은 표준 하루치를 넘지 않으면서 자연스러운 재휴식·이탈·재합류 공간 확보 → 피로·처리속도 결손에 안전한 구조.
- 설계 원칙: **입력 부담 최소화 (AI가 타이핑 대부분 수행) + 자주 짧은 성취 지점** → 블록 0(10분)에 반드시 "내 캐릭터 등장" 성취 1개.

### 3.3 감염관리 — **파일럿 당일 필수 체크리스트**

출처: PMC7122566 (peer-reviewed review). **우리 감염관리 설계의 load-bearing 근거**.

- [ ] **손 위생 스테이션 + 입구 구두 안내** (단일 최강 통제. 사이니지만으로는 불충분, 운영자 구두 프롬프트 필수).
- [ ] **사전 증상 문진 + 당일 발열 체크** — 어린이·보호자·운영진·튜터 **전원**. 증상자 입장 불가.
- [ ] **ANC 컷오프 의료진 합의** — ANC <100은 대규모 실내 모임 contraindication. 국립암센터 담당의와 사전 합의 문서화. 제외 환아 대상 대체안(Zoom·개별 방문) 준비.
- [ ] **강당 HVAC 사양 확인** — HSCT 기준 ≥12 ACH. 미달 시 HEPA 이동식 백업.
- [ ] **1인 1기기 + 사용 전후 70% 에탄올 와이프**.
- [ ] **전원 수술마스크 착용** (국내 관행 + 면역저하 아동 보호).

### 3.4 심리사회적 프레이밍

- **학업 연속성은 standard of care** — Psychosocial Standards of Care Project (PMC5198902) 기준, *"잘 훈련된 경험 있는 소아암 팀 구성원"*이 제공해야 함. **단순 개발자 자원봉사 ≠ 충분** → 튜터 사전 오리엔테이션 필수.
- **협력형 서사 기본값 · 전투/체력 소거 메커니즘 제외** — 소아암 환아는 "악당을 때려 없애기" 어휘가 치료 서사와 충돌할 위험. Starlight Foundation도 **combat/violence 프레이밍을 명시적으로 회피**함 → 외부 기관 관행과 일치. 아이 요청 시 운영자 재량으로만 스위칭.
- **대체 서사 레퍼토리**: 친구 모으기 · 씨앗 심기 · 길 만들기 · 힐링 웨이브. 공통 규칙: 적·체력·소거 없음. 상호작용은 **획득·연결·성장**.

---

## 4. 파일럿의 독창성과 한계

### 우리가 선례 없는 영역 (novel implementation)

- 기존 병원 교육학 문헌이 확립한 **3가지 전달 모드** — bedside / async micro-learning / synchronous remote — 중 어느 것에도 해당하지 않는 **4번째 모드**: "synchronous in-person large-group event at a designated venue".
- Starlight(824개 병원 · 300만 환아)도 **bedside 1:1 중심**이며 대규모 group 코딩 이벤트 precedent 없음.
- 국내 병원학교 문헌(KCI 2026 3월)은 **치유환경 디자인 중심**, ICT·디지털·코딩 교육 구체 프로그램 전혀 없음.

→ **40명 동시 소아암 환아 실내 AI 코딩 이벤트는 국내외 공개 문헌 기준 최초 사례 가능성**. IRB 승인 + 사전 동의 구조를 갖추면 **publishable**.

### 한계 / 주장 금지 영역

- EF 전이·인지 개선 효과 주장 금지 (dose가 다름).
- Starlight 82% 스트레스 감소 수치도 hospital-partner 자가보고 — 우리 또한 RCT가 아닌 **experiential delight 기반 evaluation**임을 명시.
- 국내 40명 동시 소아암 환아 실내 이벤트의 **행정·IRB 선례가 확인되지 않음** → 국립암센터 측 절차 확인 필요.

---

## 5. 팀별 Action Items (4/20 이전 목표)

| 담당 | 액션 | 근거 |
|---|---|---|
| **JY (대외·의료)** | 국립암센터 담당의와 ANC 컷오프 · 사전 문진 양식 · 참석 가능성 확정 | § 3.3 |
| **JY** | 교육부 건강장애 학생 지원 정책 / 병원학교 가이드라인 확인 | § 3.1 OEP 교훈 |
| **운영** | 손 위생 · 문진 · 마스크 · 기기 와이프 런북을 `pilot-operator-guide`에 편입 | § 3.3 전체 |
| **운영** | 튜터 사전 오리엔테이션 커리큘럼 작성 — 소아암 심리사회 기본 + 감염관리 + 페다고지 제약 | § 3.4 (PMC5198902) |
| **설계** | 성과 지표 재조정: **EF 주장 폐기** → ① 완주율 ② 자기효능감 self-report ③ 부모 만족도 ④ 치명 장애 0건 | § 3.1, OKR Q2 정렬 |
| **설계** | 협력형 대체 서사 3개 이상 확정 + Cline/Gemini 시스템 프롬프트에 "전투 메커니즘 제안 금지" 규칙 추가 | § 3.4 |
| **인프라** | 강당 HVAC 사양 확인, 미달 시 HEPA 이동식 수급 경로 | § 3.3 |
| **인프라** | 병동 WiFi WebSocket 안정성 리허설 · 어린이 Google 계정 보유 여부 확인 · 대리 로그인 플랜 B | `pilot-env-design` 위험 항목 |
| **Post-pilot** | 파일럿 이후 접근 경로(도메인·계정·콘텐츠 지속성) 결정 — 미결정 시 WebEx 재현 위험 | § 3.1 (OEP WebEx 실패) |
| **확장** | 콘텐츠 **학교 배포 후속** 기획 — 또래 교육 세션 · 교사 워크숍 증거(PMC5198902: 놀림 감소, 태도 개선) 기반 저비용 확장 | § 3.4 |

---

## 6. 우리가 외부에 설명할 때 쓸 문장 (narrative anchors)

- **의료진/IRB용**: *"St. Jude의 소아암 교실 편의 권고를 AI·웹 환경에 구조적으로 이식한 파일럿. 감염관리는 peds-onc 표준을 따르며, 성과 지표는 완주율·자기효능감·부모 만족도이고 인지 개선 주장은 하지 않는다."*
- **보호자용**: *"오늘 2시간 만큼은 평범한 아이로. 아이가 자기 손으로 '이걸 내가 만들었다'는 경험을 집으로 가져갑니다."*
- **funder/이사회용**: *"Pediatric Blood & Cancer 2025가 정의한 Techquity 프레임워크의 직접 구현 사례. 국내 소아암 환아 대상 AI 코딩 교육의 첫 문헌화 기회."*
- **학교·재진입용**: *"학업 연속성은 소아암 standard of care. 본 파일럿은 환아가 학교로 돌아갈 때 또래에 나눌 수 있는 '내가 만든 것'을 제공한다."*

---

## 7. 출처

| 출처 | 유형 | 신뢰도 |
|---|---|---|
| Sickle Cell Coding Intervention — *Journal of Intelligence* 2026 | peer-reviewed | high |
| St. Jude Together: Educational Challenges | clinical guide | high |
| Starlight Therapeutic Gaming Program | org-program | medium |
| Techquity in Pediatric/AYA Oncology — *Pediatric Blood & Cancer* 2025 (Puthenpura) | peer-reviewed | high |
| Hospital Pedagogy Framework — *American J. Tech & Applied Sciences* 2026 | journal-framework | medium |
| Infection Prevention in Pediatric Oncology — PMC7122566 | peer-reviewed review | high |
| 국내 어린이 공공전문진료센터 병원학교 — KCI 2026 3월 32(1) | Korean journal | medium (원문 파싱 부분) |
| Academic Continuity — PMC5198902 (Psychosocial Standards of Care Project) | peer-reviewed | high |
| Oncology Education Program — *Continuity in Education* | peer-reviewed evaluation | high |

상세 요약과 개별 사례 분석: `kids_edu_vault/wiki/intel/research-peds-onc-coding-ed.md` 및 관련 case-*.md 페이지.

---

*작성: 2026-04-12. 리허설(4월 말) 이후 세션 길이·피로 측정값으로 본 문서 갱신 예정.*
