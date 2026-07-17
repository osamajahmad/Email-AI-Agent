import os
from datetime import datetime, timezone
from email.utils import parseaddr, parsedate_to_datetime

import httpx


GMAIL_API_BASE_URL = "https://gmail.googleapis.com/gmail/v1/users/me"


def get_gmail_access_token():
    return os.getenv("GMAIL_ACCESS_TOKEN", "").strip()


def get_gmail_headers():
    token = get_gmail_access_token()

    if not token:
        return None

    return {
        "Authorization": f"Bearer {token}",
        "Accept": "application/json",
    }


def extract_gmail_headers(message):
    payload = message.get("payload", {})
    headers = payload.get("headers", [])

    return {
        header.get("name", "").lower(): header.get("value", "")
        for header in headers
    }


def parse_gmail_datetime(message, header_date):
    internal_date = message.get("internalDate")

    if internal_date:
        try:
            return datetime.fromtimestamp(
                int(internal_date) / 1000,
                tz=timezone.utc,
            )
        except (TypeError, ValueError):
            pass

    if header_date:
        try:
            return parsedate_to_datetime(header_date)
        except (TypeError, ValueError):
            pass

    return None


def normalize_gmail_message(message):
    gmail_headers = extract_gmail_headers(message)

    from_header = gmail_headers.get("from", "")
    to_header = gmail_headers.get("to", "")
    subject = gmail_headers.get("subject", "(No subject)")
    header_date = gmail_headers.get("date", "")

    sender_name, sender_email = parseaddr(from_header)
    _, recipient_email = parseaddr(to_header)

    received_datetime = parse_gmail_datetime(
        message=message,
        header_date=header_date,
    )

    if received_datetime:
        date_text = received_datetime.strftime("%B %d, %Y")
        received_at = received_datetime.isoformat()
    else:
        date_text = header_date
        received_at = ""

    label_ids = message.get("labelIds", [])

    provider_message_id = message.get("id", "")
    provider_thread_id = message.get("threadId", "")

    return {
        "id": f"gmail_{provider_message_id}",
        "thread_id": f"gmail_thread_{provider_thread_id}",
        "provider": "gmail",
        "provider_message_id": provider_message_id,
        "provider_thread_id": provider_thread_id,
        "sender": sender_name or sender_email or "Unknown Sender",
        "sender_email": sender_email,
        "recipient_email": recipient_email,
        "subject": subject,
        "date": date_text,
        "received_at": received_at,
        "body": message.get("snippet", ""),
        "preview": message.get("snippet", ""),
        "summary": "",
        "is_read": "UNREAD" not in label_ids,
        "reviewed": False,
        "starred": "STARRED" in label_ids,
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


def fetch_gmail_message(provider_message_id):
    headers = get_gmail_headers()

    if not headers:
        return None

    clean_message_id = provider_message_id.replace("gmail_", "")

    response = httpx.get(
        f"{GMAIL_API_BASE_URL}/messages/{clean_message_id}",
        headers=headers,
        params=[
            ("format", "metadata"),
            ("metadataHeaders", "From"),
            ("metadataHeaders", "To"),
            ("metadataHeaders", "Subject"),
            ("metadataHeaders", "Date"),
        ],
        timeout=15,
    )

    if response.status_code == 404:
        return None

    response.raise_for_status()

    return normalize_gmail_message(response.json())


def get_gmail_emails(max_results=20, query="in:inbox"):
    headers = get_gmail_headers()

    if not headers:
        return []

    response = httpx.get(
        f"{GMAIL_API_BASE_URL}/messages",
        headers=headers,
        params={
            "maxResults": max_results,
            "q": query,
        },
        timeout=15,
    )

    response.raise_for_status()

    message_refs = response.json().get("messages", [])

    emails = []

    for message_ref in message_refs:
        message = fetch_gmail_message(message_ref.get("id", ""))

        if message:
            emails.append(message)

    return emails


def get_gmail_email_by_id(email_id):
    return fetch_gmail_message(email_id)


def get_gmail_thread(thread_id):
    headers = get_gmail_headers()

    if not headers:
        return []

    clean_thread_id = thread_id.replace("gmail_thread_", "")

    response = httpx.get(
        f"{GMAIL_API_BASE_URL}/threads/{clean_thread_id}",
        headers=headers,
        params={
            "format": "metadata",
        },
        timeout=15,
    )

    if response.status_code == 404:
        return []

    response.raise_for_status()

    thread_data = response.json()

    return [
        normalize_gmail_message(message)
        for message in thread_data.get("messages", [])
    ]