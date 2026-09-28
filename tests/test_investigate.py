"""Scaffolding tests. None of these call DeepSeek or need DEEPSEEK_API_KEY."""

import pytest
from fastapi import FastAPI
from fastapi.testclient import TestClient
from pydantic import ValidationError

from api import llm_client
from api.main import app
from api.schemas import InvestigationRequest, InvestigationResponse


@pytest.fixture
def client(monkeypatch):
    monkeypatch.delenv("DEEPSEEK_API_KEY", raising=False)
    return TestClient(app)


def test_app_is_fastapi_instance():
    assert isinstance(app, FastAPI)


def test_health(client):
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json() == {"status": "ok"}


def test_request_schema_accepts_valid_question():
    request = InvestigationRequest(question="Why did checkout latency spike?")
    assert request.question == "Why did checkout latency spike?"


@pytest.mark.parametrize("payload", [{}, {"question": ""}, {"question": "q", "extra": 1}])
def test_request_schema_rejects_invalid_input(payload):
    with pytest.raises(ValidationError):
        InvestigationRequest(**payload)


def test_response_schema_accepts_valid_answer():
    assert InvestigationResponse(answer="Root cause: X").answer == "Root cause: X"


def test_response_schema_rejects_missing_answer():
    with pytest.raises(ValidationError):
        InvestigationResponse()


def test_investigate_rejects_invalid_body(client):
    assert client.post("/investigate", json={"question": ""}).status_code == 422


def test_investigate_returns_501_until_llm_call_is_implemented(client):
    response = client.post("/investigate", json={"question": "Why did it fail?"})
    assert response.status_code == 501


def test_investigate_uses_llm_client_boundary(client, monkeypatch):
    monkeypatch.setattr(llm_client, "complete", lambda question: f"stub: {question}")
    response = client.post("/investigate", json={"question": "Why did it fail?"})
    assert response.status_code == 200
    assert response.json() == {"answer": "stub: Why did it fail?"}


def test_llm_client_is_not_implemented_yet():
    with pytest.raises(NotImplementedError):
        llm_client.complete("anything")
