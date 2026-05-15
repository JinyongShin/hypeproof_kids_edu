---
type: decision
status: proposed
priority: 1
date: 2026-04-12
created: 2026-04-12
updated: 2026-04-12
owner: "[[jinyong-shin]]"
context: "파일럿 실행환경 아키텍처 피벗"
tags:
  - decision
  - pilot
  - architecture
  - pivot
related:
  - "[[pilot-env-design]]"
  - "[[iframe-sandbox-over-webcontainers]]"
  - "[[parent-gated-signup-first]]"
  - "[[intel-wrapper-architecture]]"
  - "[[intel-competitive-landscape-2026]]"
  - "[[code-server]]"
  - "[[cline]]"
  - "[[gemini-2-5-flash]]"
---

# Pivot: code-server+cline → Chat+Preview 래퍼

## 결정
- 기존 "VSCode 포크(code-server) + cline + Gemini" 스택을 **커스텀 chat+preview 웹 래퍼**로 피벗.
- 래퍼 구성: 좌 pane **채팅(AI와 대화)** / 우 pane **게임 라이브 프리뷰**. 코드 패널은 기본 숨김, "Show Code" 토글로만 공개.
- 인증은 OAuth 기반 ([[parent-gated-signup-first]])이며 향후 유료화 경로 ([[intel-auth-billing-compliance]]) 내장 설계.
- 기존 [[pilot-env-design]]의 code-server·oauth2-proxy·caddy·cline 배선은 **부분 supersede** (스모크테스트·파일럿 당일 실제 실행 스택 여부는 별도 스케줄 결정).

## 근거

### 1. 대상(8–12세, 병동)에 IDE UI는 노이즈
- code-server = 성인 개발자 워크플로우(파일트리·터미널·세팅 패널)를 아이에게 강제 → 주의 자원 낭비.
- cline을 VSCode 안에 감싸면 한 번 더 래핑됨.
- 아이에게 실제 필요한 표면은 **채팅 + 실행되는 게임** 두 pane만 ([[single-html-runtime]], [[no-debug-philosophy]]).

### 2. 시장 기회 — 무주공산
- bolt.new/Lovable/v0 = 성인용 코드 노출.
- Scratch/엔트리 = 블록(무료·교과서 채택 → 블록으로는 못 이김).
- Khanmigo = 소크라틱 리뷰(생성 아님).
- Scratch 4.0 AI는 2027+ 예상 → **12–18개월 기회 창** ([[intel-competitive-landscape-2026]]).
- 병동 제약(체력·세션·한 손)이 성인용 도구는 만들지 않을 **급진적 단순화**를 강제 → 차별화 moat.

### 3. 유료화 경로가 IDE 포크로는 열리지 않음
- VSCode 포크 + Google OAuth로는 **아동 PIPA 문제 + 유료화 인프라(결제·구독·B2B 라이선스)를 0부터 구축**해야 함.
- 웹앱은 Next.js App Router + Clerk/Stripe + 포트원으로 스택이 표준화됨 ([[intel-auth-billing-compliance]]).

### 4. 엔지니어링 리스크 감소
- Agent SDK(`Edit`/`MultiEdit`)로 점진 수정 → 프리뷰 프레임 안정.
- iframe + srcdoc 샌드박스 ([[iframe-sandbox-over-webcontainers]]) = 무료·오프라인·초경량.

## 대안 및 기각 이유

### A. VSCode 포크 + Google OAuth (기존 계획)
- 기각: UI 복잡도, 아동 PIPA 노출, 유료화 경로 부재.

### B. bolt.new / Lovable / v0 등 기성 SaaS 사용
- 기각: 외부 서비스 → 병원 네트워크·개인정보·계정 이슈. 코드 패널 기본 노출. 성인 UX.

### C. p5.js Web Editor + Claude 채팅 사이드카
- 부분 보류: 스모크테스트 fast-path 후보. 커스텀 래퍼 확정 후 **선행 스모크테스트 수단**으로만 검토.

## 영향 범위

### Supersede / 재검토 대상
- [[pilot-env-design]] — 래퍼 기반으로 섹션 대체 필요.
- [[pilot-oauth-setup]] — Google OAuth 주 경로 폐기, 부모 이메일 우선 ([[parent-gated-signup-first]]).
- [[pilot-cline-gemini-integration]] — cline 의존 제거.
- [[pilot-server-domain]] — 유지 (apex 도메인은 래퍼에서도 필요).
- [[pilot-game-starter-template]] — 유지·강화. p5.js/canvas 단일 HTML 템플릿.
- [[pilot-operator-guide]] — UX 변경 반영 필요.
- [[code-server]] / [[cline]] — 컴포넌트 상태 `superseded`로 전환 후보.

### 모델 선택 (Open)
- Claude Agent SDK는 `Edit`/`MultiEdit` 등 편집 툴 내장 → 3주 MVP에 유리.
- 그러나 [[gemini-2-5-flash]] 결정은 **세션당 $0.15 미만 비용 목표** 근거 ([[okr-q2-jy]]).
- **별도 결정 필요**: (a) Claude로 스위치 + 비용 재검토, (b) Gemini Function Calling + 자체 Edit 루프 구현, (c) 이중 제공 후 A/B.

### 타임라인 리스크
- 2026-05-05 파일럿까지 **23일**. 래퍼 MVP + 부모 가입 + 프리뷰 샌드박스를 3주에 완성은 타이트.
- 리스크 완화: (i) 스모크테스트는 간단 p5.js 에디터 + 채팅으로 먼저, (ii) 파일럿 당일은 운영자 계정 하드코드 + 로그인 플로우 축소 버전, (iii) 정식 유료화 배선은 파일럿 후 확장.

## 현재 실행 방향 (JY 내부 결정, 2026-04-12)
- **옵션 C → A 단계 진행**. 초기엔 C(운영자 하드코드·가입 플로우 생략)로 래퍼 착수, **최종 파일럿 당일은 A(새 래퍼 정식)로 진행**.
- 근거: 파일럿 자체가 포지셔닝(chat-native, 코드-invisible) 검증이므로 차별화된 UX가 아이 앞에 서야 데이터가 의미 있음. C에서 멈추면 UX 피드백과 제품 방향이 괴리.
- **주의**: 이 방향은 JY 결정이며 Jay 확인 전. Jay 피드백에 따라 변경 가능 (특히 타임라인 리스크가 너무 크다고 판단되면 옵션 B로 철수).

## Follow-up (결정해야 할 것)
- [ ] **Jay 방향 승인** (C→A 단계 진행 확인, 또는 B 철수 제안)
- [ ] 모델: Claude vs Gemini 최종 결정 (비용·품질 A/B 테스트)
- [ ] MVP 스코프: OAuth·결제 포함 여부 (C 단계는 제외, A 단계에 선택적)
- [ ] 도메인: hypeproof-ai.xyz 유지 or 서비스 공식 도메인 분리
- [ ] C→A 전환 gate 기준·일정 (리허설 [[pilot-rehearsal-late-april]]에서 A 준비 상태 검증)

## 관련
- [[intel-wrapper-architecture]] · [[intel-auth-billing-compliance]] · [[intel-competitive-landscape-2026]]
- [[iframe-sandbox-over-webcontainers]] · [[parent-gated-signup-first]]
- [[pilot-env-design]] · [[okr-q2-jy]] · [[fast-implementation-mode]]
