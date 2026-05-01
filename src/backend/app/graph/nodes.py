import asyncio
import json
import os
import re
import logging
import time
import uuid
from pathlib import Path
from langchain_core.messages import HumanMessage, AIMessage, SystemMessage

from app.graph.state import EduSessionState

logger = logging.getLogger(__name__)

_BACKEND_ROOT = Path(__file__).parent.parent.parent  # src/backend/
_PERSONA_PATH = _BACKEND_ROOT / "personas" / "TUTOR.md"
_DATA_DIR = _BACKEND_ROOT / "data"
_MAX_CARDS_PER_SESSION = 10

# 게임 관련 키워드 (기존 백업 코드에서 이식)
_GAME_CREATE_KEYWORDS = ["게임 만들", "게임 시작", "플레이", "놀자", "게임해", "시작해줘", "만들어줘"]
_GAME_EDIT_KEYWORDS = [
    "더 빠르게", "더 느리게", "어렵게", "쉽게", "적 추가", "아이템 추가",
    "시간 늘려", "시간 줄여", "점프 게임", "횡스크롤",
    "바꿔줘", "수정해줘", "변경해줘", "추가해줘", "없애줘", "지워줘",
    "색 바꿔", "색깔", "크게", "작게", "체력", "목숨", "점프", "배경",
]

_MOCK_CARD_RESPONSE = '''와, 토끼 전사 캐릭터를 만들었어! 귀도 쫑긋하고 너무 귀엽다!

```json
{"card_type":"character","name":"별빛 토끼 전사","description":"달빛 아래서 태어난 용감한 토끼. 친구들을 지키는 수호자야.","traits":["용감함","친절함","점프 마스터"],"world":"","image_prompt":"cute brave rabbit warrior","image_svg":"<svg xmlns=\'http://www.w3.org/2000/svg\' viewBox=\'0 0 200 200\'><circle cx=\'100\' cy=\'100\' r=\'50\' fill=\'#fef3c7\'/></svg>"}
```

💡 다음엔 "토끼가 사는 세계는 꽃이 가득한 숲이야"라고 해봐!'''


def _load_persona() -> str:
    if _PERSONA_PATH.exists():
        return _PERSONA_PATH.read_text(encoding="utf-8").strip()
    return ""


def _get_last_user_message(state: EduSessionState) -> str:
    for msg in reversed(state.get("messages", [])):
        if isinstance(msg, HumanMessage):
            return msg.content
    return ""


# ── 1. Intent 분류 ──
async def classify_intent_node(state: EduSessionState) -> dict:
    from app.llm import get_intent_llm
    user_msg = _get_last_user_message(state)

    # 키워드로 먼저 빠르게 분류
    has_game = bool(state.get("current_game_html"))
    if any(kw in user_msg for kw in _GAME_EDIT_KEYWORDS) and has_game:
        return {"intent": "game_edit"}
    if any(kw in user_msg for kw in _GAME_CREATE_KEYWORDS):
        return {"intent": "game_create"}

    # 애매한 경우 LLM에 위임 (session_context 포함)
    llm = get_intent_llm()
    ctx = state.get("session_context") or ""
    ctx_line = f"세션 요약: {ctx}\n" if ctx else ""
    prompt = (
        f'{ctx_line}'
        f'다음 아이의 메시지를 분류해. 반드시 아래 중 하나만 출력해:\n'
        f'card / game_create / game_edit / chitchat\n\n'
        f'메시지: "{user_msg}"\n'
        f'현재 캐릭터 카드 있음: {bool(state.get("latest_character"))}\n'
        f'현재 게임 진행 중: {has_game}\n\n'
        f'분류:'
    )
    response = await llm.ainvoke([HumanMessage(content=prompt)])
    intent = response.content.strip().lower()
    if intent not in ("card", "game_create", "game_edit", "chitchat"):
        intent = "card"  # 기본값
    return {"intent": intent}


# ── 2. 카드 생성 ──
async def generate_card_node(state: EduSessionState) -> dict:
    user_msg = _get_last_user_message(state)

    if os.getenv("MOCK_LLM") == "1":
        text = _MOCK_CARD_RESPONSE
        card_data = _extract_card_json(text)
        hint = _extract_hint(text)
        return {
            "card_result": card_data,
            "hint": hint or "💡 다음엔 세계를 만들어봐!",
            "token_usage": {},
        }

    from app.llm import get_card_llm
    llm = get_card_llm()

    persona = _load_persona()

    # 이전 카드 컨텍스트 주입
    context_parts: list[str] = []
    if state.get("latest_character"):
        context_parts.append(f"이전 카드 (character): {json.dumps(state['latest_character'], ensure_ascii=False)}")
    if state.get("latest_world"):
        context_parts.append(f"이전 카드 (world): {json.dumps(state['latest_world'], ensure_ascii=False)}")

    ctx = state.get("session_context") or ""
    if ctx:
        context_parts.insert(0, f"[세션 요약] {ctx}")
    full_user_msg = "\n".join(context_parts + [user_msg]) if context_parts else user_msg

    messages: list = []
    if persona:
        messages.append(SystemMessage(content=persona))
    messages.append(HumanMessage(content=full_user_msg))

    response = await llm.ainvoke(messages)
    text = response.content

    card_data = _extract_card_json(text)
    hint = _extract_hint(text)
    usage = getattr(response, "usage_metadata", {}) or {}

    import sys
    sys.path.insert(0, str(_BACKEND_ROOT))
    import storage as _storage
    await asyncio.to_thread(
        _storage.log_token_usage,
        state.get("session_id", ""),
        state.get("child_id", ""),
        state.get("tenant_id", "default"),
        "generate_card",
        usage.get("input_tokens", 0),
        usage.get("output_tokens", 0),
    )

    return {
        "card_result": card_data,
        "hint": hint or "💡 다음엔 세계를 만들어봐!",
        "token_usage": usage,
    }


# ── 3. 카드 저장 ──
async def save_card_node(state: EduSessionState) -> dict:
    import sys
    sys.path.insert(0, str(_BACKEND_ROOT))
    import storage as _storage

    card = state.get("card_result")
    if not card:
        return {}

    child_id = state["child_id"]
    session_id = state["session_id"]
    card_id = f"card_{uuid.uuid4().hex}"

    card_dir = (_DATA_DIR / "cards" / child_id / session_id).resolve()
    cards_base = (_DATA_DIR / "cards").resolve()
    if not card_dir.is_relative_to(cards_base):
        logger.error("경로 순회 감지: %s", card_dir)
        return {"error": "invalid path"}

    def _mkdir():
        card_dir.mkdir(parents=True, exist_ok=True)

    await asyncio.to_thread(_mkdir)

    # LRU: 세션당 최신 10개 유지
    existing = sorted(card_dir.glob("card_*.json"), key=lambda p: p.name)
    while len(existing) >= _MAX_CARDS_PER_SESSION:
        old_path = existing.pop(0)
        old_card_id = old_path.stem

        def _evict(p=old_path, cid=old_card_id):
            p.unlink(missing_ok=True)
            _storage.delete_card(session_id, cid)

        await asyncio.to_thread(_evict)

    card_json_str = json.dumps(card, ensure_ascii=False)
    card_path = card_dir / f"{card_id}.json"

    def _write():
        card_path.write_text(card_json_str, encoding="utf-8")

    await asyncio.to_thread(_write)

    backend_base = os.getenv("BACKEND_BASE_URL", "http://localhost:8000")
    card_url = f"{backend_base}/cards/{child_id}/{session_id}/{card_id}"

    await asyncio.to_thread(
        _storage.add_card,
        session_id, child_id, card_id, card.get("card_type", "character"), card_json_str, card_url,
    )

    # 어시스턴트 메시지 히스토리 보존
    hint = state.get("hint", "")
    if hint:
        await asyncio.to_thread(_storage.add_message, session_id, child_id, "assistant", hint)

    updates: dict = {"card_url": card_url}
    card_type = card.get("card_type")
    if card_type == "character":
        updates["latest_character"] = card
    elif card_type == "world":
        updates["latest_world"] = card

    return updates


_SPEC_SYSTEM = (
    "너는 게임 spec JSON generator다.\n"
    "오직 하나의 JSON 객체만 출력한다. 다음을 절대 출력하지 않는다:\n"
    "- 인사말, 설명, 마크다운\n"
    "- ```json / ```html / ```javascript 등 코드 펜스\n"
    "- card_type 필드 (이건 카드 페르소나 출력. spec과 무관)\n"
    "- HTML / JavaScript 코드\n\n"
    "출력은 반드시 `{`로 시작해 `}`로 끝나는 단일 JSON 객체.\n\n"
    "부품 라이브러리:\n"
    "player.movement: free | x_fixed | jump | swim\n"
    "spawns[].role: item | hazard | friend\n"
    "spawns[].from: top | bottom | left | right | alternating_lr | static_grid_bottom | wandering\n"
    "spawns[].motion: fall | rise | horizontal | sine | static | wandering\n"
    "spawns[].rate: 0~0.1 (스폰 빈도)\n"
    "spawns[].speed: 1~12\n"
    "spawns[].score_delta: 정수 (item=+1 default, hazard=-1 default)\n"
    "world.scroll: none | horizontal | parallax\n"
    "goal.time_limit: 0~180 (초, 0=무제한)\n"
    "goal.target_score: 0=목표 없음\n"
)

_SPEC_PARTS_PROMPT = (
    "\n요청을 바탕으로 game spec JSON을 생성해. "
    "반드시 player, spawns(1~3개), world, goal 모두 포함할 것."
)

SPEC_EDIT_SYSTEM = """너는 게임 spec JSON 패처야.
현재 spec JSON과 아이의 수정 요청이 주어진다.
요청에 해당하는 필드만 수정하고, 나머지는 그대로 둔다.
반드시 완전한 spec JSON 객체 하나만 출력한다. 코드 펜스, 설명 텍스트 금지.

수정 가이드:
- "더 빠르게" / "빠르게" → spawns 각 speed를 1.3~1.5배, player.speed +1~2
- "더 느리게" / "쉽게" → spawns 각 speed를 0.6~0.8배, player.speed -1
- "어렵게" → spawn rate 1.3배, time_limit -10
- "시간 늘려" / "시간 더" → goal.time_limit += 15 (최대 180)
- "시간 줄여" → goal.time_limit -= 10 (최소 10)
- "적 추가" / "위험 추가" → spawns에 hazard role spawn 추가
- "아이템 추가" / "별 더" → spawns에 item role spawn 추가 또는 rate *= 1.4
- "점프 게임" → player.movement = "jump", gravity = 0.7, jump_v = -13
- "횡스크롤" → world.scroll = "horizontal"
- "수영" / "바닷속" → player.movement = "swim"

출력은 반드시 {{ 로 시작해 }} 로 끝나는 단일 JSON."""


# ── 4. 새 게임 스펙 생성 ──
async def generate_spec_node(state: EduSessionState) -> dict:
    from app.llm import get_spec_llm
    llm = get_spec_llm()
    user_msg = _get_last_user_message(state)

    # 카드 컨텍스트 주입
    card_summary = ""
    char_card = state.get("latest_character")
    world_card = state.get("latest_world")
    if char_card:
        card_summary += f"\n캐릭터: {char_card.get('name', '?')} — {char_card.get('description', '')}"
    if world_card:
        card_summary += f"\n세계: {world_card.get('name', '?')} — {world_card.get('description', '')}"

    full_prompt = card_summary + "\n요청: " + user_msg + _SPEC_PARTS_PROMPT

    response = await llm.ainvoke([
        SystemMessage(content=_SPEC_SYSTEM),
        HumanMessage(content=full_prompt),
    ])
    spec = _extract_spec_json(response.content)
    usage = getattr(response, "usage_metadata", {}) or {}

    import sys
    sys.path.insert(0, str(_BACKEND_ROOT))
    import storage as _storage
    await asyncio.to_thread(
        _storage.log_token_usage,
        state.get("session_id", ""),
        state.get("child_id", ""),
        state.get("tenant_id", "default"),
        "generate_spec",
        usage.get("input_tokens", 0),
        usage.get("output_tokens", 0),
    )

    return {
        "current_spec": spec,
        "token_usage": usage,
    }


# ── 5. 게임 코드 직접 편집 ──

_CODE_EDIT_SYSTEM = """너는 HTML5 게임 코드 편집 전문가야.
사용자의 수정 요청에 따라 현재 게임 HTML을 수정하고, 수정된 완전한 HTML을 반환한다.

규칙:
1. 반드시 완전한 HTML 문서 전체를 반환한다 (<!DOCTYPE html>부터 </html>까지).
2. 캐릭터 SVG (// char_sprite: 주석 또는 data-char 속성 포함 요소) 는 절대 변경하지 않는다.
3. 게임 제목은 변경 요청이 없으면 그대로 유지한다.
4. 요청한 부분만 최소한으로 수정한다. 나머지 코드는 그대로 유지한다.
5. 외부 CDN, 이미지 URL, fetch() 사용 금지. 순수 HTML+JS+Canvas만 사용한다.
6. 병원 어린이 대상: 전투·죽음·폭력 요소는 추가하지 않는다.
"""

_MOCK_EDITED_HTML = """<!DOCTYPE html>
<html><head><meta charset="utf-8"><title>별 모으기!</title></head>
<body style="margin:0;background:#1a1a2e">
<canvas id="c" width="400" height="600"></canvas>
<script>
// SPEC: {"player":{"speed":8}}
const c = document.getElementById('c');
const ctx = c.getContext('2d');
// char_sprite: <svg viewBox='0 0 200 200'><circle cx='100' cy='100' r='80' fill='#FFB6C1'/></svg>
const player = {x:200, y:500, speed:8};
let score = 0;
function draw() {
  ctx.fillStyle='#1a1a2e'; ctx.fillRect(0,0,400,600);
  ctx.fillStyle='#FFB6C1'; ctx.fillRect(player.x-20,player.y-20,40,40);
  requestAnimationFrame(draw);
}
draw();
</script></body></html>"""


async def edit_code_node(state: EduSessionState) -> dict:
    current_html = state.get("current_game_html")
    if not current_html:
        # 편집할 게임이 없으면 새 게임 생성으로 전환
        return {"intent": "game_create"}

    # MOCK_LLM: speed 증가된 픽스처 HTML 반환
    if os.getenv("MOCK_LLM") == "1":
        return {"current_game_html": _MOCK_EDITED_HTML}

    from app.llm import get_edit_llm
    from pydantic import BaseModel, Field

    class _GameCodeOutput(BaseModel):
        html: str = Field(description="수정된 완전한 HTML 게임 코드 (<!DOCTYPE html>부터 </html>까지)")

    user_msg = _get_last_user_message(state)
    llm = get_edit_llm()
    structured_llm = llm.with_structured_output(_GameCodeOutput)

    ctx = state.get("session_context") or ""
    ctx_block = f"\n[세션 요약] {ctx}" if ctx else ""
    messages = [
        SystemMessage(content=_CODE_EDIT_SYSTEM + ctx_block),
        HumanMessage(content=(
            f"현재 게임 코드:\n\n{current_html}\n\n"
            f"수정 요청: {user_msg}"
        )),
    ]

    try:
        result = await structured_llm.ainvoke(messages)
        new_html = result.html if (result and result.html) else current_html
    except Exception as e:
        logger.warning(f"edit_code_node 구조화 출력 실패, 원본 유지: {e}")
        new_html = current_html

    import sys
    sys.path.insert(0, str(_BACKEND_ROOT))
    import storage as _storage
    await asyncio.to_thread(
        _storage.log_token_usage,
        state.get("session_id", ""),
        state.get("child_id", ""),
        state.get("tenant_id", "default"),
        "edit_code",
        0, 0,  # structured_output은 usage_metadata 미지원
    )

    return {"current_game_html": new_html}


# ── 6. 게임 빌드 (game_engine.py 재사용) ──
async def validate_and_build_node(state: EduSessionState) -> dict:
    import sys
    sys.path.insert(0, str(_BACKEND_ROOT))
    from game_engine import validate_spec, build_game_with_spec

    raw_spec = state.get("current_spec", {})
    char_card = state.get("latest_character")
    world_card = state.get("latest_world")

    char_svg = (char_card or {}).get("image_svg", "")
    world_svg = (world_card or {}).get("image_svg", "")
    char_name = (char_card or {}).get("name", "모험가")

    validated = validate_spec(raw_spec, char_svg=char_svg, world_svg=world_svg, char_name=char_name)
    html = build_game_with_spec(validated, char_card=char_card, world_card=world_card)
    return {"current_game_html": html}


# ── 7. 게임 저장 ──
async def save_game_node(state: EduSessionState) -> dict:
    import sys
    sys.path.insert(0, str(_BACKEND_ROOT))
    import storage as _storage

    html = state.get("current_game_html", "")
    if not html:
        return {}

    child_id = state["child_id"]
    session_id = state["session_id"]
    game_id = f"game_{uuid.uuid4().hex}"

    game_dir = (_DATA_DIR / "games" / child_id / session_id).resolve()
    games_base = (_DATA_DIR / "games").resolve()
    if not game_dir.is_relative_to(games_base):
        logger.error("경로 순회 감지: %s", game_dir)
        return {"error": "invalid path"}

    def _mkdir():
        game_dir.mkdir(parents=True, exist_ok=True)

    await asyncio.to_thread(_mkdir)

    game_file = game_dir / f"{game_id}.html"

    def _write():
        game_file.write_text(html, encoding="utf-8")

    await asyncio.to_thread(_write)

    backend_base = os.getenv("BACKEND_BASE_URL", "http://localhost:8000")
    game_url = f"{backend_base}/games/{child_id}/{session_id}/{game_id}"

    await asyncio.to_thread(
        _storage.add_game,
        session_id, child_id, game_id, str(game_file), game_url,
    )

    hint = "💡 다음엔 '더 빠르게 해줘'라고 해봐!"
    await asyncio.to_thread(_storage.add_message, session_id, child_id, "assistant", hint)

    return {"current_game_url": game_url, "hint": hint}


# ── 8. 잡담 ──
async def chitchat_node(state: EduSessionState) -> dict:
    from app.llm import get_card_llm
    llm = get_card_llm()
    user_msg = _get_last_user_message(state)
    ctx = state.get("session_context") or ""
    messages: list = []
    persona = _load_persona()
    if persona:
        messages.append(SystemMessage(content=persona))
    if ctx:
        messages.append(SystemMessage(content=f"[세션 요약] {ctx}"))
    messages.append(HumanMessage(content=user_msg))
    response = await llm.ainvoke(messages)
    return {"hint": "💡 캐릭터를 만들어볼까?"}


# ── 9. 롤링 컨텍스트 요약 ──

_SUMMARY_SYSTEM = """너는 아이 학습 세션 요약 전문가야.
이전 요약과 이번 턴 정보를 바탕으로 새 요약을 만든다.

규칙:
1. 200자 이내 한국어 불릿 없는 단문으로 작성.
2. 포함할 것: 만든 캐릭터명/특성, 게임 종류/특징, 아이가 표현한 선호(빠르게/색깔 등).
3. 이번 턴에서 변경된 내용은 이전 내용을 덮어씀.
4. 감정·칭찬·인사 같은 잡담 내용은 제외.
5. 아직 아무것도 없으면 빈 문자열 반환."""

_MOCK_SUMMARY = "캐릭터: 테스트용사(용감함). 게임: 별 모으기(낙하형, 속도3). 선호: 빠른 속도."


async def summarize_turn_node(state: EduSessionState) -> dict:
    if os.getenv("MOCK_LLM") == "1":
        return {"session_context": _MOCK_SUMMARY}

    from app.llm import get_summary_llm
    llm = get_summary_llm()

    prev_ctx = state.get("session_context") or ""
    user_msg = _get_last_user_message(state)

    # 이번 턴 결과 요약
    turn_facts: list[str] = []
    if state.get("card_result"):
        c = state["card_result"]
        turn_facts.append(f"카드생성: {c.get('card_type','?')} '{c.get('name','?')}' 특성={c.get('traits',[])}")
    if state.get("current_game_html"):
        turn_facts.append(f"게임상태: 게임 HTML 존재 (url={state.get('current_game_url','')})")
    turn_facts.append(f"아이 발화: {user_msg}")

    turn_block = "\n".join(turn_facts)
    prev_block = f"이전 요약: {prev_ctx}" if prev_ctx else "이전 요약: (없음)"

    prompt = f"{prev_block}\n이번 턴:\n{turn_block}\n\n새 요약:"
    try:
        response = await llm.ainvoke([
            SystemMessage(content=_SUMMARY_SYSTEM),
            HumanMessage(content=prompt),
        ])
        new_ctx = response.content.strip()
    except Exception as e:
        logger.warning(f"summarize_turn_node 실패, 이전 요약 유지: {e}")
        new_ctx = prev_ctx

    return {"session_context": new_ctx}


# ── 유틸 함수 ──
def _extract_card_json(text: str) -> dict | None:
    m = re.search(r"```json\s*([\s\S]*?)```", text)
    if m:
        try:
            return json.loads(m.group(1).strip())
        except json.JSONDecodeError:
            pass
    return None


def _extract_hint(text: str) -> str:
    for line in reversed(text.splitlines()):
        if line.strip().startswith("💡"):
            return line.strip()
    return ""


def _extract_spec_json(text: str) -> dict:
    # 코드 펜스 제거
    text = re.sub(r"```(?:json)?\s*", "", text).strip()
    # { ... } 추출
    m = re.search(r"\{[\s\S]*\}", text)
    if m:
        try:
            return json.loads(m.group())
        except json.JSONDecodeError:
            pass
    return {}


def _extract_and_merge_spec(text: str, current_spec: dict) -> dict:
    patched = _extract_spec_json(text)
    if not patched:
        return current_spec

    merged = dict(current_spec)

    # spawns: LLM이 수정한 경우 통째로 교체 (부분 병합 시 순서·타입 충돌 방지)
    if "spawns" in patched:
        merged["spawns"] = patched["spawns"]

    # player / goal / world: field-level merge (LLM이 누락한 필드는 원본 유지)
    for section in ("player", "goal", "world"):
        if section in patched:
            base = merged.get(section, {}) if isinstance(merged.get(section), dict) else {}
            merged[section] = {**base, **patched[section]}

    # 나머지 최상위 키 (char_sprite, title_msg 등 LLM이 포함하지 않은 필드 유지)
    for k, v in patched.items():
        if k not in ("spawns", "player", "goal", "world"):
            merged[k] = v

    # LLM이 패치에 포함하지 않은 최상위 필드는 current_spec에서 그대로 보존됨
    # (merged = dict(current_spec)으로 시작했으므로)

    return merged
