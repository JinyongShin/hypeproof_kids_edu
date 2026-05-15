"""
게임 코드 편집 루프 테스트. MOCK_LLM=1 환경에서 API 키 없이 실행 가능.
핵심: edit_code_node가 현재 HTML을 보고 수정된 HTML을 반환하는지 검증.
"""
import os
import pytest

os.environ["MOCK_LLM"] = "1"

from langchain_core.messages import HumanMessage

SAMPLE_HTML = """<!DOCTYPE html>
<html><head><meta charset="utf-8"><title>별 모으기!</title></head>
<body style="margin:0;background:#1a1a2e">
<canvas id="c" width="400" height="600"></canvas>
<script>
// SPEC: {"player":{"speed":3}}
// char_sprite: <svg viewBox='0 0 200 200'><circle cx='100' cy='100' r='80' fill='#FFB6C1'/></svg>
const player = {x:200, y:500, speed:3};
let score = 0;
function draw() {
  requestAnimationFrame(draw);
}
draw();
</script></body></html>"""

SAMPLE_CHARACTER = {
    "card_type": "character",
    "name": "테스트 용사",
    "image_svg": "<svg viewBox='0 0 200 200'><circle cx='100' cy='100' r='80' fill='#FFB6C1'/></svg>",
}


def make_state(**kwargs):
    from app.graph.state import EduSessionState
    base: EduSessionState = {
        "messages": [], "session_id": "edit-session", "child_id": "edit-child",
        "tenant_id": "default", "latest_character": SAMPLE_CHARACTER, "latest_world": None,
        "current_spec": None, "current_game_html": None, "current_game_url": None,
        "intent": "game_edit", "card_result": None, "card_url": None,
        "hint": None, "session_context": None, "token_usage": {}, "error": None,
    }
    base.update(kwargs)
    return base


# ── edit_code_node ──

@pytest.mark.asyncio
async def test_edit_code_returns_html():
    """'더 빠르게 해줘' → 유효한 HTML이 반환되어야 함."""
    from app.graph.nodes import edit_code_node
    state = make_state(
        messages=[HumanMessage(content="더 빠르게 해줘")],
        current_game_html=SAMPLE_HTML,
    )
    result = await edit_code_node(state)
    html = result.get("current_game_html", "")
    assert "<!DOCTYPE" in html.upper() or "<html" in html.lower()


@pytest.mark.asyncio
async def test_edit_code_speed_increased():
    """MOCK 응답에서 player.speed가 원본(3)보다 높아야 함."""
    from app.graph.nodes import edit_code_node
    state = make_state(
        messages=[HumanMessage(content="더 빠르게 해줘")],
        current_game_html=SAMPLE_HTML,
    )
    result = await edit_code_node(state)
    html = result.get("current_game_html", "")
    # MOCK HTML에 speed:8 포함됨
    assert "speed:8" in html or "speed: 8" in html


@pytest.mark.asyncio
async def test_edit_code_preserves_char_sprite():
    """편집 후 char_sprite SVG 주석이 보존되어야 함."""
    from app.graph.nodes import edit_code_node
    state = make_state(
        messages=[HumanMessage(content="더 빠르게 해줘")],
        current_game_html=SAMPLE_HTML,
    )
    result = await edit_code_node(state)
    html = result.get("current_game_html", "")
    # MOCK HTML에도 char_sprite 주석 포함
    assert "char_sprite" in html


@pytest.mark.asyncio
async def test_edit_code_no_current_html_fallback():
    """current_game_html이 없으면 game_create 인텐트로 폴백해야 함."""
    from app.graph.nodes import edit_code_node
    state = make_state(
        messages=[HumanMessage(content="더 빠르게 해줘")],
        current_game_html=None,
    )
    result = await edit_code_node(state)
    # HTML 없이 intent만 변경
    assert result.get("intent") == "game_create"
    assert "current_game_html" not in result or not result.get("current_game_html")


@pytest.mark.asyncio
async def test_edit_code_empty_html_fallback():
    """current_game_html이 빈 문자열이어도 안전하게 폴백해야 함."""
    from app.graph.nodes import edit_code_node
    state = make_state(
        messages=[HumanMessage(content="더 빠르게 해줘")],
        current_game_html="",
    )
    result = await edit_code_node(state)
    assert result.get("intent") == "game_create"


# ── route_after_edit_code ──

def test_route_after_edit_code_with_html():
    """HTML이 있으면 save_game으로 라우팅해야 함."""
    from app.graph.edges import route_after_edit_code
    state = make_state(current_game_html="<html>...</html>")
    assert route_after_edit_code(state) == "save_game"


def test_route_after_edit_code_without_html():
    """HTML이 없으면 generate_spec으로 폴백해야 함."""
    from app.graph.edges import route_after_edit_code
    state = make_state(current_game_html=None)
    assert route_after_edit_code(state) == "generate_spec"


# ── 편집 후 저장까지 전체 루프 ──

@pytest.mark.asyncio
async def test_edit_then_save_produces_game_url(tmp_path, monkeypatch):
    """edit_code → save_game 전체 루프가 game_url을 반환해야 함."""
    import sys
    sys.path.insert(0, str(__file__.replace("tests/test_edit_loop.py", "")))

    monkeypatch.setenv("MOCK_LLM", "1")
    monkeypatch.setenv("BACKEND_BASE_URL", "http://localhost:8000")

    # save_game_node가 data/ 디렉터리를 쓰므로 tmp_path로 패치
    import app.graph.nodes as nodes_mod
    monkeypatch.setattr(nodes_mod, "_DATA_DIR", tmp_path)

    # SQLite 연산 stub
    import storage as _storage
    monkeypatch.setattr(_storage, "add_game", lambda *a, **kw: None)
    monkeypatch.setattr(_storage, "add_message", lambda *a, **kw: None)

    from app.graph.nodes import edit_code_node, save_game_node

    # Step 1: 편집
    edit_state = make_state(
        messages=[HumanMessage(content="더 빠르게 해줘")],
        current_game_html=SAMPLE_HTML,
    )
    edit_result = await edit_code_node(edit_state)

    # Step 2: 저장
    save_state = make_state(
        current_game_html=edit_result.get("current_game_html", SAMPLE_HTML),
    )
    save_result = await save_game_node(save_state)

    assert save_result.get("current_game_url", "").startswith("http://localhost:8000/games/")
