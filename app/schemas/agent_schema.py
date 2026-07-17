from typing import Optional

from pydantic import BaseModel, Field


class AgentAskRequest(BaseModel):
    """
    Request body for asking the Email AI Agent a natural-language prompt.
    """

    prompt: str = Field(
        ...,
        min_length=1,
        description="Natural-language prompt entered by the user.",
        examples=[
            "Filter emails that are subscription based.",
            "Get unread client emails and filter out ads and unimportant emails.",
            "Get subscription emails from July 1, 2026 to July 31, 2026 and group them by provider.",
        ],
    )

    mode: Optional[str] = Field(
        default="general",
        description="Optional agent mode: general, unread_clients, subscriptions_by_provider.",
    )

    start_date: Optional[str] = Field(
        default=None,
        description="Optional start date for date-based email searches. Format: YYYY-MM-DD.",
        examples=["2026-07-01"],
    )

    end_date: Optional[str] = Field(
        default=None,
        description="Optional end date for date-based email searches. Format: YYYY-MM-DD.",
        examples=["2026-07-31"],
    )