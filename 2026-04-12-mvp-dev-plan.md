# HypeProof Kids Edu — MVP 개발 계획

작성일: 2026-04-12
작성자: JY + Claude
파일럿까지: **23일** (2026-05-05)

> JY가 개발 중 참고하는 단일 지도. 결정의 근거는 볼트 ADR·intel에 있고, 이 문서는 **실행 목록**이다. 결정이 바뀌면 이 문서도 갱신한다.

---

## 1. 무엇을 만드나

**Chat + Preview 래퍼** — 아이가 AI와 대화하면 AI가 HTML/JS 게임을 생성해 우측 iframe에서 즉시 실행되는 웹앱.

- 좌측: 채팅 pane (스트리밍 응답).
- 우측: 라이브 프리뷰 iframe (`srcdoc` + `sandbox="allow-scripts"`).
- **아이에게 코드는 절대 노출되지 않는다.** (no-debug-philosophy)

근거: [[pivot-to-chat-preview-wrapper]], [[intel-wrapper-architecture]], [[intel-competitive-landscape-2026]].

---

## 2. 기술 스택 (확정)

| 레이어 | 선택 | 근거 ADR / Intel |
|---|---|---|
| Frontend | **Next.js App Router** (TypeScript) | [[intel-wrapper-architecture]] |
| Agent | **Claude Agent SDK** (`Edit`/`MultiEdit` 툴) | [[pivot-to-chat-preview-wrapper]] |
| Sandbox | **iframe + `srcdoc` + `sandbox="allow-scripts"`** | [[iframe-sandbox-over-webcontainers]] |
| Auth (A-Lite) | **Clerk** 기본 통합, 운영자가 배치로 40개 계정 생성 | [[parent-gated-signup-first]] |
| Billing | **미포함** (파일럿 이후 Stripe + 포트원) | [[intel-auth-billing-compliance]] |
| Python (있을 경우) | `uv` 전용 | `.claude/rules/uv.md` |

### 금지
- WebContainers (상용 라이선스 트랩).
- `sandbox="allow-same-origin"` · `allow-popups-to-escape-sandbox`.
- 아이 Google OAuth (PIPA 만 14세 미만 트랩).
- API key 코드/커밋 인라인.

---

## 3. 단계 전략: C → A-Lite

- **C 단계 (착수 ~ 리허설)**: 래퍼 MVP + 운영자 하드코드 계정 1개. 가입·결제 0.
- **A-Lite (리허설 gate 통과 ~ 파일럿 당일)**: Clerk로 운영자가 40개 계정 배치 생성. 아이는 배정 계정으로 로그인. **부모 가입 미포함** (리허설 전 부모 참여 불확실).
- **파일럿 이후**: 부모 이메일 플로우·유료화·다회차 기능 (A-Full).

근거: [[pivot-to-chat-preview-wrapper]] 및 JY 내부 결정(2026-04-12).

---

## 4. 디렉토리 구조

```
hypeproof_kids_edu/
├── src/                       # 앱 코드 (이 MVP)
│   ├── frontend/              # Next.js App Router 앱
│   └── backend/               # API routes / Agent SDK 서버 로직 (필요 시 분리)
├── kids_edu_vault/            # Obsidian 볼트 (지식 자산, 손대지 않음)
├── meeting_notes/             # 기존 미팅 노트 (레거시)
├── .claude/                   # agents / skills / rules
├── CLAUDE.md                  # 프로젝트 전반 규약
└── 2026-04-12-mvp-dev-plan.md # 이 파일
```

> 볼트 파일(`kids_edu_vault/`)은 앱 코드에서 참조하지 않음. `src/`는 완전 독립.

---

## 5. 환경변수 (`.env.local` / `.env.example`)

| 키 | 용도 | 단계 |
|---|---|---|
| `ANTHROPIC_API_KEY` | Claude Agent SDK 인증 | C부터 |
| `NEXT_PUBLIC_MOCK_AGENT` | `1`이면 SDK 대신 하드코딩 응답 (dev 전용) | C부터 |
| `CLERK_SECRET_KEY` | Clerk 서버 | A-Lite부터 |
| `NEXT_PUBLIC_CLERK_PUBLISHABLE_KEY` | Clerk 클라이언트 | A-Lite부터 |

- `.env.local`은 gitignored. `.env.example`에는 키 이름만 placeholder.
- **시크릿 인라인 금지.** reviewer가 커밋 전 `rg -i "sk-|api[_-]?key"` 스윕.

---

## 6. 비용 전략

### 모델
- 내부 dev·테스트: **Haiku 4.5** + prompt caching. 예상 총비용 $3~5.
- 리허설·파일럿: **Sonnet** 고려 (품질 필요 시). 파일럿 $0.15/세션 × 40명 = $6.
- Gemini 2.5 Flash(기존 OKR 전제)는 후순위 A/B 옵션.

### Mock 모드
- UI·스트리밍·iframe·레이아웃 반복 = `NEXT_PUBLIC_MOCK_AGENT=1` → **API 호출 0**.
- 실제 API는 "AI가 만드는 게임 품질" 검증할 때만.

---

## 7. 3주 개발 로드맵

### Week 1 (2026-04-13 ~ 04-19): 래퍼 MVP 스캐폴드
- [ ] **@architect** — `wrapper-mvp-scaffold` ADR (프로젝트 구조, 두 pane 레이아웃, Agent SDK 통합 패턴, mock 모드 스위치)
- [ ] **@implementer** — `src/frontend/` 스캐폴드, 채팅 스트리밍, iframe 프리뷰, mock 모드 구현
- [ ] **@tester** — iframe sandbox escape Playwright 테스트 + SDK mock 테스트
- [ ] **@reviewer** — 1차 PR 전 보안·sandbox·시크릿 스윕
- [ ] JY — 실제 API key로 1~2회 end-to-end 확인

### Week 2 (2026-04-20 ~ 04-26): A-Lite 통합 + 리허설 준비
- [ ] **@architect** — Clerk A-Lite 통합 ADR (배치 계정 생성 플로우)
- [ ] **@implementer** — Clerk 미들웨어·로그인 UI·배치 계정 스크립트
- [ ] **@tester** — 인증 흐름 e2e
- [ ] [[pilot-rehearsal-late-april]] — C→A 전환 gate 검증

### Week 3 (2026-04-27 ~ 05-04): 안정화 + 리허설 반영
- [ ] 리허설 피드백 반영, 블로커 해소
- [ ] [[pilot-day-operation]] runbook 확정
- [ ] 튜터 오리엔테이션 자료
- [ ] 파일럿 당일 백업 시나리오 (API 장애·네트워크 장애·개별 기기 장애)

---

## 8. 개발 워크플로우 (Subagent 파이프라인)

```
기능 요청
  ↓
@architect → kids_edu_vault/wiki/decisions/<slug>.md (proposed)
  ↓ (ADR 경로 전달)
@implementer → src/ 코드 + .env.example
  ↓ (변경 파일 경로 전달)
@tester → 테스트 파일
  ↓ (변경 파일 경로 전달)
@reviewer → 리뷰 리포트
  ↓
JY → git commit (로컬)
  ↓
@wiki-ingest or save → 볼트 반영, hot.md 갱신
```

세부 위임 규칙: `.claude/CLAUDE.md`. 팀 개요: 루트 `CLAUDE.md` "팀 & 워크플로우" 섹션. ADR: [[subagent-team-structure]].

---

## 9. 이번 세션 Open Questions

파일럿 전에 결정되어야 하는 것들.

- [ ] **리허설 날짜 확정** ([[pilot-rehearsal-late-april]]) — C→A 전환 gate.
- [ ] **ANC 컷오프** (의료진) — [[case-pediatric-onc-infection-control]].
- [ ] **강당 HVAC 사양** — HEPA 이동식 필요 여부.
- [ ] **Jay 브리핑 회신** — `2026-04-12-pivot-briefing-jay.md`. 방향 뒤집히면 이 문서 전면 수정.
- [ ] **모델 A/B 재평가** — Haiku vs Sonnet 실전 품질 확인 후 확정.
- [ ] **게임 장르·서사** 재조정 ([[combat-vs-cooperative-framing]]).

---

## 10. Scope 경계 (이번 MVP에 포함 안 됨)

- 부모 대시보드 / 학습 이력 조회.
- 다회차 세션 / 진도 저장.
- 결제·구독 (포트원·Stripe).
- 튜터 전용 UI (관찰·개입 도구).
- 다국어 (한국어만).
- 모바일 최적화 (랩탑·데스크탑 강당 기기 기준).
- 게임 저장·공유 (세션 끝나면 휘발).

**"이번 MVP는 파일럿 당일 2시간이 전부다"**를 결정의 기준으로 삼는다.

---

## 관련 문서

- 볼트 ADR: [[pivot-to-chat-preview-wrapper]] · [[iframe-sandbox-over-webcontainers]] · [[parent-gated-signup-first]] · [[subagent-team-structure]]
- 볼트 Intel: [[intel-wrapper-architecture]] · [[intel-auth-billing-compliance]] · [[intel-competitive-landscape-2026]]
- 볼트 Runbook (stub): [[pilot-day-operation]]
- Jay 브리핑: `2026-04-12-pivot-briefing-jay.md`
- 팀 규약: `.claude/CLAUDE.md`, 루트 `CLAUDE.md`
