---
type: spec
status: draft
owner: "[[jinyong-shin]]"
target_date: 2026-05-19
created: 2026-05-01
updated: 2026-05-14
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

`docker-compose.yml` 루트 파일에 두 서비스가 포함된다.

```yaml
  langfuse-db:
    image: postgres:16-alpine
    environment:
      POSTGRES_DB: langfuse
      POSTGRES_USER: langfuse
      POSTGRES_PASSWORD: langfuse_local
    volumes:
      - langfuse_db_data:/var/lib/postgresql/data
    healthcheck:
      test: ["CMD-SHELL", "pg_isready -U langfuse"]
      interval: 5s
      timeout: 5s
      retries: 5

  langfuse:
    image: langfuse/langfuse:2.95.11   # v2 패치버전 핀 고정
    ports:
      - "3002:3000"
    environment:
      DATABASE_URL: postgresql://langfuse:langfuse_local@langfuse-db:5432/langfuse
      NEXTAUTH_SECRET: local_dev_secret_change_in_prod
      NEXTAUTH_URL: http://localhost:3002
      SALT: local_dev_salt_change_in_prod
    depends_on:
      langfuse-db:
        condition: service_healthy
```

> [!note]
> `NEXTAUTH_SECRET`과 `SALT`는 로컬 개발용 플레이스홀더. 운영 환경에서는 반드시 강한 랜덤값으로 교체.

v2를 채택한 이유: v3는 ClickHouse + S3/MinIO 필요 → 로컬/소규모 운영에 오버스펙.

---

## 초기 설정 절차

### 1. 서비스 기동

```bash
docker compose up -d langfuse-db langfuse
```

### 2. 관리 UI 접속 및 계정 생성

1. 브라우저에서 `http://localhost:3002` 접속
2. "Sign Up" → 관리자 계정 생성 (이메일 + 비밀번호)
3. "Create New Organization" → 예: `hypeproof-kids-edu`
4. "Create New Project" → 예: `pilot-2026-05-05`

### 3. API 키 발급

1. 프로젝트 설정 → "API Keys" 탭
2. "Create new API key" 클릭
3. Public Key (`pk-lf-...`)와 Secret Key (`sk-lf-...`) 복사

### 4. `.env.local` 설정

`src/backend/.env.local`:

```bash
LANGFUSE_ENABLED=true
LANGFUSE_PUBLIC_KEY=pk-lf-xxxxxxxxxxxx
LANGFUSE_SECRET_KEY=sk-lf-xxxxxxxxxxxx
LANGFUSE_HOST=http://localhost:3002
```

파일럿 당일(맥북 로컬)에는 `LANGFUSE_ENABLED=false`로 비활성화하여 오버헤드 제거.

---

## 백엔드 통합

### 의존성

```bash
uv add langfuse
```

### CallbackHandler 주입 패턴

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

LangGraph `astream_events` 호출 시:

```python
callbacks = [cb for cb in [get_langfuse_callback()] if cb is not None]

async for event in graph.astream_events(
    input_data,
    config={"callbacks": callbacks},
    version="v2",
):
    ...

# 요청 완료 시 flush (마지막 트레이스 누락 방지)
if callbacks:
    callbacks[0].flush()
```

---

## 대시보드에서 확인 가능한 정보

| 항목 | 설명 |
|---|---|
| **Traces** | 사용자 요청 1건 = 트레이스 1개. LangGraph 그래프 실행 전체 타임라인 |
| **노드별 토큰 사용량** | 각 노드(`generate_card`, `edit_code` 등)의 input/output 토큰 수 |
| **레이턴시** | 노드별·전체 그래프 실행 소요 시간. 병목 노드 식별 |
| **비용 추적** | 등록된 모델 단가 기반 자동 계산. Gemini 커스텀 모델 단가 등록 필요 |
| **세션 그루핑** | `session_id`로 묶어 사용자별 전체 대화 흐름 추적 |

---

## 운영 시 고려사항

### PostgreSQL 백업

```bash
docker exec langfuse-db pg_dump -U langfuse langfuse > langfuse_backup_$(date +%Y%m%d).sql
```

### 버전 고정 이유

`langfuse/langfuse:2.95.11` 패치버전 핀 고정. latest 태그는 스키마 변경 시 무중단 업그레이드를 보장하지 않음.

업그레이드 절차:
1. `docker compose pull langfuse`
2. `docker compose up -d langfuse` — 기동 시 DB 마이그레이션 자동 실행
3. 대시보드 접속 확인

### fly.io VPS 배포 시

Langfuse Postgres를 fly.io Volume 내부에 둘지, fly.io managed Postgres를 쓸지 [[adr-container-deployment]] 참조.

### 파일럿 당일 (2026-05-05)

`LANGFUSE_ENABLED=false` 권장. Langfuse 컨테이너 기동 불필요. 맥북 리소스 절약.

---

## 관련 페이지

- [[adr-container-deployment]]
- [[adr-langgraph-gemini-backend]]
- [[adr-multitenant-schema]]
- [[llm-provider-scaling]]
