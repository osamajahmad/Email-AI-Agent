import json

from app.services.gemini_service import (
    GeminiServiceError,
    generate_json,
    get_model_status,
)


def prepare_email_for_agent(email):
    """
    Prepare email data before sending it to the AI model.
    """

    return {
        "id": email.get("id", ""),
        "thread_id": email.get("thread_id", ""),
        "sender": email.get("sender", ""),
        "sender_email": email.get("sender_email", ""),
        "recipient_email": email.get("recipient_email", ""),
        "subject": email.get("subject", ""),
        "date": email.get("date", ""),
        "body": email.get("body", "")[:1500],
        "reviewed": email.get("reviewed", False),
        "tags": email.get("tags", []),
    }


def build_agent_prompt(user_prompt, emails):
    """
    Build the structured Email AI Agent prompt for Gemini.
    """

    prepared_emails = [
        prepare_email_for_agent(email)
        for email in emails
    ]

    return f"""
You are an internal Email AI Agent for CSP Solutions.

Your job:
- Understand the user's natural-language request.
- Inspect the provided company emails.
- Decide which emails match the user's intent.
- Classify each matching email.
- Summarize each matching email.
- Give a confidence score from 0 to 100.
- Explain why each email matched.
- Suggest a practical user action.

Important rules:
- Do not use keyword matching only.
- Use meaning and context.
- Do not invent emails.
- Only use the email data provided.
- Return JSON only.
- Do not return markdown.
- Do not include emails that do not match the user's request.

User prompt:
{user_prompt}

Available emails:
{json.dumps(prepared_emails, indent=2)}

Return this exact JSON structure:
{{
    "interpreted_intent": "One sentence explaining what the user is asking for.",
    "agent_answer": "Short summary of what the agent found.",
    "tools_used": [
        "Prompt Understanding Tool",
        "Email Provider Tool",
        "Email Inspection Tool",
        "AI Classification Tool",
        "AI Summary Tool",
        "Confidence Scoring Tool"
    ],
    "matched_emails": [
        {{
            "id": "email id from provided emails",
            "category": "Subscription Renewal / Invoice / Cloud Hosting / Domain Renewal / Software License / Client Support / Other",
            "summary": "Short summary of this email.",
            "confidence_score": 95,
            "reason": "Why this email matches the user's prompt.",
            "suggested_action": "What the user should do next."
        }}
    ]
}}
"""


def clamp_confidence(value):
    """
    Keep confidence score between 0 and 100.
    """

    try:
        number = int(value)
    except (TypeError, ValueError):
        return 0

    return max(0, min(100, number))


def merge_agent_results(agent_response, source_emails):
    """
    Merge Gemini results with the original email data.
    """

    emails_by_id = {
        email.get("id"): email
        for email in source_emails
    }

    matched_emails = []

    for result in agent_response.get("matched_emails", []):
        email_id = result.get("id")

        if email_id not in emails_by_id:
            continue

        original_email = emails_by_id[email_id]

        enriched_email = {
            **original_email,
            "category": result.get("category", "Other"),
            "summary": result.get("summary", ""),
            "confidence_score": clamp_confidence(
                result.get("confidence_score", 0)
            ),
            "reason": result.get("reason", ""),
            "suggested_action": result.get("suggested_action", ""),
        }

        matched_emails.append(enriched_email)

    matched_emails.sort(
        key=lambda email: email.get("confidence_score", 0),
        reverse=True,
    )

    return matched_emails


def run_email_agent(user_prompt, emails):
    """
    Main Email AI Agent function.
    """

    model_status = get_model_status()

    if not user_prompt.strip():
        return {
            "status": "empty_prompt",
            "model_status": model_status,
            "interpreted_intent": "",
            "agent_answer": "Please enter a request for the Email AI Agent.",
            "tools_used": [],
            "emails": [],
            "error": "",
        }

    try:
        agent_prompt = build_agent_prompt(
            user_prompt=user_prompt,
            emails=emails,
        )

        agent_response = generate_json(agent_prompt)

        matched_emails = merge_agent_results(
            agent_response=agent_response,
            source_emails=emails,
        )

        return {
            "status": "success",
            "model_status": model_status,
            "interpreted_intent": agent_response.get("interpreted_intent", ""),
            "agent_answer": agent_response.get("agent_answer", ""),
            "tools_used": agent_response.get("tools_used", []),
            "emails": matched_emails,
            "error": "",
        }

    except GeminiServiceError as error:
        return {
            "status": "ai_error",
            "model_status": model_status,
            "interpreted_intent": "",
            "agent_answer": "The Email AI Agent could not complete the request.",
            "tools_used": [],
            "emails": [],
            "error": str(error),
        }

    except Exception as error:
        return {
            "status": "system_error",
            "model_status": model_status,
            "interpreted_intent": "",
            "agent_answer": "A system error occurred while running the Email AI Agent.",
            "tools_used": [],
            "emails": [],
            "error": str(error),
        }