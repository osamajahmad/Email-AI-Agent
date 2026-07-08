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
            "Find urgent emails that need action today.",
        ],
    )