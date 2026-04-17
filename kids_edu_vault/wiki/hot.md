---
type: meta
title: "Hot Cache"
created: 2026-04-12
updated: 2026-04-17
tags:
  - meta/cache
---

# Hot Cache — 2026-04-17

최근 컨텍스트 스냅샷. 세션 시작 시 가장 먼저 읽을 것.

---

## 현재 상태: 4/19 마감 D-2 — BH 커리큘럼 + Ryan 와우 포인트 대기 중

### 프로젝트 개요
- 목표: 소아암 병동 어린이(8-12세) AI 크리에이터 워크샵 파일럿 (2026-05-05, 국립암센터 강당)
- 스택: FastAPI (Python/uv) + Next.js 16 (App Router) + Claude CLI subprocess
- 래퍼: 채팅(WebSocket) + iframe 게임 프리뷰 + 블록별 프롬프트 스캐폴드

### 긴급 마일스톤 (현재 ~ 4/26)

| 날짜 | 마일스톤 | 담당 | 상태 |
|---|---|---|---|
| 2026-04-19 | 커리큘럼 초안 (2시간 타임테이블 + 조 편성) | BH | **대기 중** |
| 2026-04-19 | 와우 포인트 설계 + 반응 측정 설계 | Ryan | **대기 중** |
| 2026-04-21 | 커리큘럼 리뷰 → Track A 스택 최종 결정 | Jay + JY | Pending |
| 2026-04-26 | Track A 래퍼 리허설 가능 상태 | JY | Pending |
| 2026-04-26 | 갤러리 페이지 + 랜딩 페이지 | JeHyeong | Pending |

### Jay에게 공유 필요한 내용 (JY 담당, 4/17)
1. **BH 커리큘럼 초안 4/19 수령 확인** — 스택 확정 인풋. Jay가 독촉 필요.
2. **랩탑/태블릿 40대 확보 방향 결정** — 4/21 미팅 전 Jay 액션.
3. **자원봉사자 퍼실리테이터 섭외 여부** — 팀원만으로 8–10조 커버 불가.
4. Track A 개발 진행 중. 4/26 리허설 목표 유지.

### 완료된 개발 작업 (최신순, 2026-04-17 기준)
| 기능 | 상태 |
|---|---|
| SQLite 마이그레이션 (storage.py) + 게임 파일시스템 저장 | ✅ |
| 세션 이름 자동 할당 ("대화 N" → 첫 메시지 앞 15자) | ✅ |
| 세션 전환 버그 3종 수정 (히스토리 유실·스피너·stale game URL) | ✅ |
| WS 재연결 로직 (최대 3회, 1.5초 간격) | ✅ |
| 말풍선 원본 프롬프트 표시 (주입 전 저장) | ✅ |
| 게임 수정 vs 신규 분기 (Read 도구 활용) | ✅ |
| TUTOR.md 게임 코딩 규칙 추가 (roundRect 금지, 고정 캔버스) | ✅ |
| Claude subprocess cwd 격리 (프로젝트 컨텍스트 차단) | ✅ |
| 채팅 히스토리 저장/복원 | ✅ |
| Windows CP949 UTF-8 버그 수정 | ✅ |
| 재로그인 시 게임 복원 + 로딩 UI | ✅ |
| 로그인 + 세션 관리 + 게임 HTML 저장 | ✅ |

### 아키텍처 요약 (최신)

```
아이 브라우저
  └─ Next.js (localhost:3000)
       ├─ /login — 로그인 페이지 (root/0000, 환경변수 기반)
       ├─ SessionSidebar — 세션 목록·생성·삭제 (name 표시, × 버튼 삭제)
       ├─ ChatPane — WebSocket → /ws/chat/{child_id}?session_id={session_id}
       └─ GamePreview — <iframe src="/games/{child_id}/{session_id}/{game_id}">

FastAPI (localhost:8000)
  ├─ GET/POST/DELETE /sessions/{child_id}
  ├─ PATCH /sessions/{child_id}/{session_id}/name
  ├─ GET /sessions/{child_id}/{session_id}/messages
  ├─ GET /games/{child_id}/{session_id}/{game_id}
  └─ WS /ws/chat/{child_id}?session_id={session_id}

데이터 레이어 (SQLite)
  ├─ data/kids_edu.db — sessions, messages, games 테이블 + FTS5
  └─ data/games/{child_id}/{session_id}/*.html — 게임 파일 (세션당 최대 10개)
```

### 핵심 파일 경로
- `src/backend/storage.py` — SQLite 래퍼 (init_db, CRUD)
- `src/backend/main.py` — WebSocket 핸들러, 세션 API, JSON→SQLite 마이그레이션
- `src/backend/claude_runner.py` — Claude CLI subprocess, 게임 HTML 저장
- `src/backend/personas/TUTOR.md` — 게임 생성 규칙 (Canvas 고정 크기, roundRect 금지)
- `src/frontend/hooks/useChat.ts` — sessionId 변경 시 리셋, WS 자동 재연결
- `src/frontend/app/page.tsx` — sessionRefreshToken, activeSessionId 변경 시 game URL fetch

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

### 보안 결정 & 주의사항
- 경로 순회 방어: `path.resolve().is_relative_to(base)` 검증
- 자격증명: `.env.local` 환경변수. 하드코딩 금지
- WebSocket: `accept()` 는 인증 검증 이전에 호출
- iframe sandbox: `"allow-scripts"` 유지. `allow-same-origin` 추가 금지
- Claude subprocess: `cwd=tempfile.gettempdir()` + `--add-dir` 로 프로젝트 컨텍스트 격리
