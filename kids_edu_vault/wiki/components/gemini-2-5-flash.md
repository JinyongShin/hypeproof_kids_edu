---
type: component
status: active
stack_layer: ai
version: "2.5-flash"
license: "Google proprietary API"
tags:
  - component
  - pilot
  - ai
created: 2026-04-12
updated: 2026-04-12
---

# Gemini 2.5 Flash

## 역할
- 파일럿 AI 튜터 모델. [[cline]] 에서 호출되어 아이들 요청에 코드로 응답.

## 설정 / 구성
- API Key는 서버 환경변수로 주입 (수강생 미관여).
- 시스템 프롬프트에 [[fast-implementation-mode]] 지침 포함.

## 의존성
- Google AI Studio / Vertex AI 계정.

## 대안 및 비교
- Claude: 품질 ↑, 비용 ↑. 파일럿 목표 비용 $0.15 미만이라 Flash 우선.
- Gemini Pro: 품질 ↑, 지연 ↑ — 아이 체감 대기 시간 증가 위험.
- GPT-4o-mini: 비교 대상이나 Google 생태계 통합(OAuth 등) 이점에서 Gemini가 유리.

## 운영 주의사항
- Rate limit 초과 시 fallback 계획 필요 (다른 API Key 세트? 큐잉?).
- 아이들이 부적절한 요청 시 모델 응답 안전장치 — 시스템 프롬프트에 명시.

## 비용
- 파일럿 1회 예상: ~$0.09 (전체 $0.15 미만의 주요 구성요소).

## 관련
- [[pilot-env-design]] · [[fast-implementation-mode]]
