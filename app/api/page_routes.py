from fastapi import APIRouter, Request
from fastapi.templating import Jinja2Templates

from app.services.email_provider import (
    get_active_email_provider,
    get_email_by_id,
    get_emails,
)
from app.services.gemini_service import get_model_status
from app.services.ui_state import get_latest_agent_state


router = APIRouter()

templates = Jinja2Templates(directory="app/templates")


def get_default_selected_email(emails):
    """
    Select Notion by default if available.
    Otherwise select the first email.
    """

    for email in emails:
        if email.get("sender") == "Notion":
            return email

    if emails:
        return emails[0]

    return None


@router.get("/")
def dashboard(
    request: Request,
    selected_email_id: str = "",
):
    """
    Main inbox dashboard.

    The email list, preview pane, and AI panel stay on the same screen.
    """

    emails = get_emails()
    active_provider = get_active_email_provider()
    latest_agent_state = get_latest_agent_state()

    selected_email = None

    if selected_email_id:
        selected_email = get_email_by_id(selected_email_id)

    if not selected_email:
        selected_email = get_default_selected_email(emails)

    return templates.TemplateResponse(
        request=request,
        name="dashboard.html",
        context={
            "emails": emails,
            "selected_email": selected_email,
            "active_provider": active_provider,
            "model_status": get_model_status(),
            "prompt": latest_agent_state.get("prompt", ""),
            "agent_result": latest_agent_state.get("agent_result"),
            "results": latest_agent_state.get("results", []),
        },
    )