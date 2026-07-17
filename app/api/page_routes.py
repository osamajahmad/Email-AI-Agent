from fastapi import APIRouter, Request
from fastapi.responses import RedirectResponse
from fastapi.templating import Jinja2Templates

from app.services.email_provider import (
    get_active_email_provider,
    get_emails,
    get_provider_connection_status,
)
from app.services.gemini_service import get_model_status


router = APIRouter()
templates = Jinja2Templates(directory="app/templates")


def email_matches_terms(email, terms):
    searchable_text = " ".join([
        str(email.get("category", "")),
        str(email.get("subject", "")),
        str(email.get("body", "")),
        str(email.get("preview", "")),
        " ".join(email.get("tags", [])),
    ]).lower()

    return any(term in searchable_text for term in terms)


def build_dashboard_metrics(emails):
    return {
        "total": len(emails),
        "reviewed": sum(1 for email in emails if email.get("reviewed") is True),
        "unread": sum(1 for email in emails if email.get("is_read") is False),
        "subscriptions": sum(
            1 for email in emails
            if email.get("is_subscription_related") is True
            or email_matches_terms(email, ["subscription"])
        ),
        "renewals": sum(
            1 for email in emails
            if email_matches_terms(email, ["renewal", "renewed", "renews"])
        ),
        "invoices": sum(
            1 for email in emails
            if email_matches_terms(email, ["invoice", "billing", "amount charged", "amount paid"])
        ),
        "saas": sum(
            1 for email in emails
            if email_matches_terms(email, ["saas", "workspace", "software", "license"])
        ),
        "domains": sum(
            1 for email in emails
            if email_matches_terms(email, ["domain", "dns", "godaddy"])
        ),
        "cloud": sum(
            1 for email in emails
            if email_matches_terms(email, ["cloud", "aws", "hosting", "compute"])
        ),
        "software": sum(
            1 for email in emails
            if email_matches_terms(email, ["software", "license", "creative cloud"])
        ),
    }


@router.get("/")
def dashboard(request: Request):
    demo_user = request.cookies.get("demo_user")

    if not demo_user:
        return RedirectResponse(
            url="/login",
            status_code=303,
        )

    emails = get_emails()
    active_provider = get_active_email_provider()
    metrics = build_dashboard_metrics(emails)
    provider_status = get_provider_connection_status()

    return templates.TemplateResponse(
        request=request,
        name="dashboard.html",
        context={
            "emails": emails,
            "active_provider": active_provider,
            "provider_status": provider_status,
            "metrics": metrics,
            "model_status": get_model_status(),
            "current_user": demo_user,
        },
    )