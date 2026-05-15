---
type: deliverable
status: delivered
priority: 2
owner: "[[jinyong-shin]]"
due_date: 2026-04-25
tags:
  - deliverable
  - pilot
  - ai
created: 2026-04-12
updated: 2026-05-15
---

# Cline + Gemini 자동 연동

## 목표
- [[cline]] Extension이 [[code-server]] 이미지에 사전 설치되어, 수강생 진입 즉시 [[gemini-2-5-flash]] 와 대화 가능.

## 수용 기준
- [ ] Cline 익스텐션이 code-server 이미지에 포함.
- [ ] 환경변수로 Gemini API Key가 주입되어 수강생 설정 불필요.
- [ ] [[fast-implementation-mode]] 지침이 시스템 프롬프트에 반영.
- [ ] 테스트: "점프하는 캐릭터 만들어줘" 입력 → 실제 코드 생성·실행 확인.

## 진행 현황
- 미시작.

## 의존성
- [[pilot-gemini-api-key]] 완료.
- [[sans-kids-school-2025]] 템플릿 결정.

## 관련
- [[cline]] · [[gemini-2-5-flash]] · [[pilot-env-design]]
