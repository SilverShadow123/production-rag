import os

from pydantic_settings import BaseSettings
from functools import lru_cache
class Settings(BaseSettings):

    # OpenRouter LLM Configurations
    openrouter_api_key: str = os.getenv('OPENROUTER_API_KEY')
    openrouter_api_base: str = "https://openrouter.ai/api/v1"
    primary_model: str = "openai/gpt-4o-mini"
    fallback_model: str = "openai/gpt-4o"

    #LangSmith
    langsmith_tracing: bool = True
    langsmith_api_key: str = os.getenv('LANGSMITH_API_KEY')
    langsmith_endpoint: str = 'https://api.smith.langchain.com'
    langsmith_project: str = 'production-api'

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

    def model_post_init(self, __context):
        env_map = {
            'LANGSMITH_TRACING': str(self.langsmith_tracing).lower(),
            'LANGSMITH_API_KEY': self.langsmith_api_key,
            'LANGSMITH_ENDPOINT': self.langsmith_endpoint,
            'LANGSMITH_PROJECT': self.langsmith_project,
        }
        for key, value in env_map.items():
            if value:
                os.environ[key] = value

    @property
    def is_production(self) -> bool:
        return self.app_env == 'production'

@lru_cache
def get_settings() -> Settings:
    """
    Cached Settings instance - load once and reused everywhere
    """
    return Settings()
