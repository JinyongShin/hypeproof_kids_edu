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

# 텍스트 스트리밍 노드 (LLM 응답을 채팅 말풍선으로 실시간 표시)
_STREAMING_NODES = {"generate_card", "chitchat"}
# Thinking 스트리밍 노드 (thinking 토큰만 추출해 별도 이벤트로 전송, 본문 JSON/HTML은 채팅 미노출)
_THINKING_NODES = {"generate_spec", "edit_code"}


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
    WS 이벤트(text/thinking/card/game/done/error)로 스트리밍.
    """
    from langchain_core.messages import HumanMessage

    config = get_thread_config(session_id)
    langfuse_cb = _get_langfuse_callback()
    if langfuse_cb:
        config["callbacks"] = [langfuse_cb]

    card_sent = False
    game_sent = False
    commentary_sent = False

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

            if kind == "on_chat_model_stream":
                chunk = event["data"].get("chunk")
                if not chunk or not hasattr(chunk, "content"):
                    continue

                if node_name in _STREAMING_NODES:
                    # 일반 텍스트 스트리밍 — 채팅 말풍선
                    if chunk.content:
                        await ws.send_json({"type": "text", "chunk": chunk.content})

                elif node_name in _THINKING_NODES:
                    # thinking 토큰만 추출 — JSON/HTML 본문은 전송 안 함
                    content = chunk.content
                    if isinstance(content, list):
                        for part in content:
                            if isinstance(part, dict) and part.get("type") == "thinking":
                                thinking_text = part.get("thinking", "")
                                if thinking_text:
                                    await ws.send_json({"type": "thinking", "chunk": thinking_text})

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
                    # 게임 생성/편집 완료 텍스트 응답 먼저 전송
                    commentary = output.get("game_commentary", "")
                    if commentary:
                        await ws.send_json({"type": "text", "chunk": commentary})
                        commentary_sent = True
                    # save_game 출력엔 current_game_html이 없으므로 fallback에서 처리
                    # 단, commentary 중복 방지를 위해 플래그만 설정

        # 그래프 실행 완료 후 최종 상태에서 결과 보완
        final_state = await graph.aget_state(config)
        values = final_state.values if final_state else {}

        hint = values.get("hint", "")
        game_url = values.get("current_game_url", "")

        if not card_sent:
            card_result = values.get("card_result")
            card_url = values.get("card_url", "")
            if card_result:
                await ws.send_json({
                    "type": "card",
                    "card_json": json.dumps(card_result, ensure_ascii=False),
                    "card_url": card_url,
                })

        if not game_sent:
            game_html = values.get("current_game_html", "")
            if game_html:
                if not commentary_sent:
                    commentary = values.get("game_commentary", "")
                    if commentary:
                        await ws.send_json({"type": "text", "chunk": commentary})
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
