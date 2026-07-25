from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore",
    )

    litellm_api_key: str = ""
    litellm_api_base: str = ""
    litellm_model: str = "openai/glm-5.2"
    kb_path: str = "knowledge_base.txt"


settings = Settings()
