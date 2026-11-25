# Testing Guide and Quality Gates

**Current stage:** Phase 5, Step 5.20. Automated GitHub Actions setup is **planned for Step 5.21**, not documented as complete.

## Test strategy

1. **Offline unit tests:** pure Python logic and SQLite behaviors with temporary databases.
2. **API integration tests:** FastAPI `TestClient` with mocked LLM/webhook side effects and isolated storage.
3. **AI evaluation:** real KB retrieval and Groq inference, fake side effects.
4. **Manual end-to-end tests:** local customer UI, admin UI, n8n workflow and fictional Gmail test mailbox.

## Run representative offline tests

The following test names were created in the implementation walkthrough. Confirm their names/files in your repository before running the entire set.

```powershell
python -m tests.testCustomerSessionCore
python -m tests.testCustomerSessions
python -m tests.testTicketDeduplication
python -m tests.testEvaluationRegression
```

Some tests import `main.py` and initialize LangGraph/ChromaDB; others may need live service availability or mocked dependencies. Do not assume every test is fully isolated unless verified.

## AI evaluation

```powershell
python -m scripts.runAgentEvaluation
python -m scripts.checkEvaluationRegression --check
```

Do not automatically run the live Groq evaluation on every source-code change without controlling cost and result variability.

## Integration/manual scenarios

| Scenario | Expected behavior |
| --- | --- |
| FAQ policy question | RAG answer with support or safe uncertainty |
| Order tracking without order integration | Escalation; no invented shipment status |
| Human support request | One active ticket and a notification attempt |
| Repeat request | Reuses appropriate unresolved ticket |
| New customer cookie | Independent conversation namespace |
| Cross-session conversation ID | Rejected |
| Excessive requests | Rate limiting planned for Step 5.25 |
| Admin without API key | 401 |
| Invalid ticket status transition | Rejected and not audited as successful |
| Ambiguous webhook delivery | `unconfirmed`; no unsafe automatic resend |
| Analytics CSV | Includes requested dates, excludes raw chat message |

## GitHub publication gate

Before committing: check `git status`, `git ls-files .env`, `git ls-files '*.db'`, saved screenshots and evaluated report outputs. Avoid committing secrets, SQLite databases, raw chat logs or private evaluation artifacts.

## Remaining testing work

CI, full compatibility checks, a consistent backup/restore drill, deployment acceptance tests and final independent security review are outside the verified Step 5.20 scope.
