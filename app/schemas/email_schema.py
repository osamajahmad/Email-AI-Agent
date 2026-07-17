from typing import List, Optional

from pydantic import BaseModel, Field


class EmailSchema(BaseModel):
    """
    Normalized email structure used by the application.

    All providers should be converted into this same shape:
    - Mock provider
    - Gmail
    - Outlook / Microsoft Graph
    - Any future dynamic email provider
    """

    id: str
    thread_id: str

    # Provider metadata
    provider: str = "mock"
    provider_message_id: Optional[str] = ""
    provider_thread_id: Optional[str] = ""

    # Email people
    sender: str
    sender_email: str
    recipient_email: str

    # Email content
    subject: str
    date: str
    received_at: Optional[str] = ""
    body: str
    preview: Optional[str] = ""
    summary: Optional[str] = ""

    # Mailbox status from Gmail / Outlook
    is_read: bool = False

    # Internal app status
    reviewed: bool = False
    starred: bool = False
    tags: List[str] = Field(default_factory=list)

    # AI classification fields
    category: Optional[str] = "Other"
    confidence_score: Optional[int] = 0
    reason: Optional[str] = ""
    suggested_action: Optional[str] = ""

    # Client/subscription detection fields
    is_client_related: bool = False
    is_subscription_related: bool = False
    is_unimportant_or_ad: bool = False
    detected_provider: Optional[str] = ""


class TagEmailRequest(BaseModel):
    """
    Request body for adding a tag to an email.
    """

    tag_name: str = Field(
        ...,
        min_length=1,
        description="Tag name to apply to the email.",
        examples=["Needs Finance Review", "Subscription", "Renewal"],
    )