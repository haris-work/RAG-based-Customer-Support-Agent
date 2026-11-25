# Operations Runbook

**Applies to:** reported project functionality through Step 5.20. Commands and exact function exports should be checked against the current repository.

## Start services

1. Activate the project virtual environment.
2. Ensure `.env` is configured and private.
3. Start n8n and activate the escalation workflow when testing notifications.
4. Start API: `python -m uvicorn main:app --reload`.
5. Open customer UI at `/`, admin UI at `/admin`, and API documentation at `/docs`.

## Human escalation flow

1. Customer requests human assistance or an issue requiring account/order action.
2. LangGraph routes to human review.
3. `FindOrCreateSupportTicket` creates a ticket or reuses an appropriate unresolved duplicate.
4. The ticket service attempts the authenticated n8n webhook and records the outcome.
5. The retry service cautiously retries only clearly safe failures.
6. Ambiguous outcomes must be checked manually; transactional outbox and a monitoring UI are future steps.

## Ticket status operations

Typical lifecycle: `pending` → `in_progress` → `resolved`. The service may permit resolved tickets to be reopened as `in_progress`. Status changes are written to audit history.

Use `GET /api/tickets/{ticket_id}/history` to investigate a record's lifecycle. The audit actor `admin_api_key` identifies a credential, not an individual administrator.

## Notification history

Use the existing ticket notification history service and n8n execution history to investigate delivery. Dedicated admin notification monitoring routes are planned for Step 5.24.

- **`sent`:** n8n reported successful send operation; not proof of recipient inbox delivery.
- **`unconfirmed`:** no matching acknowledgment; do not automatically resend.
- **`failed` / `not_configured`:** examine the actual error; only certain cases are safe to retry.

## Manual recovery

For ambiguous outcomes, inspect the n8n execution and Gmail send information. The dedicated `confirm_sent` / `approve_retry` administration workflow is planned for Step 5.24. **Do not automatically retry ambiguous events.**

There is no completed Step 5.24 review UI at this cutoff; document investigation and decisions manually.

## Scheduled recovery

The local development worker was implemented using Windows Task Scheduler and the script:

```powershell
python -m scripts.scheduledRecovery
```

The intended schedule was every 15 minutes. Ensure the task is configured on the current machine and the local n8n service is reachable. The schedule is not guaranteed to run when the laptop is off.

A transactional outbox replacement for the retry worker is planned in Step 5.23.

## Analytics and exports

Use `/api/analytics/report` for inclusive UTC creation-date filters, and `/api/analytics/export` for CSV downloads. The sample data is fictional and development-generated. Avoid portraying test metrics as live customer performance.

## Troubleshooting

| Symptom | First checks |
| --- | --- |
| Chat 401 | Session cookie expiry or missing ownership token |
| Chat 403 | Conversation owned by another session |
| Admin 401 | Missing/incorrect `X-Admin-Key` |
| Webhook rejected | n8n Header Auth name and secret mismatch |
| No Gmail | Check notification-attempt history and n8n execution |
| RAG empty | Check Chroma collection, embeddings and KB indexing |
| Analytics unexpected | Historical test tickets and incomplete pre-audit history |

## Backup caveat

At Step 5.20, a fully tested cross-database backup/restore process is **not yet implemented**. Do not treat copies of live SQLite `.db` files as verified backups. Before handling real customer data, implement and test consistent backup/restore and retention procedures.
