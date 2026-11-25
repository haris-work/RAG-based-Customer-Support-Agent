# Human Escalation and Routing Policy

## Purpose and non-negotiable rule

Escalate whenever the request requires discretion, identity/payment investigation, a system action the AI cannot execute, a safety decision, or information not supported by approved knowledge. The AI must not delay a required handoff by repeatedly asking the customer to troubleshoot.

## Priority and routing matrix

| Case category | Priority | Routing team | Required information (minimum necessary) | AI action before handoff |
|---|---|---|---|---|
| Battery/electrical safety: smoke, swelling, sparks, burning odor, shock, abnormal heat | P1 Critical | Product Safety / Product Support | Product SKU/model, symptom, whether power was disconnected safely, order reference if readily available | Tell customer to stop use; no further tests; urgent handoff |
| Suspected account takeover or compromised credentials | P1 Critical | Trust & Safety | Verified account reference if possible, suspicious event description, safe contact channel | Do not request secrets; advise official password reset/email security; secure escalation |
| Exposed payment credentials or suspected payment fraud | P1 Critical | Trust & Safety + Finance | Order/payment reference from secure lookup, date/amount description, incident summary | Do not repeat sensitive data; tell customer not to send card details; urgent handoff |
| Missing/stolen or delivered-but-not-received parcel | P2 High | Logistics | Order number, verified delivery destination, carrier status/time, checks already completed | Do not label theft or promise refund/replacement; open investigation |
| Shipment >2 business days beyond transit estimate | P2 High | Logistics | Order reference, service level, carrier scan and last movement date | Compare against correct estimate; open delayed-shipment case |
| Duplicate charge, failed refund, unexpected charge, payment mismatch | P2 High | Finance | Verified order reference, approximate amount/date, provider transaction reference if tool returns it | Never request full card/CVV; do not promise payment outcome |
| Refund exception, partial refund dispute, fee waiver or out-of-window request | P2 High | Returns / Finance | Order, delivery date, return status, reason, customer's requested remedy | Explain standard policy; state exception requires review |
| Warranty dispute, denial challenge, repeated defect or remedy request | P2 High | Warranty / Product Support | SKU, verified purchase evidence, delivery date, symptom, troubleshooting history | Explain published term; do not adjudicate or promise remedy |
| Angry or dissatisfied customer requesting supervisor | P2 High | Customer Experience supervisor | Case/order reference, concise issue summary, prior contacts and requested outcome | Acknowledge, remain neutral, honor human request; do not argue |
| Unresolved technical problem after documented steps | P3 Normal, raise to P2 if business-critical | Product Support | SKU, host model/OS, symptoms, steps, error text, safety symptoms | Stop repeating failed steps; create case |
| Customer explicitly asks for human | P3 Normal (or higher by issue) | Customer Experience | Contact reason, order reference if relevant, preferred safe channel | Honor request; do not force bot-only path |
| Unsupported question, conflicting policy evidence, unclear eligibility | P3 Normal | Relevant policy owner / Customer Experience | Exact question, relevant retrieved source references, known context | Admit uncertainty; do not guess; route for authoritative answer |
| Privacy/data access/deletion/correction request | P2 High | Privacy owner | Request type, verified account reference, minimum contact details | Do not promise deletion; initiate secure privacy workflow |
| Marketplace order issue | P2 or P3 based on impact | Marketplace Support / Customer Experience | Marketplace name, marketplace order reference, issue summary | Direct customer to marketplace workflow; handoff if unable to resolve |

## Escalation trigger details

### Refund exceptions
Escalate requests outside the 30-calendar-day return window, requests to waive the $7.95 buyer-remorse label fee, requests for outbound shipping reimbursement, partial-refund disputes, or requests to refund to a different payment method. The AI may explain the standard policy but cannot approve the exception.

### Angry or dissatisfied customers
Escalate when the customer asks for a manager/human, says prior support failed, expresses repeated dissatisfaction, or the conversation is becoming adversarial. A single frustrated sentence does not justify arguing or ending the conversation. Acknowledge and offer a human handoff.

### Missing or stolen packages
For “delivered but not received,” guide the customer through the checks in `07_order_tracking.md`, then route to Logistics. If the customer reports suspected theft or safety concerns, do not make a factual finding; escalate. Replacement/refund decisions require investigation.

### Warranty disputes
Escalate disputed exclusions, failed remedies, repeat failures, products outside the listed SKU set, and safety symptoms. Do not say a claim is definitely covered or rejected solely from a short chat description.

### Payment and fraud
Any suspected fraud, chargeback, unexpected/duplicate charge, failed refund, payment mismatch, or account/payment credential exposure goes to Finance or Trust & Safety. Never collect card secrets or authentication codes.

### Unresolved technical problems
Escalate when the listed steps have been exhausted, the issue occurs on multiple compatible devices, symptoms imply hardware failure, or the user is uncomfortable continuing. Safety incidents are P1 and stop routine diagnostics immediately.

### Unsupported or conflicting knowledge
When the RAG system retrieves no adequate evidence, two documents conflict, or the requested fact is not specified, the agent must state that it cannot confirm the answer and route to the document owner or Customer Experience. It must not fill the gap with plausible-sounding information.

## Required handoff payload

A handoff payload should contain only:
- Case category and priority.
- Customer's concise issue statement (or accurate summary).
- Product SKU/order reference only after authorized verification, where relevant.
- Relevant dates, status and tool-returned references.
- Troubleshooting steps and observed results.
- Safety/security indicators.
- Relevant knowledge-base document names/sections.
- Requested next step or remedy.

Do not include passwords, full card data, CVV, OTPs, recovery codes or unnecessary personal information.

## Handoff interaction

Tell the customer what team is being contacted and what information is being passed. Do not claim a ticket was created or a human was notified until the integration confirms success. If the ticketing/transfer system fails or is unavailable, say so plainly and provide the fictional support email `support@novatech.example` as a placeholder channel for this simulation. Do not invent a ticket number or human response deadline.
