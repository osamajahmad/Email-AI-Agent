# Email Integration Options for Email AI Agent

## Purpose

This document explains the possible ways to connect the Email AI Agent to real email accounts such as Gmail and Outlook, and also identifies tools that can connect multiple email providers dynamically.

The goal is to support the Task 4 update:

- Integrate the Email AI Agent with Gmail/Outlook so it can be tested.
- Check if there are tools we can use to connect any email dynamically.
- Allow the agent to get unread client emails while filtering ads and unimportant emails.
- Allow the agent to find subscription emails in a specific time period and output a table grouped by provider.

---

## Option 1: Direct Gmail API Integration

### Description

Use the official Gmail API to connect Google Workspace or Gmail accounts directly.

### How it works

The user connects their Gmail account through OAuth. The backend receives an access token and refresh token, then uses Gmail API endpoints to read messages, threads, labels, and unread status.

### Advantages

- Official Google API
- Good support for Gmail search queries
- Can filter unread emails using Gmail search
- Supports threads and labels
- Good for Google Workspace accounts

### Limitations

- Requires Google Cloud project setup
- Requires OAuth configuration
- Gmail-specific logic is needed
- Different from Outlook/Microsoft Graph structure

### Best use

Best when CSP wants direct control over Gmail integration.

---

## Option 2: Direct Outlook / Microsoft Graph Integration

### Description

Use Microsoft Graph API to connect Microsoft 365 / Outlook mailboxes.

### How it works

The user connects their Microsoft account through OAuth. The backend uses Microsoft Graph endpoints to read messages, conversation IDs, unread status, senders, recipients, and message previews.

### Advantages

- Official Microsoft API
- Best option for Microsoft 365 / Outlook accounts
- Supports user mailbox access
- Supports read/unread state
- Supports conversation/thread structure through conversation IDs

### Limitations

- Requires Azure App Registration
- Requires Microsoft Graph permissions
- Outlook data format differs from Gmail
- Requires separate normalization logic

### Best use

Best when CSP mainly uses Microsoft 365 or wants enterprise Outlook integration.

---

## Option 3: Unified Email API Provider such as Nylas

### Description

Nylas provides a unified email API that can connect to Gmail, Outlook, Microsoft Exchange, and IMAP-based accounts using one normalized API.

### Advantages

- One API for multiple email providers
- Reduces provider-specific backend logic
- Handles OAuth flows for different providers
- Useful for dynamic email account connection
- Can speed up development for multi-provider support

### Limitations

- Third-party dependency
- Usually paid for production usage
- Less direct control than using Gmail API or Microsoft Graph directly
- Data privacy and compliance need to be reviewed before production use

### Best use

Best if CSP wants to allow many different client email providers dynamically without building every provider integration manually.

---

## Option 4: IMAP Fallback

### Description

Use IMAP to connect to generic mailboxes that do not support Gmail API or Microsoft Graph.

### Advantages

- Works with many traditional email providers
- Can be useful as a backup option
- Does not depend on Gmail or Microsoft only

### Limitations

- Weaker modern API support
- Harder to manage labels, threads, and metadata
- OAuth support varies by provider
- Less suitable for rich enterprise workflows
- More difficult to normalize accurately

### Best use

Backup option only, not recommended as the primary integration method.

---

## Recommended Approach

For this Task 4 update, the recommended approach is:

1. Keep the current mock provider for demo and testing.
2. Add direct provider support for Gmail and Outlook/Microsoft Graph.
3. Normalize all provider emails into one internal email schema.
4. Keep internal app fields separate from provider fields:
   - `is_read` comes from Gmail/Outlook.
   - `reviewed` is internal to the Email AI Agent.
   - `tags` are internal unless provider label sync is added later.
5. Document Nylas as the strongest option for dynamic multi-provider email connection.

---

## Current Implementation Status

The project currently supports:

- Mock provider for demo data.
- Gmail provider structure.
- Microsoft Graph provider structure.
- Provider switching through `EMAIL_PROVIDER`.
- Provider connection status display.
- Normalized email schema.
- Unread client email filtering.
- Subscription email detection by date range.
- Subscription table grouped by provider.

OAuth connection buttons and secure token storage can be added in the next phase if testing credentials are provided.