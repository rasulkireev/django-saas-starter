from dataclasses import dataclass

from django.conf import settings

from pydantic_ai.models.openai import OpenAIChatModel
from pydantic_ai.models.anthropic import AnthropicModel
from pydantic_ai.models.google import GoogleModel

@dataclass(frozen=True, slots=True)
class PydanticAIModelSpec:
    provider: str  # provider id, e.g. "openai", "anthropic", "gemini"
    label: str  # e.g. "fast"


def build_model(*, provider: str, label: str):
    supported: dict[str, dict[str, str]] = settings.SUPPORTED_AI_MODELS
    provider_tiers = supported.get(provider)
    if not provider_tiers:
        raise ValueError(f"Unsupported provider {provider!r}.")

    model_name = provider_tiers.get(label)
    if not model_name:
        raise ValueError(f"Unsupported label {label!r} for provider {provider!r}.")

    if provider == "openai":
        return OpenAIChatModel(model_name)

    if provider == "anthropic":
        return AnthropicModel(model_name)

    if provider == "google":
        return GoogleModel(model_name)

    raise ValueError(f"Unsupported provider: {provider!r}")
