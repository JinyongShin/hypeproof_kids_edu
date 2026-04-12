---
type: component
status: active
stack_layer: content
repo: "jayleekr/sans-kids-school-2025"
version: "v1.1.2"
license: "교육 목적 자유 사용"
tags:
  - component
  - pilot
  - content
created: 2026-04-12
updated: 2026-04-12
---

# sans-kids-school-2025 (실습 자산)

## 역할
- 2025-08-03 SANS Kids VibeCoding 워크숍의 전체 자료. 8–16세 대상 **Cursor + AI 협업 게임 개발** 4시간 풀셋 (v1.1.2).
- 제작: Jay Lee, [[jinyong-shin]], Jiwoong Kim.
- 파일럿 당일 [[code-server]] 세션에 자동 탑재할 **HTML/JS 게임 스타터 + 교수법 자료**의 원천.
- 로컬 경로: `D:\HypeProofLab\hypeproof_kids_edu\sans-kids-school-2025\`.
- .raw 스냅샷: `.raw/sans-kids-2025/` (md 전용 부분 복제).

## 설정 / 구성
- **아키텍처**: [[single-html-runtime]] — 단일 HTML + 빌드 없음 + 브라우저 더블클릭 실행.
- **교수법 철학**: [[no-debug-philosophy]] — 아이와 디버깅 금지, 10초 피드백 루프, 에러→"좋은 발견".
- **AI 교수법 페르소나**: [[ai-persona-workflows]] — Friendly Teacher / Problem-Solving Coach / Quick Implementation / Storytelling / Checklist 5종 Cursor Rules로 구현.
- **표준 게임**: "바나나 히어로의 모험" (전투형). **병동 파일럿에서는 [[combat-vs-cooperative-framing]] 결정에 따라 협력형 서사로 치환.**
- **운영자 자료**: facilitator-checklist, emergency-troubleshooting(30-second rule), lecture_script(분 단위 타임라인), expected-questions, age-based-optimization, workflow-comparison-analysis, offline-backup 템플릿.
- **핵심 기술 제약**: 단일 HTML, Canvas API, CDN 라이브러리만 허용. Node.js·npm·빌드 도구·DB·서버 기능 금지.

## 의존성
- 없음 (정적 HTML/JS, CDN 선택).
- 원본 워크숍은 Cursor·Volta·Node 설치형이었으나, 파일럿은 [[code-server]] 위 브라우저 실행으로 대체.

## 대안 및 비교
- 원본 배포 경로(GitHub Release ZIP + Cursor 설치)는 **병동 PC 환경에서 사용 불가**(관리자 권한·방화벽). 실습 자산 레벨에서만 재활용.

## 운영 주의사항
- 자산 재활용 시 라이선스·저자 표기 확인.
- 연령(8–12세)·피로도 제약에 맞춰 난이도 조정 필요 ([[2026-04-11-call-note]]).
- **병동 맞춤 변경점 4가지**:
  1. 4시간 → 90분 ([[pilot-curriculum-adapted]] 6블록).
  2. 전투 서사 → 협력 서사 ([[combat-vs-cooperative-framing]]).
  3. Cursor 설치형 → [[code-server]] + [[cline]] 브라우저형.
  4. 단체 발표·피어 리뷰 → 1:1 시연 (감염관리·격리 고려).
- 원본 저장소 `sandbox-environments/game-template-starter.html`을 [[pilot-game-starter-template]]의 출발점으로 사용.

## 관련
- [[pilot-env-design]] · [[pilot-curriculum-adapted]] · [[pilot-game-starter-template]]
- [[no-debug-philosophy]] · [[ai-persona-workflows]] · [[single-html-runtime]]
- [[fast-implementation-mode]] · [[combat-vs-cooperative-framing]]
- 원본: `.raw/sans-kids-2025/{README,CLAUDE,CHANGELOG}.md`, `.raw/sans-kids-2025/workflows/**`, `.raw/sans-kids-2025/workshop-materials/**`
