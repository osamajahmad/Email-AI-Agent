import csv
import io


def build_emails_csv(emails):
    """
    Convert email records into CSV text.
    """

    output = io.StringIO()

    fieldnames = [
        "id",
        "thread_id",
        "sender",
        "sender_email",
        "recipient_email",
        "subject",
        "date",
        "category",
        "summary",
        "confidence_score",
        "reason",
        "suggested_action",
        "reviewed",
        "tags",
        "body",
    ]

    writer = csv.DictWriter(
        output,
        fieldnames=fieldnames,
    )

    writer.writeheader()

    for email in emails:
        writer.writerow(
            {
                "id": email.get("id", ""),
                "thread_id": email.get("thread_id", ""),
                "sender": email.get("sender", ""),
                "sender_email": email.get("sender_email", ""),
                "recipient_email": email.get("recipient_email", ""),
                "subject": email.get("subject", ""),
                "date": email.get("date", ""),
                "category": email.get("category", ""),
                "summary": email.get("summary", ""),
                "confidence_score": email.get("confidence_score", ""),
                "reason": email.get("reason", ""),
                "suggested_action": email.get("suggested_action", ""),
                "reviewed": email.get("reviewed", ""),
                "tags": ", ".join(email.get("tags", [])),
                "body": email.get("body", ""),
            }
        )

    return output.getvalue()