from fastapi import APIRouter, Request
from fastapi.templating import Jinja2Templates

from app.services.audit_service import get_audit_logs, log_action


router = APIRouter(
    tags=["Audit Logs"],
)

templates = Jinja2Templates(directory="app/templates")


@router.get("/audit-logs")
def audit_logs(request: Request):
    """
    Display audit logs.
    """

    logs = get_audit_logs()

    log_action(
        action="view_audit_logs",
        extra_details={
            "logs_count": len(logs),
        },
    )

    return templates.TemplateResponse(
        request=request,
        name="audit_logs.html",
        context={
            "logs": logs,
        },
    )