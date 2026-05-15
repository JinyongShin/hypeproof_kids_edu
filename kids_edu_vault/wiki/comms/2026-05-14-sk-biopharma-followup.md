---
type: comms
title: "SK바이오팜 후속 — HypeProof Lab 진행 사항 (2026-05-14)"
created: 2026-05-14
updated: 2026-05-14
tags:
  - comms/internal
  - stakeholder/sk-biopharma
  - product/hypeproof-studio
status: ingested
---

# SK바이오팜 후속 — HypeProof Lab 진행 사항 (2026-05-14)

5/12 미팅 후 HypeProof Lab 내부 진행 사항 정리.  
소스: `meeting_notes/2026-05-14.md`

---

## 제품 정체성 결정

| 항목 | 결정 |
|---|---|
| 도구 | **[[hypeproof-studio]]** — VS Code fork + 자체 chat panel |
| 첫 데뷔 | [[sk-biopharma]] 1회차 (브랜드 100% HypeProof) |
| 백엔드 | HypeProof Proxy (Anthropic API 중계 + 측정 데이터 자동 수집) |
| 차별점 | STT(음성 입력) v0.2부터 통합 예정 — 8~12세 타이핑 부담 해소 |

→ ADR: [[adr-hypeproof-studio-v01]]

---

## 교육 IP 구조 — [[sixteen-essence]]

[[sixteen-essence]] 프레임워크를 학년대별 누적 적용:

| 학년 | Essence 수 | 영역 |
|---|---|---|
| 초3~4 | 6개 | 감지·입력·소격 |
| 초5~6 | +5개 = 11개 | AI 부리기 |
| 중1~2 | +5개 = 16개 | 메타 사고 |

**4시간 5단계 플로우:**

| 단계 | 시간 | 내용 |
|---|---|---|
| 감지 | 0:00~0:30 | 세계관·방향 이해 |
| 입력 | ~1:00 | 아이디어·컨셉 정하기 |
| 부리기 | ~2:00 | AI와 대화하며 게임 완성 |
| 검증 | ~3:00 | 직접 플레이·개선 아이디어 발견 |
| 사다리 | ~4:00 | 발표 및 공유 |

**운영 제약:** 부모-자녀 페어 모드 강제 (단독 수강 불가)

---

## 측정 체계

- 운영진은 수업 중 **트리거 질문만** — 직접 측정 안 함
- AI가 사후 분석 ([[sixteen-essence]] 행동 매핑, 페어 협업 패턴 포함)
- 운영진 검토 게이트 후 부모 리포트 (24~48h 이내 발송)
- **등급·순위 없음** — 본인 이전 회차와만 비교

---

## 운영 차별점

"보조강사" = HypeProof Lab 운영진 직접 투입 (시급 알바 아님):

| 운영진 배경 | 역할 |
|---|---|
| CERN 물리 박사 | 가족 옆에 앉아 코칭 |
| AI/ML 엔지니어 | 가족 옆에 앉아 코칭 |
| 글로벌 마케터 | 가족 옆에 앉아 코칭 |
| 미디어 전문가 | 가족 옆에 앉아 코칭 |

운영진 1인당 5~7 가족 코칭.

---

## 일정 및 마일스톤

| 기간 | 내용 |
|---|---|
| 5월 15~30 | [[hypeproof-studio]] v0.1 압축 빌드 (Track A: VS Code fork / Track B: 자체 chat panel 병렬) |
| 5월 28~30 | 운영진 자녀 대상 dry-run (4시간) |
| 6월 1주 | Studio v0.1 release + 가족 안내 메일 |
| 6월 2~3주 | [[sk-biopharma]] 1회차 |
| **Plan B** | 5/28 dry-run 미달 시 → Cline + Proxy로 1회차 운영, Studio는 8월 데뷔 |
| 7월 이후 | Studio v0.2 (STT, web 모드) — 국립암센터 대비 |

---

## 비용 구조

| 항목 | 내용 |
|---|---|
| AI 사용료 | 가족당 4시간 200K 토큰 한도 → 약 $5~10 (HypeProof 부담) |
| 회차당 인프라+AI | 약 $20 (20가족 기준) |
| Apple Developer 계정 | $99/년 (Mac 코드사이닝) |
| Freelancer 백업 | Track B chat panel UI 전담, $5~8K 검토 |

---

## 운영 환경

| 항목 | 내용 |
|---|---|
| 설치 | One-line installer (5분, Mac/Win) |
| 백업 노트북 | 5대 (설치 실패 가족용) |
| 보안 모드 | Manual-approve 강제 — file write/exec 부모 승인 필수 |
| 데이터 보존 | 원본 대화 30일 자동 삭제, 익명 분석 결과 1년 보관 |
| 동의서 | 7개 항목 (법무 검토 의뢰 예정) |

---

## 관련 페이지

- [[2026-05-12-sk-biopharma-meeting]] — 5/12 원본 미팅
- [[sk-biopharma]] · [[bitree]]
- [[hypeproof-studio]] · [[adr-hypeproof-studio-v01]]
- [[sixteen-essence]]
- [[sk-biopharma-pilot]]
