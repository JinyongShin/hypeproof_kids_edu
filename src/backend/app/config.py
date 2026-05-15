from pydantic_settings import BaseSettings
from functools import lru_cache


class Settings(BaseSettings):
    # LLM
    GEMINI_API_KEY: str = ""
    MOCK_LLM: bool = False

    # 백엔드
    BACKEND_BASE_URL: str = "http://localhost:8000"
    ADMIN_USERNAME: str = "admin"
    ADMIN_PASSWORD: str = "admin"

    # Langfuse (로컬 셀프호스팅 관측성)
    LANGFUSE_PUBLIC_KEY: str = ""
    LANGFUSE_SECRET_KEY: str = ""
    LANGFUSE_HOST: str = "http://localhost:3002"
    LANGFUSE_ENABLED: bool = False

    model_config = {"env_file": ".env.local", "env_file_encoding": "utf-8"}


@lru_cache
def get_settings() -> Settings:
    return Settings()
