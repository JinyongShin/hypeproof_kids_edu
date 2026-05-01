---
type: decision
title: "Docker Compose + 단일 VPS (fly.io/Railway) 배포"
created: 2026-05-01
updated: 2026-05-01
status: proposed
priority: 2
owner: "JY"
context: "파일럿(2026-05-05) 이후 상품화 단계 — Cloudflare Quick Tunnel URL 불안정·맥북 단일 장애점 해소"
tags:
  - decision
  - architecture
  - deployment
  - infra
  - docker
related:
  - "[[nextjs-fastapi-wrapper-architecture]]"
  - "[[auth-session-game-persistence]]"
  - "[[llm-provider-scaling]]"
  - "[[adr-langgraph-gemini-backend]]"
  - "[[langfuse-observability]]"
deciders:
  - "[[jinyong-shin]]"
---

# Docker Compose + 단일 VPS (fly.io/Railway) 배포

## 결정

파일럿(2026-05-05) 이후 상품화 v1 시점에 **Docker Compose + fly.io 단일 VPS**로 전환한다. 로컬 dev와 VPS 배포를 단일 `docker-compose.yml`로 관리하고, fly.io Volumes로 SQLite 영속화, Cloudflare Named Tunnel로 URL 고정을 달성한다.

## 배경

현행 배포([[nextjs-fastapi-wrapper-architecture]], CLAUDE.md 배포 섹션)의 한계:

- **Quick Tunnel URL 매 재시작 변경** — `_backend.js` / `BACKEND_BASE_URL` 수동 갱신 필수. 상품화 환경에서 운영 불가.
- **맥북 단일 장애점** — 절전 진입 시 외부 접속 즉시 끊김. 파일럿 당일 절전 OFF 필수이나 상시 운영 불가.
- **어카운트리스 정책 위험** — 40명 동시 접속 트래픽 패턴에서 Cloudflare가 accountless tunnel을 차단할 수 있음.
- **확장 불가** — 맥북 로컬은 스케일아웃 경로 없음.

## 결정 사항

### 컨테이너 구성

| 파일 | 내용 |
|---|---|
| `src/backend/Dockerfile` | Python 3.12-slim, `uv sync`, `uvicorn` entrypoint |
| `src/frontend/Dockerfile` | node:20-alpine, `next build`, `next start` |
| `docker-compose.yml` (루트) | backend + frontend 서비스, 로컬 dev + VPS 공용 |

### 영속화

- fly.io Volume `/app/data` 마운트 → `kids_edu.db`, `langgraph.db`([[adr-langgraph-gemini-backend]]) 보존.
- 컨테이너 재시작·배포 시에도 SQLite 데이터 유지.

### URL 고정

- Cloudflare **Named Tunnel** 전환 (파일럿 이후) — 재시작 후에도 동일 subdomain 유지.
- Named Tunnel은 `cloudflared tunnel create` + `config.yml` 기반, accountless 아님.

### 단계별 전환 계획

| 단계 | 시점 | 구성 |
|---|---|---|
| 파일럿 | 2026-05-05 | 현행 Quick Tunnel 유지 (변경 없음) |
| 상품화 v1 | 파일럿 +2주 이내 | fly.io VPS + Named Tunnel 전환 |
| 스케일아웃 | 필요 시 | Cloud Run (backend) + Vercel (frontend) + RDS 검토 |

### 관측성 (Observability) — Langfuse

LangGraph 기반 백엔드([[adr-langgraph-gemini-backend]])의 LLM 호출·그래프 실행 흐름을 추적하기 위해 **Langfuse를 docker-compose 서비스로 셀프호스팅**한다. 상세 설정은 [[langfuse-observability]] 스펙 참조.

#### docker-compose 서비스 추가

`docker-compose.yml`에 두 서비스를 추가한다.

```yaml
langfuse:
  image: langfuse/langfuse:2.95.11
  ports:
    - "3002:3000"
  environment:
    - DATABASE_URL=postgresql://langfuse:langfuse@langfuse_db:5432/langfuse
    - NEXTAUTH_SECRET=${LANGFUSE_NEXTAUTH_SECRET}
    - SALT=${LANGFUSE_SALT}
    - NEXTAUTH_URL=http://localhost:3002
  depends_on:
    - langfuse_db

langfuse_db:
  image: postgres:16-alpine
  environment:
    - POSTGRES_USER=langfuse
    - POSTGRES_PASSWORD=langfuse
    - POSTGRES_DB=langfuse
  volumes:
    - langfuse_db_data:/var/lib/postgresql/data

volumes:
  langfuse_db_data:
```

- **이미지 버전 핀 고정**: `langfuse/langfuse:2.95.11` — `latest` 사용 시 더 높은 버전의 Langfuse가 실행되어 DB 스키마(`ScoreDataType` enum, `observations_view`)가 변경되고 langfuse SDK v2 컨테이너와 충돌이 발생한 이력 있음. 재현성 확보를 위해 2.95.11로 핀 고정.
- **포트**: 3002 — 프론트(3000), 백엔드(8000)와 충돌 없음.
- **데이터 영속화**: `langfuse_db_data` named volume — 컨테이너 재시작 후에도 트레이스 유지.

#### 백엔드 통합

`langfuse.callback.CallbackHandler`를 LangGraph `astream_events` 호출 시 콜백으로 주입한다. 활성화 여부는 환경변수 `LANGFUSE_ENABLED`로 제어하여 파일럿 당일(맥북 환경)에는 오버헤드 없이 비활성화 가능.

필요한 환경변수 (`.env.local`):

| 변수명 | 설명 |
|---|---|
| `LANGFUSE_ENABLED` | `true` / `false` — 콜백 주입 여부 |
| `LANGFUSE_PUBLIC_KEY` | Langfuse 프로젝트 Public Key |
| `LANGFUSE_SECRET_KEY` | Langfuse 프로젝트 Secret Key |
| `LANGFUSE_HOST` | `http://localhost:3002` (로컬) 또는 VPS URL |

#### 제공하는 관측 정보

- **노드별 토큰 사용량** — LangGraph 각 노드의 input/output 토큰 집계
- **그래프 실행 흐름** — 어느 노드가 어느 순서로 호출되었는지 trace
- **레이턴시** — 노드별·전체 그래프 실행 시간
- **비용 추적** — 모델별 단가 기반 자동 비용 계산 (Gemini 모델 단가 등록 필요)

#### LangSmith 대비 선택 이유

| 항목 | Langfuse (채택) | LangSmith |
|---|---|---|
| 호스팅 | 셀프호스팅 가능 | SaaS 전용 |
| 데이터 유출 | 없음 — 로컬/VPS 내부 | 외부 서버로 전송 |
| 비용 | 무료 (오픈소스) | 유료 플랜 필요 |
| 소아암 병동 데이터 | 외부 유출 없음 (규정 준수) | 외부 전송 우려 |

## 대안 및 기각 이유

| 대안 | 기각 이유 |
|---|---|
| Cloudflare Named Tunnel + 맥북 유지 | 장기 맥북 상시 가동 비현실적, 하드웨어 장애 단일 위험 |
| Render / Heroku | fly.io 대비 SQLite Volume 지원 제한적, 가격 불리 |
| AWS EC2 직접 운영 | 운영 부담 과도, fly.io 관리형 대비 이점 없음 |
| Docker 없이 직접 배포 | 로컬 dev와 prod 환경 차이 → 재현 불가 버그 위험 |
| 파일럿에 즉시 적용 | D-4 시점에 배포 구조 변경은 리스크 과대. 파일럿은 현행 유지. |
| LangSmith (관측성) | SaaS — 소아암 환아 데이터 외부 전송 우려. 셀프호스팅 Langfuse 채택. |

## 영향 범위

- **신규 파일**: `src/backend/Dockerfile`, `src/frontend/Dockerfile`, `docker-compose.yml` (루트), `fly.toml`.
- **변경 파일**: `src/backend/.env.example` — `BACKEND_BASE_URL`, `LANGFUSE_*` 환경변수 예시 추가. `src/frontend/public/_backend.example.js` — Named Tunnel URL 예시로 갱신.
- **gitignore 추가**: `src/backend/data/langgraph.db` (로컬 체크포인터 파일).
- **운영 절차**: `kids_edu_vault/wiki/runbooks/deployment.md` — Docker Compose + fly.io 배포 단계 추가.
- **스펙 신규**: [[langfuse-observability]] — Langfuse 셀프호스팅 설정·통합 상세.
- **파일럿 당일(2026-05-05)**: 영향 없음. 현행 Quick Tunnel 절차 유지. Langfuse는 `LANGFUSE_ENABLED=false`로 비활성.

## Open Questions

- [ ] fly.io 무료 티어 RAM (256MB) vs. 유료 (512MB~) — Next.js `next build` 메모리 요구량 확인 필요.
- [ ] Named Tunnel 도메인 — `hypeproof.kr` 서브도메인 사용 여부. 도메인 소유 확인 필요.
- [ ] `langgraph.db`([[adr-langgraph-gemini-backend]])와 `kids_edu.db`를 같은 Volume에 둘지, Volume 분리 여부.
- [ ] fly.io Volume는 단일 리전. 멀티리전 요구 시 Litestream(SQLite 스트리밍 복제) 도입 검토.
- [ ] Langfuse VPS 배포 시 fly.io Volume에 Postgres 데이터 포함 여부 — 별도 managed Postgres (fly.io Postgres) 사용 검토.
- [ ] Gemini 모델 단가를 Langfuse에 등록하는 방법 확인 필요 (커스텀 모델 정의).

## 관련

- [[nextjs-fastapi-wrapper-architecture]]
- [[auth-session-game-persistence]]
- [[llm-provider-scaling]]
- [[adr-langgraph-gemini-backend]]
- [[langfuse-observability]]
- [[pilot-server-domain]]
