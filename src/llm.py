import litellm
from langchain_litellm import ChatLiteLLM

from settings import settings

litellm.drop_params = True


def get_llm(temperature: float = 0.3) -> ChatLiteLLM:
    """LLM used by all agents, routed via LiteLLM proxy."""
    return ChatLiteLLM(
        model=settings.litellm_model,
        api_key=settings.litellm_api_key,
        api_base=settings.litellm_api_base,
        temperature=temperature,
    )
