"""
Google GenAI 클라이언트 — claude_runner 대체.
Gemini 2.5 Flash (텍스트) + 이미지 생성 (Nano Banana) 통합.
"""

import json
import logging
import os
import time
from dataclasses import dataclass
from pathlib import Path

import storage

logger = logging.getLogger(__name__)

_BACKEND_ROOT = Path(__file__).parent
_PERSONA_DIR = _BACKEND_ROOT / "personas"
_DATA_DIR = _BACKEND_ROOT / "data"

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY", "")
GEMINI_TEXT_MODEL = os.getenv("GEMINI_TEXT_MODEL", "gemini-2.5-flash")
GEMINI_IMAGE_MODEL = os.getenv("GEMINI_IMAGE_MODEL", "gemini-2.0-flash-exp")
MOCK_MODE = os.getenv("MOCK_GENAI", "0") == "1"

_MAX_CARDS_PER_SESSION = 10

_MOCK_CARD_RESPONSE = '''와, 토끼 전사 캐릭터를 만들었어! 귀도 쫑긋하고 너무 귀엽다!

```json
{"card_type":"character","name":"별빛 토끼 전사","description":"달빛 아래서 태어난 용감한 토끼. 친구들을 지키는 수호자야.","traits":["용김","친절함","점프 마스터"],"world":"","image_prompt":"cute brave rabbit warrior with long ears, wearing light armor with star patterns, soft pastel colors, friendly expression, chibi style, magical sparkles"}
```

💡 다음엔 "토끼가 사는 세계는 꽃이 가득한 숲이야"라고 해봐!'''


@dataclass
class StreamEvent:
    type: str  # "text" | "card" | "image" | "done" | "error"
    chunk: str = ""
    card_json: str = ""
    card_url: str = ""
    image_url: str = ""
    image_data: bytes = b""
    hint: str = ""


def _load_persona() -> str:
    path = _PERSONA_DIR / "TUTOR.md"
    if path.exists():
        return path.read_text(encoding="utf-8").strip()
    return ""


def _extract_hint(text: str) -> str:
    for line in reversed(text.splitlines()):
        line = line.strip()
        if line.startswith("💡"):
            return line
    return ""


def _extract_card_json(text: str) -> str | None:
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

    try:
        from google import genai
    except ImportError:
        logger.error("google-genai 패키지 미설치. pip install google-genai")
        yield StreamEvent(type="error", chunk=_friendly_error("not_found"))
        return

    if not GEMINI_API_KEY:
        logger.error("GEMINI_API_KEY 미설정")
        yield StreamEvent(type="error", chunk=_friendly_error("not_found"))
        return

    client = genai.Client(api_key=GEMINI_API_KEY)
    persona = _load_persona()

    full_text = ""
    try:
        # 프롬프트 구성
        system_prompt = persona if persona else ""
        contents = prompt

        response = await _run_async(
            client.models.generate_content,
            model=GEMINI_TEXT_MODEL,
            contents=contents,
            config=genai.types.GenerateContentConfig(
                system_instruction=system_prompt if system_prompt else None,
                temperature=0.9,
            )
        )

        if response.text:
            full_text = response.text
            yield StreamEvent(type="text", chunk=full_text)

        # 카드 JSON 추출
        card_json_str = _extract_card_json(full_text)
        card_url = ""
        if card_json_str:
            card_id = f"card_{int(time.time() * 1000)}"
            card_url = _save_card(card_id, child_id, session_id, card_json_str)
            yield StreamEvent(type="card", card_json=card_json_str, card_url=card_url)

        yield StreamEvent(
            type="done",
            hint=_extract_hint(full_text),
            card_url=card_url,
        )

    except Exception as e:
        logger.exception("[%s::%s] generate_card 오류: %s", child_id, session_id, e)
        yield StreamEvent(type="error", chunk=_friendly_error("generic"))


async def generate_image(image_prompt: str) -> tuple[bytes, str]:
    """
    Nano Banana로 이미지 생성.
    Returns: (image_bytes, mime_type)
    """
    if MOCK_MODE:
        # Mock: 1x1 투명 PNG
        import base64
        mock_png = base64.b64decode(
            "iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAYAAAAfFcSJAAAADUlEQVR42mNkYPj/HwADBwIAMCbHYQAAAABJRU5ErkJggg=="
        )
        return mock_png, "image/png"

    try:
        from google import genai
    except ImportError:
        raise RuntimeError("google-genai 패키지 미설치")

    client = genai.Client(api_key=GEMINI_API_KEY)

    response = await _run_async(
        client.models.generate_content,
        model=GEMINI_IMAGE_MODEL,
        contents=f"Create a cute, child-friendly illustration: {image_prompt}. Style: chibi, soft pastel colors, magical, wholesome.",
        config=genai.types.GenerateContentConfig(
            response_modalities=["IMAGE", "TEXT"],
            temperature=1.0,
        )
    )

    for part in response.candidates[0].content.parts:
        if part.inline_data is not None:
            return part.inline_data.data, part.inline_data.mime_type

    raise RuntimeError("이미지 생성 실패: 응답에 이미지 없음")


async def _run_async(func, **kwargs):
    """동기 함수를 비동기로 실행."""
    import asyncio
    return await asyncio.to_thread(func, **kwargs)
