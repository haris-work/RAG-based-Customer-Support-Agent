# Project Roadmap and Status

**Status:** The user reported implementation complete through **Phase 5, Step 5.20** (November 2026). This documentation is based on the build walkthrough, not a direct checkout or code audit.

## Implemented or covered by Step 5.20

### Core capabilities

- Fictional NovaTech Markdown knowledge base, section-aware chunking, ChromaDB retrieval and RAG.
- LangGraph request routing, grounded answers, safe fallback and human-review workflow.
- FastAPI customer and administrator web interfaces.
- SQLite support tickets, status management and n8n/Gmail escalation notifications.

### Operational improvements through the Step 5.20 milestone

- Notification-history and conservative retry logic, n8n send acknowledgment.
- Customer conversation persistence in SQLite and customer-session ownership.
- Escalation ticket deduplication, audit history and administrator activity timeline.
- Support analytics, date range filters and CSV export.
- Agent evaluation dataset, automated scoring and regression baseline comparison.

All completion statements are from the iterative walkthrough. Run the actual code and tests to establish a verified release state.

## Later steps: NOT assumed completed

| Step | Planned work |
| --- | --- |
| 5.21 | GitHub Actions offline CI |
| 5.22 | API/database integration CI |
| 5.23 | Transactional notification outbox |
| 5.24 | Notification monitoring and manual recovery UI |
| 5.25 | SQLite chat rate limiting |
| 5.26 | Security headers and error handling |
| 5.27 | CSRF/Origin and Trusted Host protections |
| 5.28 | Environment validation |
| 5.29 | Health and readiness probes |
| 5.30 | Structured logging and request tracing |
| 5.31 | Backups and restoration |
| 5.32 | Final security/reliability gate |
| 5.33 | Docker packaging |
| 5.34 | Deployment preparation |
| 5.35 | End-to-end acceptance tests |
| 5.36 | Documentation review |
| 5.37 | GitHub/portfolio publication |

## Release requirements

Before claiming the project complete, verify current repository paths and APIs, use fictional test data, run the actual tests, record real evaluation metrics and verify each announced production/deployment feature. Publication should clearly label the project a demonstration, not a service handling real NovaTech customers.
