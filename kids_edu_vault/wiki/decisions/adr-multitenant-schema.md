---
type: decision
title: "멀티테넌트 DB 스키마 — 테넌트·어드민 계정, 아이 개인 계정 없음"
created: 2026-05-01
updated: 2026-05-01
status: proposed
priority: 2
owner: "JY"
context: "파일럿(2026-05-05) 이후 상품화 — 병원/학교별 데이터 격리·플랜별 요금제·토큰 사용량 추적"
tags:
  - decision
  - architecture
  - database
  - auth
  - multitenant
related:
  - "[[auth-session-game-persistence]]"
  - "[[parent-gated-signup-first]]"
  - "[[adr-langgraph-gemini-backend]]"
  - "[[adr-container-deployment]]"
  - "[[product-requirements]]"
deciders:
  - "[[jinyong-shin]]"
---

# 멀티테넌트 DB 스키마 — 테넌트·어드민 계정, 아이 개인 계정 없음

## 결정

**테넌트(병원/학교) 단위 데이터 격리**를 위해 `tenants`, `admins`, `token_log` 테이블을 신규 추가하고, 기존 `sessions` 테이블에 `tenant_id` 컬럼을 추가한다. **아이 개인 계정은 만들지 않는다.** 어드민이 테넌트를 대표하며, 아이는 `child_id`(세션 식별자) 수준으로만 식별한다.

## 배경

- **파일럿**: 국립암센터 단일 테넌트, 어드민 1명 (하드코딩 `root/0000` 로그인 — [[auth-session-game-persistence]]).
- **상품화**: 병원·학교별 데이터 격리, 플랜별 요금제, 토큰 사용량 집계 필요.
- [[parent-gated-signup-first]] — 부모 이메일 가입 우선, 구글 OAuth는 14+/교사 한정 결정과 일관성 유지. 아이 개인 계정은 이 ADR 범위 밖.

## 결정 사항

### 신규 테이블

```sql
-- 테넌트 (병원/학교)
CREATE TABLE tenants (
    tenant_id   TEXT PRIMARY KEY,
    name        TEXT NOT NULL,
    plan        TEXT NOT NULL DEFAULT 'free'
                    CHECK (plan IN ('free', 'pilot', 'pro')),
    created_at  TEXT NOT NULL DEFAULT (datetime('now'))
);

-- 어드민 계정 (테넌트당 복수 가능)
CREATE TABLE admins (
    admin_id    TEXT PRIMARY KEY,
    tenant_id   TEXT NOT NULL REFERENCES tenants(tenant_id),
    email       TEXT NOT NULL UNIQUE,
    pw_hash     TEXT NOT NULL,
    role        TEXT NOT NULL DEFAULT 'admin'
                    CHECK (role IN ('superadmin', 'admin')),
    created_at  TEXT NOT NULL DEFAULT (datetime('now'))
);

-- 토큰 사용량 로그
CREATE TABLE token_log (
    id            INTEGER PRIMARY KEY AUTOINCREMENT,
    session_id    TEXT NOT NULL,
    child_id      TEXT NOT NULL,
    tenant_id     TEXT NOT NULL,
    model         TEXT NOT NULL,
    node          TEXT,
    input_tokens  INTEGER NOT NULL DEFAULT 0,
    output_tokens INTEGER NOT NULL DEFAULT 0,
    created_at    TEXT NOT NULL DEFAULT (datetime('now'))
);
```

### 기존 테이블 변경

```sql
-- sessions 테이블에 tenant_id 컬럼 추가
ALTER TABLE sessions ADD COLUMN tenant_id TEXT NOT NULL DEFAULT 'default';
```

기존 파일럿 데이터는 `tenant_id = 'default'`로 마이그레이션. `tenants` 테이블에 `(tenant_id='default', name='파일럿', plan='pilot')` 시드 데이터 추가.

### Auth 흐름

1. `POST /auth/login` — `{ email, password }` 수신.
2. `admins` 테이블에서 `email` 조회 → `bcrypt.verify(password, pw_hash)`.
3. 성공 시 응답: `{ admin_id, tenant_id, role, token }` (JWT, 24h 만료).
4. 이후 API 요청에 `Authorization: Bearer <token>` 헤더 → 미들웨어에서 `tenant_id` 추출.

### 플랜별 제어 (결제 훅 defer)

- `tenants.plan` 컬럼이 rate limit과 `max_children` 결정.
- `free`: max_children=5, RPM=10.
- `pilot`: max_children=50, RPM=60.
- `pro`: max_children=unlimited, RPM=200.
- **Stripe 연동 시** `tenants` 테이블에 `stripe_customer_id TEXT`, `subscription_status TEXT` 컬럼 추가. 현재 미구현.

## 대안 및 기각 이유

| 대안 | 기각 이유 |
|---|---|
| 아이 개인 계정 즉시 도입 | 소아암 환아 개인정보 수집 → 병원 개인정보보호 절차 필요. 파일럿 범위 초과. [[parent-gated-signup-first]] 와 충돌 |
| 단일 테넌트 구조 유지 | 상품화 시 병원별 데이터 격리 재설계 비용 과대 |
| Row-Level Security (PostgreSQL) | 현재 SQLite 스택([[adr-container-deployment]])과 불일치. 스케일아웃 시 재검토 |
| 별도 DB 인스턴스 per 테넌트 | fly.io Volume 수 제한 + 운영 복잡도 과대 |

## 영향 범위

- **변경 파일**: `src/backend/storage.py` — `tenants`, `admins`, `token_log` 테이블 DDL + 마이그레이션 함수 추가.
- **신규 파일**: `src/backend/auth.py` — `POST /auth/login` 엔드포인트, JWT 발급, bcrypt 검증.
- **변경 파일**: `src/backend/main.py` — WS 핸들러에 `tenant_id` 추출 미들웨어 추가. `token_log` insert 연동.
- **추가 의존성**: `bcrypt`, `python-jose` (JWT) — `pyproject.toml`.
- **파일럿 당일(2026-05-05)**: `admins` 테이블 미사용. 기존 하드코딩 `root/0000` 유지. 마이그레이션은 파일럿 이후.
- **[[auth-session-game-persistence]] 부분 대체**: 하드코딩 로그인 → `admins` 테이블 기반 로그인으로 교체. 세션·게임 저장 로직은 그대로.

## Open Questions

- [ ] JWT 서명 키 (`SECRET_KEY`) 환경변수 추가 필요 — `.env.example`에 placeholder 추가.
- [ ] `token_log.node` 컬럼 — [[adr-langgraph-gemini-backend]] LangGraph 노드명 기록 여부. 과금 granularity 결정 필요.
- [ ] `max_children` 강제 시점 — 세션 생성 시 차단할지, 소프트 경고만 할지 구현자 결정.
- [ ] Stripe 연동 타이밍 — 상품화 v1 포함 여부. 별도 ADR로 분리 권장.
- [ ] `superadmin` 역할 범위 — 모든 테넌트 조회 가능 여부. 관리자 콘솔 설계 전 미정.

## 관련

- [[auth-session-game-persistence]]
- [[parent-gated-signup-first]]
- [[adr-langgraph-gemini-backend]]
- [[adr-container-deployment]]
- [[product-requirements]]
