---
type: component
status: active
stack_layer: infra
version: "2.x"
license: Apache-2.0
repo: "https://github.com/caddyserver/caddy"
tags:
  - component
  - pilot
  - infra
created: 2026-04-12
updated: 2026-04-12
---

# Caddy

## 역할
- 리버스 프록시 + HTTPS 자동 인증서(Let's Encrypt).
- `hypeproof-ai.xyz` 도메인 TLS 처리, [[oauth2-proxy]] 로 트래픽 전달.

## 설정 / 구성
- Caddyfile에 도메인·업스트림 정의.
- ACME challenge 통과를 위해 80/443 포트 개방 필요.

## 의존성
- DNS: 도메인 `hypeproof-ai.xyz` 구매 + A 레코드 설정.

## 대안 및 비교
- Nginx + Certbot: 수동 갱신·설정량 많음.
- Traefik: Caddy와 유사, 파일럿엔 Caddy가 더 단순.

## 운영 주의사항
- 인증서 발급 실패 시 HTTP로라도 접근 가능해야 리허설이 덜 막힘 (fallback 고려).

## 관련
- [[pilot-env-design]]
