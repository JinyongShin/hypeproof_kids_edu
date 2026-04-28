---
type: runbook
title: "Deployment — 파일럿 환경 수동 배포"
status: active
created: 2026-04-28
updated: 2026-04-28
tags:
  - runbook
  - deployment
  - pilot/2026-05-05
---

# Deployment — 수동 배포 절차

운영자 맥북에서 백엔드(FastAPI/uvicorn) + 프론트(Next.js dev) + Cloudflare Quick Tunnel 2개를 띄우는 절차. 자동화는 [[pilot-deploy]] 스킬 사용.

## 사전 조건

| 도구 | 확인 명령 | 설치 (macOS) |
|---|---|---|
| `git` | `git --version` | 기본 포함 |
| `uv` | `uv --version` | `brew install uv` |
| `node` ≥ 20 | `node --version` | `brew install node` |
| `cloudflared` | `cloudflared --version` | `brew install cloudflared` |

## 1. 소스 받기

```bash
git clone https://github.com/JinyongShin/hypeproof_kids_edu.git
cd hypeproof_kids_edu
```

## 2. 시크릿 채우기

```bash
cp src/backend/.env.example src/backend/.env.local
vi src/backend/.env.local
```

필수 키:
- `ZAI_API_KEY` — z.ai (GLM-5) 텍스트 모델
- `GEMINI_API_KEY` — Google GenAI (이미지)
- `ADMIN_USERNAME` / `ADMIN_PASSWORD` — 운영자 로그인
- `BACKEND_BASE_URL` — Cloudflare 백엔드 터널 URL (3단계 후 채움)

## 3. Cloudflare Quick Tunnel 2개 기동

```bash
nohup cloudflared tunnel --url http://localhost:8000 > /tmp/cf_be.log 2>&1 &
nohup cloudflared tunnel --url http://localhost:3000 > /tmp/cf_fe.log 2>&1 &
sleep 5
grep "trycloudflare.com" /tmp/cf_be.log /tmp/cf_fe.log
```

각각 `https://<random>.trycloudflare.com` URL이 출력된다. 백엔드 URL은 BE_URL, 프론트 URL은 FE_URL.

## 4. 백엔드용 URL 반영

```bash
# .env.local 의 BACKEND_BASE_URL을 BE_URL로 수정
sed -i '' "s|^BACKEND_BASE_URL=.*|BACKEND_BASE_URL=$BE_URL|" src/backend/.env.local
```

## 5. 프론트 환경변수 + 런타임 오버라이드

```bash
cat > src/frontend/.env.local <<EOF
NEXT_PUBLIC_BACKEND_HTTP_URL=$BE_URL
NEXT_PUBLIC_BACKEND_WS_URL=$(echo $BE_URL | sed 's|^https|wss|')
EOF

cat > src/frontend/public/_backend.js <<EOF
window.__BACKEND_URL__ = "$BE_URL";
EOF
```

## 6. 의존성 설치

```bash
cd src/backend && uv sync
cd ../frontend && npm install
```

## 7. 서버 기동

```bash
# 백엔드
cd src/backend
nohup env $(cat .env.local | xargs) uv run uvicorn main:app --host 0.0.0.0 --port 8000 > /tmp/kids_be.log 2>&1 &

# 프론트
cd ../frontend
nohup npm run dev > /tmp/kids_fe.log 2>&1 &
```

## 8. 검증

```bash
curl -s http://localhost:8000/health           # {"status":"ok"}
curl -s -o /dev/null -w "%{http_code}\n" http://localhost:3000/   # 200
curl -s "$BE_URL/health"                       # {"status":"ok"} (외부에서 도달 가능)
```

## 9. 외부 URL 공지

`$FE_URL` 을 운영자/조교에게 공지. 로그인 정보는 `.env.local`의 `ADMIN_USERNAME` / `ADMIN_PASSWORD`.

## 종료

```bash
pkill -f "uvicorn main:app"
pkill -f "next-server"
pkill -f "cloudflared tunnel"
```

## 트러블슈팅

| 증상 | 원인 | 해결 |
|---|---|---|
| 프론트 "로딩 중" 무한 | `.env.local`의 백엔드 URL이 죽었음 | 4·5단계 다시 |
| 외부 URL 응답 안 됨 | cloudflared 죽음 | 3단계부터 다시 (URL 새로 발급됨) |
| `npm run dev` 에서 호스트 차단 경고 | `next.config.ts` `allowedDevOrigins` 누락 | 이미 `*.trycloudflare.com` 허용됨 — 다른 호스트면 추가 |
| 게임 저장 안 됨 | DB 마이그레이션 미실행 | uvicorn 첫 기동 로그에서 `games 테이블에 saved 컬럼 추가` 확인 |

## 자동화

`/pilot-deploy` 슬래시 커맨드가 위 1~9단계를 한 번에 처리한다. 새 운영자는 이 runbook 대신 `claude` 띄운 뒤 슬래시 커맨드를 쓰면 됨.

## 한계

- Quick tunnel은 cloudflared 재시작마다 URL 바뀜 → 파일럿 D-day 전에 **Named Tunnel + 고정 도메인**으로 전환 권장.
- 맥 절전 들어가면 외부 접속 끊김 → `caffeinate -d` 또는 시스템 설정에서 절전 OFF.
- SQLite 단일 파일 — 동시 쓰기 부하 시 락 가능성. 40명 동시 접속은 [[load-test]] 결과 참고.
