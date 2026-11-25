# Local Configuration and Secrets

**Scope:** development through Phase 5, Step 5.20. Central startup configuration validation is planned later (Step 5.28).

## Prerequisites

- Windows + PowerShell (the primary development environment), Python with a working virtual environment.
- Local ChromaDB knowledge index and embedding dependencies.
- Valid Groq account/API key for live model inference.
- Optional local Docker/n8n plus Gmail credentials for escalation workflow tests.

## Private `.env`

Create a private `.env` file at the repository root. Use the variable names consumed by your code:

```dotenv
GROQ_API_KEY=YOUR_PRIVATE_GROQ_KEY
ADMIN_API_KEY=GENERATE_A_LONG_RANDOM_SECRET
N8N_WEBHOOK_SECRET=GENERATE_AN_INDEPENDENT_RANDOM_SECRET
N8N_SUPPORT_WEBHOOK_URL=http://localhost:5678/webhook/novatech-support-ticket
```

Do not commit this file. Generate strong secrets with:

```powershell
python -c "import secrets; print(secrets.token_urlsafe(48))"
```

Optional local cookie and application settings depend on your exact code. Full validation of hosts, production mode and HTTPS will be addressed in the later configuration step.

## Run locally

```powershell
python -m pip install -r requirements.txt
python -m uvicorn main:app --reload
```

The knowledge-base index must be built according to the repository's actual ingestion scripts before expecting successful RAG answers.

## n8n webhook

The webhook uses a shared secret in the `X-NovaTech-Webhook-Key` header. Configure the matching n8n Webhook **Header Auth** credential. Keep the workflow's actual production webhook URL, not its testing-only URL, in the environment variable when running the activated workflow.

A webhook HTTP 200 response alone is insufficient to claim that Gmail sent a message; the Python client expects a matching ticket ID and explicit delivery confirmation.

## Security settings

- Local development may run at `http://127.0.0.1:8000`.
- An HTTPS deployment will require secure cookies, validated trusted hosts, HSTS and reverse-proxy configuration; those are not yet completed at Step 5.20.
- Keep administrator and webhook secrets independent and private.

## Production warning

Changing `APP_ENV` is not a production deployment. Real-customer deployment also requires staff identity/authorization, backup/restore capability, privacy retention controls, HTTPS, integration tests, observability, incident response and infrastructure monitoring. These are not claimed complete in the Step 5.20 project state.
