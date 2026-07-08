from typing import List, Optional

from pydantic import BaseModel, Field


class EmailSchema(BaseModel):
    """
    Normalized email structure used by the application.

    The mock provider currently returns emails in this shape.
    Later, Microsoft Graph emails should be converted into this same shape.
    """

    id: str
    thread_id: str
    sender: str
    sender_email: str
    recipient_email: str
    subject: str
    date: str
    body: str

    preview: Optional[str] = ""
    summary: Optional[str] = ""
    category: Optional[str] = "Other"
    confidence_score: Optional[int] = 0
    reviewed: bool = False
    starred: bool = False
    tags: List[str] = Field(default_factory=list)


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