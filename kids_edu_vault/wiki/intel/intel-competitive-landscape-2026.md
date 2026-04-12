---
type: intel
title: "Intel: 경쟁 구도 — Chat-to-Code/Game (2026-Q2)"
created: 2026-04-12
updated: 2026-04-12
status: developing
confidence: high
tags:
  - intel
  - competitive
  - market
related:
  - "[[pivot-to-chat-preview-wrapper]]"
  - "[[intel-wrapper-architecture]]"
  - "[[intel-auth-billing-compliance]]"
sources:
  - "bolt.new/pricing, stackblitz.com/pricing"
  - "lovable.dev/pricing, docs.lovable.dev/introduction/plans-and-credits"
  - "v0.app/pricing, uibakery.io/blog/vercel-v0-pricing-explained"
  - "replit.com/pricing, blog.replit.com/effort-based-pricing"
  - "scratch.mit.edu/statistics, playentry.org"
  - "khanmigo.ai/pricing, khanmigo.ai/learners"
---

# Intel: 경쟁 구도 — Chat-to-Code/Game (2026-Q2)

## Overview

2026-04-12 리서치. "챗으로 게임을 만드는 아이 대상 AI 도구" 포지셔닝에 대한 경쟁 구도 스캔.

## AI 챗→앱 빌더 (성인 타깃, 아키텍처상 가장 근접)

### bolt.new (StackBlitz)
- 타깃: 개발자·인디 빌더.
- 스택: **WebContainers** + Anthropic/OpenAI 모델.
- 인증: Email / Google / GitHub.
- 과금: Free (300K 토큰/일, 1M/월), Pro ~$20/mo, Teams, Enterprise. **토큰 기반** (파일 싱크 헤비 → 프로젝트 커지면 비용 급증).
- 코드: **전체 노출 (IDE 스타일)**.
- 훔칠 것: one-shot deploy (호스팅·인증·도메인 번들).
- 피할 것: 토큰 미터 불안 — 아이에게 치명적 UX.

### Lovable
- 타깃: 비개발자 파운더.
- 스택: React/Vite/Supabase 생성 템플릿.
- 과금: Free (5일/30월 크레딧), Pro $25 (100), Launch ~$50, Scale $100 (800), Business $50 SSO. **크레딧, 토큰 아님**.
- 코드: 노출되나 de-emphasized ("chat-first").
- 훔칠 것: "< 1 크레딧"의 단위 감각 — 아이용 "에너지/하트"로 리스킨 가능.
- 피할 것: Supabase 의존은 성인 레벨.

### v0 (Vercel)
- 타깃: 프론트 개발자.
- 스택: 프로프라이어터리 Mini/Pro/Max → shadcn/ui + Tailwind.
- 과금: Free ($5 크레딧), Premium $20, Team $30/user, Biz $100/user. **2026-02부터 토큰 기반**.
- 코드: 노출.
- 훔칠 것: 티어별 모델 품질(Mini/Pro/Max) — 비용 레버.

### Replit Agent
- 타깃: 메이커·학생.
- 스택: 전체 Linux VM + Agent 3.
- 인증: email/Google/SSO.
- 과금: Free Starter, Core $25/mo (연간 $20), Pro $100. **effort-based "checkpoints"** — 단순 변경 <$0.25.
- 코드: 노출.
- 훔칠 것: **checkpoint = 아이용 단위 가치** (한 번의 부탁 = 한 번의 저장 포인트).
- 갭: **전용 키즈 티어 없음**.

## 키즈/비기너 코딩 플랫폼

### Scratch 3 (MIT)
- 8–16세, 1억 300만+ 사용자. 무료 영구. Blockly JS.
- 인증: 로그인 없이 플레이 가능, 저장 시 계정.
- 코드: **블록 노출, 텍스트 숨김** — 표준 모델.
- 2025+ 기부 기반 Memberships 시작.
- 훔칠 것: 로그인 없는 체험 + 저장 시 계정 / 블록 메타포.

### Code.org App Lab / Game Lab
- 학령기, 무료, JS + 블록↔텍스트 토글.
- 인증: Google Classroom / Clever.
- 훔칠 것: **블록↔텍스트 토글** = 문해력 스캐폴드.

### Tynker
- 5–14세, $20/mo 분기, $120/yr, $240 평생. Minecraft 모드 + Python/JS.
- 피할 것: 코어 UX에 페이월.

### MakeCode (Microsoft)
- 무료 오픈소스. **오프라인 데스크탑 앱** 존재 → 병동 Wi-Fi에 결정적.
- 교훈: 오프라인 우선이 병원 네트워크에서 진짜 의미.

### 한국
- **엔트리 (playentry.org)** — **네이버 커넥트재단, 무료 영구, 초·중 교과서 채택, AI 블록 내장**. **최대 경쟁자**. 한국 교사 친숙도 압도적.
- **엘리스 / 코드잇**: 성인·청소년 중심, **키즈 세그먼트 갭 존재**.
- **엘리하이 키즈**: 4–7세 학습지, 코딩은 곁가지.

## AI-Native 키즈 코딩 (신생, 2024–2026)

### Khanmigo (Khan Academy)
- $4/mo 학습자, 교사 무료, $15/학생/년 디스트릭트.
- JS/HTML/Python/SQL, **소크라틱 리뷰 — 생성 아님**.
- 교훈: 어시스턴트지 빌더가 아님 → **chat-to-game 화이트스페이스 열려 있음**.

### Scratch 4.0 (GenAI)
- 로드맵 존재, 출시 일정 미정 (2027+ 추정).
- **12–18개월의 기회 창**.

### Roblox AI (2026-02)
- 텍스트→3D 모델 네이티브. 단 Roblox Studio는 성인 복잡도.

### "bolt.new for kids"
- **명명된 incumbent 없음**. 비즈니스 인사이더의 bolt.new 부모-자식 데모는 제품 아님.
- **화이트스페이스 명확**.

## 시장 갭 — 파일럿이 선점 가능한 공간

### 1. Chat-native, 코드-invisible, 키즈-first 저작
- Scratch는 블록으로 텍스트 감추고, bolt/Lovable은 풀 코드 노출. **"한국어로 게임 묘사 → 30초 내 실행 가능 → 블록도 코드 패널도 없음"** 을 배송한 사람 없음.
- 병동 제약(낮은 체력, 짧은 세션, 한 손 iPad)이 **성인용 도구는 절대 만들지 않을 급진적 단순화**를 강제. 제약이 moat.

### 2. 오프라인/저대역 + 병원-safe 인증
- MakeCode 오프라인이 수요 증명. Scratch/엔트리는 Wi-Fi 필수.
- 병원 Wi-Fi는 적대적. **PWA 로컬 캐시 + 보호자 스코프 로그인(아이는 이메일 없음, COPPA/PIPA 클린)** 이 비어 있음.

### 3. effort/체크포인트 과금을 아이용 "에너지"로 번역, 스폰서에 청구
- Replit checkpoint + Lovable "< 1 credit" 프레이밍을 아이에게 **하트/별**로 리스킨, 결제는 보호자/병원/CSR(소아암재단, 병원 사회공헌)로.
- 모든 성인 도구는 긴 프롬프트를 토큰 죄책감으로 처벌. 키즈 제품 중 이걸 푼 곳 없음.
- 파일럿은 **free-to-child + B2B2C sponsor-paid**로 런치 가능, 이후 방어 가능.

## Sources
- Bolt: [pricing](https://bolt.new/pricing), [2026 review](https://www.banani.co/blog/bolt-new-ai-review-and-alternatives)
- Lovable: [pricing](https://lovable.dev/pricing), [plans & credits](https://docs.lovable.dev/introduction/plans-and-credits)
- v0: [pricing](https://v0.app/pricing), [UI Bakery guide](https://uibakery.io/blog/vercel-v0-pricing-explained-what-you-get-and-how-it-compares)
- Replit: [pricing](https://replit.com/pricing), [effort-based](https://blog.replit.com/effort-based-pricing)
- Scratch: [statistics](https://scratch.mit.edu/statistics/), [4.0 outlook](https://itsmybot.com/scratch-4-0-release-date/)
- Code.org: [tools](https://code.org/en-US/tools), [App Lab docs](https://studio.code.org/docs/ide/applab)
- Tynker: [pricing](https://www.tynker.com/parents/pricing/)
- MakeCode: [home](https://www.microsoft.com/en-us/makecode)
- 엔트리: [playentry.org](https://playentry.org/)
- Khanmigo: [pricing](https://www.khanmigo.ai/pricing)

## Open Questions
- [ ] 엔트리와 **명시적 경쟁 vs 보완** 포지셔닝 — 블록 vs 채팅은 기술적으로는 공존 가능. 초기 마케팅 메시지 정리 필요.
- [ ] 국내 "AI 네이티브 키즈 코딩" 신생 경쟁자 — 엘리스·코드잇이 키즈 세그먼트에 언제 진입할지 감시.
- [ ] 소아암재단·소아 병원 CSR 프로그램 목록 (스폰서 후보).
