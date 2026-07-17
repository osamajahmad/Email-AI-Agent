# CSP Email AI Agent

An internal AI-powered email dashboard for **CSP Solutions**.

The purpose of this project is to allow CSP users to review, filter, classify, and act on company emails using natural language prompts through an AI assistant interface.

Users can ask prompts such as:

```text
Filter emails that are subscription based.
```

```text
Get unread client emails and filter out ads and unimportant emails.
```

```text
Get subscription emails from July 1, 2026 to July 31, 2026 and group them by provider.
```

The Email AI Agent analyzes available emails, detects subscription, renewal, invoice, license, SaaS, cloud, domain, software, and client-related emails, summarizes the results, assigns categories and confidence scores, and allows users to open, review, tag, and export the results.

---

## Project Overview

This project is built as a **FastAPI-based internal web application**.

The application uses a provider-based email architecture. During development, it can run with a mock email provider for testing and demo purposes. The project also includes provider structures for Gmail and Outlook/Microsoft Graph so the system can later connect to real mailboxes when OAuth credentials or access tokens are available.

The Email AI Agent does not depend on local mailbox files. It reads emails through the provider layer, normalizes them into one internal schema, and then allows the AI agent to classify, summarize, filter, tag, review, and export email results.

This update also includes the new Task 4 email integration requirements:

- Integrate the email agent with Gmail/Outlook so it can be tested.
- Check tools that can connect email accounts dynamically.
- Get unread client emails while filtering out ads and unimportant emails.
- Get subscription emails within a specific time period and output a table grouped by provider.

---

## Main Features

### Email Dashboard

- View company emails in an inbox-style dashboard.
- Browse emails manually.
- Select emails from the inbox list.
- View full email content in the preview page.
- Filter emails by category.
- Search emails by sender, subject, category, tag, or preview text.
- Sort emails by newest, confidence score, or sender.
- View dynamic inbox counts based on the active email provider.

### AI Agent

- Ask natural language prompts.
- AI reads the available inbox data.
- AI detects matching emails based on meaning and context.
- Backend logic handles required task-specific flows:
  - unread client email filtering
  - subscription emails grouped by provider
- AI returns structured results with:
  - sender
  - subject
  - date
  - summary
  - category
  - confidence score
  - reason
  - suggested action
- AI results appear inside the right-side assistant panel.
- The inbox stays visible while the AI works.

### Email Provider Layer

The project supports provider switching through the `EMAIL_PROVIDER` environment variable.

Supported provider modes:

```env
EMAIL_PROVIDER=mock
EMAIL_PROVIDER=gmail
EMAIL_PROVIDER=microsoft_graph
```

Current provider support:

- Mock provider for local development and demo data.
- Gmail provider structure for Gmail mailbox integration.
- Microsoft Graph provider structure for Outlook/Microsoft 365 mailbox integration.
- Provider connection status displayed in the dashboard.

### Email Actions

Users can perform actions from email cards or detail pages:

- Open email
- View thread
- Mark as reviewed
- Add tag
- Export email
- Export all emails
- Export AI results

### Audit Logging

The system logs important actions such as:

- AI prompt submitted
- Matched emails returned
- Email opened
- Email marked as reviewed
- Tag added
- Export created
- Thread viewed
- Audit logs viewed

This supports traceability and enterprise auditing.

### Export

The project supports CSV export for:

- All emails
- One selected email
- AI matched results

---

## Technology Stack

| Area | Technology |
|---|---|
| Backend | FastAPI |
| Server | Uvicorn |
| Templates | Jinja2 |
| AI Model | Google Gemini |
| HTTP Client | HTTPX |
| Environment Variables | python-dotenv |
| Form Handling | python-multipart |
| Frontend | HTML, CSS, JavaScript |
| Email Provider Layer | Mock Provider, Gmail Provider, Microsoft Graph Provider |
| Dynamic Email Tool Research | Nylas / Unified Email API options documented |

---

## Project Structure

```text
Task 4/
│
├── main.py
├── requirements.txt
├── README.md
├── .env.example
├── .gitignore
│
├── docs/
│   └── email-integration-options.md
│
├── app/
│   ├── __init__.py
│   │
│   ├── api/
│   │   ├── __init__.py
│   │   ├── agent_routes.py
│   │   ├── audit_routes.py
│   │   ├── email_routes.py
│   │   ├── mock_provider_routes.py
│   │   └── page_routes.py
│   │
│   ├── schemas/
│   │   ├── __init__.py
│   │   ├── agent_schema.py
│   │   └── email_schema.py
│   │
│   ├── services/
│   │   ├── __init__.py
│   │   ├── audit_service.py
│   │   ├── email_agent.py
│   │   ├── email_provider.py
│   │   ├── export_service.py
│   │   ├── gemini_service.py
│   │   ├── gmail_provider.py
│   │   ├── microsoft_graph_provider.py
│   │   ├── mock_email_provider.py
│   │   └── ui_state.py
│   │
│   ├── templates/
│   │   ├── audit_logs.html
│   │   ├── dashboard.html
│   │   ├── email_detail.html
│   │   ├── login.html
│   │   └── thread_detail.html
│   │
│   └── static/
│       └── styles.css
```

---

## Folder Explanation

### `main.py`

The FastAPI application entry point.

It starts the backend server, mounts static files, and includes all route modules.

### `app/api/`

Contains all FastAPI route files.

| File | Purpose |
|---|---|
| `page_routes.py` | Handles main dashboard and page rendering |
| `agent_routes.py` | Handles AI Agent prompt requests |
| `email_routes.py` | Handles email actions such as open, review, tag, thread view, and export |
| `audit_routes.py` | Handles audit log page display |
| `mock_provider_routes.py` | Provides the mock email provider API used during development |

### `app/schemas/`

Contains Pydantic schemas.

| File | Purpose |
|---|---|
| `email_schema.py` | Defines the normalized email structure used across all providers |
| `agent_schema.py` | Defines the AI Agent request body, including prompt, mode, and optional date range |

### `app/services/`

Contains the business logic.

| File | Purpose |
|---|---|
| `email_agent.py` | Main AI Agent logic, including unread client filtering and subscription grouping |
| `gemini_service.py` | Handles communication with the Gemini AI model |
| `email_provider.py` | Provider selection layer for mock, Gmail, and Microsoft Graph |
| `gmail_provider.py` | Gmail API provider structure |
| `microsoft_graph_provider.py` | Microsoft Graph / Outlook provider structure |
| `mock_email_provider.py` | Mock email data and mock email actions |
| `audit_service.py` | In-memory audit logging |
| `export_service.py` | CSV export generation |
| `ui_state.py` | Temporary UI state for latest AI Agent result during development |

### `app/templates/`

Contains HTML templates rendered by FastAPI/Jinja2.

### `app/static/`

Contains frontend CSS.

### `docs/`

Contains supporting documentation.

| File | Purpose |
|---|---|
| `email-integration-options.md` | Documents Gmail, Outlook, Nylas, and IMAP integration options |

---

## How the System Works

### Provider-Based Email Flow

```text
User
 ↓
FastAPI Dashboard
 ↓
Email Provider Layer
 ↓
Selected Provider
 ├── Mock Provider
 ├── Gmail Provider
 └── Microsoft Graph Provider
 ↓
Normalized Email Schema
 ↓
Email AI Agent
 ↓
Gemini AI Model / Backend Filtering Logic
 ↓
Structured Results
 ↓
Dashboard / AI Panel / Export
```

The provider layer allows the application to switch between mock data, Gmail, and Outlook/Microsoft Graph using the `EMAIL_PROVIDER` environment variable.

The same AI agent logic works across providers because all provider emails are normalized into the same internal schema.

---

## Normalized Email Schema

All providers are converted into one internal email format.

Important fields include:

| Field | Purpose |
|---|---|
| `provider` | Source provider such as `mock`, `gmail`, or `microsoft_graph` |
| `provider_message_id` | Original provider message ID |
| `provider_thread_id` | Original provider thread/conversation ID |
| `sender` | Sender display name |
| `sender_email` | Sender email address |
| `recipient_email` | Recipient email address |
| `subject` | Email subject |
| `date` | Human-readable email date |
| `received_at` | ISO-style received datetime |
| `body` | Email body or snippet |
| `preview` | Short preview text |
| `is_read` | Mailbox read/unread status from Gmail or Outlook |
| `reviewed` | Internal Email AI Agent review status |
| `tags` | Internal tags applied in the app |
| `is_client_related` | Whether the email is considered client-related |
| `is_subscription_related` | Whether the email is related to a subscription |
| `is_unimportant_or_ad` | Whether the email is an ad, newsletter, promotion, or unimportant |
| `detected_provider` | Subscription provider detected from the email |

The app separates `is_read` from `reviewed`.

- `is_read` comes from the mailbox provider.
- `reviewed` is an internal workflow status in the Email AI Agent.

---

## Setup Instructions

### 1. Clone the Repository

```bash
git clone https://github.com/osamajahmad/Email-AI-Agent.git
cd Email-AI-Agent
```

---

### 2. Create a Virtual Environment

On Windows PowerShell:

```powershell
python -m venv .venv
```

Activate it:

```powershell
.venv\Scripts\activate
```

---

### 3. Install Dependencies

```powershell
pip install -r requirements.txt
```

---

### 4. Create `.env`

Create a `.env` file in the root folder.

Example:

```env
APP_MODE=development

# Provider options:
# mock
# gmail
# microsoft_graph
EMAIL_PROVIDER=mock

SECRET_KEY=dev_secret_key_change_later
AUTHORIZED_EMAIL_DOMAIN=cspsolutions.com

MOCK_PROVIDER_BASE_URL=http://127.0.0.1:8000

GOOGLE_API_KEY=your_google_api_key_here
GEMINI_MODEL=gemini-2.5-flash

# Temporary provider tokens for testing.
# In production, these should be replaced by OAuth connect flows and secure token storage.
GMAIL_ACCESS_TOKEN=
MS_GRAPH_ACCESS_TOKEN=
```

---

### 5. Create `.env.example`

The `.env.example` file should not contain real secrets.

```env
APP_MODE=development

# Provider options:
# mock
# gmail
# microsoft_graph
EMAIL_PROVIDER=mock

SECRET_KEY=your_secret_key_here
AUTHORIZED_EMAIL_DOMAIN=cspsolutions.com

MOCK_PROVIDER_BASE_URL=http://127.0.0.1:8000

GOOGLE_API_KEY=your_google_api_key_here
GEMINI_MODEL=gemini-2.5-flash

GMAIL_ACCESS_TOKEN=
MS_GRAPH_ACCESS_TOKEN=
```

---

### 6. Run the Application

```powershell
uvicorn main:app --reload
```

Open:

```text
http://127.0.0.1:8000
```

---

## Email Provider Modes

### Mock Provider

Used for local development and demo testing.

```env
EMAIL_PROVIDER=mock
```

Expected result:

- Dashboard loads mock emails.
- Agent can test unread client email filtering.
- Agent can test subscription emails grouped by provider.
- No external email credentials are required.

---

### Gmail Provider

Used for Gmail integration structure.

```env
EMAIL_PROVIDER=gmail
GMAIL_ACCESS_TOKEN=
```

Expected result without token:

```text
Gmail — Not connected
Inbox (0)
```

This confirms that the app switched away from mock data and is ready for Gmail connection when credentials are available.

---

### Outlook / Microsoft Graph Provider

Used for Outlook or Microsoft 365 integration structure.

```env
EMAIL_PROVIDER=microsoft_graph
MS_GRAPH_ACCESS_TOKEN=
```

Expected result without token:

```text
Outlook / Microsoft Graph — Not connected
Inbox (0)
```

OAuth connection buttons and secure token storage can be added when testing credentials are provided.

---

## Task 4 Update: Email Integration Requirements

This update addresses the email integration requirements added after the original Task 4 submission.

### 1. Gmail/Outlook Integration Structure

The project now includes provider files for:

- Gmail
- Outlook / Microsoft Graph
- Mock provider

The active provider is controlled by:

```env
EMAIL_PROVIDER=mock
EMAIL_PROVIDER=gmail
EMAIL_PROVIDER=microsoft_graph
```

The dashboard also displays provider connection status, such as:

```text
Mock Provider — Connected
Gmail — Not connected
Outlook / Microsoft Graph — Not connected
```

---

### 2. Dynamic Email Connection Research

The file below documents possible tools and approaches for connecting email accounts dynamically:

```text
docs/email-integration-options.md
```

It compares:

- Direct Gmail API integration
- Direct Outlook / Microsoft Graph integration
- Unified email APIs such as Nylas
- IMAP fallback

---

### 3. Unread Client Email Agent

The agent supports prompts such as:

```text
Get unread client emails and filter out ads and unimportant emails.
```

The backend separates:

- `is_read`: mailbox read/unread state from Gmail or Outlook
- `reviewed`: internal review status inside the Email AI Agent

The agent filters out newsletters, promotions, ads, and unimportant emails before returning unread client-related emails.

---

### 4. Subscription Emails by Provider

The agent supports prompts such as:

```text
Get subscription emails from July 1, 2026 to July 31, 2026 and group them by provider.
```

The result includes:

- AI summary
- Table of subscriptions grouped by provider
- Related email cards for detailed review
- Export option

---

## Important URLs

### Main Dashboard

```text
http://127.0.0.1:8000
```

### FastAPI Docs

```text
http://127.0.0.1:8000/docs
```

### Health Check

```text
http://127.0.0.1:8000/health
```

### Mock Provider Emails

```text
http://127.0.0.1:8000/mock-provider/emails
```

### Audit Logs

```text
http://127.0.0.1:8000/audit-logs
```

---

## API Endpoints

### Dashboard

| Method | Endpoint | Description |
|---|---|---|
| GET | `/` | Shows the main Email AI Agent dashboard |
| GET | `/health` | Health check endpoint |

---

### AI Agent

| Method | Endpoint | Description |
|---|---|---|
| POST | `/api/agent/ask` | Runs the Email AI Agent and returns JSON results |
| POST | `/agent/ask` | Fallback form route |

Example JSON request:

```json
{
  "prompt": "Get subscription emails from July 1, 2026 to July 31, 2026 and group them by provider.",
  "mode": "subscriptions_by_provider",
  "start_date": "2026-07-01",
  "end_date": "2026-07-31"
}
```

Example unread client request:

```json
{
  "prompt": "Get unread client emails and filter out ads and unimportant emails.",
  "mode": "unread_clients"
}
```

---

### Mock Provider API

| Method | Endpoint | Description |
|---|---|---|
| GET | `/mock-provider/emails` | Returns all mock emails |
| GET | `/mock-provider/emails/{email_id}` | Returns one mock email |
| GET | `/mock-provider/threads/{thread_id}` | Returns emails in one thread |
| POST | `/mock-provider/emails/{email_id}/reviewed` | Marks a mock email as reviewed |
| POST | `/mock-provider/emails/{email_id}/tags` | Adds a tag to a mock email |

---

### Email Actions

| Method | Endpoint | Description |
|---|---|---|
| GET | `/emails/{email_id}` | Opens one email detail page |
| GET | `/threads/{thread_id}` | Opens one email thread page |
| POST | `/emails/{email_id}/reviewed` | Marks email as reviewed |
| POST | `/emails/{email_id}/tags` | Adds tag to email |
| POST | `/api/emails/{email_id}/reviewed` | Interactive reviewed API endpoint |
| POST | `/api/emails/{email_id}/tags` | Interactive tag API endpoint |

---

### Export

| Method | Endpoint | Description |
|---|---|---|
| GET | `/export` | Exports all emails as CSV |
| GET | `/export?prompt=...` | Exports AI matched results as CSV |
| GET | `/emails/{email_id}/export` | Exports one email as CSV |

---

### Audit

| Method | Endpoint | Description |
|---|---|---|
| GET | `/audit-logs` | Shows audit log page |

---

## How to Use the Application

### 1. Open the Dashboard

Run the app and open:

```text
http://127.0.0.1:8000
```

You will see:

- Top navigation bar
- Sidebar navigation
- Inbox email list
- AI Agent panel on the right
- Provider connection status
- Dynamic email counts

---

### 2. Browse Emails Manually

Click any email from the inbox list.

The selected email can be opened in its detail page or reviewed from the available actions.

---

### 3. Ask the AI Agent

Use the AI prompt box on the right.

Example prompt:

```text
Filter emails that are subscription based.
```

The AI Agent will:

1. Read the available inbox emails.
2. Analyze the prompt.
3. Classify matching emails.
4. Return structured result cards.
5. Show confidence scores and suggested actions.

---

### 4. Find Unread Client Emails

Use this prompt:

```text
Get unread client emails and filter out ads and unimportant emails.
```

The agent will:

1. Check unread emails.
2. Keep client-related emails.
3. Remove newsletters, ads, promotions, and unimportant messages.
4. Return only important unread client emails.

---

### 5. Find Subscription Emails by Provider

Use this prompt:

```text
Get subscription emails from July 1, 2026 to July 31, 2026 and group them by provider.
```

The agent will return:

1. A summary of what it found.
2. A table grouped by provider.
3. Related subscription email cards.
4. Export option.

---

### 6. Open AI Results

From the AI result cards, click:

- Open
- Thread
- Review
- Tag
- Export

---

### 7. Mark Email as Reviewed

Click:

```text
Review
```

The system updates the email status and creates an audit log entry.

---

### 8. Add Tags

Click:

```text
Tag
```

Then choose or enter a tag such as:

```text
Needs Finance Review
```

The tag is applied and logged.

---

### 9. Export Emails

Click export from:

- Email card
- AI result card
- Export modal
- Direct export endpoint

CSV export will be generated.

---

## Example Prompts

```text
Get unread client emails and filter out ads and unimportant emails.
```

```text
Get subscription emails from July 1, 2026 to July 31, 2026 and group them by provider.
```

```text
Filter emails that are subscription based.
```

```text
Find subscription emails from the last 30 days.
```

```text
Show invoices and renewal emails that may require payment.
```

```text
Find urgent emails that need action today.
```

```text
Export SaaS payment and subscription emails.
```

```text
Only show high confidence matches above 90%.
```

```text
Show domain renewal emails.
```

```text
Find cloud hosting invoices.
```

---

## Mock Email Data

The mock provider currently includes realistic sample emails from:

- Client contacts
- Marketing newsletters
- Promotional emails
- Adobe Billing
- AWS Billing
- GoDaddy Renewals
- Notion Billing
- Zoom Billing

These emails cover categories such as:

- Client Email
- Client Support
- Newsletter
- Promotion
- Subscription
- Invoice
- Domain Renewal
- License Renewal
- Cloud Invoice
- Software Renewal

The mock data is designed to test the two required Task 4 update prompts:

```text
Get unread client emails and filter out ads and unimportant emails.
```

```text
Get subscription emails from July 1, 2026 to July 31, 2026 and group them by provider.
```

---

## AI Output Format

The Gemini model is instructed to return structured JSON.

General AI output includes:

```json
{
  "interpreted_intent": "The user is asking for subscription-related emails.",
  "agent_answer": "I found subscription and renewal related emails.",
  "tools_used": [
    "Prompt Understanding Tool",
    "Email Provider Tool",
    "Email Inspection Tool",
    "AI Classification Tool",
    "AI Summary Tool",
    "Confidence Scoring Tool"
  ],
  "matched_emails": [
    {
      "id": "email_005",
      "category": "Subscription",
      "summary": "Adobe Billing sent an email about an upcoming Creative Cloud renewal.",
      "confidence_score": 95,
      "reason": "The email mentions a subscription renewal and payment amount.",
      "suggested_action": "Review the renewal details and confirm whether this subscription should continue."
    }
  ]
}
```

Task-specific backend results can also include:

```json
{
  "result_type": "subscription_provider_table",
  "agent_answer": "I found 4 subscription-related emails from July 01, 2026 to July 31, 2026, grouped by 4 providers.",
  "provider_summary": [
    {
      "provider": "Adobe",
      "count": 1,
      "latest_email_date": "July 14, 2026",
      "latest_subject": "Your Creative Cloud plan renewal",
      "category": "Subscription"
    }
  ],
  "emails": []
}
```

---

## Current Development Notes

### Provider Strategy

The project uses a provider-based architecture.

Currently supported provider modes:

- `mock`
- `gmail`
- `microsoft_graph`

The mock provider is used for demo and testing.

Gmail and Microsoft Graph provider structures are included, but real mailbox testing requires valid access tokens or OAuth credentials.

The AI Agent does not directly depend on a specific email provider. It receives normalized email data from `email_provider.py`, so provider-specific logic stays isolated.

---

## Gmail Integration Status

The file below contains the Gmail provider structure:

```text
app/services/gmail_provider.py
```

Current Gmail provider support:

- Reads `GMAIL_ACCESS_TOKEN` from environment variables.
- Lists Gmail messages through the Gmail provider structure.
- Normalizes Gmail message metadata into the internal email schema.
- Shows `Gmail — Not connected` when no token is configured.
- Returns `Inbox (0)` instead of falling back to mock data when Gmail is selected without a token.

Expected provider switch:

```env
EMAIL_PROVIDER=gmail
```

Full OAuth login/connect flow is not completed yet.

---

## Microsoft Graph Integration Status

The file below contains the Microsoft Graph provider structure:

```text
app/services/microsoft_graph_provider.py
```

Current Microsoft Graph provider support:

- Reads `MS_GRAPH_ACCESS_TOKEN` from environment variables.
- Lists Outlook/Microsoft 365 messages through the Microsoft Graph provider structure.
- Normalizes Graph message metadata into the internal email schema.
- Shows `Outlook / Microsoft Graph — Not connected` when no token is configured.
- Returns `Inbox (0)` instead of falling back to mock data when Microsoft Graph is selected without a token.

Expected provider switch:

```env
EMAIL_PROVIDER=microsoft_graph
```

Full OAuth login/connect flow is not completed yet.

---

## Dynamic Email Connection Research

The document below explains possible approaches for connecting different email providers dynamically:

```text
docs/email-integration-options.md
```

It compares:

| Option | Description | Best Use |
|---|---|---|
| Direct Gmail API | Official Gmail integration | Google Workspace / Gmail accounts |
| Direct Microsoft Graph | Official Outlook/Microsoft 365 integration | Microsoft 365 / Outlook accounts |
| Nylas | Unified email API for multiple providers | Dynamic multi-provider email connection |
| IMAP fallback | Generic email protocol | Backup option only |

Recommended current approach:

1. Keep mock provider for demo and testing.
2. Add direct Gmail and Outlook/Microsoft Graph provider structures.
3. Normalize all emails into one internal schema.
4. Use Nylas as the strongest researched option for future dynamic multi-provider email connection.
5. Add OAuth and secure token storage when testing credentials are available.

---

## Security Notes

The `.env` file should never be committed to GitHub.

Make sure `.gitignore` includes:

```gitignore
.env
.venv/
__pycache__/
*.pyc
.pytest_cache/
logs/
*.log
```

Only `.env.example` should be committed.

Do not commit:

- real API keys
- Gmail access tokens
- Microsoft Graph access tokens
- virtual environment folders
- cache files
- logs
- exported files containing sensitive email content

---

## Limitations

Current limitations:

- Gmail and Outlook provider structures are implemented, but full OAuth login/connect flow is not completed yet.
- Real Gmail/Outlook testing requires valid access tokens or OAuth credentials.
- Reviewed status and tags are stored internally during development.
- Audit logs are stored in memory, so they reset when the server restarts.
- Email action persistence should later be moved to a database.
- Provider labels/categories are not synced back to Gmail or Outlook yet.
- Enterprise authentication is represented as a frontend/demo concept and is not fully implemented yet.
- Export currently supports CSV only.
- Reports, Settings, and advanced permissions are planned but not fully implemented.

---

## Planned Improvements

Future improvements may include:

- Full OAuth connection flow for Gmail.
- Full OAuth connection flow for Outlook/Microsoft Graph.
- Secure token storage.
- Database persistence for reviewed status, tags, and audit logs.
- Role-based access control.
- Real Reports dashboard.
- Advanced filtering.
- Export to Excel/PDF.
- AI follow-up context memory.
- AI result history.
- Provider label/category sync.
- Production deployment configuration.

---

## Running Checklist

Before submitting or pushing:

```powershell
git status
```

Make sure `.env` and `.venv/` are not included.

Run the app:

```powershell
uvicorn main:app --reload
```

Test the main pages:

```text
http://127.0.0.1:8000
http://127.0.0.1:8000/docs
http://127.0.0.1:8000/mock-provider/emails
http://127.0.0.1:8000/audit-logs
```

Test with mock provider:

```env
EMAIL_PROVIDER=mock
```

Expected:

```text
Inbox contains mock emails.
Mock Provider — Connected.
```

Test with Gmail provider and no token:

```env
EMAIL_PROVIDER=gmail
GMAIL_ACCESS_TOKEN=
```

Expected:

```text
Inbox (0)
Gmail — Not connected
```

Test with Microsoft Graph provider and no token:

```env
EMAIL_PROVIDER=microsoft_graph
MS_GRAPH_ACCESS_TOKEN=
```

Expected:

```text
Inbox (0)
Outlook / Microsoft Graph — Not connected
```

Test required prompts:

```text
Get unread client emails and filter out ads and unimportant emails.
```

```text
Get subscription emails from July 1, 2026 to July 31, 2026 and group them by provider.
```

---

## Git Commands Used

Initialize Git:

```powershell
git init
```

Add files:

```powershell
git add .
```

Commit:

```powershell
git commit -m "Update Email AI Agent with provider architecture and Task 4 integration requirements"
```

Connect remote repository:

```powershell
git remote add origin https://github.com/osamajahmad/Email-AI-Agent.git
```

Rename branch to main:

```powershell
git branch -M main
```

Push:

```powershell
git push -u origin main
```

If the GitHub repo only contains an empty README and you want to replace it:

```powershell
git push -u origin main --force
```

---

## Author

Osama Ahmad

CSP Solutions — Email AI Agent Task