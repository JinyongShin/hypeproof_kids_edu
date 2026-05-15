from langgraph.graph import StateGraph, END
from langgraph.checkpoint.sqlite.aio import AsyncSqliteSaver

from app.graph.state import EduSessionState
from app.graph.nodes import (
    classify_intent_node,
    generate_card_node,
    save_card_node,
    generate_spec_node,
    edit_code_node,
    validate_and_build_node,
    save_game_node,
    chitchat_node,
    summarize_turn_node,
)
from app.graph.edges import (
    route_after_classify,
    route_after_generate_card,
    route_after_spec,
    route_after_edit_code,
)


def build_graph() -> StateGraph:
    g = StateGraph(EduSessionState)

    # 노드 등록
    g.add_node("classify_intent", classify_intent_node)
    g.add_node("generate_card", generate_card_node)
    g.add_node("save_card", save_card_node)
    g.add_node("generate_spec", generate_spec_node)
    g.add_node("edit_code", edit_code_node)
    g.add_node("validate_and_build", validate_and_build_node)
    g.add_node("save_game", save_game_node)
    g.add_node("chitchat", chitchat_node)
    g.add_node("summarize_turn", summarize_turn_node)

    # 엣지
    g.set_entry_point("classify_intent")
    g.add_conditional_edges("classify_intent", route_after_classify, {
        "generate_card": "generate_card",
        "generate_spec": "generate_spec",
        "edit_code": "edit_code",
        "chitchat": "chitchat",
    })
    g.add_conditional_edges("generate_card", route_after_generate_card, {
        "save_card": "save_card",
        "__end__": END,
    })
    g.add_edge("save_card", "summarize_turn")
    g.add_conditional_edges("generate_spec", route_after_spec, {
        "validate_and_build": "validate_and_build",
        "__end__": END,
    })
    # edit_code → save_game 직행 (validate_and_build 불필요 — HTML 전체 반환)
    g.add_conditional_edges("edit_code", route_after_edit_code, {
        "save_game": "save_game",
        "generate_spec": "generate_spec",
    })
    g.add_edge("validate_and_build", "save_game")
    g.add_edge("save_game", "summarize_turn")
    g.add_edge("chitchat", "summarize_turn")
    g.add_edge("summarize_turn", END)

    return g


async def get_compiled_graph(db_path: str = "data/langgraph.db", checkpointer=None):
    """컴파일된 그래프 반환 (테스트용 — checkpointer 직접 전달 시).

    프로덕션 lifespan에서는 graph_lifespan() 컨텍스트 매니저를 사용할 것.
    checkpointer가 주어지면 그대로 사용 (InMemorySaver 등 테스트용).
    """
    if checkpointer is None:
        from langgraph.checkpoint.memory import MemorySaver
        checkpointer = MemorySaver()
    return build_graph().compile(checkpointer=checkpointer)


from contextlib import asynccontextmanager

@asynccontextmanager
async def graph_lifespan(db_path: str = "data/langgraph.db"):
    """AsyncSqliteSaver를 올바르게 async context manager로 관리.

    사용법 (main.py lifespan):
        async with graph_lifespan() as graph:
            app.state.graph = graph
            yield
    """
    from pathlib import Path
    Path(db_path).parent.mkdir(parents=True, exist_ok=True)
    async with AsyncSqliteSaver.from_conn_string(db_path) as saver:
        yield build_graph().compile(checkpointer=saver)
