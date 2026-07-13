import os

import httpx
from dotenv import load_dotenv

# This allows the app to read EMAIL_PROVIDER and MOCK_PROVIDER_BASE_URL
load_dotenv()


def get_active_email_provider():
    """
    Return the active email provider name.
    """

    return os.getenv("EMAIL_PROVIDER", "mock").strip().lower()


def get_mock_provider_base_url():
    """
    Return the mock provider base URL.
    """

    return os.getenv(
        "MOCK_PROVIDER_BASE_URL",
        "http://127.0.0.1:8000",
    ).strip()


def get_mock_provider_emails():
    """
    Fetch emails from the mock email provider API.
    """

    base_url = get_mock_provider_base_url()

    # Even though the mock provider is inside the FastAPI app, it acts like it comes from a provider, so it proves that its not a frontend hardcode
    response = httpx.get(
        f"{base_url}/mock-provider/emails",
        timeout=10,
    )

    response.raise_for_status()

    data = response.json()

    return data.get("emails", [])


def get_mock_provider_email_by_id(email_id):
    """
    Fetch one email from the mock email provider API.
    """

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
    """
    Fetch one email thread from the mock email provider API.
    """

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
    """
    Mark one email as reviewed through the mock provider API.
    """

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
    """
    Add a tag through the mock provider API.
    """

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
    """
    Get emails from the active email provider.
    """

    active_provider = get_active_email_provider()

    if active_provider == "mock":
        return get_mock_provider_emails()

    if active_provider == "microsoft_graph":
        return get_graph_emails()

    return []


def get_email_by_id(email_id):
    """
    Get one email from the active provider.
    """

    active_provider = get_active_email_provider()

    if active_provider == "mock":
        return get_mock_provider_email_by_id(email_id)

    return None


def get_thread_emails(thread_id):
    """
    Get one thread from the active provider.
    """

    active_provider = get_active_email_provider()

    if active_provider == "mock":
        return get_mock_provider_thread(thread_id)

    return []


def mark_email_as_reviewed(email_id):
    """
    Mark one email as reviewed using the active provider.
    """

    active_provider = get_active_email_provider()

    if active_provider == "mock":
        return mark_mock_provider_email_as_reviewed(email_id)

    return None


def add_email_tag(email_id, tag_name):
    """
    Add one tag using the active provider.
    """

    active_provider = get_active_email_provider()

    if active_provider == "mock":
        return add_mock_provider_email_tag(
            email_id=email_id,
            tag_name=tag_name,
        )

    return None