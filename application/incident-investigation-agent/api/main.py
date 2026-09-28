"""FastAPI entry point.

Run locally from the repository root:
    uvicorn api.main:app --app-dir application/incident-investigation-agent
"""

from fastapi import FastAPI, HTTPException

from api import llm_client
from api.schemas import InvestigationRequest, InvestigationResponse

app = FastAPI(title="incident-investigation-agent")


@app.get("/health")
def health() -> dict[str, str]:
    return {"status": "ok"}


@app.post("/investigate", response_model=InvestigationResponse)
def investigate(request: InvestigationRequest) -> InvestigationResponse:
    try:
        answer = llm_client.complete(request.question)
    except NotImplementedError as exc:
        raise HTTPException(status_code=501, detail=str(exc)) from exc
    return InvestigationResponse(answer=answer)
