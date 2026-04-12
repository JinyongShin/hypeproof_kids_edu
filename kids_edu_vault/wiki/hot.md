---
type: meta
title: "Hot Cache"
updated: 2026-04-12
tags:
  - meta/hot
---

# Recent Context

## Last Updated
2026-04-12. Autoresearch: 소아암 환아 대상 코딩·AI 교육 선례 9개 케이스 + 합성 1건 파일링.

## Key Recent Facts
- 파일럿 일시: **2026-05-05 13:30–15:30** / 장소: **국립암센터 일산로323 강당(200석)** / 인원: **40명, 8–12세** ([[environ-kukrip-amsenter]]).
- 접속 URL: `hypeproof-ai.xyz` — [[caddy]] + [[oauth2-proxy]] + [[code-server]] + [[cline]] + [[gemini-2-5-flash]] 스택 ([[pilot-env-design]]).
- AI 튜터 운영 모드: [[fast-implementation-mode]] (피로도·타이핑 제약 대응).
- 비용 목표: $0.15 미만 / 회. Q2 OKR (JY): KR1 수강생 5명+ 실습 / KR2 치명 장애 0 / KR3 운영자 가이드 ([[okr-q2-jy]]).

## Research 결과 (2026-04-12) — 소아암 환아 대상 코딩·AI 교육 선례
- **합성**: [[research-peds-onc-coding-ed]]. 9개 case 기반.
- **핵심 결론**: 우리 파일럿 형식(40명 소아암 환아 단일 90분 AI 코딩 이벤트)의 peer-reviewed 직접 선례 없음. 인접 증거는 충분.
- **직접 analog**: [[case-sickle-cell-coding-study]] (Journal of Intelligence 2026). Code.org 11세션 x 5-6주, 7-8세 SCD 환아 3명, 100% 완주, EF 전이 입증. **단 11세션 집약 투여**이므로 우리 90분 단회성에 EF 전이 주장 불가.
- **교수법 지지**: [[case-stjude-educational-challenges]]. 스크라이브·연장시간·조용한 공간·자주 체크인·예고 없는 지명 금지 = 우리 4가지 병동 맞춤 변경과 구조적으로 일치.
- **감염관리 (파일럿 당일 load-bearing)**: [[case-pediatric-onc-infection-control]]. 손 위생 + 운영자 구두 프롬프트, 전원 사전 문진·발열체크, ANC<100 contraindication 의료진 합의 필요, ≥12 ACH 환기, 1인 1기기 + 와이프, 전원 수술마스크 보수적 권장.
- **프레임워크**: [[case-techquity-pediatric-oncology]] (Pediatric Blood & Cancer 2025) — AI+VR 형평성 개입. 우리 파일럿 = Techquity intervention으로 프레이밍 가능.
- **국내 gap**: [[case-korean-hospital-schools]]. SNU·Severance·전북대·전남대 공공전문진료센터 병원학교는 치유환경·체험(바리스타·공예) 중심. ICT/코딩 프로그램은 검색 스니펫에 없음 → 우리 파일럿이 국내 **최초 사례 가능성**.
- **정직한 성과 프레임**: [[case-oep-socioecological-program]] — 부모가 가치로 꼽은 건 "학교는 중요하다" 메시지와 "치료로부터의 주의 분산". EF 전이 같은 과장보다 이 프레이밍이 방어적이고 진실.

## Active Threads
- **Jay 확인 대기** (pilot blocker): 어린이 Google 계정 보유 여부 → [[pilot-oauth-setup]] 영향.
- **JY 이번 주**: [[pilot-gemini-api-key]], [[pilot-server-domain]].
- **신규 — 의료진 합의 필요**: ANC 컷오프, 사전 문진 양식, 강당 HVAC 사양. 4/20 전 확정.
- **[[combat-vs-cooperative-framing]] 후속**: 대체 서사 3개 이상 확정, 시스템 프롬프트에 서사 제약 추가, 의료진·보호자 고지문 반영.
- **성과 지표 재조정**: OKR KR1 "5명+ 실습" 유지하되, EF 전이 같은 과장 주장 폐기 → ①완주율 ②자기효능감 self-report ③부모 만족도 ④치명 장애 0으로 측정.
- **[[pilot-curriculum-adapted]] 검증**: 리허설([[pilot-rehearsal-late-april]])에서 블록별 실시간 측정.
- **Runbook 미작성**: `pilot-day-operation`, `deploy-code-server`, `rehearsal-checklist`, `operator-script-per-block`. 감염관리 프로토콜을 `pilot-day-operation`에 편입.
- **튜터 사전 오리엔테이션 커리큘럼** 초안 필요 — psychosocial 기본 + 감염관리 + 교수법 제약. [[case-academic-continuity-peds-onc]] 기준 "단순 자원봉사 ≠ 충분".
- **External stakeholders** (이동훈/문조일/김성경 대표, 박재현 소장, 노수림 교수) 페이지 미생성.
