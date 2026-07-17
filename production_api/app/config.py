from pydantic_settings import BaseSettings
from functools import lru_cache
class Settings(BaseSettings):

    # LLM Configurations
    openai_api_key: str
    openai_api_base: str = "https://api.openai.com/v1"
    primary_model: str = "openai/gpt-4o-mini"
    fallback_model: str = "openai/gpt-4o-mini"

    #LangSmith
    langchain_tracing_v2: bool = True
    langchain_api_key: str = ''
    langchain_project_id: str = 'production-api'

    #Application
    app_env: str = 'development'
    log_level: str = 'INFO'
    rate_limit: str = '20/minute'
    cache_ttl_seconds: int = 300
    max_retries: int = 3

    model_config = {
        'env_file': '.env',
        "extra" : "ignore"
    }

    @property
    def is_production(self) -> bool:
        return self.app_env == 'production'

@lru_cache
def get_settings() -> Settings:
    """
    Cached Settings instance - load once and reused everywhere
    """
    return Settings()
