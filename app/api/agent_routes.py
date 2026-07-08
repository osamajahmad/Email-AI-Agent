from fastapi import APIRouter, Depends, Form, HTTPException
from fastapi.responses import RedirectResponse

from app.schemas.agent_schema import AgentAskRequest
from app.services.audit_service import log_prompt
from app.services.auth_service import require_demo_user
from app.services.email_agent import run_email_agent
from app.services.email_provider import get_emails


router = APIRouter(
    tags=["Email AI Agent"],
)


@router.post("/agent/ask")
def ask_agent_fallback(
    prompt: str = Form(...),
    demo_user: str = Depends(require_demo_user),
):
    """
    Fallback form route.

    The interactive dashboard uses /api/agent/ask.
    This route is kept in case a normal HTML form submits a prompt.
    """

    cleaned_prompt = prompt.strip()

    if not cleaned_prompt:
        raise HTTPException(
            status_code=400,
            detail="Prompt is required.",
        )

    emails = get_emails()

    agent_result = run_email_agent(
        user_prompt=cleaned_prompt,
        emails=emails,
    )

    log_prompt(
        prompt=cleaned_prompt,
        agent_result=agent_result,
        user=demo_user,
    )

    return RedirectResponse(
        url="/",
        status_code=303,
    )


@router.post("/api/agent/ask")
def ask_agent_api(
    payload: AgentAskRequest,
    demo_user: str = Depends(require_demo_user),
):
    """
    Interactive API endpoint.

    Receives a natural-language prompt from the frontend,
    runs the Email AI Agent, logs the prompt and matched emails,
    and returns structured JSON results.
    """

    prompt = payload.prompt.strip()

    if not prompt:
        raise HTTPException(
            status_code=400,
            detail="Prompt is required.",
        )

    emails = get_emails()

    agent_result = run_email_agent(
        user_prompt=prompt,
        emails=emails,
    )

    log_prompt(
        prompt=prompt,
        agent_result=agent_result,
        user=demo_user,
    )

    return {
        "success": True,
        "prompt": prompt,
        "agent_result": agent_result,
        "results": agent_result.get("emails", []),
    }