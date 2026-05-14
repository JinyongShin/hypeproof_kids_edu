---
type: decision
title: "ADR: 멀티테넌트 스키마"
status: active
created: 2026-05-01
updated: 2026-05-14
tags:
  - decision
  - adr
  - database
  - multitenant
  - sqlite
---

# ADR: 멀티테넌트 스키마 (SQLite)

**날짜**: 2026-05-01  
**브랜치**: `feature/langgraph-gemini`  
**상태**: active (MVP는 tenant_id="default" 단일 테넌트 운영)

---

## 결정

SQLite에 `tenants` / `admins` / `token_log` 테이블을 추가하고, 기존 `sessions` 테이블에 `tenant_id` 컬럼을 마이그레이션. 멀티 파일럿 고객(SK바이오팜, 보아치과 등)을 단일 DB에서 격리 운영하는 구조를 준비.

---

## 배경

파일럿 1회차는 단일 어드민 계정으로 충분했으나, 이후 상황이 달라짐:

- SK바이오팜 파일럿 (2026-06~07) + 보아치과 파일럿 동시 운영 예정
- 파일럿별 관리자 계정·세션·토큰 사용량을 분리 추적해야 함
- 기존 단일 `ADMIN_USERNAME/PASSWORD` env-var 방식은 복수 테넌트 불가

---

## 스키마 변경 (`src/backend/storage.py`)

### 신규 테이블

```sql
CREATE TABLE IF NOT EXISTS tenants (
    tenant_id   TEXT PRIMARY KEY,
    name        TEXT NOT NULL DEFAULT '',
    created_at  TEXT NOT NULL DEFAULT (strftime('%Y-%m-%dT%H:%M:%fZ','now'))
);

CREATE TABLE IF NOT EXISTS admins (
    admin_id    TEXT PRIMARY KEY,
    tenant_id   TEXT NOT NULL REFERENCES tenants(tenant_id),
    email       TEXT NOT NULL UNIQUE,
    pw_hash     TEXT NOT NULL,          -- bcrypt 해시
    role        TEXT NOT NULL DEFAULT 'admin',
    created_at  TEXT NOT NULL DEFAULT (strftime('%Y-%m-%dT%H:%M:%fZ','now'))
);

CREATE TABLE IF NOT EXISTS token_log (
    id              INTEGER PRIMARY KEY AUTOINCREMENT,
    session_id      TEXT NOT NULL,
    child_id        TEXT NOT NULL,
    tenant_id       TEXT NOT NULL DEFAULT 'default',
    node            TEXT NOT NULL,      -- LangGraph 노드명
    input_tokens    INTEGER NOT NULL DEFAULT 0,
    output_tokens   INTEGER NOT NULL DEFAULT 0,
    created_at      TEXT NOT NULL DEFAULT (strftime('%Y-%m-%dT%H:%M:%fZ','now'))
);
```

### 기존 테이블 마이그레이션

```sql
-- sessions.tenant_id 컬럼 추가 (기존 DB backward compat)
ALTER TABLE sessions ADD COLUMN tenant_id TEXT NOT NULL DEFAULT 'default';
```

`init_db()`에서 try/except로 처리 — 이미 컬럼이 있으면 무시.

---

## 인증 구조 (`app/auth.py`)

**DB 우선, env-var 폴백** 방식:

```
1. DB admins 테이블에서 email로 조회
   → 있으면: bcrypt.checkpw(password, pw_hash)
   → 성공: {admin_id, tenant_id, role} 반환

2. DB에 없으면: ADMIN_USERNAME/ADMIN_PASSWORD env-var와 비교
   → 성공: {admin_id=username, tenant_id="default", role="admin"} 반환
```

env-var 폴백이 존재하는 이유: 파일럿 당일 하드코딩 `root/0000` 호환성 유지. 기존 파일럿 환경에서 `_backend.js`를 바꾸지 않아도 동작.

### 시딩 로직 (`ensure_default_admin`)

서버 시작 시 1회 호출. `ADMIN_USERNAME`이 기본값("admin", "root")이면 DB 시딩 생략 (env-var 전용 모드).  
의미있는 계정명이 설정된 경우에만 bcrypt 해시로 DB에 등록.

---

## MVP 운영 방식

현재(`tenant_id="default"`) 단일 테넌트로 운영 중.  
멀티테넌트 전환 시 필요한 작업:
1. `tenants` 테이블에 고객사 row 삽입
2. `admins` 테이블에 해당 tenant의 관리자 계정 생성
3. 세션 생성 API에서 `tenant_id` 파라미터 활성화

---

## token_log 활용

각 LangGraph 노드 실행 시 input/output 토큰을 `token_log`에 기록.  
노드별·세션별·테넌트별 LLM 비용 추적 가능.  
→ 파일럿 고객에게 사용량 리포트 제공 시 활용.

---

## 관련 페이지

- [[adr-langgraph-gemini-backend]] — token_log가 기록하는 LangGraph 노드 구조
- [[adr-container-deployment]] — 이 스키마가 배포되는 환경
- [[langfuse-observability]] — 토큰 로깅의 보완적 관측성 레이어
- [[sk-biopharma-pilot]] — 첫 멀티테넌트 대상 파일럿
