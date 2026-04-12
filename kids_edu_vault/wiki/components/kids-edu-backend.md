---
type: component
title: "Kids Edu Backend"
created: 2026-04-12
updated: 2026-04-12
status: active
tags:
  - component
  - backend
  - fastapi
  - pilot/2026-05-05
related:
  - "[[nextjs-fastapi-wrapper-architecture]]"
  - "[[iframe-sandbox-over-webcontainers]]"
  - "[[ai-prompting-literacy-input]]"
---

# Kids Edu Backend

## 역할
FastAPI 기반 WebSocket 서버. 어린이의 채팅 입력을 받아 Claude CLI subprocess로 전달하고, 스트리밍 응답(텍스트 + 게임 HTML)을 프론트엔드로 실시간 전달.

## 위치
`hypeproof_kids_edu/src/backend/`

## 실행
```bash
# 개발 (Mock 모드)
MOCK_CLAUDE=1 uv run uvicorn main:app --reload

# 실제 Claude 연동
uv run uvicorn main:app --reload
```

## 엔드포인트

| 경로 | 방식 | 설명 |
|---|---|---|
| `/health` | GET | 서버 상태 확인 |
| `/ws/chat/{child_id}` | WebSocket | 어린이별 채팅 세션 |
| `/admin/reset/{child_id}` | POST | 운영자용 세션 초기화 |

## WebSocket 프로토콜

**클라이언트 → 서버**
```json
{"prompt": "별을 모으는 게임 만들어줘"}
```

**서버 → 클라이언트**
```json
{"type": "text",  "chunk": "게임 만들고 있어!"}
{"type": "game",  "html": "<!DOCTYPE html>..."}
{"type": "done",  "hint": "💡 다음엔 ...", "session_id": "..."}
{"type": "error", "chunk": "오류 메시지"}
```

## 핵심 모듈

### claude_runner.py
- `SessionStore` — child_id → claude_session_id JSON 영구 저장
- `stream_claude(prompt, child_id)` — async generator, StreamEvent yield
- `reset_session(child_id)` — 세션 초기화
- `_extract_hint(text)` — 응답에서 💡 힌트 줄 추출
- `_HTML_RE` — ```html ... ``` 블록 추출 정규식

### personas/TUTOR.md
W3(빠른 구현) + W4(스토리텔링) 합성 페르소나. [[ai-persona-workflows]] 참조.
- 즉시 완성품 반환
- 코드 노출 금지
- 협력형 서사 (전투·체력 소거)
- 응답 끝 "💡 다음엔 ~라고 해봐!" 필수

## 환경변수 (.env.example)

| 키 | 기본값 | 설명 |
|---|---|---|
| `CLAUDE_TIMEOUT` | 120 | subprocess 타임아웃 (초) |
| `CLAUDE_MODEL` | sonnet | Claude 모델 |
| `MOCK_CLAUDE` | 0 | 1이면 실제 호출 없이 mock 응답 |

## 테스트
```bash
uv run pytest -v   # 28개 전체 통과
```
테스트 파일: `tests/test_claude_runner.py` — SessionStore, _extract_hint, _HTML_RE, reset_session, stream_claude mock 커버.

## 보안 제약
- `--allowedTools Read,Write,Glob` — Bash 제거 (아동 환경)
- 입력 prompt는 subprocess 인자로만 전달 (shell=False)
