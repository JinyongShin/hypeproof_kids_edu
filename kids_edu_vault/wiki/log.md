---
type: meta
title: "Log"
created: 2026-04-12
updated: 2026-04-19
tags:
  - meta/log
---

# Log

추가 전용. 새 엔트리는 **최상단**에 삽입. 과거 엔트리 수정 금지.

---

## 2026-05-15 | pr-merge | PR#7 feature/langgraph-gemini → main 머지 + 리뷰 반영
- PR: https://github.com/JinyongShin/hypeproof_kids_edu/pull/7
- Pages updated: [[adr-langgraph-gemini-backend]]
- Key insight: [[langgraph]]+[[gemini-2-5-flash]] 백엔드 전환 PR이 리뷰 후 main에 머지됨. `edit_code_node` 실패 피드백 추가(사용자 경험), `sys.path` 반복 패턴 정리(코드 품질), Langfuse 시크릿 외부 주입(보안). 파일럿 후 처리 항목(Ping/Pong, CSP, rolling summary)은 별도 이슈로 추적 예정.

---

## 2026-05-15 | ingest | 국립암센터 행사 사전 확인 요청 초안
- Source: `.raw/meeting_notes/2026-04-21-hospital-inquiry-draft.md`
- Pages created: [[2026-04-21-hospital-inquiry-draft]]
- Pages updated: [[comms/_index]], [[index]]
- Key insight: 파일럿 당일 운영의 9개 핵심 체크포인트 (허가·감염관리·장비·콘텐츠 등)가 한 문서에 정리됨. [[game-content-guideline-pending]] 및 [[case-pediatric-onc-infection-control]] 과 직결.

---

## 2026-05-14 | vault-migration | 볼트 구조 정렬 — 스킬 철학 일치
- 작업: wiki/wiki-ingest/wiki-query/wiki-lint 스킬 철학과 볼트 구조 갭 해소
- Phase 0: git commit + tag (`vault-pre-migration-2026-05-14`) + 파일시스템 백업
- Phase 1: [[sources/_index]] · [[questions/_index]] 신규 폴더 생성
- Phase 2: `HypeProof-business-strategy.md` 루트→[[hypeproof-business-strategy]] (concepts/) 이동 + frontmatter 추가, 중복 파일 삭제
- Phase 3: dead link 4개 stub 생성 — [[adr-langgraph-gemini-backend]] · [[adr-container-deployment]] · [[adr-multitenant-schema]] · [[langfuse-observability]]
- Phase 4: orphan 파일 39개 → [[index]] 등록 (Validation·Projects·Assets·Sources·Questions 섹션 신설, Decisions·Specs·Runbooks·Components·Concepts·Comms 섹션 확장)
- Phase 5: frontmatter 보완 — projects/ 3개·runbooks/ 1개·comms/ 1개 frontmatter 추가, _index.md 13개 `status: navigational` 추가, validation/ 6개 `status: archive` + `updated` 추가
- Phase 6: vault CLAUDE.md 구조 문서 갱신 — 5개 폴더 추가, kebab-case 컨벤션 명시, 스킬 관리 폴더 주의사항 추가
- Key insight: sources/와 questions/가 없으면 wiki-ingest·wiki-query의 지식 누적 루프가 단절됨

---

## 2026-05-14 — JY 액션 리스트 저장 + LangGraph E2E 완료 기록

- Type: save / status update
- Created: [[jy-action-list-2026-05-14]]
- Updated: [[hot]]
- Key insight: [[langgraph]] MOCK_LLM=0 E2E 테스트 완료 확인. fly.io 배포만 남음. [[sk-biopharma]] 파일럿 critical path: 제안서 초안 → Freelancer 채용 → Studio v0.1 빌드.

---

## 2026-05-14 — 배치 ingest 3종 (SK바이오팜 5/12 미팅 × 2 + 5/14 후속)

- Source: `meeting_notes/2026-05-12.md`, `meeting_notes/20260512_meeting.md` (동일 내용), `meeting_notes/2026-05-14.md`
- Type: batch ingest
- Created: [[2026-05-12-sk-biopharma-meeting]], [[2026-05-14-sk-biopharma-followup]], [[sk-biopharma]], [[bitree]], [[oh-sungeun]], [[sixteen-essence]], [[hypeproof-studio]], [[adr-hypeproof-studio-v01]], [[sk-biopharma-pilot]]
- Updated: [[index]], [[hot]]
- Key insight: HypeProof Lab이 [[sk-biopharma]] 임직원 가족 대상 AI 게임 창작 교육 파일럿을 추진 중. 자체 IDE "[[hypeproof-studio]]" (VS Code fork) 개발 결정. 5/28 dry-run이 Go/No-go 게이트. [[sixteen-essence]] 프레임워크를 교육 IP의 핵심으로 구조화.
- 주의: 2026-05-12.md와 20260512_meeting.md는 동일 내용 — 단일 comms 페이지로 통합.

---

## 2026-04-21 — 병원 측 확인 질문 초안 작성

- Type: 작업 기록
- 산출물: `meeting_notes/2026-04-21-hospital-inquiry-draft.md`
- 내용: 소아암 환아 교육 선례 조사 기반 + 운영 미확정 사항을 병원 측에 확인하는 질문 초안 (9개 섹션, 행사허가·연령·참가기준·감염관리·공간·기기·보호자·콘텐츠·진행인력)
- 상태: 팀 공유 완료, 검토 의견 대기 중
- Updated: [[hot]] (JY 현장 상황 정리 태스크 In Progress로 갱신)

---

## 2026-04-21 — 배치 ingest 3종 (wizard-curriculum / asap / meeting-briefing)

- Source: `.raw/wizard-curriculum-20260420.md`, `.raw/2026-04-21-asap.md`, `.raw/2026-04-20-meeting-briefing.md`
- Type: batch ingest
- Created: [[2026-04-20-wizard-curriculum]], [[2026-04-21-asap-action-items]], [[2026-04-20-meeting-briefing]], [[curriculum-wizard-v1]], [[filamentary]], [[vibe-coding]]
- Updated: [[pilot-curriculum-adapted]] (3-way 커리큘럼 방향 contradiction 추가), [[pilot-5-5-milestones]] (4/24 필라멘트리 전달 마일스톤 추가), [[pilot-day-operation]] (wizard curriculum 참조 + open questions 확장), [[comms/_index]], [[stakeholders/_index]], [[index]], [[hot]]

### 핵심 내용

- **커리큘럼 방향 3종 병존**: HTML게임([[pilot-curriculum-adapted]]) vs 그림책([[2026-04-19-curriculum-v0.3]]) vs 게임타이틀카드([[curriculum-wizard-v1]]). 확정 필요.
- **마감 2026-04-24**: BH+지웅 커리큘럼 + JY 현장상황 → [[filamentary]] 부대표 전달.
- **신규 이해관계자**: [[filamentary]] — 현장 교육 협력 기관, 커리큘럼 피드백 파트너.
- **교육 철학**: [[vibe-coding]] 개념 등장 (자연어로 AI를 지휘해 창작물 생성), 16가지 AI 덕목.
- **인력 갭**: 브리핑 권장 6~7명 vs 현 계획 5명 → 1~2명 부족 가능성.

---

## 2026-04-19 — 커리큘럼 v0.3 ingest (2026-04-19-curriculum-v0.3.html)

- Source: `.raw/2026-04-19-curriculum-v0.3.html`
- Type: ingest
- Created: [[2026-04-19-curriculum-v0.3]] (comms), [[curriculum-v0.3]] (deliverable)
- Updated: [[pilot-5-5-milestones]] (커리큘럼 초안 Done 처리), [[pilot-curriculum-adapted]] (v0.3 cross-ref callout 추가), [[deliverables/_index]] (Curriculum 섹션 추가), [[comms/_index]] (v0.3 등록), [[index]] (Comms 9, Deliverables 11, Recent Sources 추가), [[hot]] (커리큘럼 v0.3 컨텍스트로 갱신)

### 핵심 내용
- 봉호([[bongho-tae]])·지웅([[jiwoong-kim]]) 공동 작성. 4/19 마감 목표 달성.
- 코어 골: "내가 존재하는 세계가 있다" — 소아암 병동 어린이가 처음 통제하는 창작 세계.
- 6블록 2시간 구성 (오프닝→캐릭터→세계→꾸미기→발표회→수료식).
- 결과물 형식: **그림책** (표지 + 이름 삽입 이야기 + "지은이: OOO"). 기존 [[pilot-curriculum-adapted]] 게임 HTML 중심과 상이.
- AI 호출 포인트 3종: 캐릭터 카드 생성 / 이름 삽입 이야기 / 표지 이미지.
- 안전 체계 4종: R4(완성보장) / R6(콘텐츠) / R5(에러) / 퍼실리테이터 원칙.
- 다음 게이트: 2026-04-21 Jay·JY 커리큘럼 리뷰 → [[stack-decision-after-curriculum]] 스택 결정.

### 구현 주의사항
- v0.3 커리큘럼의 AI 호출 3종(캐릭터 카드, 이야기, 표지 이미지)은 현재 백엔드 미구현.
- R4 완성보장 폴백도 P0 미충족 상태 — 4/21 후 [[subagent-team-structure]] 작업 범위 재산정 필요.

---

## 2026-04-18 — 0417-call.md ingest: Jay–JY 통화 (2026-04-17)

- Source: `0417-call.md` (원본 날짜 4/18 표기 → 실제 통화일 **2026-04-17**로 정정)
- Type: ingest
- Created: [[2026-04-17-jay-jinyong-call]] (comms), [[jay]] (stakeholder 별칭), [[2026-05-05-pilot]] (deliverable)
- Updated: [[index]] (Stakeholders 10, Comms 8, Deliverables 10, Recent Sources 추가)

### 핵심 내용
- Jay가 HypeProof 사업 구조 브리핑: 교육 트랙 (라이센스 인증 모델) + AX 전환 트랙 (SI/서비스 이원화).
- 세일즈 파이프라인 이미 확보 — 프로덕트가 "필터" 역할. JY → 사업 구조 러프 초안 → 지웅 엔지니어링 디테일.
- 파일럿 개발 현황 공유: 채팅+게임 프레임 완성, 커리큘럼 미완 (봉호 4/19 목표).
- 소아암 환자 게임 콘텐츠 주의: 적/체력 깎임 요소 치료 철학 충돌 가능 → 국립암센터 사전 확인 필요 (JY 액션).
- 4/21 월요일 미팅 확인: 지웅·봉호·정우 참석 확정.

---

## 2026-04-18 — UX 개선 5종 구현 + QA (E2E, 실제 Claude)

- Type: session
- Location: wiki/meta/session-2026-04-18-ux-improvements.md
- 개선 1: iframe `srcdoc` 전환 — `game_html` 필드 WS 전송, 네트워크 독립적 렌더링
- 개선 3: 아동 친화적 에러 메시지 — `_friendly_error()` 헬퍼 4곳 적용
- 개선 4: 블록 버튼 스킬 이름 표시 — `SCAFFOLD_DATA` 사용, 1-based, `flex-wrap`
- 개선 5: 대기 중 중간 피드백 메시지 — 15초/40초 타이머
- 개선 6: WS 재연결 상태 배너 — 황색/적색 조건부 배너
- QA 버그 수정 3건: 블록 버튼 5·6 잘림, 힌트 중복 표시, 세션 전환 시 힌트 잔류
- 커밋: db1df5d

---

## 2026-04-17 — SQLite 마이그레이션 + 세션 버그 수정 + WS 재연결

### 백엔드
- `storage.py` 신규: SQLite DB (`kids_edu.db`), sessions/messages/games/FTS5 테이블
- JSON 파일 → SQLite 자동 마이그레이션 (서버 시작 1회, flag 파일로 멱등성 보장)
- 세션 이름: "대화 N" 기본값 → 첫 메시지 앞 15자 자동 갱신
- `PATCH /sessions/{child_id}/{session_id}/name` 수동 이름 변경 엔드포인트 추가
- WebSocket: user 메시지 스트리밍 전 저장, assistant 메시지 done 시점 저장, 연결 해제 시 부분 저장
- 말풍선 버그 수정: `original_prompt` 를 DB 저장 (주입 전), Claude에는 게임 파일 경로 주입
- 게임 수정/신규 분기: "수정 요청이면 Read 도구로, 새 게임이면 무시하고 새로 만들어"
- `from pathlib import Path` 누락 → NameError → WebSocket 크래시 수정
- Claude subprocess `cwd=tempfile.gettempdir()` + `--add-dir` 로 프로젝트 컨텍스트 격리
- `TUTOR.md` 게임 코딩 규칙 추가: Canvas 고정 480×480, `roundRect()` 금지, try-catch 게임 루프

### 프론트엔드
- `useChat.ts`: sessionId 변경 시 `isLoading`·`gameUrl` 리셋, WS 자동 재연결 (최대 3회)
- `page.tsx`: `activeSessionId` 변경 시 `last_game_url` fresh fetch, `sessionRefreshToken` 추가
- `SessionSidebar.tsx`: `name` 필드 표시, `refreshToken` prop으로 게임 생성 후 re-fetch

---

## 2026-04-17 — 0412 워크샵 구조 문서 확인 + Jay 공유 내용 정리

### 확인
- `0412.md` (프로젝트 루트) 내용 검토 → 볼트 이미 완전 반영됨 (중복 ingest 불필요)
- 기존 `2026-04-12-jay-workshop-structure.md` + `pilot-5-5-milestones.md` 가 최신 기준

### JY → Jay 공유 내용 (4/17 기준)
- Track A 개발 진행 중 (채팅 히스토리, 게임 복원, 로딩 UI 완료)
- **4/21 스택 결정 미팅 전 선행 조건**: BH 커리큘럼 초안 4/19 수령 확인 (Jay 독촉)
- **Jay 액션 필요**: 랩탑/태블릿 40대 확보 방향 결정 (4/21 이전)
- **Jay 액션 필요**: 자원봉사자 퍼실리테이터 섭외 여부 결정

### 다음 게이트
- 2026-04-19: BH 커리큘럼 초안 + Ryan 와우 포인트 설계 마감
- 2026-04-21: Jay ↔ JY 스택 확정 미팅

---

## 2026-04-14 — 채팅 히스토리 저장/복원 + Windows UTF-8 버그 수정

### 구현
- **채팅 히스토리 저장**: `done` 이벤트 시 `data/messages/{child_id}/{session_id}.json` 에 user+assistant pair 저장. atomic write, 경로 순회 방어 적용.
- **복원 API**: `GET /sessions/{child_id}/{session_id}/messages` 엔드포인트 추가.
- **프론트엔드**: `useChat.ts` sessionId 변경 감지 시 자동 히스토리 로드.
- **세션 삭제 연동**: `delete_session` 호출 시 messages 파일도 함께 삭제.

### 버그 수정 (f59b5e4) — Windows CP949 인코딩
- `_append_messages`, `_save_session_meta`, `SessionStore._save` 의 `write_text()` 3곳에 `encoding='utf-8'` 누락 → 한국어 깨짐 + HTTP 500 오류 발생.
- `_load_messages` 에 `UnicodeDecodeError` 예외 처리 추가.

### E2E 검증
- 메시지 전송 → 로그아웃 → 재로그인 → 세션 클릭 → 히스토리 복원 전 구간 확인 완료.

### 커밋
- `f59b5e4` fix(backend): Windows CP949 인코딩 버그 수정
- `40e585d` feat: 채팅 히스토리 백엔드 저장/복원
- `5ee623b` fix(frontend): 재로그인 시 게임 복원 + 로딩 UI
- `2d8693f` fix(frontend): React Strict Mode WS 오류 오탐 수정

---

## 2026-04-13 — 채팅 히스토리 백엔드 저장/복원

### 구현
- **백엔드**: `done` 이벤트 시 `data/messages/{child_id}/{session_id}.json` 에 user+assistant pair 저장 (atomic write, 경로 순회 방어). `GET /sessions/{child_id}/{session_id}/messages` 엔드포인트 추가. `delete_session` 시 메시지 파일도 함께 삭제.
- **프론트엔드**: 세션 전환 시 `GET /sessions/.../messages` 호출 → 메시지 목록 즉시 복원. React state에만 존재하던 기존 구조 탈피.

### 커밋
- `40e585d` feat: 채팅 히스토리 백엔드 저장/복원

---

## 2026-04-13 — 재로그인 게임 복원 + 로딩 UI 개선

### 수정
- **게임 복원**: 세션 전환 시 `last_game_url`을 `onSessionChange` 콜백으로 전달, `setGameUrl(lastGameUrl)`로 즉시 복원. 기존엔 `setGameUrl("")`로 강제 초기화하던 버그.
- **로딩 UI**: 전송 후 AI 첫 응답 전 구간에 `●●●` bounce dots 버블 표시. GamePreview에 `isLoading` prop 추가, 게임 없을 때 스피너, 게임 있을 때 반투명 오버레이+스피너.

### 커밋
- `5ee623b` fix(frontend): 재로그인 시 게임 복원 + 로딩 UI 개선

---

## 2026-04-13 — React Strict Mode WS 오탐 버그 수정 + Playwright MCP 설정

### 수정
- **useChat.ts**: `intentionallyClosed` 플래그 추가. React Strict Mode에서 effect 2회 실행 시 첫 번째 WS cleanup이 연결 수립 전 `onerror`를 트리거하던 문제 해결.
- **.mcp.json**: Windows 환경에서 `npx` 실행 시 `cmd /c` 래퍼 누락 문제 수정. Playwright·context7·sequential-thinking 모두 적용.

### 확인 (Playwright MCP)
- `localhost:3000` → `/login` 자동 리다이렉트 정상
- root/0000 로그인 → 메인 앱 진입, 세션 사이드바 표시 정상
- WS 연결 에러 메시지 제거 확인

### 커밋
- `2d8693f` fix(frontend): React Strict Mode WS 오류 메시지 오탐 수정

---

## 2026-04-13 — 로그인 + 채팅 세션 관리 + 게임 HTML 파일 저장

### 구현된 기능
- **로그인**: `/login` 페이지 신규. `ADMIN_USERNAME`/`ADMIN_PASSWORD` 환경변수 기반 검증. sessionStorage auth state. 미인증 시 `/login` 리다이렉트.
- **채팅 세션 관리**: `SessionSidebar` 신규. `{child_id}_{YYYYMMDD_HHmmss}` 형식 `session_id`. REST API `GET/POST/DELETE /sessions/{child_id}`. 세션 전환 시 마지막 게임 URL 복원.
- **게임 HTML 파일 저장**: `srcdoc` → 파일 저장 + `/games/{child_id}/{session_id}/{game_id}` URL 서빙. React 재렌더 시 게임 중단 버그 해결. 세션당 최신 10개 보관.

### 보안 수정
- 경로 순회 공격 방어: `path.resolve().is_relative_to(base)` 검증
- 하드코딩 자격증명 → 환경변수 이동
- WebSocket `accept()` 순서 수정
- `asyncio.Lock` 동시쓰기 race condition 방어

### 테스트
- 백엔드 pytest: 29개 통과 (`src/backend/tests/test_auth_session_game.py`)
- 프론트엔드 Vitest: 9개 통과 (`src/frontend/__tests__/useChat.test.ts`)

### ADR
- [[auth-session-game-persistence]] — status: proposed → implemented

### 커밋
- `2e9f555` feat: 로그인 + 세션 관리 + 게임 HTML 파일 저장

---

## 2026-04-13 — 클릭 즉시 전송 UI

- Type: decision
- Location: wiki/decisions/click-to-send-ui.md
- From: PromptScaffold 카드 + 힌트 클릭 시 textarea 거치지 않고 즉시 채팅 전송
- 변경 파일: `src/frontend/components/ChatPane.tsx` (handleQuickSend 추가, hint `<p>` → `<button>`)

---

## 2026-04-13 — 모바일 스와이프 네비게이션

- Type: decision
- Location: wiki/decisions/mobile-swipe-navigation.md
- From: 모바일에서 채팅창이 너무 작아지는 문제 → 스와이프 전환 UX 구현
- 변경 파일: `hooks/useSwipe.ts` (신규), `app/layout.tsx`, `app/page.tsx`

---

## 2026-04-12 (16) — 상품 요구사항 인제스트 + 갭 분석

### 내용
- `meeting_notes/production_requirements.md` (R1-R9) 수신
- 현재 구현 대비 갭 분석 완료
- ❌ 미충족: R4(폴백), R7(갤러리), R8(공유), R9(밝은 UI)
- 🔶 부분: R2(타이핑 최소화 — 원클릭 전송 검토 필요)
- ✅ 충족: R1, R3, R5, R6

### 생성 파일
- `kids_edu_vault/wiki/specs/product-requirements.md` — R1-R9 요구사항 + 현황 태그
- `product-requirements-gap-plan.md` (프로젝트 루트) — 갭 해소 구현 계획 (P0/P1/P2)

---

## 2026-04-12 (15) — Unit 7 완료: MVP 통합 확인

### 검증 항목 (MOCK_CLAUDE=1)
- WS 이벤트 시퀀스 (text×N → game → done): PASS
- 세션 독립 (child01 vs child02 동시 접속): PASS
- 5탭 동시 접속 (child01-05): PASS
- /admin/reset 엔드포인트: PASS (mock 세션 미저장으로 false 반환 — 정상)
- `uv run pytest -v` 28개 전체: PASS
- `npm run build` Turbopack 컴파일: PASS

### 볼트 업데이트
- `hot.md` 전면 갱신 (MVP 완료 스냅샷)
- `specs/ai-prompting-literacy-input.md` status → implemented

### 커밋
- `feat: MVP 통합 확인 완료`

---

## 2026-04-12 (14) — Frontend Unit 6 완료: 프롬프트 스캐폴딩 카드

### 완료 내용
- `scaffoldData.ts`: 블록 0-5 교육 목표·스킬·예시 문장 데이터 (이 파일만 봐도 커리큘럼 구조 파악 가능)
- `PromptScaffold.tsx`: 블록별 클릭형 예시 문장 카드 UI
- `ChatPane.tsx` 통합: 카드 클릭 → 입력창 자동 채워짐
- 블록 4(자유 조합)·5(언어화)는 카드 미표시 (자유 입력 유도)
- `npm run build` 통과 확인

### 커밋
- `feat(frontend): 블록별 프롬프트 스캐폴딩 카드`

---

## 2026-04-12 (12) — Frontend Unit 4 완료: 2-pane 레이아웃 + GamePreview

### 완료 내용
- `GamePreview.tsx`: srcdoc + sandbox="allow-scripts" iframe
- `page.tsx`: 채팅 40% | 게임 60% 분할 레이아웃, 임시 테스트 버튼
- `wiki/components/kids-edu-frontend.md` 신규 생성
- 빌드 통과 확인

### 다음 Unit
- Unit 5: ChatPane (WebSocket + 스트리밍)

---

## 2026-04-12 (11) — Frontend Unit 3 완료: Next.js 초기화

### 완료 내용
- `src/frontend/` create-next-app@16 초기화 (TypeScript + App Router + Tailwind)
- 보일러플레이트 정리 (page.tsx, layout.tsx, globals.css)
- 빌드 통과 확인

### 다음 Unit
- Unit 4: 2-pane 레이아웃 + GamePreview (iframe sandbox)

---

## 2026-04-12 (10) — Backend Unit 2 완료: 서버 기동 확인 + 볼트 문서화

### 완료 내용
- `.env.example` 추가 (CLAUDE_TIMEOUT, CLAUDE_MODEL, MOCK_CLAUDE)
- `/health` 응답 확인 완료
- `.gitignore` 수정 (`.env.example` 추적 가능하도록)
- `wiki/components/kids-edu-backend.md` 신규 생성

### 다음 Unit
- Unit 3: Next.js 프론트엔드 초기화

---

## 2026-04-12 (9) — Backend TDD Unit 1 완료: 28/28 테스트 통과

### 완료 내용
- `src/backend/` 초기 구현: `main.py`(FastAPI WebSocket), `claude_runner.py`(subprocess + SessionStore), `personas/TUTOR.md`(W3+W4)
- TDD 테스트 28개 작성·통과: SessionStore(10), _extract_hint(5), _HTML_RE(5), reset_session(2), stream_claude mock(6)
- `pyproject.toml` dev 의존성 추가 (pytest, pytest-asyncio)
- 발견한 패턴: `MOCK_CLAUDE` 같은 모듈 레벨 상수는 `monkeypatch.setattr(module, 'VAR', val)`로 패치해야 함

### 다음 Unit
- Unit 2: `.env.example` 작성 + 서버 기동 확인 → backend 볼트 컴포넌트 페이지

---

## 2026-04-12 (8) — MVP 개발 계획 확정: FastAPI + CLI subprocess + AI 프롬프팅 리터러시

### Why
- 어린이 인터페이스에서 Claude를 어떻게 호출할지 결정. Claude Agent SDK vs CLI subprocess 검토.
- 4/21 스택 결정 게이트 후 4/26 리허설까지 5일밖에 없어 `sanshome_bot/claude_runner.py` 재활용이 유일한 현실적 선택.
- "AI로 게임 만들기" + "AI에게 잘 시키는 법 체득" 두 교육 목표 병행 필요성 확인 → 커리큘럼 + 제품 동시 설계.

### 결정
- 백엔드: FastAPI (Python) + `claude -p --output-format stream-json` CLI subprocess.
- 프론트: Next.js — 채팅 pane + 게임 preview iframe + 프롬프트 스캐폴딩 카드.
- 블록별 프롬프팅 스킬 매핑 (묘사→구체화→추가→수정→자유→언어화) 커리큘럼에 반영 요청.

### 파일 변경
- 갱신: `2026-04-12-mvp-dev-plan.md` — FastAPI 스택으로 전면 업데이트
- 생성: `wiki/specs/ai-prompting-literacy-input.md` — BH 커리큘럼 인풋 spec
- 생성: `wiki/decisions/nextjs-fastapi-wrapper-architecture.md` — 아키텍처 ADR

---

## 2026-04-12 (7) — Subagent 팀 빌드: Dev 4 추가 (architect / implementer / reviewer / tester)

### Why
- 피벗 후 3주 MVP 착수를 위해 개발 파이프라인(설계→구현→테스트→리뷰) 에이전트가 필요. 기존 wiki-ingest/wiki-lint 2개로는 지식측만 커버.
- `build_teams.md` 처방(6개)에서 `debugger`·`docs-writer`는 보류 — pain 축적 시 후행 추가. 과도한 specialist는 자동 위임 신뢰도 저하.

### 팀 구성 (총 6개)
- **Wiki**: `wiki-ingest`, `wiki-lint` (기존)
- **Dev** (신규): `architect`, `implementer`, `reviewer`, `tester` — 전원 `sonnet`, 각 `wiki-query` 스킬 포함.

### 파일 변경
- 생성: `.claude/agents/{architect,implementer,reviewer,tester}.md`
- 생성: `.claude/CLAUDE.md` — 위임 규칙·핸드오프·Bash 스코프·시크릿·주간 루프.
- 수정: 루트 `CLAUDE.md` — "팀 & 워크플로우" 섹션 추가 (6-agent 표, 스킬 인벤토리, 7단계 규칙 표, 표준 흐름 다이어그램, 비용 가드레일).

### 운영 규약 (요지)
- 컨텍스트 시딩: 모든 subagent 첫 작업 전 `hot.md` + 루트 `CLAUDE.md` + 지정 ADR 경로 Read.
- 핸드오프 = 파일 경로 (요약 복붙 금지).
- Bash: `git push`·`reset --hard`·`rm -rf`·전역 설치는 메인만.
- 표준 흐름: architect → implementer → tester → reviewer → (메인 commit) → wiki-ingest/save.

### Open
- Smoke test 미실시 — MVP 착수(=Jay 승인 후 C 진입) 시점에 `@architect`부터 실전 가동 예정.

### Related
- ADR: [[subagent-team-structure]] (proposed, 2026-04-12).
- [[pivot-to-chat-preview-wrapper]], [[fast-implementation-mode]].

---

## 2026-04-12 (6) — JY 내부 결정: 옵션 C→A 단계 진행

- **초기 C**(래퍼 MVP + 운영자 하드코드 계정)로 래퍼 착수, **최종 파일럿 당일은 A**(새 래퍼 정식)로 전환하는 단계 진행안 채택.
- 근거: 파일럿 자체가 "chat-native, 코드-invisible" 포지셔닝 검증이므로 아이 앞에 차별화 UX가 서야 데이터 의미. C에서 멈추면 피드백과 제품 방향 괴리.
- **상태**: JY 내부 결정. Jay 확인 전 — 브리핑 문서 `pivot-briefing-jay.md` 회신 시 변경 가능 (특히 타임라인 리스크 크면 B 철수).
- Updated: [[pivot-to-chat-preview-wrapper]] (현재 실행 방향 섹션 추가), [[hot]], `2026-04-12-pivot-briefing-jay.md`.
- New gate: [[pilot-rehearsal-late-april]]에서 A 준비 상태 검증.

---

## 2026-04-12 (5) — Pivot: code-server+cline → chat+preview 래퍼 리서치·결정

### Context
- 논의: 아이가 AI와 채팅으로 게임을 만드는 데 코드를 볼 이유가 없다 → VSCode 포크(code-server+cline) 구조가 최선이 아니라고 판단.
- 방향: 커스텀 웹 래퍼(좌 채팅 / 우 라이브 프리뷰) + OAuth + 향후 유료화.

### Research filed (3 intel pages)
- [[intel-wrapper-architecture]] — Claude Agent SDK, iframe+srcdoc 샌드박스, Next.js App Router, 코드 숨김 UX 선례.
- [[intel-auth-billing-compliance]] — Clerk/Supabase/NextAuth 비교, Stripe + 포트원 이원화, PIPA 만 14세 미만 트랩.
- [[intel-competitive-landscape-2026]] — bolt/Lovable/v0/Replit/Scratch/엔트리/Khanmigo 비교, 무주공산 3개 파악.

### Decisions (3 proposed)
- [[pivot-to-chat-preview-wrapper]] — 스택 피벗 (기존 [[pilot-env-design]] 부분 supersede).
- [[iframe-sandbox-over-webcontainers]] — 프리뷰 샌드박스 기술 선택 (WebContainers 상용 라이선스 트랩 회피).
- [[parent-gated-signup-first]] — PIPA 대응, 부모 이메일 가입 우선.

### Key findings
- **WebContainers는 상용 라이선스 필요** — bolt.new 모방 트랩. iframe+srcdoc만으로 충분 (p5/canvas엔 Node 불필요).
- **Google OAuth를 아동 주 경로로 삼으면 PIPA 위반 리스크** — 엘리스·코드잇 키즈·구름EDU 전부 부모 계정+자녀 서브프로필 방식.
- **"Chat-native, 코드-invisible, kid-first" 포지셔닝은 무주공산** — Scratch 4.0 AI는 2027+ → 12–18개월 기회 창.
- Claude Agent SDK 전환 시 기존 [[gemini-2-5-flash]] 비용 목표($0.15/세션) 재검토 필요.

### Updated
- [[intel/_index]] — Competitive·Technical References 섹션 채움.
- [[decisions/_index]] — Pending에 3건 추가.
- [[index]] — Decisions(10)·Intel(14) 카운트 갱신.
- [[hot]] — 덮어씀.

### Briefing
- 프로젝트 루트 `2026-04-12-pivot-briefing-jay.md` 작성 — Jay 전달용.

### Follow-up (Jay·JY 결정 필요)
- 모델: Claude vs Gemini (Agent SDK 전환 비용 영향).
- 파일럿 당일 실행 스택: 새 래퍼 vs 기존 code-server (23일 남음).
- MVP 스코프: OAuth·결제를 파일럿 전/후 어디에 둘지.
- 어린이 Google 계정 보유 여부 → 가입 플로우 확정 (기존 blocker 유지).

---

## 2026-04-12 (4) — autoresearch: 소아암 환아 대상 코딩·AI 교육 선례

### Rounds
- 2 rounds, 10 WebSearch, 10 WebFetch (1개 실패: MDPI 403, 1개 unparseable: 한국 KCI PDF).

### Sources filed (9)
- [[case-sickle-cell-coding-study]] — Journal of Intelligence 2026, code.org 11세션 EF 전이 (direct analog).
- [[case-stjude-educational-challenges]] — St. Jude Together 임상 가이드.
- [[case-starlight-therapeutic-gaming]] — Starlight Foundation program description.
- [[case-techquity-pediatric-oncology]] — Pediatric Blood & Cancer 2025 AI+VR 형평성.
- [[case-hospital-pedagogy-framework]] — Hospital pedagogy 3모드/5메커니즘 (Am. J. Tech & Applied 2026).
- [[case-pediatric-onc-infection-control]] — PMC peer-reviewed 감염관리.
- [[case-korean-hospital-schools]] — 국내 4개 어린이 공공전문진료센터 (KCI 2026, partial).
- [[case-academic-continuity-peds-onc]] — Psychosocial Standards (PMC5198902).
- [[case-oep-socioecological-program]] — 호주 OEP 평가 (Continuity in Education).

### Synthesis
- [[research-peds-onc-coding-ed]] — 파일럿 적용 함의 정리.

### Key finding
**우리 파일럿 형식(40명 소아암 환아 단일 90분 AI 코딩 이벤트)의 peer-reviewed 직접 선례는 없음.** 인접 영역 증거는 충분 — 파일럿 설계 4가지 변경([[no-debug-philosophy]] / [[ai-persona-workflows]] / [[single-html-runtime]] / [[combat-vs-cooperative-framing]])은 St. Jude accommodations + Starlight narrative standards와 구조적으로 일치. EF 전이 주장은 증거 부족 → 성과 지표를 **경험·완주율·자기효능감**으로 재정렬 필요.

### Follow-up actions
- ANC 컷오프·사전 문진 양식 의료진 합의.
- 감염관리 프로토콜을 [[pilot-operator-guide]]에 런북 형태 편입.
- 튜터 사전 오리엔테이션 커리큘럼 초안.
- 국립암센터 내부 병원학교 존재 여부 확인.

---

## 2026-04-12 (3) — sans-kids-school-2025 ingest + 병동 재설계 페이지 생성

### Source
- `sans-kids-school-2025/` (2025-08-03 SANS Kids VibeCoding 워크숍 v1.1.2) 검토 및 md 자료 `.raw/sans-kids-2025/`로 복사.
- 복사 범위: `README.md`, `CLAUDE.md`, `CHANGELOG.md`, `workflows/workflow-{1..5}/cursor-rules.md`, `educational-scenarios/*.md`, `workshop-materials/{lecture_script,facilitator-checklist,emergency-troubleshooting,expected-questions,age-based-optimization,workflow-comparison-analysis}.md`, `evaluation/workflow-evaluation-criteria.md`. HTML·이미지·릴리즈 바이너리·setup 스크립트는 제외.

### Created (5 pages)
- Concepts (3): [[no-debug-philosophy]], [[ai-persona-workflows]], [[single-html-runtime]] — Pedagogy 섹션 신설.
- Decisions (1, proposed): [[combat-vs-cooperative-framing]] — 병동 파일럿 서사 전투형→협력형 채택.
- Specs (1, draft): [[pilot-curriculum-adapted]] — 4h → 90분 6블록 재설계.

### Updated
- [[components/sans-kids-school-2025]] — 버전·저자·아키텍처·교수법·병동 변경점 4가지 반영.
- [[concepts/_index]], [[decisions/_index]], [[specs/_index]] — 신규 페이지 등록.
- [[index]] — Decisions/Specs/Concepts 카운트 및 Recent Sources 갱신.
- [[hot]] — 덮어씀.

### 핵심 인사이트
- 원본 워크숍의 전투 서사·Cursor 설치형 배포는 병동에 부적합 → 서사 교체 + [[code-server]] 브라우저형으로 재구성.
- 5종 AI 페르소나 중 W3(속도) + W4(스토리) 합성이 병동에 가장 적합. W3는 [[fast-implementation-mode]]의 원형.
- 원본 자산의 핵심 재활용 포인트는 "게임 템플릿 파일"보다 **교수법 패턴**(no-debug, 30-second rule, 즉시 실행 루프)임.

---

## 2026-04-12 (2) — 개발 문서 관리 확장 + meeting_notes ingest

### Structure
- 볼트 구조 확장: `specs/`, `components/`, `runbooks/`, `concepts/` 4개 도메인 추가.
- 템플릿 4종 추가: `component.md`, `spec.md`, `runbook.md`, `concept.md`.
- 프로젝트 루트 `CLAUDE.md` 및 볼트 `CLAUDE.md` 갱신 예정.

### Ingested (meeting_notes/ 기준)
- Stakeholders (6): [[jay-lee]], [[jinyong-shin]], [[jiwoong-kim]], [[tj]], [[bongho-tae]], [[kiwon-nam]].
- Comms (6): [[2026-01-05-meeting]], [[2026-01-12-meeting]], [[2026-01-19-meeting]], [[2026-01-26-meeting]], [[2026-02-09-meeting]], [[2026-04-11-call-note]].
- Decisions (6): [[regular-meeting-monday-930]], [[discord-for-comms]], [[podcast-format-host-panels-guest]], [[markdown-for-knowledge-share]], [[ai-onboarding-role]], [[fast-implementation-mode]].
- Deliverables (8): [[okr-q2-jy]] + 7개 pilot 작업.
- Components (6): [[code-server]], [[oauth2-proxy]], [[caddy]], [[cline]], [[gemini-2-5-flash]], [[sans-kids-school-2025]].
- Concepts (5): [[hypeproof-lab]], [[mission-driven]], [[tracks-a-b]], [[fundamental-content-teams]], [[ai-native-workflow]].
- Specs (1): [[pilot-env-design]].
- Intel (1): [[environ-kukrip-amsenter]].

### Index/cache
- [[index]] 전면 재작성 — 전체 카탈로그 반영.
- [[hot]] 갱신 — 최근 파일럿 컨텍스트 중심으로 덮어씀.

---

## 2026-04-12 (1) — Scaffold
- Scaffold: `kids_edu_vault/` Mode C (Business/Project) 구조 생성.
- 생성: `index.md`, `log.md`, `hot.md`, `overview.md`.
- 생성: `stakeholders/`, `decisions/`, `deliverables/`, `intel/`, `comms/` 각 `_index.md`.
- 생성: `_templates/` (stakeholder, decision, deliverable, intel, meeting, source).
- 생성: vault 루트 `CLAUDE.md`.
