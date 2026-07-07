from fastapi import APIRouter, Form
from fastapi.responses import RedirectResponse
from pydantic import BaseModel

from app.services.audit_service import log_prompt
from app.services.email_agent import run_email_agent
from app.services.email_provider import get_emails


router = APIRouter(
    tags=["Email AI Agent"],
)


class AgentAskRequest(BaseModel):
    prompt: str


@router.post("/agent/ask")
def ask_agent_fallback(prompt: str = Form(...)):
    """
    Fallback form route.
    The interactive dashboard uses /api/agent/ask instead.
    """

    emails = get_emails()

    agent_result = run_email_agent(
        user_prompt=prompt,
        emails=emails,
    )

    log_prompt(
        prompt=prompt,
        agent_result=agent_result,
    )

    return RedirectResponse(
        url="/",
        status_code=303,
    )


@router.post("/api/agent/ask")
def ask_agent_api(payload: AgentAskRequest):
    """
    Interactive API endpoint.

    Receives a prompt from the frontend, runs the Email AI Agent,
    and returns JSON without refreshing or replacing the inbox UI.
    """

    prompt = payload.prompt.strip()
    emails = get_emails()

    agent_result = run_email_agent(
        user_prompt=prompt,
        emails=emails,
    )

    log_prompt(
        prompt=prompt,
        agent_result=agent_result,
    )

    return {
        "prompt": prompt,
        "agent_result": agent_result,
        "results": agent_result.get("emails", []),
    }