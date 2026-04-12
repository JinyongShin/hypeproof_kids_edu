---
type: decision
status: proposed
priority: 2
date: 2026-04-12
owner: "[[jinyong-shin]]"
context: "래퍼 라이브 프리뷰의 실행 샌드박스 기술 선택"
tags:
  - decision
  - pilot
  - architecture
  - security
related:
  - "[[pivot-to-chat-preview-wrapper]]"
  - "[[intel-wrapper-architecture]]"
  - "[[single-html-runtime]]"
---

# Sandbox: iframe + srcdoc (WebContainers 기각)

## 결정
- 라이브 게임 프리뷰 샌드박스는 **iframe + `srcdoc` + `sandbox="allow-scripts"`** 를 사용.
- `allow-same-origin`, `allow-popups-to-escape-sandbox`는 **절대 사용 금지** (escape 취약점).
- StackBlitz **WebContainers는 기각**.

## 근거

### iframe + srcdoc의 장점
- **무료·오프라인·초경량** (~0 KB 추가, 네이티브 HTML).
- p5.js / HTML5 canvas / 단일 HTML 게임은 `<script>` 태그 하나면 충분 — Node·npm·번들러 불필요.
- 브라우저 네이티브 보안 모델 + 적절한 sandbox 속성으로 강한 격리.
- [[single-html-runtime]] 철학과 자연스럽게 정합.

### WebContainers 기각 이유
- **상용 라이선스 필수** — StackBlitz 자체 상용 제품. 영리 목적 서드파티는 유료 계약 필요 (가격 비공개).
- 유료화 로드맵이 있는 우리에게 **장기 비용 노출**.
- p5/canvas만 돌리면 되는데 브라우저 내 Node 전체가 overkill.
- bolt.new가 쓴다고 따라가면 안 됨 — 아키텍처 우상숭배.

### Sandpack 부분 검토
- Apache-2.0으로 라이선스는 클린.
- React 컴포넌트 200KB+ 오버헤드. 번들러 기능이 필요 없는 우리에겐 과함.
- Sandpack은 향후 "코드 에디터 + 실행 환경" 공식 뷰가 필요해질 때 재검토 후보.

## 보안 운용 규칙
- iframe sandbox 속성은 **`sandbox="allow-scripts"`만**.
- 아이 생성 코드가 외부 네트워크에 접근해야 할 때: 우리 도메인 CDN에서만 asset 로딩하도록 CSP로 차단.
- parent document는 iframe과 **항상 cross-origin** 유지 (같은 origin에서 제공해도 `sandbox`가 `allow-same-origin` 없이 동작하므로 자동으로 null origin).

## 대안 및 기각 이유

| 대안 | 라이선스 | 세트업 | 기각 이유 |
|---|---|---|---|
| WebContainers | **상용 유료** | 고 | 라이선스 비용·오버헤드 |
| Sandpack | Apache-2.0 | 중 | 번들러 불필요, 200KB 오버헤드 |
| Service Worker 샌드박스 | 무료 | 고 | 구현 복잡도, 네트워크 가로채기 이슈 |
| Web Worker | 무료 | 중 | DOM 없음 → canvas 게임 프리뷰 불가능 |

## 영향 범위
- [[pivot-to-chat-preview-wrapper]] 래퍼 프리뷰 pane 구현.
- [[pilot-game-starter-template]] — 단일 HTML 임베드 포맷으로 준비.
- CSP(Content Security Policy) 정책 문서 필요.

## Open Questions
- [ ] iframe 내부에서 외부 이미지·사운드 asset 로딩 정책 (화이트리스트 CDN)
- [ ] 파일·이미지 업로드 기능 도입 시 postMessage 프로토콜 설계
- [ ] 오프라인 PWA 모드에서 프리뷰 iframe의 asset 캐싱

## 관련
- [[intel-wrapper-architecture]] · [[single-html-runtime]] · [[no-debug-philosophy]]
