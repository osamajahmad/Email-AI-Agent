import os

import httpx
from dotenv import load_dotenv

from app.services.gmail_provider import (
    get_gmail_email_by_id,
    get_gmail_emails,
    get_gmail_thread,
)
from app.services.microsoft_graph_provider import (
    get_graph_email_by_id,
    get_graph_emails,
    get_graph_thread,
)


load_dotenv()


def get_active_email_provider():
    return os.getenv("EMAIL_PROVIDER", "mock").strip().lower()


def get_mock_provider_base_url():
    return os.getenv(
        "MOCK_PROVIDER_BASE_URL",
        "http://127.0.0.1:8000",
    ).strip()


def get_mock_provider_emails():
    base_url = get_mock_provider_base_url()

    response = httpx.get(
        f"{base_url}/mock-provider/emails",
        timeout=10,
    )

    response.raise_for_status()

    data = response.json()

    return data.get("emails", [])


def get_mock_provider_email_by_id(email_id):
    base_url = get_mock_provider_base_url()

    response = httpx.get(
        f"{base_url}/mock-provider/emails/{email_id}",
        timeout=10,
    )

    if response.status_code == 404:
        return None

    response.raise_for_status()

    return response.json()


def get_mock_provider_thread(thread_id):
    base_url = get_mock_provider_base_url()

    response = httpx.get(
        f"{base_url}/mock-provider/threads/{thread_id}",
        timeout=10,
    )

    if response.status_code == 404:
        return []

    response.raise_for_status()

    data = response.json()

    return data.get("emails", [])


def mark_mock_provider_email_as_reviewed(email_id):
    base_url = get_mock_provider_base_url()

    response = httpx.post(
        f"{base_url}/mock-provider/emails/{email_id}/reviewed",
        timeout=10,
    )

    if response.status_code == 404:
        return None

    response.raise_for_status()

    return response.json()


def add_mock_provider_email_tag(email_id, tag_name):
    base_url = get_mock_provider_base_url()

    response = httpx.post(
        f"{base_url}/mock-provider/emails/{email_id}/tags",
        data={
            "tag_name": tag_name,
        },
        timeout=10,
    )

    if response.status_code in [400, 404]:
        return None

    response.raise_for_status()

    return response.json()


def get_emails():
    active_provider = get_active_email_provider()

    if active_provider == "mock":
        return get_mock_provider_emails()

    if active_provider == "gmail":
        return get_gmail_emails()

    if active_provider == "microsoft_graph":
        return get_graph_emails()

    return []


def get_email_by_id(email_id):
    active_provider = get_active_email_provider()

    if active_provider == "mock":
        return get_mock_provider_email_by_id(email_id)

    if active_provider == "gmail":
        return get_gmail_email_by_id(email_id)

    if active_provider == "microsoft_graph":
        return get_graph_email_by_id(email_id)

    return None


def get_thread_emails(thread_id):
    active_provider = get_active_email_provider()

    if active_provider == "mock":
        return get_mock_provider_thread(thread_id)

    if active_provider == "gmail":
        return get_gmail_thread(thread_id)

    if active_provider == "microsoft_graph":
        return get_graph_thread(thread_id)

    return []


def mark_email_as_reviewed(email_id):
    active_provider = get_active_email_provider()

    if active_provider == "mock":
        return mark_mock_provider_email_as_reviewed(email_id)

    # For Gmail/Outlook, reviewed should be stored internally in the app.
    # We will add internal reviewed-state support in the next step.
    return None


def add_email_tag(email_id, tag_name):
    active_provider = get_active_email_provider()

    if active_provider == "mock":
        return add_mock_provider_email_tag(
            email_id=email_id,
            tag_name=tag_name,
        )

    # For Gmail/Outlook, tags should be stored internally in the app.
    # We will add internal tag-state support in the next step.
    return None

def get_provider_connection_status():
    active_provider = get_active_email_provider()

    if active_provider == "mock":
        return {
            "provider": "Mock Provider",
            "status": "Connected",
            "message": "Using mock provider data for demo and testing.",
            "connected": True,
        }

    if active_provider == "gmail":
        gmail_token = os.getenv("GMAIL_ACCESS_TOKEN", "").strip()

        return {
            "provider": "Gmail",
            "status": "Connected" if gmail_token else "Not connected",
            "message": "Gmail token found." if gmail_token else "Gmail provider selected, but no access token is configured yet.",
            "connected": bool(gmail_token),
        }

    if active_provider == "microsoft_graph":
        graph_token = os.getenv("MS_GRAPH_ACCESS_TOKEN", "").strip()

        return {
            "provider": "Outlook / Microsoft Graph",
            "status": "Connected" if graph_token else "Not connected",
            "message": "Microsoft Graph token found." if graph_token else "Microsoft Graph provider selected, but no access token is configured yet.",
            "connected": bool(graph_token),
        }

    return {
        "provider": active_provider,
        "status": "Unknown provider",
        "message": "The selected email provider is not supported.",
        "connected": False,
    }