---
type: component
status: active
stack_layer: platform
version: "latest"
license: MIT
repo: "https://github.com/oauth2-proxy/oauth2-proxy"
tags:
  - component
  - pilot
  - auth
created: 2026-04-12
updated: 2026-04-12
---

# oauth2-proxy

## 역할
- Google OAuth 게이트웨이. `hypeproof-ai.xyz` 접속 시 Google 로그인 → 화이트리스트 확인 → [[code-server]] 로 프록시.

## 설정 / 구성
- Google OAuth Client 등록 필요 — 파일럿 전 발급.
- 어린이 계정 **화이트리스트**로만 통과. 수강생 인원 확정 후 등록.
- 세션 쿠키 도메인: `hypeproof-ai.xyz`.

## 의존성
- Google OAuth Client Credentials.
- [[caddy]] 리버스 프록시 뒤.

## 대안 및 비교
- 자체 구현 OIDC: 관리 복잡, 파일럿 규모에 과함.
- Auth0: 유료, 파일럿 1회에 불필요.

## 운영 주의사항
- 화이트리스트 등록 누락 시 수강생 로그인 실패 — 리허설·당일 사전 점검 필수.
- Jay 확인 필요: 어린이들이 Google 계정이 있는지. 없으면 운영자 계정으로 대리 로그인 방식 검토.

## 관련
- [[pilot-env-design]] · [[environ-kukrip-amsenter]]
