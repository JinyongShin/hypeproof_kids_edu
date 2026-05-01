from app.graph.state import EduSessionState


def route_after_classify(state: EduSessionState) -> str:
    intent = state.get("intent", "chitchat")
    if intent == "game_create":
        return "generate_spec"
    elif intent == "game_edit":
        # 현재 게임 HTML 없으면 새로 생성으로 폴백
        if state.get("current_game_html"):
            return "edit_code"
        return "generate_spec"
    elif intent == "card":
        return "generate_card"
    return "chitchat"


def route_after_generate_card(state: EduSessionState) -> str:
    if state.get("error"):
        return "__end__"
    if state.get("card_result"):
        return "save_card"
    return "__end__"


def route_after_spec(state: EduSessionState) -> str:
    if state.get("current_spec"):
        return "validate_and_build"
    return "__end__"


def route_after_edit_code(state: EduSessionState) -> str:
    if state.get("current_game_html"):
        return "save_game"
    # HTML 없으면 새 게임 생성으로 폴백
    return "generate_spec"
