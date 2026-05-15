"""카드 노드 단위 테스트 — MOCK_LLM=1 환경에서 실제 API 호출 없이 실행."""
import os
import json
import pytest
from pathlib import Path
from langchain_core.messages import HumanMessage

os.environ["MOCK_LLM"] = "1"

import pytest
from app.graph.state import EduSessionState
from app.graph.nodes import generate_card_node, save_card_node


@pytest.fixture(autouse=True)
def _patch_data_dir(monkeypatch, tmp_path):
    """파일 생성 테스트가 실제 data/ 를 오염시키지 않도록 _DATA_DIR 을 tmp_path 로 교체."""
    import app.graph.nodes as nodes_mod
    monkeypatch.setattr(nodes_mod, "_DATA_DIR", tmp_path)


def make_state(**kwargs) -> EduSessionState:
    defaults: EduSessionState = {
        "messages": [],
        "session_id": "test-session",
        "child_id": "child-test",
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


# ── generate_card_node ──

async def test_generate_card_returns_card_result():
    state = make_state(messages=[HumanMessage(content="용감한 토끼 캐릭터 만들어줘")])
    result = await generate_card_node(state)
    assert "card_result" in result
    assert result["card_result"] is not None


async def test_generate_card_result_has_card_type():
    state = make_state(messages=[HumanMessage(content="캐릭터 만들어줘")])
    result = await generate_card_node(state)
    assert result["card_result"]["card_type"] == "character"


async def test_generate_card_has_hint():
    state = make_state(messages=[HumanMessage(content="캐릭터 만들어줘")])
    result = await generate_card_node(state)
    assert "hint" in result
    assert result["hint"]


async def test_generate_card_hint_starts_with_bulb():
    state = make_state(messages=[HumanMessage(content="캐릭터 만들어줘")])
    result = await generate_card_node(state)
    assert result["hint"].startswith("💡")


async def test_generate_card_has_token_usage():
    state = make_state(messages=[HumanMessage(content="캐릭터 만들어줘")])
    result = await generate_card_node(state)
    assert "token_usage" in result


# ── save_card_node ──

async def test_save_card_returns_card_url():
    card = {"card_type": "character", "name": "별빛 토끼 전사", "description": "용감한 토끼"}
    state = make_state(
        messages=[HumanMessage(content="캐릭터 만들어줘")],
        card_result=card,
        hint="💡 다음엔 세계를 만들어봐!",
    )
    result = await save_card_node(state)
    assert "card_url" in result
    assert result["card_url"]


async def test_save_card_url_contains_child_id():
    card = {"card_type": "character", "name": "루나", "description": "달빛 요정"}
    state = make_state(
        messages=[HumanMessage(content="캐릭터 만들어줘")],
        card_result=card,
        child_id="child-abc",
        session_id="sess-xyz",
    )
    result = await save_card_node(state)
    assert "child-abc" in result["card_url"]


async def test_save_card_character_updates_latest_character():
    card = {"card_type": "character", "name": "루나", "description": "달빛 요정"}
    state = make_state(card_result=card, messages=[HumanMessage(content="캐릭터")])
    result = await save_card_node(state)
    assert result.get("latest_character") == card


async def test_save_card_world_updates_latest_world():
    card = {"card_type": "world", "name": "별빛 왕국", "description": "반짝이는 세계"}
    state = make_state(card_result=card, messages=[HumanMessage(content="세계")])
    result = await save_card_node(state)
    assert result.get("latest_world") == card


async def test_save_card_no_card_result_returns_empty():
    state = make_state(card_result=None)
    result = await save_card_node(state)
    assert result == {}


async def test_save_card_creates_json_file():
    card = {"card_type": "character", "name": "파일저장테스트", "description": "테스트용"}
    state = make_state(
        card_result=card,
        child_id="child-file-test",
        session_id="sess-file-test",
        messages=[HumanMessage(content="테스트")],
    )
    await save_card_node(state)

    import app.graph.nodes as nodes_mod
    card_dir = nodes_mod._DATA_DIR / "cards" / "child-file-test" / "sess-file-test"
    json_files = list(card_dir.glob("card_*.json"))
    assert len(json_files) >= 1


async def test_save_card_json_file_content():
    card = {"card_type": "world", "name": "파일내용테스트", "description": "내용확인용"}
    state = make_state(
        card_result=card,
        child_id="child-content-test",
        session_id="sess-content-test",
        messages=[HumanMessage(content="테스트")],
    )
    await save_card_node(state)

    import app.graph.nodes as nodes_mod
    card_dir = nodes_mod._DATA_DIR / "cards" / "child-content-test" / "sess-content-test"
    json_files = sorted(card_dir.glob("card_*.json"))
    assert json_files
    saved = json.loads(json_files[-1].read_text(encoding="utf-8"))
    assert saved["card_type"] == "world"
    assert saved["name"] == "파일내용테스트"
