---
name: pilot-deploy
description: "HypeProof Kids Edu 파일럿 환경을 한 번에 배포. 의존성 설치 → Cloudflare Quick Tunnel 2개 기동 → _backend.js / .env.local 자동 작성 → uvicorn + next dev 백그라운드 실행 → 외부 접속 가능한 프론트 URL 1개 출력. Triggers: pilot-deploy, /pilot-deploy, 파일럿 배포, 띄워줘, 배포해줘, deploy pilot, set up pilot, 새 환경에 배포, 외부 접속 URL 만들어줘."
allowed-tools: Bash Read Write Edit Glob Grep
---

# pilot-deploy: 파일럿 배포 자동화

새 운영자가 레포 클론 직후 한 번 호출하면 외부 접속 가능한 URL이 나오는 것이 목적. 이미 떠 있는 서버가 있으면 스킵하고 누락된 부분만 채운다.

## 작동 원칙

1. **멱등** — 이미 돌아가는 프로세스는 죽이지 않는다. `lsof -i :PORT` 로 확인.
2. **복구 가능** — 실패하면 사용자에게 어디서 멈췄는지 + 다음 명령 안내.
3. **시크릿 보존** — 기존 `.env.local`이 있으면 덮어쓰지 않음. 누락된 키만 prompt.
4. **마지막 출력은 짧게** — 프론트 URL · 로그인 정보 · 종료 명령. 그 이상은 운영자 산만하게 함.

## 실행 순서

### 0. 사전 진단

```bash
# 작업 디렉토리 확인
test -f src/backend/main.py && test -f src/frontend/package.json
```

해당 파일이 없으면 "레포 루트에서 실행해주세요" 안내하고 중단.

```bash
# 도구 존재 확인
for cmd in git uv node npm cloudflared; do
  command -v $cmd >/dev/null || echo "MISSING: $cmd"
done
```

`uv` 누락 → `brew install uv`. `cloudflared` 누락 → `brew install cloudflared`. node 누락 → `brew install node`. 사용자에게 한 줄로 안내한 뒤 설치 동의 받고 진행.

### 1. 시크릿 점검

`src/backend/.env.local` 존재 여부 확인. 없으면 `.env.example` 복사 후, 누락된 키만 사용자에게 묻는다.

```bash
test -f src/backend/.env.local || cp src/backend/.env.example src/backend/.env.local
```

필수 키 (`grep -c "^KEY=$" src/backend/.env.local` 로 빈 값 확인):
- `ZAI_API_KEY` — z.ai GLM-5 텍스트 모델 키
- `GEMINI_API_KEY` — (선택) 이미지 생성용. 비어 있어도 텍스트 흐름은 동작함.
- `ADMIN_USERNAME` / `ADMIN_PASSWORD` — 운영자 로그인. 디폴트 `root` / `0000` 권장 안 함.

비어 있는 값을 발견하면 사용자에게 차례로 묻고 채워 넣는다. **이미 채워진 키는 그대로 두고 절대 덮어쓰지 않는다.**

### 2. Cloudflare Quick Tunnel 기동 (이미 떠 있으면 스킵)

```bash
# 백엔드 터널이 이미 떠 있는지 확인
pgrep -f "cloudflared tunnel --url http://localhost:8000" >/dev/null \
  || nohup cloudflared tunnel --url http://localhost:8000 > /tmp/cf_be.log 2>&1 & disown

# 프론트 터널
pgrep -f "cloudflared tunnel --url http://localhost:3000" >/dev/null \
  || nohup cloudflared tunnel --url http://localhost:3000 > /tmp/cf_fe.log 2>&1 & disown

sleep 5
```

URL 추출:

```bash
BE_URL=$(grep -oE 'https://[a-z0-9-]+\.trycloudflare\.com' /tmp/cf_be.log | head -1)
FE_URL=$(grep -oE 'https://[a-z0-9-]+\.trycloudflare\.com' /tmp/cf_fe.log | head -1)
```

URL이 비면 5초 더 대기 후 재시도. 3회 실패 시 사용자에게 cloudflared 로그 경로 (`/tmp/cf_be.log`, `/tmp/cf_fe.log`) 안내하고 중단.

### 3. 런타임 URL 주입

**`src/frontend/public/_backend.js`** — 항상 새로 작성 (터널 URL은 매번 바뀜):

```bash
echo "window.__BACKEND_URL__ = \"$BE_URL\";" > src/frontend/public/_backend.js
```

**`src/frontend/.env.local`** — 매번 새로 작성:

```bash
cat > src/frontend/.env.local <<EOF
NEXT_PUBLIC_BACKEND_HTTP_URL=$BE_URL
NEXT_PUBLIC_BACKEND_WS_URL=$(echo $BE_URL | sed 's|^https|wss|')
EOF
```

**`src/backend/.env.local`** — `BACKEND_BASE_URL` 만 갱신 (다른 키는 보존):

```bash
if grep -q '^BACKEND_BASE_URL=' src/backend/.env.local; then
  sed -i '' "s|^BACKEND_BASE_URL=.*|BACKEND_BASE_URL=$BE_URL|" src/backend/.env.local
else
  echo "BACKEND_BASE_URL=$BE_URL" >> src/backend/.env.local
fi
```

### 4. 의존성 설치 (이미 있으면 스킵)

```bash
test -d src/backend/.venv || (cd src/backend && uv sync)
test -d src/frontend/node_modules || (cd src/frontend && npm install)
```

`npm install`은 캐시 없을 때 30~60초 걸린다. 진행 중임을 사용자에게 한 번 알려준다.

### 5. 백엔드 기동 (이미 떠 있으면 스킵)

```bash
if ! lsof -i :8000 >/dev/null 2>&1; then
  cd src/backend
  nohup env $(grep -v '^#' .env.local | xargs) \
    uv run uvicorn main:app --host 0.0.0.0 --port 8000 \
    > /tmp/kids_be.log 2>&1 & disown
  cd ../..
  sleep 3
fi
```

검증: `curl -s http://localhost:8000/health` 가 `{"status":"ok"}` 인지. 아니면 `/tmp/kids_be.log` tail 보여주고 중단.

### 6. 프론트 기동 (이미 떠 있으면 스킵)

```bash
if ! lsof -i :3000 >/dev/null 2>&1; then
  cd src/frontend
  nohup npm run dev > /tmp/kids_fe.log 2>&1 & disown
  cd ../..
  sleep 5
fi
```

검증: `curl -s -o /dev/null -w "%{http_code}\n" http://localhost:3000/` 이 `200`.

### 7. 외부 도달 검증

```bash
curl -s -o /dev/null -w "%{http_code}\n" "$BE_URL/health"   # 200 기대
curl -s -o /dev/null -w "%{http_code}\n" "$FE_URL/"         # 200 기대
```

둘 다 200이면 성공. 둘 중 하나라도 실패면 cloudflared 로그 안내.

### 8. 최종 출력

성공 시 사용자에게 다음만 출력:

```
✅ 파일럿 환경 배포 완료

🌐 외부 접속 (아이용)
   <FE_URL>

🔑 로그인
   ID: <ADMIN_USERNAME>
   PW: <ADMIN_PASSWORD>

🛠 운영 명령
   상태:   /pilot-status
   종료:   /pilot-stop  (또는 pkill -f "uvicorn main:app|next-server|cloudflared tunnel")
   재시작: /pilot-deploy

⚠️ 맥 절전이 들어가면 외부 접속이 끊깁니다 — `caffeinate -d` 권장.
```

`<FE_URL>`, `<ADMIN_USERNAME>`, `<ADMIN_PASSWORD>` 는 위 단계에서 추출한 실제 값.

## 자주 만나는 실패

| 증상 | 진단 | 해결 |
|---|---|---|
| `MISSING: cloudflared` | brew 미설치 | `brew install cloudflared` 안내 |
| BE_URL 비어 있음 | cloudflared가 5초 안에 URL 못 받음 | 3회 재시도, 그래도 실패면 인터넷·방화벽 점검 |
| `/health` 200 아닌 응답 | uvicorn 기동 실패 (포트 충돌, env 누락) | `tail /tmp/kids_be.log` 사용자에게 보여주기 |
| 프론트 "로딩 중" 무한 (배포 후) | `_backend.js`가 stale | 3단계 다시 — 동일 스킬 재실행으로 해결됨 |
| 동시 실행 중 다른 프로세스 충돌 | 기존 터널이 다른 URL 가리킴 | `pkill -f "cloudflared tunnel"` 후 재실행 |

## 관련 문서

- 배포 구조 개요: 루트 `CLAUDE.md` 의 "배포 구조" 섹션
- 수동 절차: `kids_edu_vault/wiki/runbooks/deployment.md`
- 정식 운영(named tunnel) 전환 검토: `kids_edu_vault/wiki/decisions/` (해당 ADR 작성 시)

## 만들지 않은 이유

- 자동 시크릿 회전 — 파일럿 1회용이라 과잉.
- Docker 컨테이너화 — quick tunnel 안에서 호스트 포트 노출이 까다로움. Named tunnel 전환 시 같이 검토.
- 헬스체크 모니터링 루프 — 운영자가 직접 보는 게 더 빠름.
