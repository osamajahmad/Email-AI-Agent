import os
from datetime import datetime
from email.utils import parseaddr

import httpx


GRAPH_API_BASE_URL = "https://graph.microsoft.com/v1.0"


def get_graph_access_token():
    return os.getenv("MS_GRAPH_ACCESS_TOKEN", "").strip()


def get_graph_headers():
    token = get_graph_access_token()

    if not token:
        return None

    return {
        "Authorization": f"Bearer {token}",
        "Accept": "application/json",
    }


def format_graph_date(received_at):
    if not received_at:
        return "", ""

    try:
        parsed_date = datetime.fromisoformat(
            received_at.replace("Z", "+00:00")
        )

        return parsed_date.strftime("%B %d, %Y"), parsed_date.isoformat()
    except ValueError:
        return received_at, received_at


def normalize_graph_message(message):
    from_info = (
        message.get("from", {})
        .get("emailAddress", {})
    )

    sender_name = from_info.get("name", "Unknown Sender")
    sender_email = from_info.get("address", "")

    recipients = message.get("toRecipients", [])

    recipient_email = ""

    if recipients:
        recipient_email = (
            recipients[0]
            .get("emailAddress", {})
            .get("address", "")
        )

    received_datetime = message.get("receivedDateTime", "")
    date_text, received_at = format_graph_date(received_datetime)

    provider_message_id = message.get("id", "")
    provider_thread_id = message.get("conversationId", "")

    return {
        "id": f"graph_{provider_message_id}",
        "thread_id": f"graph_thread_{provider_thread_id}",
        "provider": "microsoft_graph",
        "provider_message_id": provider_message_id,
        "provider_thread_id": provider_thread_id,
        "sender": sender_name or sender_email,
        "sender_email": sender_email,
        "recipient_email": recipient_email,
        "subject": message.get("subject") or "(No subject)",
        "date": date_text,
        "received_at": received_at,
        "body": message.get("bodyPreview", ""),
        "preview": message.get("bodyPreview", ""),
        "summary": "",
        "is_read": message.get("isRead", True),
        "reviewed": False,
        "starred": False,
        "tags": [],
        "category": "External Email",
        "confidence_score": 0,
        "reason": "",
        "suggested_action": "",
        "is_client_related": False,
        "is_subscription_related": False,
        "is_unimportant_or_ad": False,
        "detected_provider": "",
        "has_previous_contact": False,
    }


def get_graph_emails(max_results=20):
    headers = get_graph_headers()

    if not headers:
        return []

    response = httpx.get(
        f"{GRAPH_API_BASE_URL}/me/messages",
        headers=headers,
        params={
            "$top": max_results,
            "$orderby": "receivedDateTime desc",
            "$select": "id,conversationId,subject,from,toRecipients,receivedDateTime,bodyPreview,isRead",
        },
        timeout=15,
    )

    response.raise_for_status()

    messages = response.json().get("value", [])

    return [
        normalize_graph_message(message)
        for message in messages
    ]


def get_graph_email_by_id(email_id):
    headers = get_graph_headers()

    if not headers:
        return None

    clean_email_id = email_id.replace("graph_", "")

    response = httpx.get(
        f"{GRAPH_API_BASE_URL}/me/messages/{clean_email_id}",
        headers=headers,
        params={
            "$select": "id,conversationId,subject,from,toRecipients,receivedDateTime,bodyPreview,isRead",
        },
        timeout=15,
    )

    if response.status_code == 404:
        return None

    response.raise_for_status()

    return normalize_graph_message(response.json())


def get_graph_thread(thread_id):
    headers = get_graph_headers()

    if not headers:
        return []

    clean_thread_id = thread_id.replace("graph_thread_", "")

    response = httpx.get(
        f"{GRAPH_API_BASE_URL}/me/messages",
        headers=headers,
        params={
            "$filter": f"conversationId eq '{clean_thread_id}'",
            "$orderby": "receivedDateTime asc",
            "$select": "id,conversationId,subject,from,toRecipients,receivedDateTime,bodyPreview,isRead",
        },
        timeout=15,
    )

    if response.status_code == 404:
        return []

    response.raise_for_status()

    messages = response.json().get("value", [])

    return [
        normalize_graph_message(message)
        for message in messages
    ]