---
type: decision
title: "Next.js + FastAPI 래퍼 아키텍처"
created: 2026-04-12
updated: 2026-04-12
status: proposed
tags:
  - architecture
  - dev/wrapper
  - pilot/2026-05-05
related:
  - "[[pivot-to-chat-preview-wrapper]]"
  - "[[iframe-sandbox-over-webcontainers]]"
  - "[[stack-decision-after-curriculum]]"
owner: JY
---

# ADR: Next.js + FastAPI 래퍼 아키텍처

## 상태

Proposed — 4/21 커리큘럼 리뷰 후 최종 확정 예정 ([[stack-decision-after-curriculum]]).

## 맥락

[[pivot-to-chat-preview-wrapper]] 결정에 따라 Next.js 기반 채팅+게임 프리뷰 래퍼를 구현해야 한다.
핵심 질문: **백엔드에서 Claude를 어떻게 호출할 것인가?**

3가지 옵션을 검토했다.

| 옵션 | 설명 | 구현 속도 | 장기 확장성 |
|---|---|---|---|
| **A. FastAPI + CLI subprocess** | sanshome_bot 재활용, Python 유지 | ★★★★★ | ★★★☆☆ |
| B. Next.js + Agent SDK | @anthropic-ai/sdk, 단일 서비스 | ★★★☆☆ | ★★★★★ |
| C. Next.js + CLI subprocess | Node.js child_process, Python 로직 재작성 | ★★★★☆ | ★★★★☆ |

## 결정

**옵션 A — FastAPI (Python) + CLI subprocess** 선택.

Next.js는 UI만 담당. FastAPI가 Claude CLI subprocess를 호출하고 WebSocket으로 스트림 전달.

## 근거

1. **타임라인**: 4/21 스택 확정 → 4/26 리허설까지 **5일**. 검증된 코드 재활용이 유일한 현실적 선택.
2. **sanshome_bot 재사용**: `claude_runner.py`의 `SessionStore`, `run_claude()`, `_load_persona()` 로직을 그대로 포팅. 스트리밍만 `--output-format stream-json`으로 업그레이드.
3. **Tool 제어**: `--allowedTools Read,Write,Glob` — Bash 제거로 아동 환경 보안 확보. Agent SDK보다 단순·명시적.
4. **파일럿 규모**: 감독 환경(강사 상주), 동시 접속 40명 이하. 단순 아키텍처가 오히려 안정적.

## 아키텍처

```
[ 브라우저 (Next.js) ]
  ChatPane ←→ WebSocket ←→ FastAPI /ws/chat/{child_id}
  GamePreview ←iframe srcdoc←  (HTML 추출 후 주입)
  PromptScaffold (현재 블록 기반 카드)

[ FastAPI 백엔드 ]
  WebSocket handler
    ↓
  claude_runner.py
    ↓ subprocess
  claude -p {prompt}
    --model sonnet
    --output-format stream-json
    --allowedTools Read,Write,Glob
    --resume {child_session_id}
    --append-system-prompt {TUTOR.md}
    ↓ stream-json 청크
  WebSocket으로 실시간 전달
```

## 구현 세부

### 세션 관리

파일럿 규모이므로 단순하게: `sessions.json` 파일.

```json
{
  "child_01": "claude_session_abc",
  "child_02": "claude_session_def"
}
```

아이 식별: URL 파라미터 `?child=01` (운영자가 파일럿 당일 배포).
인증 없음 (C 단계). A-Lite 단계에서 Clerk 추가.

### 게임 HTML 추출

Claude 응답에서 정규식으로 추출:
```python
import re
match = re.search(r'```html\s*([\s\S]*?)```', response)
if match:
    game_html = match.group(1)
```

추출된 HTML → WebSocket으로 `{"type": "game", "html": "..."}` 전송
→ Next.js `GamePreview.tsx`가 `iframe.srcdoc`에 주입.

### 스트리밍

```python
proc = subprocess.Popen(
    ["claude", "-p", prompt, "--output-format", "stream-json", ...],
    stdout=subprocess.PIPE, text=True
)
for line in proc.stdout:
    data = json.loads(line)
    if data.get("type") == "text":
        await websocket.send_json({"type": "text", "chunk": data["text"]})
```

### 보안

- `sandbox="allow-scripts"` 만 허용. `allow-same-origin` 절대 금지.
- Claude 허용 툴: `Read,Write,Glob` (Bash 제거).
- 입력 sanitize: 프롬프트에서 shell 메타문자 제거 후 subprocess 전달.

## 파일럿 이후 마이그레이션 경로

FastAPI → Next.js API Route + `@anthropic-ai/sdk` (스트리밍 네이티브) 로 전환 가능.
FastAPI와 SDK 인터페이스를 동일하게 설계하면 프론트 변경 최소화.

## 트레이드오프

| 장점 | 단점 |
|---|---|
| 구현 속도 (5일 스프린트 현실적) | 서비스 2개 (FastAPI + Next.js) 배포 관리 |
| 검증된 Python 코드 재활용 | 장기적으로 Agent SDK 대비 기능 제한 |
| Tool 제어 단순·명시적 | streaming 파싱 커스텀 필요 |

## 관련 결정

- [[pivot-to-chat-preview-wrapper]] — 래퍼 방향 원결정
- [[iframe-sandbox-over-webcontainers]] — 게임 실행 샌드박스
- [[stack-decision-after-curriculum]] — 4/21 확정 게이트
- [[combat-vs-cooperative-framing]] — 시스템 프롬프트 서사 제약
- [[ai-prompting-literacy-input]] — 교육 목표 (UI 요건 포함)
