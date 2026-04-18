---
type: meta
title: "Hot Cache"
created: 2026-04-12
updated: 2026-04-18
tags:
  - meta/cache
---

# Hot Cache — 2026-04-18

최근 컨텍스트 스냅샷. 세션 시작 시 가장 먼저 읽을 것.

---

## 현재 상태: 파일럿 D-17 — 4/17 Jay–JY 통화 완료 / 4/21 미팅 대기

### 프로젝트 개요
- 목표: 소아암 병동 어린이(8-12세) AI 크리에이터 워크샵 파일럿 (2026-05-05, 국립암센터 강당)
- 스택: FastAPI (Python/uv) + Next.js 16 (App Router) + Claude CLI subprocess
- 래퍼: 채팅(WebSocket) + iframe 게임 프리뷰 + 블록별 프롬프트 스캐폴드

### 4/17 Jay–JY 통화 핵심 (→ [[2026-04-17-jay-jinyong-call]])

**사업 구조 (Jay 브리핑)**
- HypeProof 프로덕트 = 두 트랙: 교육 (라이센스 인증 모델) + AX 전환 (SI / 서비스 이원화).
- 세일즈 파이프라인 이미 확보 — 프로덕트가 "필터" 역할. JY → 러프 초안 → [[jiwoong-kim]] 엔지니어링 디테일.
- 프라이싱 모델·리소스 배분 구조 설계 필요.

**파일럿 현황**
- 개발 프레임 완성 (채팅+게임 미리보기, Claude subprocess). 5/5 파일럿용 MVP.
- 커리큘럼([[bongho-tae]] 담당) 아직 미완 — 4/19 목표.
- 소아암 환자 게임 콘텐츠 주의: 적/체력 깎임 요소 → 국립암센터 치료 담당자 사전 확인 필요 (JY 액션).

**4/21 월요일 미팅**
- 사무실 미팅. 참석: [[jiwoong-kim]], [[bongho-tae]], [[jungwoo]] 확정.
- 의제: 프로덕트 구조 공유 + 커리큘럼 리뷰 + [[stack-decision-after-curriculum]] 게이트.

### 긴급 마일스톤 (현재 ~ 4/26)

| 날짜 | 마일스톤 | 담당 | 상태 |
|---|---|---|---|
| 2026-04-19 | 커리큘럼 초안 (2시간 타임테이블 + 조 편성) | BH | **대기 중** |
| 2026-04-19 | 와우 포인트 설계 + 반응 측정 설계 | Ryan | **대기 중** |
| 2026-04-21 | 커리큘럼 리뷰 → Track A 스택 최종 결정 | Jay + JY | Pending |
| 2026-04-26 | Track A 래퍼 리허설 가능 상태 | JY | Pending |
| 2026-04-26 | 갤러리 페이지 + 랜딩 페이지 | JeHyeong | Pending |

### 완료된 개발 작업 (최신순, 2026-04-18 기준)
| 기능 | 상태 |
|---|---|
| **UX 개선 1: iframe srcDoc 전환** (네트워크 독립, /games/ HTTP 요청 0건) | ✅ 2026-04-18 |
| **UX 개선 3: 아동 친화적 에러 메시지** (_friendly_error 헬퍼 4곳) | ✅ 2026-04-18 |
| **UX 개선 4: 블록 버튼 스킬 이름 표시** (SCAFFOLD_DATA, flex-wrap) | ✅ 2026-04-18 |
| **UX 개선 5: 대기 중 중간 피드백** (15초/40초 타이머) | ✅ 2026-04-18 |
| **UX 개선 6: WS 재연결 상태 배너** (황색/적색 조건부 배너) | ✅ 2026-04-18 |
| SQLite 마이그레이션 (storage.py) + 게임 파일시스템 저장 | ✅ |
| 세션 이름 자동 할당 ("대화 N" → 첫 메시지 앞 15자) | ✅ |
| 세션 전환 버그 3종 수정 (히스토리 유실·스피너·stale game URL) | ✅ |
| WS 재연결 로직 (최대 3회, 1.5초 간격) | ✅ |

### 오늘(4/18) QA에서 추가 수정한 버그 3건
| 버그 | 원인 | 수정 |
|---|---|---|
| 블록 버튼 5·6 잘림 | flex 컨테이너 오버플로 | `flex-wrap` + `flex-shrink-0` |
| 힌트 메시지 말풍선 중복 | AI 응답 텍스트에 💡 줄 포함 | `.replace(/\n*💡[^\n]*$/m, "")` |
| 세션 전환 시 힌트 잔류 | `setHint("")` 누락 | 세션 전환 useEffect에 추가 |

### 아키텍처 요약 (최신, 2026-04-18)

```
아이 브라우저
  └─ Next.js (localhost:3000)
       ├─ /login — 로그인 페이지 (root/0000, 환경변수 기반)
       ├─ SessionSidebar — 세션 목록·생성·삭제 (name 표시, × 버튼 삭제)
       ├─ ChatPane — WebSocket → /ws/chat/{child_id}?session_id={session_id}
       │    ├─ WS 재연결 배너 (황색/적색)
       │    ├─ 블록 버튼 (SCAFFOLD_DATA, 스킬 이름 + flex-wrap)
       │    ├─ 대기 피드백 타이머 (15s/40s)
       │    └─ 힌트 버튼 (💡 줄 말풍선 중복 제거)
       └─ GamePreview — <iframe srcDoc={gameHtml}> (네트워크 독립)
                        폴백: <iframe src="/games/..."> (세션 복원 시)

FastAPI (localhost:8000)
  ├─ GET/POST/DELETE /sessions/{child_id}
  ├─ PATCH /sessions/{child_id}/{session_id}/name
  ├─ GET /sessions/{child_id}/{session_id}/messages
  ├─ GET /games/{child_id}/{session_id}/{game_id}
  └─ WS /ws/chat/{child_id}?session_id={session_id}
       └─ game 이벤트: game_url + game_html 동시 전송

데이터 레이어 (SQLite)
  ├─ data/kids_edu.db — sessions, messages, games 테이블 + FTS5
  └─ data/games/{child_id}/{session_id}/*.html — 게임 파일
```

### 핵심 파일 경로 (2026-04-18 기준)
- `src/backend/storage.py` — SQLite 래퍼 (init_db, CRUD)
- `src/backend/main.py` — WebSocket 핸들러, game_html 직렬화
- `src/backend/claude_runner.py` — _friendly_error 헬퍼, game html 추가, HTML 크기 로그
- `src/backend/personas/TUTOR.md` — 게임 생성 규칙
- `src/frontend/hooks/useChat.ts` — gameHtml·wsStatus·onopen, setHint 세션 리셋
- `src/frontend/components/ChatPane.tsx` — 블록 UI·flex-wrap·대기 피드백·배너·힌트 중복 제거
- `src/frontend/components/GamePreview.tsx` — srcDoc 전환
- `src/frontend/app/page.tsx` — gameHtml 상태 전파

### 남은 상품 요구사항 갭 (4/26 리허설 목표)
| 우선순위 | 항목 | 내용 |
|---|---|---|
| P0 | R4 폴백 | Claude 실패 시 기본 게임 자동 삽입 |
| P0 | R9 밝은 UI | 다크 테마 → 밝은 테마, 큰 글씨, 촬영 친화적 |
| P1 | R8 결과물 공유 | 게임 URL QR 공유 |
| P2 | R7 갤러리 | 퍼실리테이터용 전체 작품 뷰 |

### ADR
- [[auth-session-game-persistence]] — status: implemented (2026-04-13)
- [[track-a-primary-b-backup]] — Track A 주력 (스택 확정은 4/21)
- [[stack-decision-after-curriculum]] — 커리큘럼이 스택을 결정
- [[game-content-guideline-pending]] — 소아암 환아 게임 콘텐츠 제약 조건 코드 반영 **보류** (국립암센터 의료진 확인 후 진행, 담당: 봉호→진용)

### 보안 결정 & 주의사항
- 경로 순회 방어: `path.resolve().is_relative_to(base)` 검증
- 자격증명: `.env.local` 환경변수. 하드코딩 금지
- WebSocket: `accept()` 는 인증 검증 이전에 호출
- iframe sandbox: `"allow-scripts"` 유지. `allow-same-origin` 추가 금지 (srcDoc도 동일 opaque origin 적용)
- Claude subprocess: `cwd=tempfile.gettempdir()` + `--add-dir` 로 프로젝트 컨텍스트 격리
