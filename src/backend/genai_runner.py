"""
Google GenAI 클라이언트 — claude_runner 대체.
Gemini 2.5 Flash (텍스트) + 이미지 생성 (Nano Banana) 통합.
"""

import json
import logging
import os
import time
import asyncio
from dataclasses import dataclass
from pathlib import Path

import storage

logger = logging.getLogger(__name__)

_BACKEND_ROOT = Path(__file__).parent
_PERSONA_DIR = _BACKEND_ROOT / "personas"
_DATA_DIR = _BACKEND_ROOT / "data"

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY", "")
GEMINI_TEXT_MODEL = os.getenv("GEMINI_TEXT_MODEL", "gemini-2.5-flash")
GEMINI_IMAGE_MODEL = os.getenv("GEMINI_IMAGE_MODEL", "gemini-2.5-flash-image")
MOCK_MODE = os.getenv("MOCK_GENAI", "0") == "1"

_MAX_CARDS_PER_SESSION = 10

_MOCK_CARD_RESPONSE = '''와, 토끼 전사 캐릭터를 만들었어! 귀도 쫑긋하고 너무 귀엽다!

```json
{"card_type":"character","name":"별빛 토끼 전사","description":"달빛 아래서 태어난 용감한 토끼. 친구들을 지키는 수호자야.","traits":["용감함","친절함","점프 마스터"],"world":"","image_prompt":"cute brave rabbit warrior with long ears, wearing light armor with star patterns, soft pastel colors, friendly expression, chibi style, magical sparkles","image_svg":"<svg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 200 200'><ellipse cx='80' cy='55' rx='10' ry='30' fill='#fef3c7'/><ellipse cx='120' cy='55' rx='10' ry='30' fill='#fef3c7'/><ellipse cx='100' cy='130' rx='50' ry='55' fill='#fef9e7'/><circle cx='100' cy='100' r='38' fill='#fef9e7'/><circle cx='88' cy='98' r='4' fill='#1f2937'/><circle cx='112' cy='98' r='4' fill='#1f2937'/><circle cx='100' cy='112' r='3' fill='#f87171'/><polygon points='100,28 105,42 95,42' fill='#fbbf24'/></svg>"}
```

💡 다음엔 "토끼가 사는 세계는 꽃이 가득한 숲이야"라고 해봐!'''


@dataclass
class StreamEvent:
    type: str  # "text" | "card" | "image" | "game" | "done" | "error"
    chunk: str = ""
    card_json: str = ""
    card_url: str = ""
    image_url: str = ""
    image_data: bytes = b""
    hint: str = ""
    session_id: str = ""
    game_url: str = ""
    html: str = ""  # HTML5 game code


def _load_persona() -> str:
    path = _PERSONA_DIR / "TUTOR.md"
    if path.exists():
        return path.read_text(encoding="utf-8").strip()
    return ""


def _extract_game_html(text: str) -> "str | None":
    """HTML 코드블록에서 게임 코드 추출 (다중 패턴)."""
    import re
    # 1) ```html 블록
    match = re.search(r"```html\s*([\s\S]*?)```", text, re.IGNORECASE)
    if match:
        html = match.group(1).strip()
        if "<canvas" in html or "<html" in html.lower():
            return html
    # 2) 아무 ``` 블록 중 HTML 포함
    match = re.search(r"```\s*([\s\S]*?)```", text)
    if match:
        html = match.group(1).strip()
        if "<!DOCTYPE" in html.upper() or "<canvas" in html or "<script" in html:
            return html
    # 3) 텍스트 전체에서 DOCTYPE 또는 <html 태그 직접 찾기
    match = re.search(r"(<!DOCTYPE[\s\S]*?</html>|<html[\s\S]*?</html>)", text, re.IGNORECASE | re.DOTALL)
    if match:
        html = match.group(1).strip()
        if "<canvas" in html or "<script" in html:
            return html
    return None


def _extract_hint(text: str) -> str:
    for line in reversed(text.splitlines()):
        line = line.strip()
        if line.startswith("💡"):
            return line
    return ""


def _extract_card_json(text: str) -> "str | None":
    """JSON 코드블록에서 카드 JSON 추출."""
    import re
    match = re.search(r"```json\s*([\s\S]*?)```", text, re.IGNORECASE)
    if match:
        try:
            data = json.loads(match.group(1).strip())
            if "card_type" in data:
                return match.group(1).strip()
        except json.JSONDecodeError:
            pass
    return None


def _friendly_error(kind: str) -> str:
    messages = {
        "timeout": "마법사가 너무 오래 생각했어. 다시 한 번 말해봐! ⏰",
        "not_found": "AI 도우미를 찾을 수 없어. 선생님한테 도움을 요청해봐! 🙏",
        "generic": "뭔가 잘못됐어. 다시 한 번 해볼까? 😅",
    }
    return messages.get(kind, messages["generic"])


def _save_card(card_id: str, child_id: str, session_id: str, card_json: str) -> str:
    """카드 JSON을 디스크에 저장하고 storage에 등록."""
    card_dir = (_DATA_DIR / "cards" / child_id / session_id).resolve()
    cards_base = (_DATA_DIR / "cards").resolve()
    if not card_dir.is_relative_to(cards_base):
        raise ValueError(f"경로 순회 공격 감지: {card_dir}")

    card_dir.mkdir(parents=True, exist_ok=True)

    # 세션당 최신 10개 유지
    existing = sorted(card_dir.glob("card_*.json"), key=lambda p: p.name)
    while len(existing) >= _MAX_CARDS_PER_SESSION:
        old_path = existing.pop(0)
        old_card_id = old_path.stem
        old_path.unlink(missing_ok=True)
        storage.delete_card(session_id, old_card_id)

    card_path = card_dir / f"{card_id}.json"
    card_path.write_text(card_json, encoding="utf-8")

    url = f"{os.getenv('BACKEND_BASE_URL', 'http://localhost:8000')}/cards/{child_id}/{session_id}/{card_id}"
    
    data = json.loads(card_json)
    storage.add_card(session_id, child_id, card_id, data.get("card_type", "character"), card_json, url)

    return url


async def generate_card(prompt: str, child_id: str, session_id: str):
    """
    Gemini로 카드 JSON 생성.
    Yields StreamEvent (text chunks, card, done/error).
    """
    if MOCK_MODE:
        for line in _MOCK_CARD_RESPONSE.splitlines(keepends=True):
            yield StreamEvent(type="text", chunk=line)

        card_json = _extract_card_json(_MOCK_CARD_RESPONSE)
        card_url = ""
        if card_json:
            card_id = f"card_{int(time.time() * 1000)}"
            card_url = _save_card(card_id, child_id, session_id, card_json)
            yield StreamEvent(type="card", card_json=card_json, card_url=card_url)

        yield StreamEvent(type="done", hint=_extract_hint(_MOCK_CARD_RESPONSE), card_url=card_url)
        return

    # --- GLM (z.ai) 텍스트 생성 ---
    ZAI_API_KEY = os.getenv("ZAI_API_KEY", "1edec351dba64a08a4838bd5993a9322.r7Z6EBjcZJxmpKNL")
    ZAI_BASE_URL = os.getenv("ZAI_BASE_URL", "https://api.z.ai/api/coding/paas/v4/chat/completions")
    ZAI_MODEL = os.getenv("ZAI_MODEL", "glm-5")

    persona = _load_persona()
    full_text = ""

    import urllib.parse
    import urllib.request

    def _glm_chat(api_key, base_url, model, system_prompt, user_prompt):
        import json as _json
        messages = []
        if system_prompt:
            messages.append({"role": "system", "content": system_prompt})
        messages.append({"role": "user", "content": user_prompt})
        body = _json.dumps({
            "model": model,
            "messages": messages,
            "temperature": 0.7,
            "max_tokens": 8192,
            "stream": True,
        }).encode("utf-8")
        req = urllib.request.Request(
            base_url,
            data=body,
            headers={"Content-Type": "application/json", "Authorization": f"Bearer {api_key}"},
        )
        chunks = []
        with urllib.request.urlopen(req, timeout=180) as resp:
            for line in resp:
                line = line.decode("utf-8").strip()
                if line.startswith("data: ") and line != "data: [DONE]":
                    try:
                        d = _json.loads(line[6:])
                        delta = d.get("choices", [{}])[0].get("delta", {})
                        c = delta.get("content", "")
                        if c:
                            chunks.append(c)
                    except:
                        pass
        return "".join(chunks)

    def _pollinations_chat(system_prompt, user_prompt):
        import json as _json
        messages = []
        if system_prompt:
            messages.append({"role": "system", "content": system_prompt})
        messages.append({"role": "user", "content": user_prompt})
        body = _json.dumps({
            "messages": messages,
            "model": "openai",
            "seed": int(time.time())
        }).encode("utf-8")
        req = urllib.request.Request(
            "https://text.pollinations.ai/",
            data=body,
            headers={"Content-Type": "application/json", "User-Agent": "Mozilla/5.0"},
        )
        with urllib.request.urlopen(req, timeout=120) as resp:
            return resp.read().decode("utf-8")

    system_prompt = persona if persona else ""
    try:
        # 1차: GLM (z.ai) 시도
        response_text = await asyncio.to_thread(_glm_chat, ZAI_API_KEY, ZAI_BASE_URL, ZAI_MODEL, system_prompt, prompt)

        if response_text:
            full_text = response_text
            yield StreamEvent(type="text", chunk=full_text)
    except Exception as glm_err:
        logger.warning("[%s::%s] GLM 실패, Pollinations 폴백: %s", child_id, session_id, glm_err)
        # 2차: Pollinations.ai 폴백
        try:
            response_text = await asyncio.to_thread(_pollinations_chat, system_prompt, prompt)
            if response_text:
                full_text = response_text
                yield StreamEvent(type="text", chunk=full_text)
        except Exception as poll_err:
            logger.error("[%s::%s] Pollinations도 실패: %s", child_id, session_id, poll_err)

    # 카드 JSON 또는 게임 HTML 추출
    try:
        card_json_str = _extract_card_json(full_text)
    except Exception:
        card_json_str = None
    try:
        game_html = _extract_game_html(full_text)
    except Exception:
        game_html = None
    card_url = ""
    game_url = ""
    if card_json_str:
        try:
            card_id = f"card_{int(time.time() * 1000)}"
            card_url = _save_card(card_id, child_id, session_id, card_json_str)
        except Exception as save_err:
            logger.exception("[%s::%s] 카드 저장 실패 (텍스트는 정상): %s", child_id, session_id, save_err)
        yield StreamEvent(type="card", card_json=card_json_str, card_url=card_url)
    elif game_html:
        # 게임 HTML을 파일로 저장
        game_dir = (_DATA_DIR / "games" / child_id / session_id).resolve()
        games_base = (_DATA_DIR / "games").resolve()
        if game_dir.is_relative_to(games_base):
            game_dir.mkdir(parents=True, exist_ok=True)
            game_id = f"game_{int(time.time() * 1000)}"
            (game_dir / f"{game_id}.html").write_text(game_html, encoding="utf-8")
            game_url = f"{os.getenv('BACKEND_BASE_URL', 'http://localhost:8000')}/games/{child_id}/{session_id}/{game_id}"
        yield StreamEvent(type="game", html=game_html, game_url=game_url)

    if full_text:
        yield StreamEvent(
            type="done",
            hint=_extract_hint(full_text),
            card_url=card_url,
            game_url=game_url,
        )
    else:
        yield StreamEvent(type="error", chunk=_friendly_error("generic"))


async def generate_image(image_prompt: str):
    """
    Pollinations.ai로 이미지 생성 (무료, API 키 불필요).
    Returns: (image_bytes, mime_type)
    """
    import asyncio
    import base64
    import urllib.parse
    import urllib.request

    if MOCK_MODE:
        mock_png = base64.b64decode(
            "iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAYAAAAfFcSJAAAADUlEQVR42mNkYPj/HwADBwIAMCbHYQAAAABJRU5ErkJggg=="
        )
        return mock_png, "image/png"

    prompt = f"cute, child-friendly illustration, chibi style, soft pastel colors, magical, wholesome: {image_prompt}"
    url = f"https://image.pollinations.ai/prompt/{urllib.parse.quote(prompt)}?width=512&height=512&nologo=true"

    def _fetch():
        req = urllib.request.Request(url, headers={"User-Agent": "KidsEdu/1.0"})
        with urllib.request.urlopen(req, timeout=30) as resp:
            return resp.read()

    image_bytes = await asyncio.to_thread(_fetch)
    if image_bytes and len(image_bytes) > 1000:
        return image_bytes, "image/png"
    raise RuntimeError("이미지 생성 실패: 응답 없음")


async def _run_async(func, **kwargs):
    """동기 함수를 비동기로 실행."""
    import asyncio
    return await asyncio.to_thread(func, **kwargs)
