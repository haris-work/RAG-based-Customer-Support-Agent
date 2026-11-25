# Returns and Exchanges Policy

## Policy baseline and terminology

The following operating rules are the authoritative fictional baseline for this training environment. If another file summarizes a rule, this baseline governs interpretation.

- **Market:** United States only: the 50 states and Washington, DC. The company does not currently ship to US territories, APO/FPO/DPO addresses, freight forwarders, or international destinations.
- **Support hours:** Monday–Friday, 8:00 a.m.–8:00 p.m. Eastern Time; Saturday, 9:00 a.m.–5:00 p.m. Eastern Time; Sunday closed. Company-observed holidays may have reduced hours or closures. Hours are stated in ET and adjust with daylight saving time.
- **Standard support targets:** Live chat typically responds within 2 minutes while staffed; email and website contact forms within 1 business day; marketplace messages within 1 business day. These are targets, not guarantees.
- **Order processing:** In-stock orders are generally picked and packed within 1–2 business days, Monday–Friday, excluding company-observed holidays. The processing clock begins after payment authorization and fraud screening. A cutoff time of 1:00 p.m. ET is used for operational planning, not as a guaranteed same-day dispatch promise.
- **Shipping:** Contiguous US standard shipping is $6.95 and estimated at 5–7 business days after carrier acceptance. Standard shipping is free on merchandise subtotals of at least $75 after discounts and before tax for destinations in the contiguous 48 states. Contiguous US expedited shipping is $14.95 and estimated at 2–3 business days after carrier acceptance. Alaska and Hawaii standard shipping is $14.95 and estimated at 7–10 business days after carrier acceptance; free-shipping threshold and expedited service do not apply there. Estimates exclude processing time and are not guarantees.
- **Returns:** Most unused products in original condition and packaging may be returned within 30 calendar days after delivery. Products must include included accessories and proof of purchase. Opened products may be accepted if complete and undamaged, but hygiene-sensitive items, consumables, gift cards, final-sale items, and products damaged through misuse are excluded unless defective or required by applicable law. Marketplace purchases must be returned through the marketplace where purchased.
- **Return shipping:** For a confirmed defect, wrong item, or company fulfillment error reported within 10 calendar days after delivery, NovaTech provides a prepaid label. For a buyer-remorse return, the customer pays return shipping; a $7.95 label fee may be deducted from the refund if the customer elects to use a NovaTech label. No label fee applies where the company is responsible.
- **Refund timing:** Returns are normally inspected within 3–5 business days after arrival at the returns facility. Approved refunds are submitted to the original payment method within 5–10 business days after approval. Banks and card issuers may take additional time. Refunds cannot be sent to a different card or unrelated account.
- **Warranty:** Manufacturer-style limited warranty is product-specific and begins on delivery date. Product durations are shown in the catalog and warranty file. Coverage is for defects in materials or workmanship under normal intended use; accidental damage, misuse, unauthorized repair/modification, cosmetic wear, consumables and lost items are excluded. Proof of purchase is required.
- **Dynamic data:** Inventory, current price changes, live order status, shipment scans, payment capture/refund status, customer identity, active promotion availability and account details are dynamic. The assistant must use an authorized connected system or route to a human; it must never infer or fabricate these values.
- **Privacy boundary:** Never request or repeat passwords, full payment-card numbers, CVV, one-time passcodes, recovery codes or full government ID numbers. The support agent may request an order number and the email used at checkout, then use approved authentication tools to verify access before revealing account-specific information.


## Standard return eligibility

Most products purchased directly from NovaTech Store may be returned within **30 calendar days after delivery** when they are in original condition, complete and accompanied by proof of purchase. “Calendar days” includes weekends and holidays. The return window begins on the carrier's delivered date or the verified delivery date recorded by the order system.

### Condition requirements

- Include the product, standard accessories, manuals and retail packaging where reasonably available.
- The item must not show damage caused by misuse, liquid exposure, unauthorized repair, modification or neglect.
- Opened products may be accepted when complete and undamaged; opening a box does not automatically make every return ineligible.
- Missing accessories, excessive wear or signs of misuse may lead to a partial refund or denial after inspection. A final decision requires returns-team review.

### Exclusions

Unless defective or required by applicable law, the following are not eligible for standard change-of-mind returns: gift cards, consumables, hygiene-sensitive products after opening, explicitly marked final-sale items, and products damaged through misuse. The AI must not invent additional exclusions or override statutory rights.

## Return shipping responsibility

- Confirmed defect, wrong item or NovaTech fulfillment error reported within 10 calendar days after delivery: NovaTech provides a prepaid return label after review.
- Buyer-remorse/compatibility-change return: customer pays return shipping. If the customer elects a NovaTech-provided label, a $7.95 label fee may be deducted from the refund.
- If the initial report is outside the 10-day company-paid-label period but inside the 30-day return window, a standard return may still be possible; route to Returns for label/eligibility review.

## Return process

1. Customer opens a return request from the authenticated order page or contacts support.
2. The system verifies order, delivery date, product SKU, return window and return reason.
3. Returns team confirms eligibility and provides a return authorization and shipping instructions.
4. Customer packs the item securely and sends it using the authorized label/service.
5. Returns facility receives and inspects the product, normally within 3–5 business days after arrival.
6. Customer receives the inspection outcome and, if approved, the refund or exchange decision.

A return is not authorized merely because the chatbot explains this process. The AI must not create a label or authorization unless an approved tool confirms it.

## Exchanges

An exchange may be available for the same product when the replacement is in stock and the return is approved. A different product or upgrade is normally handled as a return plus a new purchase; price differences, tax and shipping may apply. Inventory is dynamic. If the exchange tool does not confirm stock and reservation, route the request to a human agent.

## Damaged, defective or incorrect items

Ask the customer to stop using a product that is hot, smoking, swollen, sparking, emitting an unusual odor or otherwise unsafe. For non-safety defects, collect the order number, SKU, symptoms and approximate discovery date. Photos/video may be requested through a secure company upload workflow, not through an unapproved channel. Reports made within 10 calendar days after delivery may qualify for a prepaid label after review. Warranty coverage may apply after the standard return period; see `10_warranty_policy.md`.

## Marketplace purchases

Purchases made through an online marketplace must be returned through the same marketplace. Its return window, label, refund and dispute process may differ from the direct-store rules. The AI should explain this distinction and avoid issuing direct-store return promises.

## Return decision boundary

The chatbot can explain the published rules and help customers prepare information. Eligibility, condition disputes, exception requests, return authorization, labels and exchange reservations require the return system or a human Returns representative.
