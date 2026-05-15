"""스펙 노드 단위 테스트 — MOCK_LLM=1 환경에서 실제 API 호출 없이 실행."""
import os
import pytest
from pathlib import Path
from langchain_core.messages import HumanMessage

os.environ["MOCK_LLM"] = "1"

from app.graph.state import EduSessionState
from app.graph.nodes import generate_spec_node, validate_and_build_node, save_game_node


@pytest.fixture(autouse=True)
def _patch_data_dir(monkeypatch, tmp_path):
    """파일 생성 테스트가 실제 data/ 를 오염시키지 않도록 _DATA_DIR 을 tmp_path 로 교체."""
    import app.graph.nodes as nodes_mod
    monkeypatch.setattr(nodes_mod, "_DATA_DIR", tmp_path)


def make_state(**kwargs) -> EduSessionState:
    defaults: EduSessionState = {
        "messages": [],
        "session_id": "test-session-spec",
        "child_id": "child-spec-test",
        "tenant_id": "default",
        "latest_character": None,
        "latest_world": None,
        "current_spec": None,
        "current_game_html": None,
        "current_game_url": None,
        "intent": None,
        "card_result": None,
        "card_url": None,
        "hint": None,
        "session_context": None,
        "token_usage": {},
        "error": None,
    }
    defaults.update(kwargs)
    return defaults


# ── generate_spec_node ──

async def test_generate_spec_returns_current_spec():
    state = make_state(messages=[HumanMessage(content="별 모으는 게임 만들어줘")])
    result = await generate_spec_node(state)
    assert "current_spec" in result
    assert isinstance(result["current_spec"], dict)


async def test_generate_spec_has_player():
    state = make_state(messages=[HumanMessage(content="게임 만들어줘")])
    result = await generate_spec_node(state)
    assert "player" in result["current_spec"]


async def test_generate_spec_has_spawns():
    state = make_state(messages=[HumanMessage(content="게임 만들어줘")])
    result = await generate_spec_node(state)
    assert "spawns" in result["current_spec"]
    assert isinstance(result["current_spec"]["spawns"], list)


async def test_generate_spec_has_goal():
    state = make_state(messages=[HumanMessage(content="게임 만들어줘")])
    result = await generate_spec_node(state)
    assert "goal" in result["current_spec"]


async def test_generate_spec_has_token_usage():
    state = make_state(messages=[HumanMessage(content="게임 만들어줘")])
    result = await generate_spec_node(state)
    assert "token_usage" in result


async def test_generate_spec_with_char_card_injects_context():
    char_card = {
        "card_type": "character",
        "name": "별빛 토끼",
        "description": "달빛 아래서 태어난 용감한 토끼",
        "image_svg": "<svg></svg>",
    }
    state = make_state(
        messages=[HumanMessage(content="별 모으는 게임")],
        latest_character=char_card,
    )
    result = await generate_spec_node(state)
    assert result["current_spec"] is not None


async def test_generate_spec_with_world_card():
    world_card = {
        "card_type": "world",
        "name": "꽃별 왕국",
        "description": "꽃이 가득한 반짝이는 세계",
        "image_svg": "<svg></svg>",
    }
    state = make_state(
        messages=[HumanMessage(content="장애물 피하는 게임")],
        latest_world=world_card,
    )
    result = await generate_spec_node(state)
    assert result["current_spec"] is not None


# ── validate_and_build_node ──

async def test_validate_and_build_returns_html():
    spec = {
        "player": {"movement": "free", "speed": 5},
        "spawns": [{"role": "item", "sprite": "⭐", "from": "top", "motion": "fall", "rate": 0.03}],
        "world": {"scroll": "none"},
        "goal": {"time_limit": 45, "target_score": 0},
    }
    state = make_state(current_spec=spec)
    result = await validate_and_build_node(state)
    assert "current_game_html" in result
    assert isinstance(result["current_game_html"], str)


async def test_validate_and_build_html_contains_canvas():
    spec = {
        "player": {"movement": "free", "speed": 5},
        "spawns": [{"role": "item", "sprite": "⭐", "from": "top", "motion": "fall", "rate": 0.03}],
        "world": {"scroll": "none"},
        "goal": {"time_limit": 45, "target_score": 0},
    }
    state = make_state(current_spec=spec)
    result = await validate_and_build_node(state)
    assert "<canvas" in result["current_game_html"]


async def test_validate_and_build_html_is_complete_document():
    spec = {
        "player": {"movement": "free"},
        "spawns": [],
        "world": {"scroll": "none"},
        "goal": {"time_limit": 30, "target_score": 0},
    }
    state = make_state(current_spec=spec)
    result = await validate_and_build_node(state)
    html = result["current_game_html"]
    assert "<!DOCTYPE html>" in html or "<!doctype html>" in html.lower()


async def test_validate_and_build_with_char_card():
    spec = {
        "player": {"movement": "free", "speed": 5},
        "spawns": [{"role": "item", "sprite": "⭐", "from": "top", "motion": "fall", "rate": 0.03}],
        "world": {"scroll": "none"},
        "goal": {"time_limit": 45, "target_score": 0},
    }
    char_card = {
        "card_type": "character",
        "name": "별빛 토끼",
        "description": "용감한 토끼",
        "image_svg": "<svg viewBox='0 0 200 200'><circle cx='100' cy='100' r='80' fill='#FFB6C1'/></svg>",
    }
    state = make_state(current_spec=spec, latest_character=char_card)
    result = await validate_and_build_node(state)
    assert result["current_game_html"]


async def test_validate_and_build_empty_spec_uses_defaults():
    state = make_state(current_spec={})
    result = await validate_and_build_node(state)
    assert result["current_game_html"]


# ── save_game_node ──

async def test_save_game_returns_game_url():
    spec = {
        "player": {"movement": "free", "speed": 5},
        "spawns": [{"role": "item", "sprite": "⭐", "from": "top", "motion": "fall", "rate": 0.03}],
        "world": {"scroll": "none"},
        "goal": {"time_limit": 45, "target_score": 0},
    }
    build_state = make_state(current_spec=spec)
    build_result = await validate_and_build_node(build_state)

    save_state = make_state(
        current_game_html=build_result["current_game_html"],
        child_id="child-save-test",
        session_id="sess-save-test",
    )
    result = await save_game_node(save_state)
    assert "current_game_url" in result
    assert result["current_game_url"]


async def test_save_game_url_contains_child_id():
    spec = {
        "player": {"movement": "free"},
        "spawns": [{"role": "item", "sprite": "⭐", "from": "top", "motion": "fall", "rate": 0.03}],
        "world": {"scroll": "none"},
        "goal": {"time_limit": 30, "target_score": 0},
    }
    build_state = make_state(current_spec=spec)
    build_result = await validate_and_build_node(build_state)

    save_state = make_state(
        current_game_html=build_result["current_game_html"],
        child_id="child-url-test",
        session_id="sess-url-test",
    )
    result = await save_game_node(save_state)
    assert "child-url-test" in result["current_game_url"]


async def test_save_game_has_hint():
    spec = {
        "player": {"movement": "free"},
        "spawns": [{"role": "item", "sprite": "⭐", "from": "top", "motion": "fall", "rate": 0.03}],
        "world": {"scroll": "none"},
        "goal": {"time_limit": 30, "target_score": 0},
    }
    build_state = make_state(current_spec=spec)
    build_result = await validate_and_build_node(build_state)

    save_state = make_state(
        current_game_html=build_result["current_game_html"],
        child_id="child-hint-test",
        session_id="sess-hint-test",
    )
    result = await save_game_node(save_state)
    assert "hint" in result
    assert result["hint"]


async def test_save_game_creates_html_file():
    spec = {
        "player": {"movement": "free", "speed": 5},
        "spawns": [{"role": "item", "sprite": "⭐", "from": "top", "motion": "fall", "rate": 0.03}],
        "world": {"scroll": "none"},
        "goal": {"time_limit": 45, "target_score": 0},
    }
    build_state = make_state(current_spec=spec)
    build_result = await validate_and_build_node(build_state)

    save_state = make_state(
        current_game_html=build_result["current_game_html"],
        child_id="child-file-game-test",
        session_id="sess-file-game-test",
    )
    await save_game_node(save_state)

    import app.graph.nodes as nodes_mod
    game_dir = nodes_mod._DATA_DIR / "games" / "child-file-game-test" / "sess-file-game-test"
    html_files = list(game_dir.glob("game_*.html"))
    assert len(html_files) >= 1


async def test_save_game_no_html_returns_empty():
    state = make_state(current_game_html=None)
    result = await save_game_node(state)
    assert result == {}


# ── 통합: generate_spec → validate_and_build → save_game ──

async def test_full_spec_pipeline():
    state = make_state(messages=[HumanMessage(content="별 모으는 게임 만들어줘")])

    spec_result = await generate_spec_node(state)
    assert spec_result["current_spec"]

    build_state = make_state(current_spec=spec_result["current_spec"])
    build_result = await validate_and_build_node(build_state)
    assert build_result["current_game_html"]

    save_state = make_state(
        current_game_html=build_result["current_game_html"],
        child_id="child-pipeline-test",
        session_id="sess-pipeline-test",
    )
    save_result = await save_game_node(save_state)
    assert save_result["current_game_url"]
    assert "child-pipeline-test" in save_result["current_game_url"]
