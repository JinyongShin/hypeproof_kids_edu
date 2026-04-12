"""
Claude CLI subprocess wrapper — Kids Edu Backend.
sanshome_bot/claude_runner.py 기반, 교육용으로 수정:
  - stream-json 스트리밍
  - allowedTools: Read,Write,Glob (Bash 제거)
  - child_id (str) 기반 세션 관리
  - 교육용 TUTOR.md 페르소나
"""

import json
import logging
import os
import re
import subprocess
from dataclasses import dataclass, field
from pathlib import Path

logger = logging.getLogger(__name__)

_BACKEND_ROOT = Path(__file__).parent
_PERSONA_DIR = _BACKEND_ROOT / "personas"
_DATA_DIR = _BACKEND_ROOT / "data"
_SESSIONS_FILE = _DATA_DIR / "sessions.json"

CLAUDE_TIMEOUT = int(os.getenv("CLAUDE_TIMEOUT", "120"))
CLAUDE_MODEL = os.getenv("CLAUDE_MODEL", "sonnet")
MOCK_CLAUDE = os.getenv("MOCK_CLAUDE", "0") == "1"

_MOCK_RESPONSE = """\
별을 모으는 게임을 만들었어! 화살표 키로 움직여봐 ⭐

```html
<!DOCTYPE html>
<html>
<head><meta charset="UTF-8"><title>별 모으기</title></head>
<body style="margin:0;background:#1a1a2e;">
<canvas id="c" width="480" height="480"></canvas>
<script>
const c=document.getElementById('c'),ctx=c.getContext('2d');
let px=240,py=400,stars=[],score=0;
for(let i=0;i<8;i++)stars.push({x:Math.random()*460+10,y:Math.random()*200+10});
const keys={};
document.addEventListener('keydown',e=>keys[e.key]=true);
document.addEventListener('keyup',e=>keys[e.key]=false);
function loop(){
  ctx.fillStyle='#1a1a2e';ctx.fillRect(0,0,480,480);
  if(keys['ArrowLeft']&&px>20)px-=4;
  if(keys['ArrowRight']&&px<460)px+=4;
  if(keys['ArrowUp']&&py>20)py-=4;
  if(keys['ArrowDown']&&py<460)py+=4;
  ctx.fillStyle='#FFD700';ctx.font='24px sans-serif';
  stars=stars.filter(s=>{
    const d=Math.hypot(px-s.x,py-s.y);
    if(d<20){score++;return false;}
    ctx.fillText('⭐',s.x-12,s.y+8);return true;
  });
  if(stars.length===0)for(let i=0;i<8;i++)stars.push({x:Math.random()*460+10,y:Math.random()*200+10});
  ctx.fillStyle='#00BFFF';ctx.beginPath();ctx.arc(px,py,16,0,Math.PI*2);ctx.fill();
  ctx.fillStyle='#fff';ctx.font='20px sans-serif';ctx.fillText('⭐ '+score,10,30);
  requestAnimationFrame(loop);
}
loop();
</script>
</body>
</html>
```

💡 다음엔 "별 대신 하트를 모으고 싶어"라고 해봐!
"""

# HTML 코드 블록 추출 정규식
_HTML_RE = re.compile(r"```html\s*([\s\S]*?)```", re.IGNORECASE)


class SessionStore:
    """child_id(str) → claude session_id(str) 영구 저장."""

    def __init__(self, path: Path):
        self._path = path
        self._path.parent.mkdir(parents=True, exist_ok=True)
        self._data: dict[str, str] = {}
        if self._path.exists():
            try:
                self._data = json.loads(self._path.read_text(encoding="utf-8"))
            except (json.JSONDecodeError, ValueError):
                logger.warning("세션 파일 손상, 초기화: %s", self._path)

    def get(self, child_id: str) -> str | None:
        return self._data.get(child_id)

    def __contains__(self, child_id: str) -> bool:
        return child_id in self._data

    def __setitem__(self, child_id: str, session_id: str):
        self._data[child_id] = session_id
        self._save()

    def __delitem__(self, child_id: str):
        self._data.pop(child_id, None)
        self._save()

    def _save(self):
        tmp = self._path.with_suffix(".tmp")
        tmp.write_text(json.dumps(self._data, indent=2, ensure_ascii=False))
        tmp.replace(self._path)


_sessions = SessionStore(_SESSIONS_FILE)


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
    type: str          # "text" | "game" | "done" | "error"
    chunk: str = ""
    html: str = ""
    session_id: str | None = None
    hint: str = ""


def _extract_hint(text: str) -> str:
    """💡 로 시작하는 마지막 줄 추출."""
    for line in reversed(text.splitlines()):
        line = line.strip()
        if line.startswith("💡"):
            return line
    return ""


async def stream_claude(prompt: str, child_id: str):
    """
    Claude CLI를 stream-json 모드로 실행하고 StreamEvent를 yield.

    Yields:
        StreamEvent(type="text", chunk=...)   — 텍스트 청크
        StreamEvent(type="game", html=...)    — 완성된 게임 HTML
        StreamEvent(type="done", session_id=..., hint=...)
        StreamEvent(type="error", chunk=...)
    """
    if MOCK_CLAUDE:
        # Mock 모드: 청크 단위 시뮬레이션
        for line in _MOCK_RESPONSE.splitlines(keepends=True):
            yield StreamEvent(type="text", chunk=line)
        html_match = _HTML_RE.search(_MOCK_RESPONSE)
        if html_match:
            yield StreamEvent(type="game", html=html_match.group(1).strip())
        yield StreamEvent(
            type="done",
            session_id="mock-session",
            hint=_extract_hint(_MOCK_RESPONSE),
        )
        return

    persona = _load_persona()
    cmd = [
        "claude", "-p", prompt,
        "--model", CLAUDE_MODEL,
        "--output-format", "stream-json",
        "--verbose",
        "--allowedTools", "Read,Write,Glob",
    ]
    if persona:
        cmd += ["--append-system-prompt", persona]
    session_id = _sessions.get(child_id)
    if session_id:
        cmd += ["--resume", session_id]

    env = os.environ.copy()
    env.pop("CLAUDECODE", None)

    try:
        proc = subprocess.Popen(
            cmd,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
            encoding="utf-8",
            cwd=str(_BACKEND_ROOT),
            env=env,
        )
    except FileNotFoundError:
        yield StreamEvent(type="error", chunk="claude CLI를 찾을 수 없습니다.")
        return

    full_text = ""
    new_session_id: str | None = None

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
                new_session_id = event.get("session_id")
                result_text = event.get("result", "").strip()
                if result_text and not full_text:
                    full_text = result_text
                    yield StreamEvent(type="text", chunk=result_text)

        proc.wait(timeout=CLAUDE_TIMEOUT)

        if proc.returncode != 0:
            stderr = (proc.stderr.read() if proc.stderr else "").strip()
            logger.error("[%s] claude 실패 (returncode=%d): %s", child_id, proc.returncode, stderr)
            if child_id in _sessions:
                del _sessions[child_id]
            yield StreamEvent(type="error", chunk=f"claude 실행 오류: {stderr or '알 수 없는 오류'}")
            return

        # 세션 저장
        if new_session_id:
            _sessions[child_id] = new_session_id
            logger.info("[%s] 세션 저장: %s", child_id, new_session_id)

        # 게임 HTML 추출
        html_match = _HTML_RE.search(full_text)
        if html_match:
            yield StreamEvent(type="game", html=html_match.group(1).strip())

        yield StreamEvent(
            type="done",
            session_id=new_session_id,
            hint=_extract_hint(full_text),
        )

    except subprocess.TimeoutExpired:
        proc.kill()
        logger.error("[%s] 타임아웃 (%d초)", child_id, CLAUDE_TIMEOUT)
        if child_id in _sessions:
            del _sessions[child_id]
        yield StreamEvent(type="error", chunk=f"응답 시간 초과 ({CLAUDE_TIMEOUT}초)")
    except Exception as e:
        logger.exception("[%s] 예외", child_id)
        yield StreamEvent(type="error", chunk=str(e))


def reset_session(child_id: str) -> bool:
    """child_id 세션 초기화 (운영자용)."""
    if child_id in _sessions:
        del _sessions[child_id]
        logger.info("[%s] 세션 리셋", child_id)
        return True
    return False
