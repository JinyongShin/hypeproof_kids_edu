---
type: spec
title: "커리큘럼 위자드 v1 기술 결정사항"
created: 2026-04-25
updated: 2026-04-25
status: pending
owner: "[[jinyong-shin]]"
tags:
  - spec
  - pilot
  - curriculum
  - tech-decision
related:
  - "[[curriculum-wizard-v1]]"
  - "[[2026-05-05-pilot]]"
---

# 기술 결정 대기 항목 (2026-04-25)

## 1. 이미지 생성 API 🔴

- **현재**: Claude CLI 텍스트만 (이미지 불가)
- **필요**: 캐릭터 이미지 + 표지 이미지 생성
- **후보**:
  - A) GPT-4o image generation (OpenAI API) — 품질 좋음, $0.02~0.08/장
  - B) DALL-E 3 — 안전, 비슷한 가격
  - C) Stable Diffusion 로컬 — 무료, 품질 편차
  - D) 기존 Claude 텍스트만 → 텍스트+이모지+CSS 카드 (이미지 API 불필요)
- **결정 필요**: 진용님 예산 확인 후 선택

## 2. QR 생성 ✅ 간단

- 사원증용 QR 코드
- 라이브러리: `qrcode` (Python) 또는 프론트엔드 JS
- **미확정**: QR 연결 URL (타이틀 카드 페이지?)

## 3. 밝은 UI 테마 🟡

- 현재 다크모드 → 아이들용 밝은 테마 필요
- 기본 파스텔톤으로 진행 예정 (특정 컬러 가이드 있으면 수정)

## 4. Claude 모델 🟡

- 현재 `sonnet` 사용중
- 40명 동시 호출 시 비용/속도 이슈
- `haiku` 다운그레이드 검토 (빠르고 저렴, 품질 약간 낮음)

## 5. 갤러리 슬라이드쇼 🟡

- 40명 카드를 대형 스크린에 순환 표시
- 자동 순환 vs 운영자 수동 넘김 결정 필요

---

## 작업 범위 (wizard-v1 기준)

| 우선순위 | 파일 | 변경 |
|---|---|---|
| 🔴 | `scaffoldData.ts` | wizard-v1 블록에 맞게 전면 수정 |
| 🔴 | `TUTOR.md` | 타이틀 카드 생성 페르소나로 재작성 |
| 🔴 | `claude_runner.py` | HTML 추출 → 이미지+카드 추출로 변경 |
| 🔴 | `GamePreview.tsx` | iframe → 타이틀 카드 뷰어 + 갤러리 |
| 🟡 | `ChatPane.tsx` | 블록 진행 UI 조정 |
| 🟡 | `storage.py` | game → card 스키마 추가 |
| 🟡 | `main.py` | API 엔드포인트 조정 |
| 🟡 | 전체 | 밝은 UI 테마 적용 |
| 신규 | QR 생성 | 사원증용 QR 코드 |

**예상 공수**: 핵심 2~3일, 전체 4~5일
