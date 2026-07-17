import json
from collections import defaultdict
from datetime import datetime
import re

from app.services.gemini_service import (
    GeminiServiceError,
    generate_json,
    get_model_status,
)


def clamp_confidence(value):
    """
    Keep confidence score between 0 and 100.
    """

    try:
        number = int(value)
    except (TypeError, ValueError):
        return 0

    return max(0, min(100, number))


def parse_email_datetime(email):
    """
    Parse the received_at value first, then fall back to date.
    """

    received_at = email.get("received_at") or ""

    if received_at:
        try:
            return datetime.fromisoformat(received_at)
        except ValueError:
            pass

    date_value = email.get("date") or ""

    for date_format in ["%B %d, %Y", "%b %d, %Y", "%Y-%m-%d"]:
        try:
            return datetime.strptime(date_value, date_format)
        except ValueError:
            continue

    return None


def parse_date_value(value):
    """
    Parse YYYY-MM-DD date values from request fields.
    """

    if not value:
        return None

    try:
        return datetime.strptime(value, "%Y-%m-%d")
    except ValueError:
        return None


def extract_date_range_from_prompt(prompt):
    """
    Extract a simple date range from prompts like:
    'from July 1, 2026 to July 31, 2026'
    """

    pattern = r"from\s+([A-Za-z]+\s+\d{1,2},\s+\d{4})\s+to\s+([A-Za-z]+\s+\d{1,2},\s+\d{4})"
    match = re.search(pattern, prompt, re.IGNORECASE)

    if not match:
        return None, None

    try:
        start_date = datetime.strptime(match.group(1), "%B %d, %Y")
        end_date = datetime.strptime(match.group(2), "%B %d, %Y")
        return start_date, end_date
    except ValueError:
        return None, None


def email_is_inside_date_range(email, start_date=None, end_date=None):
    """
    Check if email date is inside the selected date range.
    """

    email_datetime = parse_email_datetime(email)

    if not email_datetime:
        return True

    if start_date and email_datetime < start_date:
        return False

    if end_date:
        end_of_day = end_date.replace(hour=23, minute=59, second=59)
        if email_datetime > end_of_day:
            return False

    return True


def detect_agent_mode(user_prompt, mode=None):
    """
    Decide whether the prompt is one of Bassem's required task modes.
    """

    if mode and mode != "general":
        return mode

    prompt = user_prompt.lower()

    if "unread" in prompt and ("client" in prompt or "clients" in prompt):
        return "unread_clients"

    if "subscription" in prompt and ("provider" in prompt or "group" in prompt or "period" in prompt):
        return "subscriptions_by_provider"

    return "general"


def is_unread_client_email(email):
    """
    Detect unread client emails and remove ads/unimportant emails.
    """

    is_unread = email.get("is_read") is False
    is_client_related = email.get("is_client_related") is True
    has_previous_contact = email.get("has_previous_contact") is True
    is_unimportant_or_ad = email.get("is_unimportant_or_ad") is True

    if not is_unread:
        return False

    if is_unimportant_or_ad:
        return False

    if is_client_related or has_previous_contact:
        return True

    return False


def is_subscription_email(email):
    """
    Detect subscription-related emails using stored flags and fallback keywords.
    """

    if email.get("is_subscription_related") is True:
        return True

    text = " ".join([
        email.get("subject", ""),
        email.get("body", ""),
        email.get("category", ""),
        " ".join(email.get("tags", [])),
    ]).lower()

    subscription_keywords = [
        "subscription",
        "renewal",
        "renews",
        "renewed",
        "billing period",
        "invoice",
        "license",
        "amount paid",
        "amount charged",
        "plan renewal",
    ]

    return any(keyword in text for keyword in subscription_keywords)


def get_subscription_provider(email):
    """
    Return the detected subscription provider.
    """

    detected_provider = email.get("detected_provider")

    if detected_provider:
        return detected_provider

    sender = email.get("sender", "")

    if sender:
        return sender.replace("Billing", "").replace("Renewals", "").strip()

    return "Unknown Provider"


def run_unread_client_agent(user_prompt, emails):
    """
    Required Task 4 update:
    Get unread client emails and filter out ads/unimportant emails.
    """

    matched_emails = []

    for email in emails:
        if not is_unread_client_email(email):
            continue

        enriched_email = {
            **email,
            "category": email.get("category") or "Client Email",
            "summary": email.get("summary") or email.get("preview") or email.get("body", "")[:180],
            "confidence_score": 100,
            "reason": "This email is unread, client-related, and is not classified as an ad, newsletter, promotion, or unimportant email.",
            "suggested_action": "Open the email thread and respond or assign it to the correct team member.",
        }

        matched_emails.append(enriched_email)

    matched_emails.sort(
        key=lambda item: parse_email_datetime(item) or datetime.min,
        reverse=True,
    )

    return {
        "status": "success",
        "model_status": get_model_status(),
        "result_type": "email_list",
        "interpreted_intent": "The user wants unread client emails while filtering out ads and unimportant emails.",
        "agent_answer": f"I found {len(matched_emails)} unread client email{'' if len(matched_emails) == 1 else 's'} after filtering out ads, newsletters, promotions, and unimportant emails.",
        "tools_used": [
            "Prompt Understanding Tool",
            "Email Provider Tool",
            "Unread Email Filter",
            "Client Relationship Detection",
            "Ad and Unimportant Email Filter",
        ],
        "emails": matched_emails,
        "provider_summary": [],
        "error": "",
    }


def run_subscriptions_by_provider_agent(user_prompt, emails, start_date=None, end_date=None):
    """
    Required Task 4 update:
    Get subscription emails in a specific time period and group them by provider.
    """

    prompt_start, prompt_end = extract_date_range_from_prompt(user_prompt)

    final_start_date = parse_date_value(start_date) or prompt_start
    final_end_date = parse_date_value(end_date) or prompt_end

    matched_emails = []

    for email in emails:
        if not is_subscription_email(email):
            continue

        if not email_is_inside_date_range(
            email=email,
            start_date=final_start_date,
            end_date=final_end_date,
        ):
            continue

        provider = get_subscription_provider(email)

        enriched_email = {
            **email,
            "category": email.get("category") or "Subscription",
            "summary": email.get("summary") or email.get("preview") or email.get("body", "")[:180],
            "confidence_score": email.get("confidence_score") or 95,
            "reason": "This email appears to be related to a subscription, renewal, license, invoice, or recurring service.",
            "suggested_action": "Review the subscription details and confirm whether it should be tracked or exported.",
            "detected_provider": provider,
        }

        matched_emails.append(enriched_email)

    grouped = defaultdict(list)

    for email in matched_emails:
        grouped[get_subscription_provider(email)].append(email)

    provider_summary = []

    for provider, provider_emails in grouped.items():
        latest_email = sorted(
            provider_emails,
            key=lambda item: parse_email_datetime(item) or datetime.min,
            reverse=True,
        )[0]

        provider_summary.append({
            "provider": provider,
            "count": len(provider_emails),
            "latest_email_date": latest_email.get("date", ""),
            "latest_subject": latest_email.get("subject", ""),
            "category": latest_email.get("category", "Subscription"),
        })

    provider_summary.sort(
        key=lambda item: item["provider"].lower(),
    )

    matched_emails.sort(
        key=lambda item: parse_email_datetime(item) or datetime.min,
        reverse=True,
    )

    date_text = ""

    if final_start_date and final_end_date:
        date_text = f" from {final_start_date.strftime('%B %d, %Y')} to {final_end_date.strftime('%B %d, %Y')}"

    return {
        "status": "success",
        "model_status": get_model_status(),
        "result_type": "subscription_provider_table",
        "interpreted_intent": f"The user wants subscription-related emails{date_text}, grouped by provider.",
        "agent_answer": f"I found {len(matched_emails)} subscription-related email{'' if len(matched_emails) == 1 else 's'}{date_text}, grouped by {len(provider_summary)} provider{'' if len(provider_summary) == 1 else 's'}.",
        "tools_used": [
            "Prompt Understanding Tool",
            "Email Provider Tool",
            "Date Range Filter",
            "Subscription Detection Tool",
            "Provider Grouping Tool",
        ],
        "emails": matched_emails,
        "provider_summary": provider_summary,
        "error": "",
    }


def prepare_email_for_agent(email):
    """
    Prepare email data before sending it to Gemini.
    """

    return {
        "id": email.get("id", ""),
        "thread_id": email.get("thread_id", ""),
        "provider": email.get("provider", "mock"),
        "sender": email.get("sender", ""),
        "sender_email": email.get("sender_email", ""),
        "recipient_email": email.get("recipient_email", ""),
        "subject": email.get("subject", ""),
        "date": email.get("date", ""),
        "received_at": email.get("received_at", ""),
        "body": email.get("body", "")[:1500],
        "is_read": email.get("is_read", False),
        "reviewed": email.get("reviewed", False),
        "tags": email.get("tags", []),
        "is_client_related": email.get("is_client_related", False),
        "is_subscription_related": email.get("is_subscription_related", False),
        "is_unimportant_or_ad": email.get("is_unimportant_or_ad", False),
        "detected_provider": email.get("detected_provider", ""),
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


def run_general_ai_agent(user_prompt, emails):
    """
    General Gemini-based Email AI Agent mode.
    """

    model_status = get_model_status()

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
            "result_type": "email_list",
            "interpreted_intent": agent_response.get("interpreted_intent", ""),
            "agent_answer": agent_response.get("agent_answer", ""),
            "tools_used": agent_response.get("tools_used", []),
            "emails": matched_emails,
            "provider_summary": [],
            "error": "",
        }

    except GeminiServiceError as error:
        return {
            "status": "ai_error",
            "model_status": model_status,
            "result_type": "email_list",
            "interpreted_intent": "",
            "agent_answer": "The Email AI Agent could not complete the request.",
            "tools_used": [],
            "emails": [],
            "provider_summary": [],
            "error": str(error),
        }

    except Exception as error:
        return {
            "status": "system_error",
            "model_status": model_status,
            "result_type": "email_list",
            "interpreted_intent": "",
            "agent_answer": "A system error occurred while running the Email AI Agent.",
            "tools_used": [],
            "emails": [],
            "provider_summary": [],
            "error": str(error),
        }


def run_email_agent(user_prompt, emails, mode="general", start_date=None, end_date=None):
    """
    Main Email AI Agent function.
    """

    if not user_prompt.strip():
        return {
            "status": "empty_prompt",
            "model_status": get_model_status(),
            "result_type": "email_list",
            "interpreted_intent": "",
            "agent_answer": "Please enter a request for the Email AI Agent.",
            "tools_used": [],
            "emails": [],
            "provider_summary": [],
            "error": "",
        }

    detected_mode = detect_agent_mode(
        user_prompt=user_prompt,
        mode=mode,
    )

    if detected_mode == "unread_clients":
        return run_unread_client_agent(
            user_prompt=user_prompt,
            emails=emails,
        )

    if detected_mode == "subscriptions_by_provider":
        return run_subscriptions_by_provider_agent(
            user_prompt=user_prompt,
            emails=emails,
            start_date=start_date,
            end_date=end_date,
        )

    return run_general_ai_agent(
        user_prompt=user_prompt,
        emails=emails,
    )