MOCK_EMAILS = [
    {
        "id": "email_001",
        "thread_id": "thread_adobe_001",
        "sender": "Adobe Billing",
        "sender_email": "billing@adobe.com",
        "recipient_email": "finance@cspsolutions.com",
        "subject": "Your Creative Cloud plan renewal",
        "date": "May 24, 2025",
        "body": "Your Adobe Creative Cloud plan renews on May 28, 2025. Your subscription will continue using the saved payment method unless canceled before the renewal date.",
        "category": "Subscription",
        "confidence_score": 96,
        "preview": "Your plan renews on May 28, 2025. Your subscription will continue...",
        "reviewed": False,
        "tags": [],
    },
    {
        "id": "email_002",
        "thread_id": "thread_aws_001",
        "sender": "AWS",
        "sender_email": "billing@aws.amazon.com",
        "recipient_email": "finance@cspsolutions.com",
        "subject": "Monthly usage invoice available",
        "date": "May 24, 2025",
        "body": "Your AWS invoice for April 2025 is ready to view. The invoice includes cloud hosting, compute, storage, and data transfer usage.",
        "category": "Invoice",
        "confidence_score": 95,
        "preview": "Your AWS invoice for April 2025 is ready to view...",
        "reviewed": False,
        "tags": [],
    },
    {
        "id": "email_003",
        "thread_id": "thread_godaddy_001",
        "sender": "GoDaddy",
        "sender_email": "renewals@godaddy.com",
        "recipient_email": "it@cspsolutions.com",
        "subject": "Domain renewal reminder",
        "date": "May 23, 2025",
        "body": "Your domain subscription is close to expiration. Renew before it expires to avoid DNS, hosting, and email service interruption.",
        "category": "Domain",
        "confidence_score": 92,
        "preview": "Don’t lose your domain. Renew before it expires...",
        "reviewed": False,
        "tags": [],
    },
    {
        "id": "email_004",
        "thread_id": "thread_notion_001",
        "sender": "Notion",
        "sender_email": "billing@notion.so",
        "recipient_email": "alex.morgan@cspsolutions.com",
        "subject": "Workspace subscription receipt",
        "date": "May 23, 2025",
        "body": "Thank you for your payment!\n\nHi Alex,\n\nThank you for renewing your Notion workspace subscription.\n\nHere are your receipt details:\n\nWorkspace: CSP Solutions\nPlan: Notion Business\nBilling Period: May 23, 2025 – June 22, 2025\nAmount Paid: $16.00 USD\nPayment Method: Visa **** **** **** 4242\nReceipt ID: INV-2025-0523-8847\n\nYou can manage your subscription and billing details here.\n\nThanks,\nThe Notion Team",
        "category": "Subscription",
        "confidence_score": 94,
        "preview": "Thank you for your payment. Here’s your receipt...",
        "reviewed": False,
        "tags": [],
    },
    {
        "id": "email_005",
        "thread_id": "thread_zoom_001",
        "sender": "Zoom",
        "sender_email": "billing@zoom.us",
        "recipient_email": "it@cspsolutions.com",
        "subject": "License renewal confirmation",
        "date": "May 22, 2025",
        "body": "Your Zoom license has been renewed successfully. Your current plan will remain active for the next billing cycle.",
        "category": "License",
        "confidence_score": 93,
        "preview": "Your Zoom license has been renewed successfully...",
        "reviewed": False,
        "tags": [],
    },
    {
        "id": "email_006",
        "thread_id": "thread_azure_001",
        "sender": "Microsoft Azure",
        "sender_email": "azure-noreply@microsoft.com",
        "recipient_email": "cloud@cspsolutions.com",
        "subject": "Azure monthly usage summary",
        "date": "May 22, 2025",
        "body": "Review your Azure usage and charges for April 2025. This includes cloud compute, database, and hosting resources.",
        "category": "Cloud",
        "confidence_score": 91,
        "preview": "Review your Azure usage and charges for April 2025...",
        "reviewed": False,
        "tags": [],
    },
    {
        "id": "email_007",
        "thread_id": "thread_atlassian_001",
        "sender": "Atlassian",
        "sender_email": "billing@atlassian.com",
        "recipient_email": "it@cspsolutions.com",
        "subject": "Your Jira Software renewal",
        "date": "May 21, 2025",
        "body": "Your Jira Software subscription is set to renew soon. Please review your billing details and license count.",
        "category": "Software Renewal",
        "confidence_score": 90,
        "preview": "Your Jira Software subscription is set to renew...",
        "reviewed": False,
        "tags": [],
    },
    {
        "id": "email_008",
        "thread_id": "thread_digitalocean_001",
        "sender": "DigitalOcean",
        "sender_email": "billing@digitalocean.com",
        "recipient_email": "finance@cspsolutions.com",
        "subject": "Invoice for April 2025",
        "date": "May 21, 2025",
        "body": "Here is your DigitalOcean invoice for April 2025. It includes droplets, storage, databases, and bandwidth usage.",
        "category": "Invoice",
        "confidence_score": 89,
        "preview": "Here’s your DigitalOcean invoice for April 2025...",
        "reviewed": False,
        "tags": [],
    },
]


def get_mock_emails():
    return MOCK_EMAILS


def get_mock_email_by_id(email_id):
    for email in MOCK_EMAILS:
        if email["id"] == email_id:
            return email

    return None


def get_mock_emails_by_thread_id(thread_id):
    return [
        email
        for email in MOCK_EMAILS
        if email["thread_id"] == thread_id
    ]


def mark_mock_email_as_reviewed(email_id):
    email = get_mock_email_by_id(email_id)

    if not email:
        return None

    email["reviewed"] = True

    return email


def add_mock_email_tag(email_id, tag_name):
    email = get_mock_email_by_id(email_id)

    if not email:
        return None

    cleaned_tag = tag_name.strip()

    if not cleaned_tag:
        return None

    if cleaned_tag not in email["tags"]:
        email["tags"].append(cleaned_tag)

    return email