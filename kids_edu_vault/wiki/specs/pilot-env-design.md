---
type: spec
status: draft
owner: "[[jinyong-shin]]"
target_date: 2026-05-05
tags:
  - spec
  - pilot
created: 2026-04-12
updated: 2026-04-12
---

# Pilot 실행환경 설계

## 목적
- 2026-05-05 소아암 병동에서 **브라우저만으로** 아이들이 AI와 대화하며 HTML/JS 게임을 만드는 엔드투엔드 환경 제공.
- 설치·코딩 지식·API Key 불필요.

## 요구사항
- 접속: `https://hypeproof-ai.xyz` 단일 URL.
- 인증: Google 계정 로그인, 어린이 계정 **화이트리스트**.
- 실습: 브라우저 VS Code + AI 채팅 + 즉시 실행 preview.
- 비용: 파일럿 1회 **$0.15 미만**.
- 안정성: 당일 치명 장애 0건 ([[okr-q2-jy]] KR2).

## 설계
```
[브라우저]
    │ HTTPS
    ▼
[[caddy]]  ──TLS·프록시──►  [[oauth2-proxy]]  ──인증 후──►  [[code-server]]
                                                             │
                                                             ▼
                                                        [[cline]] ──► [[gemini-2-5-flash]]
                                                             │
                                                             ▼
                                                   [[sans-kids-school-2025]] 자산 탑재
```

## 구성 요소
- [[caddy]] — HTTPS + 리버스 프록시.
- [[oauth2-proxy]] — Google OAuth 화이트리스트.
- [[code-server]] — 브라우저 VS Code.
- [[cline]] — AI 채팅 익스텐션.
- [[gemini-2-5-flash]] — AI 튜터 모델.
- [[sans-kids-school-2025]] — 게임 스타터 + 워크플로우.

## 운영 모드
- AI 튜터: [[fast-implementation-mode]] (빠른 구현 우선).

## 수용 기준
- [ ] 수강생 5명 이상이 Google OAuth 로그인 → 실습 환경 진입 → 1개 과제 실행 완료 ([[okr-q2-jy]] KR1).
- [ ] 당일 치명적 장애 0건.
- [ ] 운영자 가이드로 제3자가 세팅·실행 성공 (KR3).

## 위험·미정 사항
- 병동 WiFi 안정성 — WebSocket 유지 여부 확인 필요 ([[environ-kukrip-amsenter]]: 와이파이 지원 가능이라 회신).
- 어린이들이 **Google 계정을 가지고 있는지** 미확인 — 운영자 계정 대리 로그인 플랜 B 필요.
- 어린이 인원 수 미확정 — 서버 스펙 결정 대기.

## 관련
- [[2026-04-11-call-note]] · [[environ-kukrip-amsenter]]
- [[pilot-gemini-api-key]] · [[pilot-server-domain]] · [[pilot-oauth-setup]]
