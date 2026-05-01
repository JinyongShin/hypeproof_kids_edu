from typing import Annotated, Optional
from typing_extensions import TypedDict
from langgraph.graph.message import add_messages


class EduSessionState(TypedDict):
    # LangGraph이 관리하는 메시지 히스토리
    messages: Annotated[list, add_messages]
    # 세션 정보
    session_id: str
    child_id: str
    tenant_id: str          # MVP: "default"
    # 카드 진행 상태
    latest_character: Optional[dict]
    latest_world: Optional[dict]
    # 게임 상태 (편집 루프의 핵심)
    current_spec: Optional[dict]
    current_game_html: Optional[str]
    current_game_url: Optional[str]
    # 라우팅
    intent: Optional[str]   # "card" | "game_create" | "game_edit" | "chitchat"
    # 출력 버퍼
    card_result: Optional[dict]
    card_url: Optional[str]
    hint: Optional[str]
    # 롤링 컨텍스트 요약 (매 턴 갱신)
    session_context: Optional[str]
    # 관측성
    token_usage: dict
    error: Optional[str]
