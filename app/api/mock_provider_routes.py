from fastapi import APIRouter, Form, HTTPException

from app.services.mock_email_provider import (
    add_mock_email_tag,
    get_mock_email_by_id,
    get_mock_emails,
    get_mock_emails_by_thread_id,
    mark_mock_email_as_reviewed,
)


router = APIRouter(
    prefix="/mock-provider",
    tags=["Mock Email Provider"],
)


@router.get("/emails")
def list_mock_emails():
    """
    Mock provider endpoint that returns emails as an API response.
    """

    return {
        "provider": "mock",
        "emails": get_mock_emails(),
    }


@router.get("/emails/{email_id}")
def get_mock_email(email_id: str):
    """
    Mock provider endpoint that returns one email by ID.
    """

    email = get_mock_email_by_id(email_id)

    if not email:
        raise HTTPException(
            status_code=404,
            detail="Email not found",
        )

    return email


@router.get("/threads/{thread_id}")
def get_mock_thread(thread_id: str):
    """
    Mock provider endpoint that returns emails in the same thread.
    """

    emails = get_mock_emails_by_thread_id(thread_id)

    if not emails:
        raise HTTPException(
            status_code=404,
            detail="Thread not found",
        )

    return {
        "thread_id": thread_id,
        "emails": emails,
    }


@router.post("/emails/{email_id}/reviewed")
def review_mock_email(email_id: str):
    """
    Mock provider endpoint that marks an email as reviewed.
    """

    email = mark_mock_email_as_reviewed(email_id)

    if not email:
        raise HTTPException(
            status_code=404,
            detail="Email not found",
        )

    return email


@router.post("/emails/{email_id}/tags")
def tag_mock_email(
    email_id: str,
    tag_name: str = Form(...),
):
    """
    Mock provider endpoint that adds a tag to an email.
    """

    email = add_mock_email_tag(
        email_id=email_id,
        tag_name=tag_name,
    )

    if not email:
        raise HTTPException(
            status_code=400,
            detail="Email not found or tag is empty",
        )

    return email