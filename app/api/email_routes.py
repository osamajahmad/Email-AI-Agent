from fastapi import APIRouter, Depends, Form, HTTPException, Request
from fastapi.responses import RedirectResponse, Response
from fastapi.templating import Jinja2Templates

from app.services.audit_service import log_action
from app.services.auth_service import require_demo_user
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


def build_email_audit_details(email, extra_details=None):
    """
    Build readable audit details for email-related actions.
    """

    details = {}

    if email:
        details.update(
            {
                "email_id": email.get("id"),
                "thread_id": email.get("thread_id"),
                "sender": email.get("sender"),
                "sender_email": email.get("sender_email"),
                "recipient_email": email.get("recipient_email"),
                "subject": email.get("subject"),
                "category": email.get("category"),
                "confidence_score": email.get("confidence_score"),
            }
        )

    if extra_details:
        details.update(extra_details)

    return details


@router.get("/emails/{email_id}")
def email_detail(
    request: Request,
    email_id: str,
    demo_user: str = Depends(require_demo_user),
):
    """
    Display one full email.

    Opening an email is logged for auditing, but the frontend should not show
    a success toast because this is normal navigation.
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
        user=demo_user,
        extra_details=build_email_audit_details(email),
    )

    return templates.TemplateResponse(
        request=request,
        name="email_detail.html",
        context={
            "email": email,
            "current_user": demo_user,
        },
    )


@router.get("/threads/{thread_id}")
def thread_detail(
    request: Request,
    thread_id: str,
    demo_user: str = Depends(require_demo_user),
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
        user=demo_user,
        extra_details={
            "thread_id": thread_id,
            "emails_count": len(emails),
            "email_ids": [
                email.get("id")
                for email in emails
            ],
            "email_subjects": [
                email.get("subject")
                for email in emails
            ],
        },
    )

    return templates.TemplateResponse(
        request=request,
        name="thread_detail.html",
        context={
            "thread_id": thread_id,
            "emails": emails,
            "current_user": demo_user,
        },
    )


@router.post("/emails/{email_id}/reviewed")
def review_email(
    email_id: str,
    demo_user: str = Depends(require_demo_user),
):
    """
    Mark email as reviewed using the normal form route.
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
        user=demo_user,
        extra_details=build_email_audit_details(
            email,
            {
                "source": "email_detail_page",
            },
        ),
    )

    return RedirectResponse(
        url=f"/emails/{email_id}",
        status_code=303,
    )


@router.post("/emails/{email_id}/tags")
def tag_email(
    email_id: str,
    tag_name: str = Form(...),
    demo_user: str = Depends(require_demo_user),
):
    """
    Add a tag to an email using the normal form route.
    """

    cleaned_tag_name = tag_name.strip()

    if not cleaned_tag_name:
        raise HTTPException(
            status_code=400,
            detail="Tag name is required.",
        )

    email = add_email_tag(
        email_id=email_id,
        tag_name=cleaned_tag_name,
    )

    if not email:
        raise HTTPException(
            status_code=400,
            detail="Email not found or tag is empty",
        )

    log_action(
        action="add_tag",
        email_id=email_id,
        user=demo_user,
        extra_details=build_email_audit_details(
            email,
            {
                "tag_name": cleaned_tag_name,
                "source": "email_detail_page",
            },
        ),
    )

    return RedirectResponse(
        url=f"/emails/{email_id}",
        status_code=303,
    )


@router.get("/export")
def export_emails(
    prompt: str = "",
    demo_user: str = Depends(require_demo_user),
):
    """
    Export all emails or AI Agent matched results as CSV.

    If prompt is provided:
    - The Email AI Agent runs again.
    - Only matched results are exported.

    If no prompt is provided:
    - All provider emails are exported.
    """

    emails = get_emails()
    cleaned_prompt = prompt.strip()

    if cleaned_prompt:
        agent_result = run_email_agent(
            user_prompt=cleaned_prompt,
            emails=emails,
        )

        export_data = agent_result.get("emails", [])
        filename = "agent_results.csv"

        log_action(
            action="export_agent_results",
            user=demo_user,
            extra_details={
                "prompt": cleaned_prompt,
                "emails_count": len(export_data),
                "matched_email_ids": [
                    email.get("id")
                    for email in export_data
                ],
                "matched_email_subjects": [
                    email.get("subject")
                    for email in export_data
                ],
                "matched_email_senders": [
                    email.get("sender")
                    for email in export_data
                ],
            },
        )

    else:
        export_data = emails
        filename = "all_emails.csv"

        log_action(
            action="export_all_emails",
            user=demo_user,
            extra_details={
                "emails_count": len(export_data),
                "email_ids": [
                    email.get("id")
                    for email in export_data
                ],
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
def export_single_email(
    email_id: str,
    demo_user: str = Depends(require_demo_user),
):
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
        user=demo_user,
        extra_details=build_email_audit_details(email),
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
def review_email_api(
    email_id: str,
    demo_user: str = Depends(require_demo_user),
):
    """
    Interactive API endpoint for marking an email as reviewed.

    Used by the dashboard without refreshing the page.
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
        user=demo_user,
        extra_details=build_email_audit_details(
            email,
            {
                "source": "interactive_dashboard",
            },
        ),
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
    demo_user: str = Depends(require_demo_user),
):
    """
    Interactive API endpoint for adding a tag.

    Used by the dashboard without refreshing the page.
    """

    cleaned_tag_name = tag_name.strip()

    if not cleaned_tag_name:
        raise HTTPException(
            status_code=400,
            detail="Tag name is required.",
        )

    email = add_email_tag(
        email_id=email_id,
        tag_name=cleaned_tag_name,
    )

    if not email:
        raise HTTPException(
            status_code=400,
            detail="Email not found or tag is empty",
        )

    log_action(
        action="add_tag",
        email_id=email_id,
        user=demo_user,
        extra_details=build_email_audit_details(
            email,
            {
                "tag_name": cleaned_tag_name,
                "source": "interactive_dashboard",
            },
        ),
    )

    return {
        "success": True,
        "message": "Tag added successfully.",
        "email": email,
    }