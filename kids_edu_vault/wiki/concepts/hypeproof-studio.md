---
type: concept
title: "HypeProof Studio"
created: 2026-05-14
updated: 2026-05-14
tags:
  - concept/product
  - concept/tool
status: in-progress
---

# HypeProof Studio

HypeProof Lab의 자체 교육 IDE. VS Code fork 기반 + 자체 chat panel 통합.  
SK바이오팜 1회차에서 첫 데뷔 예정.

---

## 제품 구성

| 레이어 | 기술 |
|---|---|
| IDE 본체 | VS Code fork (Track A) |
| Chat Panel | 자체 chat panel UI (Track B, 병렬 빌드) |
| 백엔드 | HypeProof Proxy (Anthropic API 중계 + 측정 데이터 수집) |

---

## 버전 로드맵

| 버전 | 목표일 | 주요 기능 |
|---|---|---|
| v0.1 | 2026-06-01 | Mac 우선, Win v0.1.1(회차 직전), 기본 chat panel |
| v0.1.1 | SK바이오팜 1회차 직전 | Windows 지원 |
| v0.2 | 2026-07 이후 | STT(음성 입력), web 모드, auto-update (국립암센터 대비) |

---

## 차별점

- **STT 통합** (v0.2~): 8~12세 타이핑 부담 해소
- **Manual-approve 모드 강제**: file write/exec 시 부모 승인 필수
- **HypeProof Proxy**: API 중계 + 측정 데이터 자동 수집 → [[sixteen-essence]] 행동 매핑
- **브랜드**: 100% HypeProof Lab 브랜딩 (Cline·VS Code 레퍼런스 노출 없음)

---

## 빌드 계획 (v0.1)

- **Track A**: VS Code fork — IDE 전체 (메인)
- **Track B**: 자체 chat panel UI — Freelancer 1인 전담 검토 ($5~8K)
- **데드라인 게이트**: 5/28 dry-run (운영진 자녀 대상 4시간)
  - 미달 시 Plan B: Cline + HypeProof Proxy로 1회차 운영

---

## Plan B

5/28 dry-run 미달 시 대안:
- **도구**: Cline + HypeProof Proxy
- **데뷔**: Studio 8월 정식 데뷔 (국립암센터 일정 맞춤)

---

## ADR

[[adr-hypeproof-studio-v01]]

---

## 관련 페이지

- [[adr-hypeproof-studio-v01]]
- [[sixteen-essence]]
- [[2026-05-14-sk-biopharma-followup]]
- [[sk-biopharma-pilot]]
