"""Provider boundary: the only module that talks to the LLM API.

DeepSeek exposes an OpenAI-compatible API, so the `openai` SDK will be used
with DeepSeek's base URL. The actual call is intentionally NOT implemented yet;
it will be written by hand in the Stage 0 coding session.
"""

import os
from dataclasses import dataclass


@dataclass(frozen=True)
class DeepSeekConfig:
    api_key: str
    model: str
    base_url: str


def load_config() -> DeepSeekConfig:
    """Read DeepSeek settings from the environment (see .env.example)."""
    return DeepSeekConfig(
        api_key=os.environ["DEEPSEEK_API_KEY"],
        model=os.environ["DEEPSEEK_MODEL"],
        base_url=os.environ["DEEPSEEK_BASE_URL"],
    )


def complete(question: str) -> str:
    """Send the question to DeepSeek and return the model's answer text.

    Not implemented yet (Stage 0 manual session): client construction,
    messages, model, temperature, max_tokens, response extraction,
    structured output, and error/timeout handling all belong here.
    """
    raise NotImplementedError("DeepSeek call not implemented yet (Stage 0).")
