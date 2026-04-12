---
type: intel
title: "Intel: Chat+Preview 래퍼 아키텍처 리서치"
created: 2026-04-12
updated: 2026-04-12
status: developing
confidence: high
tags:
  - intel
  - technical-reference
  - architecture
  - llm
related:
  - "[[pivot-to-chat-preview-wrapper]]"
  - "[[iframe-sandbox-over-webcontainers]]"
  - "[[pilot-env-design]]"
  - "[[gemini-2-5-flash]]"
sources:
  - "https://platform.claude.com/docs/en/agent-sdk/overview"
  - "https://github.com/abagames/claude-one-button-game-creation"
  - "https://github.com/stackblitz/bolt.new"
  - "https://webcontainers.io/enterprise"
  - "https://sandpack.codesandbox.io/docs/resources/faq"
  - "https://developer.mozilla.org/en-US/docs/Web/HTML/Reference/Elements/iframe"
---

# Intel: Chat+Preview 래퍼 아키텍처 리서치

## Overview

code-server + cline 포크 대신 **채팅 좌 / 라이브 게임 프리뷰 우** 두 pane으로 구성된 커스텀 웹앱을 구축하는 방향에 대한 기술 스택 리서치 (2026-04-12). 대상: 8–12세 소아암 병동 어린이, 2026-05-05 파일럿.

## Agent 레이어: Claude Agent SDK vs 기타

- **Claude Agent SDK** (2025-09-29 Claude Code SDK → Claude Agent SDK로 개명)는 `Read`/`Write`/`Edit`/`MultiEdit` 내장 툴, 스트리밍 오케스트레이션, 권한 모드(`acceptEdits`), 컨텍스트·재시도 관리를 기본 제공.
- **핵심 이점**: `Edit`/`MultiEdit`의 타깃형 패치 → 전체 재생성 없이 프리뷰 프레임이 안정적으로 유지됨. 아이가 "고양이를 더 빨리 움직이게 해줘"라고 말할 때 전체 코드 리젠이 아니라 관련 라인만 수정.
- **Raw API 대안**: tool-use 스캐폴드·edit-diff 로직·스트리밍 상태기계를 직접 구현 → 3주 일정에서 1–2주 plumbing 소비.
- **모델 선택 caveat**: Agent SDK = Anthropic/Claude 전용. 기존 [[gemini-2-5-flash]] 결정과 **비용·정책 재검토 필요**. 대안은 (a) Claude로 스위치, (b) Gemini Function Calling + 자체 Edit 루프 구현.

### 레퍼런스 구현
- [abagames/claude-one-button-game-creation](https://github.com/abagames/claude-one-button-game-creation) — LLM이 `crisp-game-lib` 기반 브라우저 미니게임을 생성. 타깃과 가장 가까움.
- [stackblitz/bolt.new](https://github.com/stackblitz/bolt.new) — MIT 오픈소스. Remix + WebContainers. 제품 수준 래퍼 구조 참고.

## 브라우저 샌드박스 (라이브 프리뷰)

| 옵션 | 셋업 | 라이선스 | 격리 | 오프라인 | 크기 |
|---|---|---|---|---|---|
| **iframe + `srcdoc`** | 최저 (네이티브) | 무료 | 강함 (`sandbox="allow-scripts"` + `allow-same-origin` 제외 시) | 예 | ~0 KB |
| **Sandpack** | 중간 (React 컴포넌트) | Apache-2.0 | 강함 (cross-subdomain iframe) | 부분 (자체 호스팅 필요 시) | ~200 KB+ |
| **WebContainers** | 최고 (브라우저 내 Node) | **상용 라이선스 필요 (유료)** | 매우 강함 (브라우저 내 OS) | 부팅 후 예 | 수 MB |

### 권고: iframe + srcdoc
- p5.js/HTML5 canvas는 `<script>` 태그 하나면 충분. Node·npm·번들러 불필요.
- 무료·오프라인·초경량·보안 단단.
- **보안 주의**: `sandbox="allow-scripts"`만 사용. `allow-same-origin` 또는 `allow-popups-to-escape-sandbox` 병용 금지 (escape 취약점).

### WebContainers 트랩
- bolt.new를 흉내 내고 싶다는 유혹 주의. WebContainers는 StackBlitz의 상용 제품 — 영리 용도는 **별도 상용 라이선스 계약 필수** (가격 비공개, sales 문의). 교육·파일럿이라도 유료화 로드맵이 있으면 라이선스 비용 사전 확인.

## 프레임워크

- **Next.js App Router** 권고. 스트리밍(Server Actions / Route Handlers + `ReadableStream`), Auth.js/Clerk, Stripe 연동, Vercel AI Gateway 모두 일급 지원. Vercel 배포 몇 분.
- **동종 제품 스택**:
  - v0 (Vercel): Next.js + Tailwind + shadcn/ui.
  - Lovable: Vite + React + Supabase (생성물).
  - bolt.new: Remix + WebContainers.
- **Vite + React**: dev가 가볍고 빠르지만, 어차피 OAuth·결제가 예정되어 있다면 Next.js가 total 비용에서 유리.

## 코드 숨김 UX 선례

- **Scratch (MIT)**: 코드 view 없음. 블록 = 기본. 교훈: 추상화에 완전히 투신, 코드 엿보기 제공 금지.
- **Code.org App Lab**: Block Mode / Text Mode 토글. 같은 프로그램 두 뷰. 교훈: 한 개의 스위치로 점진적 공개(progressive disclosure) — 검증된 패턴.
- **p5.js Web Editor**: 코드 한 pane + 프리뷰. "코드 숨김" 네이티브 지원 없음 → 어린 아이용 모델로 부적합.

### 파일럿 적용
- 대상 연령 혼합(8–12세), 체력 저하, 짧은 집중 → **App Lab 방식** 채택: 기본 코드 숨김 + 작은 "Show Code" 토글. 에러는 절대 stack trace 노출 금지 → AI가 "같이 고쳐보자" 같은 채팅 메시지로 번역.
- 참고: [[single-html-runtime]], [[no-debug-philosophy]] 교수법과 일관.

## Sources (검증 필요)
- Anthropic: [Claude Agent SDK Overview](https://platform.claude.com/docs/en/agent-sdk/overview)
- [abagames/claude-one-button-game-creation](https://github.com/abagames/claude-one-button-game-creation)
- StackBlitz: [WebContainers Enterprise](https://webcontainers.io/enterprise)
- CodeSandbox: [Sandpack FAQ](https://sandpack.codesandbox.io/docs/resources/faq)
- MDN: [iframe sandbox](https://developer.mozilla.org/en-US/docs/Web/HTML/Reference/Elements/iframe)
- [Bolt supported technologies](https://support.bolt.new/building/supported-technologies)
- [Lovable vs v0](https://lovable.dev/guides/lovable-vs-v0)
- [Code.org App Lab](https://code.org/en-US/tools/app-lab)

## Open Questions
- [ ] WebContainers 상용 라이선스 실제 가격 (StackBlitz sales에 견적 문의해도 될지)
- [ ] Claude Agent SDK 전환 시 1회 세션 비용 (기존 [[gemini-2-5-flash]] 기준 $0.15 목표 달성 여부)
- [ ] iframe sandbox 내부에서 외부 asset(이미지·사운드) 로딩 정책 — 우리 CDN만 허용할 방법
- [ ] 3주 MVP에서 "Show Code" 토글 포함 범위
