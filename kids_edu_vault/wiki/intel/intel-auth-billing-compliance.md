---
type: intel
title: "Intel: 인증·결제·컴플라이언스 (아동 SaaS)"
created: 2026-04-12
updated: 2026-04-12
status: developing
confidence: medium
tags:
  - intel
  - auth
  - billing
  - compliance
  - minors
related:
  - "[[parent-gated-signup-first]]"
  - "[[pivot-to-chat-preview-wrapper]]"
  - "[[pilot-oauth-setup]]"
  - "[[jay-lee]]"
sources:
  - "Clerk docs, Supabase Auth docs, NextAuth/Auth.js docs (라이브 검증 필요)"
  - "한국 개인정보보호법 제22조의2 (만 14세 미만 아동 동의)"
  - "COPPA §312 (미국)"
---

# Intel: 인증·결제·컴플라이언스 (아동 SaaS)

## Overview

Chat+preview 래퍼 MVP + 향후 유료화를 위한 인증·결제·법적 요건 리서치 (2026-04-12).
**주의**: 본 리서치는 WebSearch 미사용으로 학습 지식(cutoff 2025-05) 기반 → 배포 직전 모든 가격·법령·정책 상태 **라이브 재검증 필수**.

## 인증 (Google OAuth + Next.js, < 500 MAU)

| 솔루션 | 속도 | Google OAuth | Email/Magic 확장 | 가격 (<500 MAU) | Stripe 연동 |
|---|---|---|---|---|---|
| **Clerk** | 가장 빠름 (drop-in `<SignIn/>`) | 우수 | 내장 토글 | 10k MAU까지 무료 | 1급 Stripe Billing 애드온 (2025) |
| **Supabase Auth** | 빠름 (Postgres 동반 시) | 양호 | 내장 | 무료 티어 넉넉 | BYO Stripe (문서 풍부) |
| **NextAuth / Auth.js v5** | 중간 (배선 더 많음) | 양호 | 프로바이더 교체 | 무료 (자체 호스팅) | BYO (모든 것 직접) |
| **Firebase Auth** | 빠름 | 우수 | 내장 | 50k MAU까지 무료 | 어색함 (Google 생태계, Stripe 비네이티브) |

### 권고
- **Clerk**: 인증 코드 제로에 Stripe 배선까지 깔끔하면 기본값.
- **Supabase Auth**: Postgres + RLS가 필요하면(게임 저장·진행도·부모 계정) 1석2조.
- **Auth.js**: 락인·비용이 속도보다 중요할 때.

## 결제 (한국 + 글로벌 이원화)

### Stripe
- KRW 지원, 구독 + per-seat(`quantity`), 카드 coverage 좋음. 단 **부가세·세금계산서는 자체 처리 필요** (Stripe는 MoR 아님).
- Stripe KR 정식 서비스 상태: **배포 전 현시점 가용성 확인 필요** (2024년 invite-only 상태였음).

### LemonSqueezy / Paddle
- Merchant of Record(MoR) — VAT/부가세 글로벌 처리 대행. 솔로 파운더에게 단순.
- **한국 B2B 세금계산서 발급 불가** (치명적 제약).

### 국내 PG (토스페이먼츠 / 포트원)
- 병원·학교·재단 B2B 계약 시 **세금계산서 필수** → 국내 PG 병행이 현실적.

### 권고: 이원화
- **글로벌 B2C**: Stripe.
- **국내 B2B (병원·학교·CSR 예산)**: 포트원 또는 토스페이먼츠.
- MVP는 Stripe만, B2B 수주 시점에 국내 PG 추가.

## 경쟁사 과금 패턴 (2024–2026 트렌드)

- **bolt.new**: 토큰 기반 (Free 300K/일 · 1M/월, Pro ~$20/mo부터) — 파일 싱크 많으면 토큰 급증.
- **Lovable**: **크레디트 기반** ("many messages < 1 credit"). Free 5일/30월, Pro $25, Launch $50, Scale $100, Business $50 SSO.
- **v0**: 크레디트 → 2026-02부터 토큰 기반 전환. Free $5 크레딧, Premium $20, Team $30/user, Biz $100/user.
- **Replit**: **effort-based "checkpoints"**. 간단 변경 <$0.25, 복합 번들. Free Starter, Core $25, Pro $100.
- **트렌드**: LLM 비용이 변동이라 크레디트/체크포인트 모델이 주류.

## 아동 컴플라이언스 (핵심 트랩)

### 한국 개인정보보호법 (PIPA) — 만 14세 미만
- 만 14세 미만 아동의 개인정보 수집·이용 시 **법정대리인 동의 필수** (제22조의2).
- **Google OAuth를 아동의 주 가입 수단으로 삼는 것은 트랩**:
  - Google 계정은 한국에서 만 14세 이상 정책 (Family Link로 하위 자녀 관리 가능하나 추가 마찰).
  - 아동이 Google 로그인 시 실제 법정대리인 동의가 검증되지 않음.
- **한국 에듀 서비스 표준 패턴**: 부모가 계정 생성 → 자녀 서브프로필 생성.
  - 엘리스, 코드잇 키즈, 구름EDU 모두 이 방식.
  - 구름EDU는 K-12 대상으로 **학교 관리 ID** 별도 발급.

### COPPA (미국, 만 13세 미만)
- 검증 가능한 부모 동의, 행동 광고 금지, 데이터 최소화.
- 미국 확장 시 **별도 "학교/부모용" 가입 플로우 + DPA(Data Processing Agreement)** 필요.

### 병원 파일럿 특이사항
- 의료 데이터 아님(교육 파일럿) → HIPAA 불적용. 단 병원 IT는 외부 서비스 whitelisting + 알 수 없는 CDN/WebSocket 차단이 일반적.
- 실전 패턴:
  1. **apex 도메인 고정** + 서드파티 트래커 제거.
  2. 병원 IT에 **IP/도메인 allowlist 문서** 선제 제공.
  3. **오프라인 PWA 폴백** 준비 (네트워크 불안정 대비).
  4. 제약 심한 병동은 **단일 테넌트 배포** (Vercel Enterprise 또는 Docker self-host on loaner laptop).

## 아동 에듀 수익화 선례

- **Scratch / Code.org**: 무료 영구 (비영리 재단 기반) — 모델 아님.
- **Tynker**: B2C 가족 구독 (~$10–20/월) + 학교 라이선스. 이중 모델.
- **Khan Academy**: 무료, 기부·재단 기반.
- **Replit**: Freemium + EDU 티어 (교사 시트, 교실). 실수익은 프로 개인·팀에서.

### 권고: B2B2C 스폰서 결제
- **무료 티어 + B2B 중심** (병원/학교/사회공헌 예산, 지자체 교육청).
- 파일럿 = **B2B 쐐기** — 병원 단위 라이선스(per-seat 또는 사이트 라이선스)로 수익화.
- 소아암 환아 보호자에게 청구하지 않음 → CSR·재단·공공 예산으로 우회.

## 권고 스택 (3주 MVP)

**Clerk + Stripe + 포트원(국내 B2B) + 부모 이메일 가입 우선 + Google OAuth는 14+/교사 한정**

- Google OAuth를 기본 진입점으로 두지 않는다 = PIPA 리스크 제거.
- MVP 스모크테스트는 부모 이메일 하드코드 1계정으로 시작 → 본 파일럿 전 가입 플로우 완성.

## Sources
- 클럭·Supabase·NextAuth/Auth.js·Firebase 공식 문서 (라이브 재검증 필요)
- 한국 개인정보보호법 제22조의2, COPPA §312
- 엘리스 academy.elice.io, 코드잇 키즈 codeit.kr, 구름EDU goorm.io
- 경쟁사 가격: bolt.new/pricing, lovable.dev/pricing, v0.app/pricing, replit.com/pricing

## Open Questions
- [ ] Clerk Billing GA 상태 (배포 직전 재확인)
- [ ] Stripe KR 정식 서비스 가용성
- [ ] 국립암센터 병원 IT 정책상 whitelisting 절차 ([[environ-kukrip-amsenter]] 후속)
- [ ] 파일럿 당일 실제 가입 방식 — 부모 동의서 지면 + 운영자 계정 생성 대행 vs 사전 온라인 가입
- [ ] 소아암재단·CSR 스폰서 후보 리스트
