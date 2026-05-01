"""라우팅 단위 테스트 — MOCK_LLM=1 환경에서 실제 API 호출 없이 실행."""
import os
import pytest
from langchain_core.messages import HumanMessage

os.environ.setdefault("MOCK_LLM", "1")

from app.graph.state import EduSessionState
from app.graph.edges import (
    route_after_classify,
    route_after_generate_card,
    route_after_spec,
)
from app.graph.nodes import classify_intent_node


def make_state(**kwargs) -> EduSessionState:
    defaults: EduSessionState = {
        "messages": [],
        "session_id": "test-session",
        "child_id": "child-1",
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


# ── route_after_classify ──

def test_route_classify_card():
    state = make_state(intent="card")
    assert route_after_classify(state) == "generate_card"


def test_route_classify_game_create():
    state = make_state(intent="game_create")
    assert route_after_classify(state) == "generate_spec"


def test_route_classify_game_edit_with_html():
    state = make_state(intent="game_edit", current_game_html="<html>...</html>")
    assert route_after_classify(state) == "edit_code"


def test_route_classify_game_edit_without_spec_falls_back():
    state = make_state(intent="game_edit", current_spec=None)
    assert route_after_classify(state) == "generate_spec"


def test_route_classify_chitchat():
    state = make_state(intent="chitchat")
    assert route_after_classify(state) == "chitchat"


def test_route_classify_unknown_defaults_to_chitchat():
    state = make_state(intent="totally_unknown_intent")
    assert route_after_classify(state) == "chitchat"


# ── route_after_generate_card ──

def test_route_card_with_result():
    state = make_state(card_result={"card_type": "character", "name": "루나"})
    assert route_after_generate_card(state) == "save_card"


def test_route_card_no_result():
    state = make_state(card_result=None)
    assert route_after_generate_card(state) == "__end__"


def test_route_card_error():
    state = make_state(card_result={"card_type": "character"}, error="LLM timeout")
    assert route_after_generate_card(state) == "__end__"


# ── route_after_spec ──

def test_route_spec_present():
    state = make_state(current_spec={"type": "platformer"})
    assert route_after_spec(state) == "validate_and_build"


def test_route_spec_absent():
    state = make_state(current_spec=None)
    assert route_after_spec(state) == "__end__"


def test_route_spec_empty_dict():
    state = make_state(current_spec={})
    assert route_after_spec(state) == "__end__"


# ── classify_intent_node (async, keyword path) ──

@pytest.mark.anyio
async def test_classify_game_create_keyword():
    state = make_state(messages=[HumanMessage(content="게임 만들어줘!")])
    result = await classify_intent_node(state)
    assert result["intent"] == "game_create"


@pytest.mark.anyio
async def test_classify_game_edit_keyword_with_html():
    state = make_state(
        messages=[HumanMessage(content="더 빠르게 해줘")],
        current_game_html="<html>...</html>",
    )
    result = await classify_intent_node(state)
    assert result["intent"] == "game_edit"


@pytest.mark.anyio
async def test_classify_game_edit_keyword_without_html_falls_to_llm():
    # current_game_html 없으면 키워드 분기를 타지 않고 LLM에 위임 → mock returns "card"
    state = make_state(
        messages=[HumanMessage(content="더 빠르게 해줘")],
        current_game_html=None,
    )
    result = await classify_intent_node(state)
    # mock LLM은 "card"를 반환하므로 intent는 "card"
    assert result["intent"] == "card"
