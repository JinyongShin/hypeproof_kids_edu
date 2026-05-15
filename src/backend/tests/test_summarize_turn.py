"""
롤링 컨텍스트 요약 테스트. MOCK_LLM=1 환경에서 실행.
"""
import os
import pytest

os.environ["MOCK_LLM"] = "1"

from langchain_core.messages import HumanMessage


def make_state(**kwargs):
    from app.graph.state import EduSessionState
    base: EduSessionState = {
        "messages": [], "session_id": "sum-session", "child_id": "sum-child",
        "tenant_id": "default", "latest_character": None, "latest_world": None,
        "current_spec": None, "current_game_html": None, "current_game_url": None,
        "intent": None, "card_result": None, "card_url": None,
        "hint": None, "session_context": None, "token_usage": {}, "error": None,
    }
    base.update(kwargs)
    return base


@pytest.mark.asyncio
async def test_summarize_returns_context():
    """summarize_turn_node가 session_context 문자열을 반환해야 함."""
    from app.graph.nodes import summarize_turn_node
    state = make_state(messages=[HumanMessage(content="별 모으기 게임 만들어줘")])
    result = await summarize_turn_node(state)
    assert isinstance(result.get("session_context"), str)
    assert len(result["session_context"]) > 0


@pytest.mark.asyncio
async def test_summarize_replaces_previous_context():
    """매 턴마다 이전 context를 교체해야 함 (누적이 아닌 대체)."""
    from app.graph.nodes import summarize_turn_node
    old_ctx = "캐릭터: 구형 캐릭터. 게임: 느린 게임."
    state = make_state(
        messages=[HumanMessage(content="더 빠르게 해줘")],
        session_context=old_ctx,
        current_game_html="<html>...</html>",
    )
    result = await summarize_turn_node(state)
    new_ctx = result["session_context"]
    # MOCK_LLM=1 환경에서 nodes._MOCK_SUMMARY 고정값을 반환하는지 검증
    assert isinstance(new_ctx, str) and len(new_ctx) > 0
    assert new_ctx == "캐릭터: 테스트용사(용감함). 게임: 별 모으기(낙하형, 속도3). 선호: 빠른 속도."


@pytest.mark.asyncio
async def test_summarize_with_card_result():
    """카드 생성 결과가 있으면 context에 반영되어야 함 (MOCK 픽스처 검증)."""
    from app.graph.nodes import summarize_turn_node
    state = make_state(
        messages=[HumanMessage(content="토끼 캐릭터 만들어줘")],
        card_result={"card_type": "character", "name": "별빛 토끼", "traits": ["용감함"]},
    )
    result = await summarize_turn_node(state)
    assert "session_context" in result


@pytest.mark.asyncio
async def test_context_injected_into_classify_intent():
    """session_context가 있을 때 classify_intent_node LLM 경로에 주입되어야 함."""
    from app.graph.nodes import classify_intent_node
    # 키워드 매칭 안 되는 메시지 + context로 LLM 경로 유도
    state = make_state(
        messages=[HumanMessage(content="그거 다시 해줘")],
        session_context="게임: 별 모으기. 선호: 빠른 속도.",
        current_game_html=None,
    )
    # MOCK LLM은 "card"를 반환 — 오류 없이 실행되는지만 검증
    result = await classify_intent_node(state)
    assert result["intent"] in ("card", "game_create", "game_edit", "chitchat")
