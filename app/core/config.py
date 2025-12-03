from functools import lru_cache
from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    PROJECT_NAME: str = 'AG_DEV'
    VERSION: str = '0.1.0'

    GEMINI_API_KEY: str = Field(..., description="Gemini API Key")
    GOOGLE_API_KEY: str = Field(..., description="Google API Key")

    CODING_AGENT_BASIC_MODEL: str = Field("gemini-2.0-flash-exp", description="Basic model for simple tasks")
    CODING_AGENT_ADVANCED_MODEL: str = Field("gemini-2.5-flash", description="Advanced model for complex tasks")
    WORK_DIR: str = Field("agent_output", description="Working directory for agent operations")

    model_config = SettingsConfigDict(
        env_file='.env',
        env_file_encoding='utf-8',
        case_sensitive=False
    )

@lru_cache
def get_settings():
    return Settings()