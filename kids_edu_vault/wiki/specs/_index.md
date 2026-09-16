---
type: index
status: navigational
title: "Specs"
created: 2026-04-12
updated: 2026-09-15
tags:
  - index/specs
---

# Specs

설계 문서·ADR 상위·요구사항. 한 기능/시스템 = 한 페이지. 상태: `draft → review → approved → implemented → superseded`.

## Active
- ⭐ [[requirement-id-index]] (2026-09-15) — **요구사항 ID 767개 전수 인덱스.** 두 저장소 정본, ID 하나 = 한 행(코드·원문·정의 위치·구현 상태). 번호 구멍 0 · `REQ-M30` 중복 1 · lab 미러가 `HC-09` 누락
- ⭐ [[chalk-requirements]] (2026-09-15) — Chalk 요구사항 정본 정리. `CR-*` 89건 / 9묶음, 정본 15문서 매핑. **합격선 규칙이 없다**는 공백이 핵심
- ⭐ [[chalk-implementation-status]] (2026-09-15) — Chalk 구현 현황. 기준 커밋 `4195faa`. 되는 것/안 되는 것·이슈·PR 전수·**배포 부채(운영이 main보다 PR 4건 뒤)**
- [[capability-measurement-module]] — 역량 측정 모듈 (Studio·Chalk 양쪽 임포트)
- [[pilot-env-design]] — 유료 파일럿 실행환경 설계

## Draft
- [[teen-ai-startup-camp-v0]] — 중고등 AI 창업 캠프 사업 구상 v0 (2026-08-25, 대부분 미정)
- [[sk-biopharma-bongho-curriculum-v2]] — 봉호 커리큘럼 코어를 본체로 둔 SK바이오팜 가족 AI 게임 창작 커리큘럼 v2
- [[hypeproof-studio-game-skillpack-v1]] — HypeProof Studio 게임 제작 특화 스킬/룰/프롬프트팩 v1
- [[sk-biopharma-curriculum-detail-v1]] — SK바이오팜 가족 AI Creation Lab 4시간 커리큘럼 상세 v1
- [[pilot-curriculum-adapted]] — 병동 파일럿 90분 커리큘럼 (6블록 재설계)

## Notes
- 새 spec은 `_templates/spec.md`로 생성.
- 단일 결정은 `decisions/`에, 여러 결정을 품은 복합 설계는 여기.
