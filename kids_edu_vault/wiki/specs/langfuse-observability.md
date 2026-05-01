---
type: spec
status: draft
owner: "[[jinyong-shin]]"
target_date: 2026-05-19
created: 2026-05-01
updated: 2026-05-01
tags:
  - spec
  - observability
  - langfuse
  - langgraph
  - docker
related:
  - "[[adr-container-deployment]]"
  - "[[adr-langgraph-gemini-backend]]"
---

# Langfuse 관측성 스펙

## 개요

Langfuse는 LLM 애플리케이션을 위한 오픈소스 관측성(Observability) 플랫폼이다. LangGraph 기반 백엔드([[adr-langgraph-gemini-backend]])의 그래프 실행 흐름, 노드별 토큰 사용량, 레이턴시, 비용을 추적하기 위해 **셀프호스팅** 방식으로 운영한다.

셀프호스팅을 선택한 이유:
- 소아암 환아 데이터가 외부 SaaS 서버로 전송되지 않음 (데이터 규정 준수)
- 오픈소스 — 무료
- [[adr-container-deployment]]의 docker-compose 구성에 서비스로 통합 가능

---

## 아키텍처

```
백엔드 (FastAPI + LangGraph)
    │ CallbackHandler
    ▼
Langfuse Server (localhost:3002)
    │ psycopg2
    ▼
PostgreSQL 16 (langfuse_db_data volume)
```

---

## docker-compose 설정

`docker-compose.yml` 루트 파일에 두 서비스를 추가한다.

```yaml
services:
  # ... 기존 backend, frontend 서비스 ...

  langfuse:
    image: langfuse/langfuse:latest
    ports:
      - "3002:3000"
    environment:
      - DATABASE_URL=postgresql://langfuse:langfuse@langfuse_db:5432/langfuse
      - NEXTAUTH_SECRET=${LANGFUSE_NEXTAUTH_SECRET}
      - SALT=${LANGFUSE_SALT}
      - NEXTAUTH_URL=http://localhost:3002
      - TELEMETRY_ENABLED=false
    depends_on:
      langfuse_db:
        condition: service_healthy
    restart: unless-stopped

  langfuse_db:
    image: postgres:16-alpine
    environment:
      - POSTGRES_USER=langfuse
      - POSTGRES_PASSWORD=langfuse
      - POSTGRES_DB=langfuse
    volumes:
      - langfuse_db_data:/var/lib/postgresql/data
    healthcheck:
      test: ["CMD-SHELL", "pg_isready -U langfuse"]
      interval: 5s
      timeout: 5s
      retries: 5
    restart: unless-stopped

volumes:
  langfuse_db_data:
```

> [!note]
> `LANGFUSE_NEXTAUTH_SECRET`과 `LANGFUSE_SALT`는 `.env.local`에 임의 문자열로 설정. 운영 환경에서는 반드시 강한 랜덤값 사용.

---

## 초기 설정 절차

### 1. 서비스 기동

```bash
docker compose up -d langfuse langfuse_db
```

### 2. 관리 UI 접속 및 계정 생성

1. 브라우저에서 `http://localhost:3002` 접속
2. "Sign Up" 클릭 → 관리자 계정 생성 (이메일 + 비밀번호)
3. 로그인 후 "Create New Organization" → 조직명 입력 (예: `hypeproof-kids-edu`)
4. "Create New Project" → 프로젝트명 입력 (예: `pilot-2026-05-05`)

### 3. API 키 발급

1. 프로젝트 설정 → "API Keys" 탭
2. "Create new API key" 클릭
3. Public Key (`pk-lf-...`)와 Secret Key (`sk-lf-...`) 복사

### 4. `.env.local` 설정

`src/backend/.env.local`에 아래 항목 추가:

```bash
LANGFUSE_ENABLED=true
LANGFUSE_PUBLIC_KEY=pk-lf-xxxxxxxxxxxx
LANGFUSE_SECRET_KEY=sk-lf-xxxxxxxxxxxx
LANGFUSE_HOST=http://localhost:3002
```

파일럿 당일(맥북 로컬 환경)에는 `LANGFUSE_ENABLED=false`로 비활성화하여 오버헤드를 제거한다.

---

## 백엔드 통합

### 의존성 추가

```bash
uv add langfuse
```

### CallbackHandler 주입

`src/backend/genai_runner.py` (또는 LangGraph 실행 진입점)에 아래 패턴 적용:

```python
import os
from langfuse.callback import CallbackHandler

def get_langfuse_callback() -> CallbackHandler | None:
    if os.getenv("LANGFUSE_ENABLED", "false").lower() != "true":
        return None
    return CallbackHandler(
        public_key=os.environ["LANGFUSE_PUBLIC_KEY"],
        secret_key=os.environ["LANGFUSE_SECRET_KEY"],
        host=os.environ["LANGFUSE_HOST"],
    )
```

LangGraph `astream_events` 호출 시 콜백 리스트에 주입:

```python
callbacks = [cb for cb in [get_langfuse_callback()] if cb is not None]

async for event in graph.astream_events(
    input_data,
    config={"callbacks": callbacks},
    version="v2",
):
    # 기존 이벤트 처리 로직
    ...

# 세션 종료 또는 요청 완료 시 flush
if callbacks:
    callbacks[0].flush()
```

> [!tip]
> `flush()`는 비동기 배치 전송을 강제로 완료한다. 요청 핸들러 종료 직전에 호출하지 않으면 마지막 트레이스가 누락될 수 있다.

---

## 대시보드에서 확인 가능한 정보

| 항목 | 설명 |
|---|---|
| **Traces** | 사용자 요청 1건 = 트레이스 1개. LangGraph 그래프 실행 전체 타임라인. |
| **노드별 토큰 사용량** | 각 LangGraph 노드(예: `generate_card`, `run_game_spec`)의 input/output 토큰 수. |
| **레이턴시** | 노드별·전체 그래프 실행 소요 시간 (ms). 병목 노드 식별 가능. |
| **비용 추적** | 등록된 모델 단가 기반 자동 계산. Gemini 커스텀 모델 단가 등록 필요. |
| **세션 그루핑** | `session_id`로 묶어 사용자별 전체 대화 흐름 추적 가능. |

---

## 운영 시 고려사항

### PostgreSQL 백업

`langfuse_db_data` named volume을 정기 백업한다. fly.io VPS 환경에서는 fly.io Volumes 스냅샷 기능 또는 `pg_dump`를 cron으로 실행.

```bash
# 수동 백업 예시
docker exec langfuse_db pg_dump -U langfuse langfuse > langfuse_backup_$(date +%Y%m%d).sql
```

### Langfuse 버전 업그레이드

`langfuse/langfuse:latest` 태그는 자동으로 최신 버전을 가리킨다. 운영 중 예고 없는 스키마 변경을 피하려면 **고정 버전 태그** 사용 권장:

```yaml
image: langfuse/langfuse:2   # major 버전 고정
```

업그레이드 시:
1. `docker compose pull langfuse`
2. `docker compose up -d langfuse` — DB 마이그레이션은 컨테이너 기동 시 자동 실행.
3. 대시보드 접속 확인.

### fly.io VPS 배포 시

Langfuse Postgres를 fly.io Volume 내부에 둘지, fly.io managed Postgres를 사용할지 [[adr-container-deployment]] Open Questions 참조.

### 파일럿 당일 (2026-05-05)

`LANGFUSE_ENABLED=false` — Langfuse 컨테이너 기동 불필요. 맥북 리소스 절약.

---

## 관련

- [[adr-container-deployment]]
- [[adr-langgraph-gemini-backend]]
- [[llm-provider-scaling]]
