from fastapi import APIRouter, Form, HTTPException, Request
from fastapi.responses import RedirectResponse, Response
from fastapi.templating import Jinja2Templates

from app.services.audit_service import log_action
from app.services.email_agent import run_email_agent
from app.services.email_provider import (
    add_email_tag,
    get_email_by_id,
    get_emails,
    get_thread_emails,
    mark_email_as_reviewed,
)
from app.services.export_service import build_emails_csv


router = APIRouter(
    tags=["Email Actions"],
)

templates = Jinja2Templates(directory="app/templates")


@router.get("/emails/{email_id}")
def email_detail(
    request: Request,
    email_id: str,
):
    """
    Display one full email.
    """

    email = get_email_by_id(email_id)

    if not email:
        raise HTTPException(
            status_code=404,
            detail="Email not found",
        )

    log_action(
        action="open_email",
        email_id=email_id,
    )

    return templates.TemplateResponse(
        request=request,
        name="email_detail.html",
        context={
            "email": email,
        },
    )


@router.get("/threads/{thread_id}")
def thread_detail(
    request: Request,
    thread_id: str,
):
    """
    Display all emails in one thread.
    """

    emails = get_thread_emails(thread_id)

    if not emails:
        raise HTTPException(
            status_code=404,
            detail="Thread not found",
        )

    log_action(
        action="view_thread",
        extra_details={
            "thread_id": thread_id,
            "emails_count": len(emails),
        },
    )

    return templates.TemplateResponse(
        request=request,
        name="thread_detail.html",
        context={
            "thread_id": thread_id,
            "emails": emails,
        },
    )


@router.post("/emails/{email_id}/reviewed")
def review_email(email_id: str):
    """
    Mark email as reviewed.
    """

    email = mark_email_as_reviewed(email_id)

    if not email:
        raise HTTPException(
            status_code=404,
            detail="Email not found",
        )

    log_action(
        action="mark_as_reviewed",
        email_id=email_id,
    )

    return RedirectResponse(
        url=f"/emails/{email_id}",
        status_code=303,
    )


@router.post("/emails/{email_id}/tags")
def tag_email(
    email_id: str,
    tag_name: str = Form(...),
):
    """
    Add tag to email.
    """

    email = add_email_tag(
        email_id=email_id,
        tag_name=tag_name,
    )

    if not email:
        raise HTTPException(
            status_code=400,
            detail="Email not found or tag is empty",
        )

    log_action(
        action="add_tag",
        email_id=email_id,
        extra_details={
            "tag_name": tag_name,
        },
    )

    return RedirectResponse(
        url=f"/emails/{email_id}",
        status_code=303,
    )


@router.get("/export")
def export_emails(prompt: str = ""):
    """
    Export all emails or agent results as CSV.

    If prompt is provided, the Email AI Agent runs again and exports the matched results.
    If no prompt is provided, all provider emails are exported.
    """

    emails = get_emails()

    if prompt:
        agent_result = run_email_agent(
            user_prompt=prompt,
            emails=emails,
        )

        export_data = agent_result.get("emails", [])
        filename = "agent_results.csv"

        log_action(
            action="export_agent_results",
            extra_details={
                "prompt": prompt,
                "emails_count": len(export_data),
            },
        )

    else:
        export_data = emails
        filename = "all_emails.csv"

        log_action(
            action="export_all_emails",
            extra_details={
                "emails_count": len(export_data),
            },
        )

    csv_text = build_emails_csv(export_data)

    return Response(
        content=csv_text,
        media_type="text/csv",
        headers={
            "Content-Disposition": f"attachment; filename={filename}",
        },
    )


@router.get("/emails/{email_id}/export")
def export_single_email(email_id: str):
    """
    Export one email as CSV.
    """

    email = get_email_by_id(email_id)

    if not email:
        raise HTTPException(
            status_code=404,
            detail="Email not found",
        )

    log_action(
        action="export_single_email",
        email_id=email_id,
    )

    csv_text = build_emails_csv([email])

    return Response(
        content=csv_text,
        media_type="text/csv",
        headers={
            "Content-Disposition": f"attachment; filename={email_id}.csv",
        },
    )

@router.post("/api/emails/{email_id}/reviewed")
def review_email_api(email_id: str):
    """
    Interactive API endpoint for marking an email as reviewed.
    """

    email = mark_email_as_reviewed(email_id)

    if not email:
        raise HTTPException(
            status_code=404,
            detail="Email not found",
        )

    log_action(
        action="mark_as_reviewed",
        email_id=email_id,
        extra_details={
            "source": "interactive_dashboard",
        },
    )

    return {
        "success": True,
        "message": "Email marked as reviewed.",
        "email": email,
    }


@router.post("/api/emails/{email_id}/tags")
def tag_email_api(
    email_id: str,
    tag_name: str = Form(...),
):
    """
    Interactive API endpoint for adding a tag.
    """

    email = add_email_tag(
        email_id=email_id,
        tag_name=tag_name,
    )

    if not email:
        raise HTTPException(
            status_code=400,
            detail="Email not found or tag is empty",
        )

    log_action(
        action="add_tag",
        email_id=email_id,
        extra_details={
            "tag_name": tag_name,
            "source": "interactive_dashboard",
        },
    )

    return {
        "success": True,
        "message": "Tag added successfully.",
        "email": email,
    }