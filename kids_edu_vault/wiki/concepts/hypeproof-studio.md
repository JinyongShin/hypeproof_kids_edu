---
type: concept
title: "HypeProof Studio"
created: 2026-05-14
updated: 2026-09-14
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


## SK바이오팜 게임 제작 모드 (2026-06-08)

SK바이오팜 가족 AI 게임 창작 수업은 봉호 커리큘럼을 본체로 두고 Studio로 구현한다. 봉호 커리큘럼을 구현하는 Studio는 범용 코딩툴 대체물이 아니라, 아이/가족이 4시간 안에 게임 제작 루프를 완주하도록 돕는 guided education OS다.

- Skill Pack: [[hypeproof-studio-game-skillpack-v1]]
- 핵심 기능: 게임 목표 설정, 캐릭터/세계/규칙 입력, 안전 룰 적용, V1 생성, 플레이 검증, V2/V3 개선, 발표 카드, 7 Assets 리포트 데이터 저장
- 방향: 게임 제작에 특화된 스킬·룰·프롬프트를 사전 탑재하여 실패율을 낮춘다.

## 보아치과 홈페이지 제작 모드 (2026-06-29)

[[2026-06-29-weekly-on-hypeproof]]에서 보아치과 강의는 Studio가 단순 코드 생성기가 아니라 전후 비교와 수정 과정을 남기는 교육 OS여야 한다고 정리됐다.

- 목표 산출물: 홈페이지 초안, 가능하면 공개 URL
- 핵심 로그: 첫 V1, 설명 카드/Context Pack, 피드백 루프, 최종본, 발표용 Before/After
- 교육 가치: 수강자가 "AI에게 무엇을 설명해야 결과가 달라지는지"와 "원하는 방향까지 어떻게 반복 수정하는지"를 체화
- 운영 리스크: 리허설 전 Claude Code 대비 Studio 성능 격차를 테스트하고, 필요하면 fallback을 준비해야 한다.

## 보아치과 2시간 실습 운행 조건 (2026-07-06)

[[boa-dental-ai-homepage-cuesheet-20260706-spec]] 기준, Studio 세팅은 19:10-19:30 구간 안에 완료되어야 한다.

- 등록 플로우: 설치, 학생 등록, 토큰 발급, 토큰 입력, 채팅 테스트를 5분 컷으로 준비
- 사용 목적: Reference First, Context Engineering, Loop Engineering, 최종 URL/GitHub/`agent.md` 업로드까지 한 흐름에서 운행
- 보조 도구: 디자인 스킬, 배포 스킬, Playwright MCP
- 핵심 로그: URL만 넣은 1차 초안, 병원 컨텍스트 반영 2차 초안, 루브릭 검사/수정 반복, 최종 산출물과 `agent.md`

## ADR

[[adr-hypeproof-studio-v01]]

---

## 관련 페이지

- [[adr-hypeproof-studio-v01]]
- [[sixteen-essence]]
- [[2026-05-14-sk-biopharma-followup]]
- [[sk-biopharma-pilot]]

---

## ⭐ 2026-09-14 기능 현황 — 현재 6 / 로드맵 7

출처 [[members-portal-20260914-source]] (`/members/studio/features`, 원본 revision `67b4adf`, 기능 페이지 기준 2026-09-11).
제품 정의: **"내 문제를 AI와 풀고, 결과를 판단하는 곳."** 체험판 이름은 **'내 삶에 AI 더하기'**.

### 현재 기능 (6)

| # | 기능 | 제공 범위 |
|---|---|---|
| 01 | **시작하고 이어가기** | 참여 코드 연결, 체험↔수업 전환, 저장한 대화·프로젝트 복원. **Mac 실행 범위 확인** |
| 02 | **AI와 만들고 수정하기** | 파일·브라우저 도구 실행, 도구 승인·결과 표시. **명확한 요청은 바로 실행하고 부족할 때만 질문 하나** |
| 03 | **결과 미리 보고 변경 비교하기** | HTML 미리보기, 모바일·데스크톱 전환, **최초 산출물 보존 + 최근 저장과 비교** |
| 04 | **모델 선택하고 사용량 확인하기** | 허용 모델 선택, 실제 응답 모델·사용량 표시. **서버 시크릿만 사용** |
| 05 | **선택한 기록으로 도움 요청하기** | 선택 공유 → 담당 강사 열람 → 피드백. **철회·만료 처리, 수업 밖 기록 제외** |
| 06 | **내 작업 기록 돌아보기** | 원본 이벤트를 참조하는 관찰, **정정 기록**, 후속 학습 연결 |

> 06의 명시적 금지: *"이 기록을 **기능 사용량에 따른 성장 점수나 독립 능력 인증으로 표시하지 않는다.**"*

### 로드맵 (7)

| # | 기능 | 상태 |
|---|---|---|
| 01 | 음성으로 작업 이어가기 | `개발 중` (요구사항 47개) |
| 02 | 작업 전체 복구와 결과물 검수 | `개발 중` |
| 03 | 모델 자동 선택과 다른 모델 검토 | `개발 중` |
| 04 | 자료·도움 범위를 작업에 적용하기 | `개발 중` |
| 05 | 수업 종료 후 작업 묶음 내보내기 | `개발 중` |
| 06 | **다른 앱에서 작업하기 (Computer Use)** | `예정` — **별도 타당성 검토 단계** |
| 07 | 판단 변화의 근거와 해석 확장 | `예정` |

> 06 주의: *"일반 데스크톱 앱 조작이 현재 제공된다는 의미는 아니다."* 승인된 실습 + **격리 환경 + 비상 정지 + 자격 분리** 검증이 전제.
> 07 주의: *"기존 `T/I/C/V/D/R/O`, 장문 asset key, A1–A5와 과거 evidence를 유지한다. 뜻이 같아 보여도 **enum rename이나 점수 산술 변환을 하지 않는다**."* → [[six-human-capabilities]]의 무변환 원칙이 스키마 계약으로 박혀 있다.

### 요구사항 규모

**11개 문서 / 289개 요구사항**이 공개돼 있다. 가장 큰 것: 작업 화면·기본 조작 55 · 수업 만들기·리허설 53(→[[chalk]]) · 음성 47 · AI와 만들기·검토·복구 44.

### 남은 확인

- ⚠️ **공개 배포 상태는 "별도 확인"**이라고만 적혀 있다. 요구사항 US-02: *"로컬 서버 성공을 공개 체험 성공으로 보지 않는다."*
- 지원 설치본·Service 조합 범위
- 체험판의 관찰은 아직 **7 Asset 기반의 잠정 관찰**이다 → 6개 역량 전환은 [[capability-measurement-module]]
