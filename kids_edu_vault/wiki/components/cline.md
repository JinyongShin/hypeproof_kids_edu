---
type: component
status: active
stack_layer: ai
version: "latest"
license: Apache-2.0
repo: "https://github.com/cline/cline"
tags:
  - component
  - pilot
  - ai
created: 2026-04-12
updated: 2026-04-12
---

# Cline (VS Code Extension)

## 역할
- VS Code(= [[code-server]]) 내 AI 채팅. 아이들이 말을 걸면 게임을 함께 작성.
- "Cursor처럼" 자연어로 코드 생성·수정.

## 설정 / 구성
- [[gemini-2-5-flash]] 를 백엔드 모델로 사전 연동.
- **수강생 본인이 API Key 설정 불필요** — 서버측에서 미리 주입.
- 시스템 프롬프트: [[fast-implementation-mode]] (아이가 원하는 걸 말하면 바로 구현).

## 의존성
- [[gemini-2-5-flash]] API Key (JY 발급).

## 대안 및 비교
- Continue.dev: 유사 기능, 설정 유연하나 UX 복잡.
- GitHub Copilot Chat: GitHub 계정 필요 — 아이들 계정 이슈.

## 운영 주의사항
- Extension 자동 설치 스크립트로 [[code-server]] 이미지에 사전 포함.
- API Key 노출 방지 — 서버 환경변수로만 관리.

## 관련
- [[pilot-env-design]]
