# NovaTech Store — Company Overview

> **Training simulation:** NovaTech Store is a fictional company created solely for software engineering and RAG evaluation. It is not a claim about an actual registered business. All contact details use the reserved `.example` domain; no real street address or telephone number is provided.

## Company profile

**Name:** NovaTech Store  
**Business type:** US-focused e-commerce retailer  
**Industry:** Consumer electronics, technology accessories and smart-home products  
**Primary market:** United States  
**Sales channels:** novatech.example (fictional official storefront) and selected third-party marketplaces  
**Business maturity:** Established small-to-medium-sized retailer in this scenario.

NovaTech Store began in 2017 as a specialist online seller of computer accessories. It expanded into charging products, audio, video-conferencing equipment, networking and entry-level smart-home devices. The company differentiates itself through clear compatibility guidance, accessible product documentation and practical post-purchase support rather than an unusually broad catalog.

## Mission and service principles

The mission is to make useful technology easier to choose, set up and keep working. The operating principles are: explain compatibility before purchase; publish supportable specifications; provide consistent policies; protect customer information; and transfer cases to trained staff when a decision requires account access, discretion or investigation.

## Product focus

The catalog is organized into computer accessories, power and charging, cables, audio, cameras and streaming, smart home, networking and storage. The current fictional catalog contains 16 active reference products. Prices, inventory and promotional eligibility can change; the catalog in this knowledge base is a static training snapshot, not a live feed.

## US operations

NovaTech is modeled as a US-based e-commerce operation serving the 50 states and Washington, DC. Customer orders are handled through an outsourced parcel-carrier network and a domestic fulfillment operation. The knowledge base intentionally does not publish a real warehouse or corporate street address. Returns instructions and labels are issued through the order-management workflow after eligibility is reviewed.

## Departments and responsibilities

| Department | Responsibilities | AI agent boundary |
|---|---|---|
| Customer Experience | Chat, email, marketplace support, case ownership | May answer static policy questions; cannot impersonate a human or promise exceptions |
| Order Operations | Order review, address corrections, fulfillment holds, cancellations | Requires authenticated order-system lookup for individual orders |
| Fulfillment & Logistics | Picking, packing, carrier handoff, delivery investigations | Live scans and package investigations require connected systems or staff |
| Returns & Refunds | Return authorization, inspection, refund approvals | Eligibility guidance is allowed; approval and payment execution require system action |
| Product & Technical Support | Specifications, compatibility, troubleshooting, warranty triage | May provide documented steps; unresolved or safety-related faults escalate |
| Finance | Payment reconciliation, tax and invoice issues | No card details in chat; account-specific payment investigation is human/system-led |
| Trust & Safety | Fraud, account compromise, privacy incidents | Immediate restricted escalation; do not investigate by collecting secrets |

## Customer service channels

- **Website live chat:** Primary channel during staffed support hours.
- **Email/contact form:** `support@novatech.example` (fictional placeholder).
- **Marketplace messaging:** Used for orders placed on participating marketplaces; those platforms' workflows and policies may supersede the direct-store process.
- **Self-service account area:** The fictional storefront provides order history, shipment links and return-request entry points after sign-in.

No real telephone number, physical address or public social profile is defined for this simulation. Do not invent one in customer responses.

## Operating hours

**Support hours:** Monday–Friday, 8:00 a.m.–8:00 p.m. Eastern Time; Saturday, 9:00 a.m.–5:00 p.m. Eastern Time; Sunday closed. Hours adjust with daylight saving time. Company-observed holidays may have reduced hours or closures.

**Response targets:** Live chat typically responds within 2 minutes while staffed; email/contact forms and marketplace messages within 1 business day. These are targets, not guarantees.

**Order processing:** In-stock orders are generally processed within 1–2 business days after payment authorization and fraud screening, excluding weekends and company-observed holidays.

## Static and dynamic business information

**Static knowledge suitable for RAG:** company background, catalog reference specifications, compatibility notes, published shipping rules, return rules, warranty terms, support standards and troubleshooting steps.

**Dynamic data requiring tools:** stock quantity, real-time prices, order records, shipping scans, refund/payment state, identity verification, account profile and active coupons. If a connected integration is unavailable, explain the limitation and offer a support case; never manufacture a value.

## Related documents

See `02_customer_support.md` for service workflows, `03_product_catalog.md` and `04_product_specifications.md` for product data, `06_shipping_policy.md` through `09_refunds.md` for order policies, and `16_human_escalation_policy.md` for handoff rules.
