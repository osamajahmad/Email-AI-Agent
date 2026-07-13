# CSP Email AI Agent

An internal AI-powered email dashboard for **CSP Solutions**.

The purpose of this project is to allow CSP users to review, filter, classify, and act on company emails using natural language prompts through an AI assistant interface.

Users can ask prompts such as:

```text
Filter emails that are subscription based.
```

The Email AI Agent analyzes available emails, detects subscription/renewal/invoice/license/SaaS/cloud/domain/software-related emails, summarizes the results, assigns categories and confidence scores, and allows users to open, review, tag, and export the results.

---

## Project Overview

This project is built as a **FastAPI-based internal web application**.

Since Microsoft Graph mailbox access is not currently available, the project uses a **mock email provider API** during development. This allows the full AI workflow, dashboard, audit logging, tagging, reviewing, and exporting features to be built and tested now.

Later, when Microsoft Graph access is provided, only the email provider integration layer needs to be replaced.

---

## Main Features

### Email Dashboard

- View company emails in an inbox-style dashboard.
- Browse emails manually.
- Select emails from the inbox list.
- View full email content in the preview pane.
- Filter emails by category.
- Search emails by sender, subject, category, or preview text.
- Sort emails by newest, confidence score, or sender.

### AI Agent

- Ask natural language prompts.
- AI reads the available inbox data.
- AI detects matching emails based on meaning, not only keywords.
- AI returns structured results with:
  - Sender
  - Subject
  - Date
  - Summary
  - Category
  - Confidence score
  - Suggested action
- AI results appear inside the right-side assistant panel.
- The inbox and email preview stay visible while the AI works.

### Email Actions

Users can perform actions from the email preview or AI result cards:

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
| Email Provider Now | Mock Provider API |
| Email Provider Later | Microsoft Graph API |

---

## Project Structure

```text
Task 4/
│
├── main.py
├── requirements.txt
├── README.md
├── .env
├── .env.example
├── .gitignore
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
│   ├── services/
│   │   ├── __init__.py
│   │   ├── audit_service.py
│   │   ├── email_agent.py
│   │   ├── email_provider.py
│   │   ├── export_service.py
│   │   ├── gemini_service.py
│   │   ├── microsoft_graph_provider.py
│   │   ├── mock_email_provider.py
│   │   └── ui_state.py
│   │
│   ├── schemas/
│   │   └── __init__.py
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

- `page_routes.py`  
  Handles main dashboard page rendering.

- `agent_routes.py`  
  Handles AI Agent prompt requests.

- `email_routes.py`  
  Handles email actions such as open, review, tag, thread view, and export.

- `audit_routes.py`  
  Handles audit log page display.

- `mock_provider_routes.py`  
  Provides the mock email provider API used during development.

### `app/services/`

Contains the business logic.

- `email_agent.py`  
  Main AI Agent logic. Builds the AI prompt, sends emails to Gemini, and merges AI results with original email data.

- `gemini_service.py`  
  Handles communication with the Gemini AI model.

- `email_provider.py`  
  Provider selection layer. Decides whether to use the mock provider now or Microsoft Graph later.

- `mock_email_provider.py`  
  Contains mock email data and mock email actions.

- `microsoft_graph_provider.py`  
  Placeholder for future Microsoft Graph integration.

- `audit_service.py`  
  Handles in-memory audit logging.

- `export_service.py`  
  Builds CSV exports.

- `ui_state.py`  
  Stores temporary UI state for the latest AI Agent result during development.

### `app/templates/`

Contains HTML templates rendered by FastAPI/Jinja2.

### `app/static/`

Contains frontend CSS.

---

## How the System Works

### Current Development Flow

```text
User
 ↓
FastAPI Dashboard
 ↓
Email Provider Layer
 ↓
Mock Email Provider API
 ↓
Email AI Agent
 ↓
Gemini AI Model
 ↓
Structured AI Results
 ↓
Dashboard / AI Panel
```

### Future Production Flow

```text
User
 ↓
FastAPI Dashboard
 ↓
Email Provider Layer
 ↓
Microsoft Graph API
 ↓
Real Microsoft 365 Emails
 ↓
Email AI Agent
 ↓
Gemini AI Model
 ↓
Structured AI Results
 ↓
Dashboard / AI Panel
```

The important point is that the AI Agent does not directly depend on local email files. It calls the provider layer. During development, that provider uses the mock API. Later, the same provider layer can be connected to Microsoft Graph.

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
EMAIL_PROVIDER=mock

SECRET_KEY=dev_secret_key_change_later
AUTHORIZED_EMAIL_DOMAIN=cspsolutions.com

MOCK_PROVIDER_BASE_URL=http://127.0.0.1:8000

GOOGLE_API_KEY=your_google_api_key_here
GEMINI_MODEL=gemini-2.5-flash
```

---

### 5. Create `.env.example`

The `.env.example` file should not contain real secrets.

```env
APP_MODE=development
EMAIL_PROVIDER=mock

SECRET_KEY=your_secret_key_here
AUTHORIZED_EMAIL_DOMAIN=cspsolutions.com

MOCK_PROVIDER_BASE_URL=http://127.0.0.1:8000

GOOGLE_API_KEY=your_google_api_key_here
GEMINI_MODEL=gemini-2.5-flash
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
  "prompt": "Filter emails that are subscription based."
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
- Selected email preview
- AI Agent panel on the right

---

### 2. Browse Emails Manually

Click any email from the inbox list.

The selected email will open in the preview pane without leaving the dashboard.

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

### 4. Open AI Results

From the AI result cards, click:

- Open
- Thread
- Review
- Tag
- Export

The main email preview remains visible and the AI panel stays open.

---

### 5. Mark Email as Reviewed

Click:

```text
Mark as Reviewed
```

The system updates the email status and creates an audit log entry.

---

### 6. Add Tags

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

### 7. Export Emails

Click export from:

- Email preview
- AI result card
- Export modal
- Direct export endpoint

CSV export will be generated.

---

## Example Prompts

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

- Adobe Billing
- AWS
- GoDaddy
- Notion
- Zoom
- Microsoft Azure
- Atlassian
- DigitalOcean

These emails cover categories such as:

- Subscription
- Invoice
- Domain
- License
- Cloud
- Software Renewal

---

## AI Output Format

The Gemini model is instructed to return structured JSON.

Expected AI output includes:

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
      "id": "email_004",
      "category": "Subscription",
      "summary": "Notion sent a receipt for a renewed workspace subscription.",
      "confidence_score": 94,
      "reason": "The email mentions workspace subscription renewal and payment receipt.",
      "suggested_action": "Review the receipt and confirm billing details."
    }
  ]
}
```

---

## Current Development Notes

### Mock Provider Strategy

The project currently uses a mock provider because Microsoft Graph access is not available yet.

This is intentional.

The app is already built around a provider layer:

```text
email_provider.py
```

When Microsoft Graph access becomes available, the mock provider can be replaced with a real provider implementation without changing the main AI Agent logic or UI workflow.

---

## Future Microsoft Graph Integration

The file:

```text
app/services/microsoft_graph_provider.py
```

is prepared as a placeholder for the future Microsoft Graph integration.

Later, this service should:

1. Authenticate with Microsoft.
2. Read emails from Microsoft 365 mailboxes.
3. Normalize Microsoft Graph email data into the same structure used by the app.
4. Support real mailbox actions where permitted:
   - Read emails
   - View threads
   - Mark as reviewed
   - Add tags/categories
   - Export data

Expected future provider switch:

```env
EMAIL_PROVIDER=microsoft_graph
```

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

---

## Limitations

Current limitations:

- Emails are from the mock provider, not a real mailbox.
- Audit logs are stored in memory, so they reset when the server restarts.
- Email review/tag state is stored in memory during development.
- Microsoft Graph integration is not completed yet.
- Enterprise authentication is represented as a frontend/demo concept and is not fully implemented yet.
- Export currently supports CSV only.
- Some pages such as Reports, Settings, and advanced permissions are planned but not fully implemented.

---

## Planned Improvements

Future improvements may include:

- Microsoft Graph mailbox integration
- Microsoft enterprise authentication
- Persistent database for audit logs and email action history
- Role-based access control
- Real Reports dashboard
- Advanced filtering
- Export to Excel/PDF
- AI follow-up context memory
- AI result history
- Better production deployment configuration

---

## Running Checklist

Before submitting or pushing:

```powershell
git status
```

Make sure `.env` and `.venv/` are not included.

Then run:

```powershell
uvicorn main:app --reload
```

Test:

```text
http://127.0.0.1:8000
http://127.0.0.1:8000/docs
http://127.0.0.1:8000/mock-provider/emails
http://127.0.0.1:8000/audit-logs
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
git commit -m "Initial commit - Email AI Agent FastAPI app"
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