# HypeProof Kids Edu — MVP 개발 계획

작성일: 2026-04-12
작성자: JY + Claude
파일럿까지: **23일** (2026-05-05)

> JY가 개발 중 참고하는 단일 지도. 결정의 근거는 볼트 ADR·intel에 있고, 이 문서는 **실행 목록**이다. 결정이 바뀌면 이 문서도 갱신한다.

---

## 1. 무엇을 만드나

**Chat + Preview 래퍼** — 아이가 AI와 대화하면 AI가 HTML/JS 게임을 생성해 우측 iframe에서 즉시 실행되는 웹앱.

- 좌측: 채팅 pane (스트리밍 응답 + 블록별 프롬프트 스캐폴딩 카드).
- 우측: 라이브 프리뷰 iframe (`srcdoc` + `sandbox="allow-scripts"`).
- **아이에게 코드는 절대 노출되지 않는다.** (no-debug-philosophy)

**교육 목표 (2개 동시)**
1. AI와 함께 게임을 만드는 창작 경험.
2. **AI에게 잘 시키는 법 체득** — 구체화·추가·수정 등 프롬프팅 패턴을 블록별로 습득.

근거: [[pivot-to-chat-preview-wrapper]], [[ai-prompting-literacy-input]], [[intel-wrapper-architecture]].

---

## 2. 기술 스택 (확정)

| 레이어 | 선택 | 근거 |
|---|---|---|
| Frontend | **Next.js App Router** (TypeScript) | [[intel-wrapper-architecture]] |
| Backend | **FastAPI** (Python) — `sanshome_bot/claude_runner.py` 기반 | [[nextjs-fastapi-wrapper-architecture]] |
| Claude 연동 | **`claude -p --output-format stream-json`** (CLI subprocess) | 검증된 코드 재활용, 빠른 구현 |
| 허용 툴 | `Read, Write, Glob` (Bash 제거) | 아동 환경 보안 |
| Sandbox | **`iframe + srcdoc + sandbox="allow-scripts"`** | [[iframe-sandbox-over-webcontainers]] |
| Auth (A-Lite) | **Clerk** — 운영자가 배치로 40개 계정 생성 | [[parent-gated-signup-first]] |
| Billing | **미포함** (파일럿 이후 Stripe + 포트원) | — |
| Python 의존성 | `uv` 전용 | `.claude/rules/uv.md` |

### 금지
- WebContainers (상용 라이선스).
- `sandbox="allow-same-origin"` · `allow-popups-to-escape-sandbox`.
- 아이 Google OAuth (PIPA 만 14세 미만).
- API key 코드/커밋 인라인.
- Claude에게 Bash 툴 허용 (아동 환경).

---

## 3. 아키텍처

```
[ Next.js 프론트 ]  ←——WebSocket——→  [ FastAPI 백엔드 ]
  채팅 pane                                ↓
  게임 preview iframe          claude -p --output-format stream-json
  프롬프트 스캐폴딩 카드          --allowedTools Read,Write,Glob
  "잘 됐던 말들" 히스토리           --resume [child_session_id]
                                  --append-system-prompt [TUTOR.md]
```

### 레이아웃

```
┌─────────────────┬──────────────────────┐
│   채팅 pane     │   게임 preview       │
│                 │                      │
│ [메시지 목록]   │  <iframe srcdoc=...  │
│                 │   sandbox="allow-    │
│ [프롬프트 카드] │   scripts">          │
│ [히스토리]      │                      │
│ [입력창] [▶]   │                      │
└─────────────────┴──────────────────────┘
```

---

## 4. AI 프롬프팅 스킬 커리큘럼 레이어

커리큘럼 블록별로 하나씩 프롬프팅 패턴을 가르친다.

| 블록 | 활동 | 프롬프팅 스킬 | UI 지원 |
|---|---|---|---|
| Block 0 | 캐릭터 고르기 | **묘사하기** | 스캐폴딩 카드: "어떤 캐릭터야?" |
| Block 1 | 움직이기 | **구체화** | 카드: "어떤 키로? 얼마나 빨리?" |
| Block 2 | 친구 찾기 | **추가 요청** | 카드: "거기다 ~도 추가해줘" |
| Block 3 | 아이템 모으기 | **수정 요청** | 카드: "~를 ~로 바꿔줘" |
| Block 4 | 나만의 마법 | **자유 조합** | 카드 없음 — 스스로 입력 |
| Block 5 | 보여주기 | **언어화** | "어떻게 말했어?" 회고 |

Claude 시스템 프롬프트(`TUTOR.md`) 규칙:
- 즉시 완성품 반환 (설명 전에 게임 먼저).
- 코드 노출 금지 — HTML만 반환.
- 전투/체력 소거 → 협력형 서사 (꽃 피우기, 별 모으기, 길 만들기).
- 응답 끝에 "💡 다음엔 ~라고 해봐!" 1줄.

---

## 5. 디렉토리 구조

```
hypeproof_kids_edu/
├── wrapper/                   # Next.js 프론트엔드
│   ├── app/
│   │   ├── page.tsx           # 메인 레이아웃 (채팅 | 게임)
│   │   └── api/chat/route.ts  # FastAPI WebSocket 프록시
│   ├── components/
│   │   ├── ChatPane.tsx
│   │   ├── GamePreview.tsx
│   │   └── PromptScaffold.tsx
│   └── package.json
├── backend/                   # FastAPI 백엔드
│   ├── main.py                # WebSocket endpoint
│   ├── claude_runner.py       # sanshome_bot 기반
│   ├── sessions.json          # child_id → claude_session_id
│   ├── personas/
│   │   └── TUTOR.md           # W3+W4 합성 교육용 페르소나
│   └── pyproject.toml         # uv 의존성
├── kids_edu_vault/            # Obsidian 볼트 (손대지 않음)
└── 2026-04-12-mvp-dev-plan.md # 이 파일
```

---

## 6. 환경변수

| 키 | 용도 | 단계 |
|---|---|---|
| `ANTHROPIC_API_KEY` | (미사용, CLI subprocess 방식) | — |
| `MOCK_CLAUDE` | `1`이면 하드코딩 응답 (dev 전용) | C부터 |
| `CLERK_SECRET_KEY` | Clerk 서버 | A-Lite부터 |
| `NEXT_PUBLIC_CLERK_PUBLISHABLE_KEY` | Clerk 클라이언트 | A-Lite부터 |

- `.env.local`은 gitignored. `.env.example`에는 키 이름만 placeholder.

---

## 7. 비용 전략

- dev·테스트: `MOCK_CLAUDE=1` → API 호출 0.
- 실제 Claude 호출: 게임 품질 검증 시에만.
- 파일럿: Sonnet, $0.15/세션 × 40명 = $6 목표.

---

## 8. 3주 개발 로드맵

### Phase 1 (4/12 ~ 4/19): 커리큘럼 인풋 + 사전 스캐폴딩

- [x] AI 프롬프팅 스킬 spec 작성 → BH에게 전달 ([[ai-prompting-literacy-input]])
- [x] 아키텍처 ADR 작성 ([[nextjs-fastapi-wrapper-architecture]])
- [ ] `wrapper/` Next.js 프로젝트 초기화 (레이아웃·컴포넌트 스캐폴드)
- [ ] `backend/` FastAPI 초기화 + `claude_runner.py` 포팅
- [ ] `backend/personas/TUTOR.md` 작성

### Phase 2 (4/21 ~ 4/26): 핵심 구현 (스택 확정 후, 5일 스프린트)

- [ ] **Day 1 (4/21)**: Claude 스트리밍 연동 (FastAPI WebSocket → Next.js)
- [ ] **Day 2 (4/22)**: iframe 게임 실행 (HTML 추출 + srcdoc 주입)
- [ ] **Day 3 (4/23)**: 세션 관리 (`child_id` → `claude_session_id`)
- [ ] **Day 4 (4/24)**: 프롬프트 스캐폴딩 UI + 히스토리 패널
- [ ] **Day 5 (4/25)**: 통합 테스트 (5탭 동시, 모바일 레이아웃)
- [ ] 4/26 리허설 가능 상태 JY 마감

### Phase 3 (4/27 ~ 5/4): 안정화

- [ ] 리허설 피드백 반영
- [ ] [[pilot-day-operation]] runbook 확정
- [ ] 튜터 오리엔테이션 자료
- [ ] 파일럿 당일 백업 시나리오

---

## 9. Subagent 파이프라인

```
기능 요청
  ↓ @architect → kids_edu_vault/wiki/decisions/<slug>.md
  ↓ @implementer → wrapper/ 또는 backend/ 코드
  ↓ @tester → 테스트 파일
  ↓ @reviewer → 리뷰 리포트
  ↓ JY → git commit
  ↓ @wiki-ingest → 볼트 반영, hot.md 갱신
```

---

## 10. Open Questions

- [ ] **리허설 날짜 확정** ([[pilot-rehearsal-late-april]]) — C→A gate.
- [ ] **ANC 컷오프** (의료진 합의, 4/20 전).
- [ ] **강당 HVAC 사양** — HEPA 이동식 필요 여부.
- [ ] **Jay 브리핑 회신** — `2026-04-12-pivot-briefing-jay.md`.
- [ ] **랩탑/태블릿 40대 확보** (4/26까지).

---

## 11. Scope 경계 (MVP 미포함)

- 부모 대시보드 / 학습 이력.
- 다회차 세션 / 진도 저장.
- 결제·구독.
- 튜터 전용 UI.
- 다국어.
- 게임 저장·공유 (세션 끝나면 휘발).

**"이번 MVP는 파일럿 당일 2시간이 전부다."**

---

## 관련 문서

- 볼트 ADR: [[pivot-to-chat-preview-wrapper]] · [[iframe-sandbox-over-webcontainers]] · [[nextjs-fastapi-wrapper-architecture]] · [[parent-gated-signup-first]]
- 볼트 Spec: [[ai-prompting-literacy-input]] · [[pilot-curriculum-adapted]]
- 볼트 Intel: [[intel-wrapper-architecture]] · [[intel-competitive-landscape-2026]]
- 볼트 Concept: [[ai-persona-workflows]] · [[fast-implementation-mode]]
- Jay 브리핑: `2026-04-12-pivot-briefing-jay.md`
