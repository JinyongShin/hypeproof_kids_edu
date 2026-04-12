---
type: component
status: active
stack_layer: platform
version: "latest"
license: MIT
repo: "https://github.com/coder/code-server"
tags:
  - component
  - pilot
created: 2026-04-12
updated: 2026-04-12
---

# code-server

## 역할
- 브라우저에서 VS Code를 실행. 수강생이 설치 없이 링크만으로 IDE 접속.
- 실습 파일·게임 스타터 템플릿 자동 탑재.

## 설정 / 구성
- 각 수강생 세션은 컨테이너 격리(추정) — 세부는 [[pilot-env-design]].
- [[caddy]] 뒤에서 HTTPS로만 노출. [[oauth2-proxy]] 앞단에서 인증.

## 의존성
- [[oauth2-proxy]] (Google OAuth)
- [[caddy]] (HTTPS + 리버스 프록시)
- [[cline]] (VS Code Extension)

## 대안 및 비교
- GitHub Codespaces: 편리하지만 **수강생 GitHub 계정** 필요 + 비용 증가.
- GitPod: 유사하나 운영 자유도 낮음.

## 운영 주의사항
- 소아병동 네트워크 환경에서 WebSocket 끊김 가능성 — 리허설에서 확인 필요 ([[environ-kukrip-amsenter]]).

## 관련
- [[pilot-env-design]]
