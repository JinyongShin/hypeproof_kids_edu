---
type: decision
title: "ADR: HypeProof Studio v0.1 — 자체 IDE 개발 결정"
created: 2026-05-14
updated: 2026-05-14
tags:
  - decision/product
  - decision/tooling
status: decided
---

# ADR: HypeProof Studio v0.1 — 자체 IDE 개발 결정

**날짜:** 2026-05-14  
**상태:** Decided  
**결정자:** HypeProof Lab (JY 주도)

---

## 맥락

[[sk-biopharma]] 임직원 가족 대상 AI 교육 프로그램에서 사용할 도구 선택 필요.  
기존 파일럿(소아암 병동, 2026-05-05)은 Cline + VS Code 조합으로 진행했으나, 브랜드 정체성이 없고 8~12세 아이들이 사용하기에 UI/UX 최적화가 부족했음.

---

## 결정

> **자체 IDE "[[hypeproof-studio]]"를 VS Code fork 기반으로 개발하여 [[sk-biopharma]] 1회차에서 첫 데뷔한다.**

---

## 근거

1. **브랜드**: 100% HypeProof Lab 브랜딩 — 고객에게 "우리 제품"으로 포지셔닝
2. **측정 가능성**: HypeProof Proxy 통해 AI 사용 데이터 자동 수집 → [[sixteen-essence]] 행동 매핑
3. **UX 최적화**: chat panel을 아이들 수준에 맞게 커스터마이징 (STT v0.2)
4. **안전성**: Manual-approve 모드 강제 — 부모가 파일 쓰기/실행을 승인

---

## 대안 비교

| 옵션 | 장점 | 단점 |
|---|---|---|
| Cline + VS Code (현행) | 빠른 배포, 검증됨 | HypeProof 브랜드 없음, 측정 불가 |
| **HypeProof Studio (선택)** | 브랜드 완전 소유, 측정·분석 가능 | 빌드 리소스 필요, 리스크 존재 |
| 웹 기반 chat only | 설치 불필요 | v0.2에서나 완성, v0.1 스코프 초과 |

---

## 리스크 및 대응

| 리스크 | 대응 |
|---|---|
| 5/28 dry-run 실패 | **Plan B**: Cline + Proxy로 1회차 운영, Studio 8월 데뷔 |
| Windows 지원 지연 | v0.1은 Mac 우선 → v0.1.1에서 Win 추가 (회차 직전) |
| 개발 리소스 부족 | Freelancer 1인 추가 검토 (Track B chat panel, $5~8K) |

---

## 결과

- [[hypeproof-studio]] 페이지 참조
- 5월 15일~30일 v0.1 압축 빌드 시작
- 5월 28~30일 dry-run 데드라인 게이트

---

## 관련 페이지

- [[hypeproof-studio]]
- [[sixteen-essence]]
- [[2026-05-14-sk-biopharma-followup]]
- [[sk-biopharma-pilot]]
