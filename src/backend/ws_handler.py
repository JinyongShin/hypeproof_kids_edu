"""
WebSocket 핸들러 — LangGraph 그래프와 WebSocket 브릿지.
astream_events v2 로 스트리밍 토큰을 WS 이벤트로 변환.
"""
import json
import logging
from fastapi import WebSocket

from app.config import get_settings
from app.checkpointer import get_thread_config

logger = logging.getLogger(__name__)

# LangGraph 그래프 노드 이름 (graph.py g.add_node() 에 등록된 이름 그대로)
_STREAMING_NODES = {"generate_card", "chitchat"}


def _get_langfuse_callback():
    """Langfuse 활성화 시 CallbackHandler 반환, 비활성화 시 None."""
    settings = get_settings()
    if not settings.LANGFUSE_ENABLED:
        return None
    try:
        from langfuse.callback import CallbackHandler
        return CallbackHandler(
            public_key=settings.LANGFUSE_PUBLIC_KEY,
            secret_key=settings.LANGFUSE_SECRET_KEY,
            host=settings.LANGFUSE_HOST,
        )
    except Exception as e:
        logger.warning(f"Langfuse 초기화 실패 (무시하고 계속): {e}")
        return None


async def handle_chat_message(
    ws: WebSocket,
    prompt: str,
    child_id: str,
    session_id: str,
    graph,
):
    """
    WebSocket 메시지를 받아 LangGraph 그래프를 astream_events v2 로 실행하고
    WS 이벤트(text/card/game/done/error)로 스트리밍.
    """
    from langchain_core.messages import HumanMessage

    config = get_thread_config(session_id)
    langfuse_cb = _get_langfuse_callback()
    if langfuse_cb:
        config["callbacks"] = [langfuse_cb]

    # 스트리밍 중 card/game 이벤트 발송 여부 추적
    card_sent = False
    game_sent = False

    try:
        async for event in graph.astream_events(
            {
                "messages": [HumanMessage(content=prompt)],
                "session_id": session_id,
                "child_id": child_id,
                "tenant_id": "default",
                "token_usage": {},
            },
            config=config,
            version="v2",
        ):
            kind = event["event"]
            node_name = event.get("metadata", {}).get("langgraph_node", "")

            # LLM 토큰 스트리밍 — 텍스트 생성 노드만
            if kind == "on_chat_model_stream" and node_name in _STREAMING_NODES:
                chunk = event["data"].get("chunk")
                if chunk and hasattr(chunk, "content") and chunk.content:
                    await ws.send_json({"type": "text", "chunk": chunk.content})

            # 노드 완료 — 카드 또는 게임 결과 전송 시도
            elif kind == "on_chain_end":
                output = event.get("data", {}).get("output") or {}
                if not isinstance(output, dict):
                    continue

                if node_name == "save_card":
                    card_result = output.get("card_result")
                    card_url = output.get("card_url", "")
                    if card_result:
                        await ws.send_json({
                            "type": "card",
                            "card_json": json.dumps(card_result, ensure_ascii=False),
                            "card_url": card_url,
                        })
                        card_sent = True

                elif node_name == "save_game":
                    game_html = output.get("current_game_html", "")
                    game_url = output.get("current_game_url", "")
                    if game_html:
                        await ws.send_json({
                            "type": "game",
                            "html": game_html,
                            "game_url": game_url,
                        })
                        game_sent = True

        # 그래프 실행 완료 후 최종 상태에서 결과 보완
        final_state = await graph.aget_state(config)
        values = final_state.values if final_state else {}

        hint = values.get("hint", "")
        game_url = values.get("current_game_url", "")

        # card 이벤트를 스트리밍 중 못 보낸 경우 최종 상태로 폴백
        if not card_sent:
            card_result = values.get("card_result")
            card_url = values.get("card_url", "")
            if card_result:
                await ws.send_json({
                    "type": "card",
                    "card_json": json.dumps(card_result, ensure_ascii=False),
                    "card_url": card_url,
                })

        # game 이벤트를 스트리밍 중 못 보낸 경우 최종 상태로 폴백
        if not game_sent:
            game_html = values.get("current_game_html", "")
            if game_html:
                await ws.send_json({
                    "type": "game",
                    "html": game_html,
                    "game_url": game_url,
                })

        await ws.send_json({
            "type": "done",
            "hint": hint,
            "session_id": session_id,
            "game_url": game_url,
        })

    except Exception as e:
        logger.error(f"그래프 실행 오류: {e}")
        await ws.send_json({"type": "error", "chunk": "뭔가 잘못됐어. 다시 한 번 해볼까? 😅"})
    finally:
        if langfuse_cb:
            try:
                langfuse_cb.flush()
            except Exception:
                pass
