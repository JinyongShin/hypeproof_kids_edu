---
type: deliverable
status: delivered
priority: 2
owner: "[[jinyong-shin]]"
due_date: 2026-04-25
tags:
  - deliverable
  - pilot
  - auth
created: 2026-04-12
updated: 2026-05-15
---

# OAuth 연동 + HTTPS

## 목표
- [[caddy]] + [[oauth2-proxy]] 조합으로 HTTPS·Google 로그인 게이트 구축.

## 수용 기준
- [ ] Google OAuth Client 등록.
- [ ] 어린이 계정 **화이트리스트**에 실제 수강생 이메일 등록.
- [ ] Let's Encrypt 인증서 발급 성공.
- [ ] 비인가 계정 접속 시 차단 확인.

## 진행 현황
- 미시작. Google 계정 보유 여부 Jay 확인 대기.

## 의존성
- [[pilot-server-domain]] 완료 후.
- 수강생 Google 계정 보유 여부 확정 (없으면 운영자 대리 로그인 설계 변경).

## 관련
- [[oauth2-proxy]] · [[caddy]] · [[pilot-env-design]]
