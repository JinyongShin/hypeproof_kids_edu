"""
Claude CLI subprocess wrapper — Kids Edu Backend.
sanshome_bot/claude_runner.py 기반, 교육용으로 수정:
  - stream-json 스트리밍
  - allowedTools: Read,Write,Glob (Bash 제거)
  - {child_id}::{session_id} 복합키 기반 세션 관리
  - 교육용 TUTOR.md 페르소나
  - 카드 JSON → 디스크 저장 + URL 서빙
"""

import json
import logging
import os
import re
import subprocess
import tempfile
import time
from dataclasses import dataclass
from pathlib import Path
from typing import Optional, Tuple

import storage

logger = logging.getLogger(__name__)

_BACKEND_ROOT = Path(__file__).parent
_PERSONA_DIR = _BACKEND_ROOT / "personas"
_DATA_DIR = _BACKEND_ROOT / "data"

CLAUDE_TIMEOUT = int(os.getenv("CLAUDE_TIMEOUT", "120"))
CLAUDE_MODEL = os.getenv("CLAUDE_MODEL", "sonnet")
MOCK_CLAUDE = os.getenv("MOCK_CLAUDE", "0") == "1"
BACKEND_BASE_URL = os.getenv("BACKEND_BASE_URL", "http://localhost:8000")

# 세션당 보존할 최신 카드 파일 수
_MAX_CARDS_PER_SESSION = 10

_MOCK_RESPONSE = """\
와, 토끼 전사 캐릭터를 만들었어! 귀도 쫑긋하고 너무 귀엽다!

```json
{"card_type":"character","name":"별빛 토끼 전사","description":"달빛 아래서 태어난 용감한 토끼. 친구들을 지키는 수호자야.","traits":["용감함","친절함","점프 마스터"],"world":"","image_prompt":"cute brave rabbit warrior with long ears, wearing light armor with star patterns, soft pastel colors, friendly expression, chibi style, magical sparkles"}
```

💡 다음엔 "토끼가 사는 세계는 꽃이 가득한 숲이야"라고 해봐!
"""

# JSON 코드 블록 추출 정규식
_JSON_CARD_RE = re.compile(r"```json\s*([\s\S]*?)```", re.IGNORECASE)


def _load_persona() -> str:
    parts = []
    for name in ("TUTOR.md",):
        path = _PERSONA_DIR / name
        if path.exists():
            content = path.read_text(encoding="utf-8").strip()
            if content:
                parts.append(content)
    return "\n\n".join(parts)


@dataclass
class StreamEvent:
    type: str          # "text" | "card" | "done" | "error"
    chunk: str = ""
    card_json: str = ""
    session_id: Optional[str] = None
    hint: str = ""
    card_url: str = ""


def _extract_hint(text: str) -> str:
    """💡 로 시작하는 마지막 줄 추출."""
    for line in reversed(text.splitlines()):
        line = line.strip()
        if line.startswith("💡"):
            return line
    return ""


def _friendly_error(kind: str) -> str:
    """아이에게 보여줄 친근한 오류 메시지 반환. 원본 오류는 호출 전에 logger로 기록."""
    _messages = {
        "timeout":    "AI가 너무 오래 생각했어. 다시 한 번 말해봐! ⏰",
        "not_found":  "AI 도우미를 찾을 수 없어. 선생님한테 도움을 요청해봐! 🙏",
        "returncode": "AI가 잠깐 실수했어. 다시 한 번 해볼까? 🔄",
        "generic":    "뭔가 잘못됐어. 다시 한 번 해볼까? 😅",
    }
    return _messages.get(kind, _messages["generic"])


def _save_card_json(card_json: str, child_id: str, session_id: str, card_id: str) -> Path:
    """카드 JSON을 디스크에 저장하고 파일 경로를 반환. storage.add_card도 호출."""
    cards_base = (_DATA_DIR / "cards").resolve()
    card_dir = (_DATA_DIR / "cards" / child_id / session_id).resolve()
    if not card_dir.is_relative_to(cards_base):
        raise ValueError(f"경로 순회 공격 감지: {card_dir}")

    card_dir.mkdir(parents=True, exist_ok=True)

    # 세션당 최신 10개 초과 시 오래된 파일 삭제 + DB에서도 정리
    existing = sorted(card_dir.glob("card_*.json"), key=lambda p: p.name)
    while len(existing) >= _MAX_CARDS_PER_SESSION:
        old_path = existing.pop(0)
        old_card_id = old_path.stem
        old_path.unlink(missing_ok=True)
        storage.delete_card(session_id, old_card_id)

    card_path = card_dir / f"{card_id}.json"
    if not card_path.resolve().is_relative_to(cards_base):
        raise ValueError(f"경로 순회 공격 감지: {card_path}")
    card_path.write_text(card_json, encoding="utf-8")

    # JSON에서 card_type 추출
    try:
        card_data = json.loads(card_json)
        card_type = card_data.get("card_type", "character")
    except json.JSONDecodeError:
        card_type = "character"

    url = f"{BACKEND_BASE_URL}/cards/{child_id}/{session_id}/{card_id}"
    storage.add_card(session_id, child_id, card_id, card_type, card_json)

    return card_path


async def stream_claude(prompt: str, child_id: str, session_id: str):
    """
    Claude CLI를 stream-json 모드로 실행하고 StreamEvent를 yield.

    Yields:
        StreamEvent(type="text", chunk=...)   — 텍스트 청크
        StreamEvent(type="card", card_url=..., card_json=...) — 저장된 카드의 URL
        StreamEvent(type="done", session_id=..., hint=..., card_url=...)
        StreamEvent(type="error", chunk=...)
    """
    if MOCK_CLAUDE:
        ts = int(time.time() * 1000)
        mock_card_id = f"card_{ts}"
        for line in _MOCK_RESPONSE.splitlines(keepends=True):
            yield StreamEvent(type="text", chunk=line)
        json_match = _JSON_CARD_RE.search(_MOCK_RESPONSE)
        card_url = ""
        card_json_content = ""
        if json_match:
            card_json_content = json_match.group(1).strip()
            _save_card_json(card_json_content, child_id, session_id, mock_card_id)
            card_url = f"{BACKEND_BASE_URL}/cards/{child_id}/{session_id}/{mock_card_id}"
            yield StreamEvent(type="card", card_url=card_url, card_json=card_json_content)
        yield StreamEvent(
            type="done",
            session_id="mock-session",
            hint=_extract_hint(_MOCK_RESPONSE),
            card_url=card_url,
        )
        return

    persona = _load_persona()
    cmd = [
        "claude", "-p", prompt,
        "--model", CLAUDE_MODEL,
        "--output-format", "stream-json",
        "--verbose",
        "--allowedTools", "Read,Write,Glob",
        "--dangerously-skip-permissions",
    ]
    if persona:
        cmd += ["--append-system-prompt", persona]
    claude_session_id = storage.get_claude_session_id(session_id)
    if claude_session_id:
        cmd += ["--resume", claude_session_id]

    env = os.environ.copy()
    env.pop("CLAUDECODE", None)

    try:
        proc = subprocess.Popen(
            cmd + ["--add-dir", str(_BACKEND_ROOT)],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
            encoding="utf-8",
            cwd=tempfile.gettempdir(),
            env=env,
        )
    except FileNotFoundError:
        logger.error("[%s::%s] claude CLI를 찾을 수 없습니다.", child_id, session_id)
        yield StreamEvent(type="error", chunk=_friendly_error("not_found"))
        return

    full_text = ""
    new_claude_session_id: Optional[str] = None

    try:
        for raw_line in proc.stdout:  # type: ignore[union-attr]
            raw_line = raw_line.strip()
            if not raw_line:
                continue
            try:
                event = json.loads(raw_line)
            except json.JSONDecodeError:
                continue

            etype = event.get("type", "")

            # 텍스트 청크 (assistant message content)
            if etype == "assistant":
                msg = event.get("message", {})
                for block in msg.get("content", []):
                    if block.get("type") == "text":
                        chunk = block.get("text", "")
                        full_text += chunk
                        yield StreamEvent(type="text", chunk=chunk)

            # 최종 결과 (session_id 획득)
            elif etype == "result":
                new_claude_session_id = event.get("session_id")
                result_text = event.get("result", "").strip()
                if result_text and not full_text:
                    full_text = result_text
                    yield StreamEvent(type="text", chunk=result_text)

        proc.wait(timeout=CLAUDE_TIMEOUT)

        if proc.returncode != 0:
            stderr = (proc.stderr.read() if proc.stderr else "").strip()
            logger.error("[%s::%s] claude 실패 (returncode=%d): %s", child_id, session_id, proc.returncode, stderr)
            storage.delete_claude_session_id(session_id)
            yield StreamEvent(type="error", chunk=_friendly_error("returncode"))
            return

        # 세션 저장
        if new_claude_session_id:
            storage.set_claude_session_id(session_id, new_claude_session_id)
            logger.info("[%s::%s] 세션 저장: %s", child_id, session_id, new_claude_session_id)

        # 카드 JSON 추출 및 저장
        card_url = ""
        card_json_content = ""
        json_match = _JSON_CARD_RE.search(full_text)
        if json_match:
            card_json_content = json_match.group(1).strip()
            card_id = f"card_{int(time.time() * 1000)}"
            logger.info("[%s::%s] 카드 JSON 크기: %d bytes", child_id, session_id, len(card_json_content))
            _save_card_json(card_json_content, child_id, session_id, card_id)
            card_url = f"{BACKEND_BASE_URL}/cards/{child_id}/{session_id}/{card_id}"
            yield StreamEvent(type="card", card_url=card_url, card_json=card_json_content)

        yield StreamEvent(
            type="done",
            session_id=new_claude_session_id,
            hint=_extract_hint(full_text),
            card_url=card_url,
        )

    except subprocess.TimeoutExpired:
        proc.kill()
        logger.error("[%s::%s] 타임아웃 (%d초)", child_id, session_id, CLAUDE_TIMEOUT)
        storage.delete_claude_session_id(session_id)
        yield StreamEvent(type="error", chunk=_friendly_error("timeout"))
    except Exception as e:
        logger.exception("[%s::%s] 예외: %s", child_id, session_id, e)
        yield StreamEvent(type="error", chunk=_friendly_error("generic"))


def reset_session(child_id: str, session_id: Optional[str] = None) -> bool:
    """child_id (+ 선택적 session_id) claude 세션 초기화 (운영자용)."""
    if session_id is not None:
        existing = storage.get_claude_session_id(session_id)
        if existing:
            storage.delete_claude_session_id(session_id)
            logger.info("[%s::%s] 세션 리셋", child_id, session_id)
            return True
        return False
    # session_id 미지정 시 해당 child_id 의 모든 세션의 claude_session_id 초기화
    changed = storage.reset_all_claude_sessions(child_id)
    if changed:
        logger.info("[%s] 전체 세션 리셋 (%d개)", child_id, changed)
        return True
    return False
