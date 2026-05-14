---
type: decision
title: "ADR: 컨테이너 배포 전략"
status: active
created: 2026-05-01
updated: 2026-05-14
tags:
  - decision
  - adr
  - deployment
  - docker
  - flyio
---

# ADR: 컨테이너 배포 전략 (Docker + fly.io)

**날짜**: 2026-05-01  
**브랜치**: `feature/langgraph-gemini`  
**상태**: active (파일럿은 Cloudflare Quick Tunnel, 정식 운영은 fly.io 예정)

---

## 결정

백엔드 + 프론트엔드 + Langfuse를 **Docker 컨테이너**로 패키징하고, 정식 운영은 **fly.io (도쿄 리전)**에 배포.

---

## 배경 — Quick Tunnel 방식의 한계

파일럿 배포 방식(Cloudflare Quick Tunnel + 운영자 맥북)은 다음 문제가 있음:

| 한계 | 내용 |
|------|------|
| URL 불안정 | cloudflared 재시작마다 URL 변경 → `_backend.js` 수동 갱신 필요 |
| 가용성 | 맥 절전 시 외부 접속 끊김 |
| 동시 접속 | Cloudflare 어카운트리스 정책 — 40명 동시 접속 미검증 |
| 확장성 없음 | 여러 파일럿 고객(SK바이오팜, 보아치과)을 동시에 운영할 수 없음 |

---

## 컨테이너 구성

### 서비스 구조 (`docker-compose.yml`)

```
backend   (port 8000)  ← python:3.12-slim + uv + FastAPI/LangGraph
frontend  (port 3000)  ← Node.js + Next.js
langfuse  (port 3002)  ← langfuse/langfuse:2.95.11
langfuse-db            ← postgres:16-alpine
```

### 백엔드 Dockerfile (`src/backend/Dockerfile`)

```dockerfile
FROM python:3.12-slim
WORKDIR /app
COPY --from=ghcr.io/astral-sh/uv:latest /uv /usr/local/bin/uv
COPY pyproject.toml uv.lock* ./
RUN uv sync --frozen --no-dev
COPY . .
RUN mkdir -p data/games data/cards
EXPOSE 8000
CMD ["uv", "run", "uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
```

- `uv sync --frozen --no-dev`: 재현 가능한 의존성 설치
- `data/` 디렉토리: SQLite DB + 게임 HTML 파일 영속화 대상

### 프론트엔드 Dockerfile (`src/frontend/Dockerfile`)

Next.js standalone 빌드. 빌드 시 `NEXT_PUBLIC_BACKEND_HTTP_URL` / `NEXT_PUBLIC_BACKEND_WS_URL` ARG 주입.

### Langfuse 구성

```yaml
langfuse:
  image: langfuse/langfuse:2.95.11  # v2 패치버전 핀 고정
  ports: ["3002:3000"]
  environment:
    DATABASE_URL: postgresql://langfuse:langfuse_local@langfuse-db:5432/langfuse
    NEXTAUTH_SECRET: ...
    NEXTAUTH_URL: http://localhost:3002
```

v2를 채택한 이유: v3는 ClickHouse + S3/MinIO 필요 → 로컬/소규모 운영에 오버스펙. VPS 전환 시 v3 재검토.

---

## fly.io 배포 설정 (`fly.toml`)

```toml
app = "kids-edu"
primary_region = "nrt"   # 도쿄 — 한국 가장 가까운 fly.io 리전

[build]
  dockerfile = "src/backend/Dockerfile"

[[services]]
  internal_port = 8000
  [services.concurrency]
    type = "requests"
    hard_limit = 50
    soft_limit = 40

[[mounts]]
  source = "kids_edu_data"
  destination = "/app/data"  # SQLite + 게임 파일 영속 볼륨
```

- 동시 요청 한도: soft 40 / hard 50 (40명 파일럿 기준)
- `/app/data` 영속 볼륨: 서버 재시작 후에도 게임·세션 유지

---

## 배포 단계별 전략

| 단계 | 방식 | 대상 |
|------|------|------|
| 파일럿 D-day | Quick Tunnel (운영자 맥북) | 소아암 병동 (1회성) |
| SK바이오팜 파일럿 (2026-06~07) | fly.io 배포 권장 | 다회차, 외부 접속 안정성 필요 |
| 정식 운영 | fly.io + Named Tunnel (본인 도메인) | 멀티 파일럿 고객 |

---

## 환경 변수 구분

- `.env.local` (gitignore): `GEMINI_API_KEY`, `ADMIN_USERNAME`, `ADMIN_PASSWORD`, `LANGFUSE_*`
- fly.io secrets: `fly secrets set GEMINI_API_KEY=...`로 주입

---

## 관련 페이지

- [[adr-langgraph-gemini-backend]] — 배포 대상 백엔드 구현 결정
- [[adr-multitenant-schema]] — 멀티 파일럿 대응 DB 스키마
- [[langfuse-observability]] — Langfuse 서비스 상세 설정
- [[pilot-env-design]] — 파일럿 환경 설계 전체 스펙
