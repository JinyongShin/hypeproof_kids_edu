"""
WebSocket 핸들러 통합 테스트 — MOCK_LLM=1, in-memory checkpointer.
실제 LLM/DB 없이 astream_events 흐름과 WS 이벤트 프로토콜을 검증.
"""
import os
import json
import pytest
import asyncio
from unittest.mock import AsyncMock, MagicMock, patch

os.environ["MOCK_LLM"] = "1"

from langgraph.checkpoint.memory import InMemorySaver

from app.graph.graph import get_compiled_graph


# ---------------------------------------------------------------------------
# 헬퍼: FakeWebSocket — ws.send_json() 결과를 리스트로 수집
# ---------------------------------------------------------------------------

class FakeWebSocket:
    def __init__(self):
        self.sent: list[dict] = []

    async def send_json(self, data: dict):
        self.sent.append(data)

    def events_of_type(self, type_: str) -> list[dict]:
        return [e for e in self.sent if e.get("type") == type_]


# ---------------------------------------------------------------------------
# Fixture: 세션당 격리된 in-memory 그래프
# ---------------------------------------------------------------------------

@pytest.fixture
async def graph():
    # InMemorySaver 주입으로 SQLite 없이 격리 실행
    return await get_compiled_graph(checkpointer=InMemorySaver())


# ---------------------------------------------------------------------------
# 테스트 1: 카드 흐름 — done 이벤트 수신, session_id 포함
# ---------------------------------------------------------------------------

@pytest.mark.asyncio
async def test_card_flow_sends_done_with_session_id(graph):
    """
    카드 생성 요청 시 최종 done 이벤트에 session_id 가 포함돼야 한다.
    """
    from ws_handler import handle_chat_message

    ws = FakeWebSocket()
    await handle_chat_message(
        ws=ws,
        prompt="귀여운 토끼 캐릭터가 그리고 싶어",
        child_id="child-test",
        session_id="sess-card-01",
        graph=graph,
    )

    done_events = ws.events_of_type("done")
    assert len(done_events) == 1, f"done 이벤트 1개 기대, 실제: {ws.sent}"
    assert done_events[0]["session_id"] == "sess-card-01"


# ---------------------------------------------------------------------------
# 테스트 2: 카드 흐름 — card 이벤트 수신, card_json 파싱 가능
# ---------------------------------------------------------------------------

@pytest.mark.asyncio
async def test_card_flow_sends_card_event(graph):
    """
    MOCK_LLM=1 에서 카드 생성 후 card 이벤트가 발송되며
    card_json 이 유효한 JSON 문자열이어야 한다.
    게임 키워드를 포함하지 않는 프롬프트를 사용해 card 라우팅을 보장한다.
    """
    from ws_handler import handle_chat_message

    ws = FakeWebSocket()
    # "만들어줘" 는 게임 키워드이므로 사용하지 않음 — mock intent LLM 은 "card" 반환
    await handle_chat_message(
        ws=ws,
        prompt="귀여운 토끼 캐릭터가 그리고 싶어",
        child_id="child-test",
        session_id="sess-card-02",
        graph=graph,
    )

    card_events = ws.events_of_type("card")
    assert len(card_events) >= 1, f"card 이벤트 기대, 실제 이벤트: {ws.sent}"
    card_json_str = card_events[0].get("card_json", "")
    parsed = json.loads(card_json_str)
    assert isinstance(parsed, dict)


# ---------------------------------------------------------------------------
# 테스트 3: 게임 흐름 — game 이벤트 수신 + done에 game_url 포함
# ---------------------------------------------------------------------------

@pytest.mark.asyncio
async def test_game_flow_sends_game_and_done(graph):
    """
    게임 생성 요청 시 game 이벤트와 done 이벤트가 모두 발송되어야 하며
    done에 game_url 필드가 존재해야 한다.
    """
    from ws_handler import handle_chat_message

    ws = FakeWebSocket()
    await handle_chat_message(
        ws=ws,
        prompt="별을 모으는 게임 만들어줘",
        child_id="child-test",
        session_id="sess-game-01",
        graph=graph,
    )

    done_events = ws.events_of_type("done")
    game_events = ws.events_of_type("game")

    assert len(done_events) == 1, f"done 이벤트 1개 기대, 실제: {ws.sent}"
    assert len(game_events) >= 1, f"game 이벤트 기대, 실제: {ws.sent}"
    assert "game_url" in done_events[0]


# ---------------------------------------------------------------------------
# 테스트 4: 정상 프롬프트에서 error 이벤트 없음
# ---------------------------------------------------------------------------

@pytest.mark.asyncio
async def test_no_error_event_on_valid_prompt(graph):
    """
    정상 프롬프트 처리 중 error 이벤트가 발송되어선 안 된다.
    """
    from ws_handler import handle_chat_message

    ws = FakeWebSocket()
    await handle_chat_message(
        ws=ws,
        prompt="안녕! 나는 우주 탐험가야",
        child_id="child-test",
        session_id="sess-noerr-01",
        graph=graph,
    )

    error_events = ws.events_of_type("error")
    assert len(error_events) == 0, f"error 이벤트 예상치 못함: {error_events}"


# ---------------------------------------------------------------------------
# 테스트 5: 그래프 예외 발생 시 error 이벤트 발송
# ---------------------------------------------------------------------------

@pytest.mark.asyncio
async def test_error_event_sent_on_graph_exception():
    """
    그래프 실행 중 예외가 발생하면 error 타입 WS 이벤트를 발송해야 한다.
    ws_handler.py:156-158 의 except Exception 경로를 검증.
    """
    from ws_handler import handle_chat_message

    class BrokenGraph:
        """항상 예외를 던지는 가짜 그래프."""
        async def astream_events(self, *args, **kwargs):
            raise RuntimeError("테스트용 강제 오류")
            yield  # async generator 시그니처 유지

    ws = FakeWebSocket()
    await handle_chat_message(
        ws=ws,
        prompt="테스트",
        child_id="child-err",
        session_id="sess-err-01",
        graph=BrokenGraph(),
    )

    error_events = ws.events_of_type("error")
    assert len(error_events) == 1, f"error 이벤트 1개 기대, 실제: {ws.sent}"
    assert error_events[0].get("type") == "error"
