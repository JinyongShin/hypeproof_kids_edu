from langchain_core.language_models import BaseChatModel
from app.config import get_settings


def get_card_llm() -> BaseChatModel:
    """카드 생성용: 스트리밍, creative"""
    settings = get_settings()
    if settings.MOCK_LLM:
        return _mock_card_llm()
    from langchain_google_genai import ChatGoogleGenerativeAI
    return ChatGoogleGenerativeAI(
        model="gemini-2.5-flash",
        temperature=0.7,
        max_output_tokens=8192,
        google_api_key=settings.GEMINI_API_KEY,
    )


def get_spec_llm() -> BaseChatModel:
    """스펙 생성용: thinking 활성화로 게임 설계 품질 향상"""
    settings = get_settings()
    if settings.MOCK_LLM:
        return _mock_spec_llm()
    from langchain_google_genai import ChatGoogleGenerativeAI
    return ChatGoogleGenerativeAI(
        model="gemini-2.5-flash",
        temperature=0.5,
        max_output_tokens=2048,
        thinking_budget=1024,
        include_thoughts=True,
        google_api_key=settings.GEMINI_API_KEY,
    )


def get_edit_llm() -> BaseChatModel:
    """코드 편집용: thinking 활성화, 전체 HTML 반환이므로 토큰 한도 크게"""
    settings = get_settings()
    if settings.MOCK_LLM:
        return _mock_edit_llm()
    from langchain_google_genai import ChatGoogleGenerativeAI
    return ChatGoogleGenerativeAI(
        model="gemini-2.5-flash",
        temperature=0.3,
        max_output_tokens=16384,
        thinking_budget=2048,
        include_thoughts=True,
        google_api_key=settings.GEMINI_API_KEY,
    )


def get_summary_llm() -> BaseChatModel:
    """롤링 컨텍스트 요약용: 비스트리밍, very deterministic, 짧은 출력"""
    settings = get_settings()
    if settings.MOCK_LLM:
        return _mock_summary_llm()
    from langchain_google_genai import ChatGoogleGenerativeAI
    return ChatGoogleGenerativeAI(
        model="gemini-2.5-flash",
        temperature=0.1,
        max_output_tokens=256,
        google_api_key=settings.GEMINI_API_KEY,
    )


def get_intent_llm() -> BaseChatModel:
    """intent 분류용: 비스트리밍, very deterministic"""
    settings = get_settings()
    if settings.MOCK_LLM:
        return _mock_intent_llm()
    from langchain_google_genai import ChatGoogleGenerativeAI
    return ChatGoogleGenerativeAI(
        model="gemini-2.5-flash",
        temperature=0.1,
        max_output_tokens=64,
        google_api_key=settings.GEMINI_API_KEY,
    )


def _mock_card_llm() -> BaseChatModel:
    from langchain_core.language_models.fake_chat_models import FakeListChatModel
    mock_card = (
        '안녕! 캐릭터를 만들었어 🎨\n'
        '```json\n'
        '{"card_type":"character","name":"테스트용사","description":"테스트 캐릭터",'
        '"traits":["용감함"],"world":"테스트 세계","image_prompt":"test hero",'
        '"image_svg":"<svg viewBox=\'0 0 200 200\'><circle cx=\'100\' cy=\'100\' r=\'80\' fill=\'#FFB6C1\'/></svg>",'
        '"effects":[]}\n'
        '```\n'
        '💡 다음엔 세계를 만들어봐!'
    )
    return FakeListChatModel(responses=[mock_card])


def _mock_spec_llm() -> BaseChatModel:
    from langchain_core.language_models.fake_chat_models import FakeListChatModel
    mock_spec = (
        '{"player":{"movement":"free","speed":5},'
        '"spawns":[{"role":"item","sprite":"⭐","from":"top","motion":"fall",'
        '"rate":0.03,"speed":2.0,"score_delta":1}],'
        '"world":{"scroll":"none"},'
        '"goal":{"time_limit":45,"target_score":0}}'
    )
    return FakeListChatModel(responses=[mock_spec])


def _mock_edit_llm() -> BaseChatModel:
    """편집 요청 테스트용 — speed 증가된 spec 반환."""
    from langchain_core.language_models.fake_chat_models import FakeListChatModel
    mock_edit = '{"player":{"movement":"free","speed":8},"spawns":[{"role":"item","sprite":"⭐","from":"top","motion":"fall","rate":0.03,"speed":3.0,"score_delta":1}],"world":{"scroll":"none"},"goal":{"time_limit":45,"target_score":0}}'
    return FakeListChatModel(responses=[mock_edit])


def _mock_summary_llm() -> BaseChatModel:
    from langchain_core.language_models.fake_chat_models import FakeListChatModel
    mock_summary = "캐릭터: 테스트용사(용감함). 게임: 별 모으기(낙하형, 속도3). 선호: 빠른 속도."
    return FakeListChatModel(responses=[mock_summary])


def _mock_intent_llm() -> BaseChatModel:
    from langchain_core.language_models.fake_chat_models import FakeListChatModel
    return FakeListChatModel(responses=["card"])
