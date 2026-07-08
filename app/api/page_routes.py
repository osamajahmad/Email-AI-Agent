from fastapi import APIRouter, Request
from fastapi.responses import RedirectResponse
from fastapi.templating import Jinja2Templates

from app.services.email_provider import (
    get_active_email_provider,
    get_emails,
)
from app.services.gemini_service import get_model_status


router = APIRouter()

templates = Jinja2Templates(directory="app/templates")


@router.get("/")
def dashboard(request: Request):
    """
    Main dashboard page.

    Demo protection:
    User must be logged in through the demo login page.
    """

    demo_user = request.cookies.get("demo_user")

    if not demo_user:
        return RedirectResponse(
            url="/login",
            status_code=303,
        )

    emails = get_emails()
    active_provider = get_active_email_provider()

    return templates.TemplateResponse(
        request=request,
        name="dashboard.html",
        context={
            "emails": emails,
            "active_provider": active_provider,
            "model_status": get_model_status(),
            "current_user": demo_user,
        },
    )