---
type: meta
title: "Log"
created: 2026-04-12
updated: 2026-04-12
tags:
  - meta/log
---

# Log

추가 전용. 새 엔트리는 **최상단**에 삽입. 과거 엔트리 수정 금지.

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
