---
type: runbook
status: stub
title: "Pilot Deploy 슬래시 커맨드"
created: 2026-05-15
updated: 2026-05-15
tags:
  - runbook
  - deployment
  - pilot
---

# /pilot-deploy 슬래시 커맨드

파일럿 환경 배포 자동화 슬래시 커맨드. 전체 수동 배포 절차는 [[deployment]] 참조.

## 기능
`/pilot-deploy` 실행 시 아래를 자동화:
1. 의존성 설치 (`uv sync`, `npm install`)
2. FastAPI 백엔드 기동 (port 8000)
3. Next.js 프론트 기동 (port 3000)
4. Cloudflare Quick Tunnel 양쪽 개통

## 관련
- [[deployment]] — 수동 배포 절차 전문
- [[pilot-day-operation]] — 파일럿 당일 운영 절차
