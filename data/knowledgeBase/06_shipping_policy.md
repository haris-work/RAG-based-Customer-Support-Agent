# Shipping Policy

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


## Destinations

NovaTech Store ships to street addresses in the 50 US states and Washington, DC. It does not currently ship to US territories, APO/FPO/DPO addresses, international destinations or freight-forwarding addresses. A checkout address rejected by the shipping system cannot be overridden by the AI.

## Shipping options and prices

| Destination | Service | Shipping charge | Estimated carrier transit |
|---|---|---:|---|
| Contiguous 48 states | Standard | $6.95 | 5–7 business days after carrier acceptance |
| Contiguous 48 states | Free standard when eligible | $0.00 | 5–7 business days after carrier acceptance |
| Contiguous 48 states | Expedited | $14.95 | 2–3 business days after carrier acceptance |
| Alaska and Hawaii | Standard | $14.95 | 7–10 business days after carrier acceptance |

Free standard shipping applies when the merchandise subtotal is at least $75 after discounts and before tax, for delivery to the contiguous 48 states. Shipping, taxes, gift cards and excluded marketplace purchases do not count toward the threshold. Expedited shipping is not free under this rule. Alaska and Hawaii do not qualify for this threshold and do not have the expedited option in this policy snapshot.

## Processing and dispatch

In-stock orders are generally processed in 1–2 business days, Monday–Friday, excluding company-observed holidays. Payment authorization and fraud screening must be complete before processing begins. Processing is separate from carrier transit. Orders are not guaranteed to leave the warehouse the same day, even if placed before the 1:00 p.m. ET planning cutoff.

## Delivery estimates

Transit estimates begin when the carrier accepts the parcel, not when the checkout confirmation is sent. The estimate is not a guaranteed delivery date. Weather, peak-season volume, carrier capacity, address validation, service disruptions and remote-area routing can extend transit. The live carrier scan is the best available indicator after dispatch.

## Holidays and peak periods

Warehouse processing and support may pause or operate with reduced hours on company-observed holidays. Orders placed during a holiday closure resume processing on the next business day. During Black Friday/Cyber Monday and the year-end period, processing or transit may take longer than the standard estimate; the order confirmation and live tracking page should be checked for current information.

## Shipping restrictions and special cases

- Lithium-battery products may be subject to carrier and air-transport restrictions. The shipping service offered at checkout is the service authorized for that shipment.
- The AI must not suggest bypassing carrier restrictions or relabeling a parcel.
- Customers should provide a complete deliverable address. PO boxes may be unavailable for some carrier services; checkout will determine supported service.
- Once a parcel is accepted by the carrier, an address change may no longer be possible. Do not promise rerouting.
- Orders from third-party marketplaces follow the applicable marketplace shipping offer and customer-service workflow.

## Delayed, lost or damaged shipments

For a package with no tracking movement, use the carrier's latest scan and the promised estimate only as context. If the package is more than 2 business days beyond the end of its estimated transit window, open a Logistics investigation. If tracking says “delivered” but the customer cannot locate the package, follow `07_order_tracking.md` and escalate according to `16_human_escalation_policy.md`. Do not tell a customer a parcel is stolen or lost until the investigation establishes that outcome.

## Questions requiring live data

Rates displayed at checkout, serviceability for a particular ZIP code, carrier assignment, actual dispatch date and live estimated delivery are dynamic. The AI must use the shipping/checkout/order API or ask a human agent to verify them.
