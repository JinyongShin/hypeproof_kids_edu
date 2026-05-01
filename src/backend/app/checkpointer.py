def get_thread_config(session_id: str) -> dict:
    """LangGraph thread config 생성."""
    return {"configurable": {"thread_id": session_id}}
