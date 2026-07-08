from fastapi import APIRouter, Depends, Request
from fastapi.templating import Jinja2Templates

from app.services.audit_service import get_audit_logs, log_action
from app.services.auth_service import require_demo_user


router = APIRouter(
    tags=["Audit Logs"],
)

templates = Jinja2Templates(directory="app/templates")


@router.get("/audit-logs")
def audit_logs(
    request: Request,
    demo_user: str = Depends(require_demo_user),
):
    """
    Display audit logs.

    This page is protected by demo authentication.
    """

    existing_logs_count = len(get_audit_logs())

    log_action(
        action="view_audit_logs",
        user=demo_user,
        extra_details={
            "logs_count_before_view": existing_logs_count,
        },
    )

    logs = get_audit_logs()

    return templates.TemplateResponse(
        request=request,
        name="audit_logs.html",
        context={
            "logs": logs,
            "current_user": demo_user,
        },
    )