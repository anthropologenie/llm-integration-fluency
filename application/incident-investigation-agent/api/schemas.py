"""Request/response contracts for the investigation endpoint.

Placeholders for Stage 0. The response shape is expected to evolve once the
direct DeepSeek call and structured output are implemented.
"""

from pydantic import BaseModel, ConfigDict, Field


class InvestigationRequest(BaseModel):
    model_config = ConfigDict(extra="forbid")

    question: str = Field(min_length=1, description="The incident question to investigate.")


class InvestigationResponse(BaseModel):
    answer: str = Field(description="The investigation answer.")
