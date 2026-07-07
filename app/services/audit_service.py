from datetime import datetime


AUDIT_LOGS = []


def create_audit_log(event_type, details):
    """
    Create one audit log entry.

    This is an in-memory audit log for development.
    Later, this can be replaced with a database or company audit API.
    """

    entry = {
        "timestamp": datetime.now().isoformat(timespec="seconds"),
        "event_type": event_type,
        "details": details,
    }

    AUDIT_LOGS.append(entry)

    return entry


def log_prompt(prompt, agent_result):
    """
    Log the user prompt and matched emails.
    """

    matched_emails = agent_result.get("emails", [])

    matched_email_ids = [
        email.get("id")
        for email in matched_emails
    ]

    return create_audit_log(
        event_type="agent_prompt",
        details={
            "prompt": prompt,
            "agent_status": agent_result.get("status"),
            "interpreted_intent": agent_result.get("interpreted_intent"),
            "matched_count": len(matched_emails),
            "matched_email_ids": matched_email_ids,
            "tools_used": agent_result.get("tools_used", []),
        },
    )


def log_action(action, email_id=None, extra_details=None):
    """
    Log a user action.
    """

    details = {
        "action": action,
        "email_id": email_id,
    }

    if extra_details:
        details.update(extra_details)

    return create_audit_log(
        event_type="user_action",
        details=details,
    )


def get_audit_logs():
    """
    Return newest logs first.
    """

    return list(reversed(AUDIT_LOGS))