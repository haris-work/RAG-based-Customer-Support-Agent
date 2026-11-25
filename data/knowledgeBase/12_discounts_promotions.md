# Discounts, Promotions and Loyalty

## General promotion rules

Promotions are campaign-specific and time-limited. A static RAG document cannot establish whether a code is currently active, whether a customer is eligible, whether a product is excluded or whether a redemption limit has been reached. The AI must check the authorized promotion service or ask a human to verify the code.

## Coupon entry and validation

Customers enter a code in the promotion field at checkout before submitting the order. The checkout summary should show the applied discount before payment. If the code is rejected, check for spelling, start/end date, minimum spend, eligible SKU/category, destination, account eligibility and whether the code has already been redeemed. Do not promise retroactive application after an order has been placed; a human may review a request, but an adjustment is not guaranteed.

## Stacking

Unless the individual campaign terms explicitly say otherwise, only one percentage/fixed-amount coupon may be applied per order. A coupon generally cannot be combined with another coupon or a special bundle price. Free-shipping eligibility is evaluated separately under `06_shipping_policy.md`, but some campaigns may expressly exclude shipping benefits. The checkout display is authoritative for that transaction.

## Student discounts

No standing student-discount program is defined in this fictional knowledge base. The AI must not tell customers that a student discount exists. If asked, explain that no general student discount is listed and offer to check current promotions through the approved campaign tool.

## Loyalty program — NovaPoints

NovaPoints is a fictional loyalty program in this simulation. Enrolled customers earn 1 point per eligible whole USD spent on merchandise after discounts and before tax/shipping. Points are normally credited after the order is marked delivered and the return/chargeback review window is clear; the system's ledger is authoritative. 100 points may be redeemed for a $5 discount on an eligible direct-store order of at least $25 merchandise subtotal. Points have no cash value, cannot be transferred and cannot be combined with another coupon unless a campaign explicitly permits it.

Points may be reversed for refunded or charged-back merchandise. Gift-card purchases, taxes, shipping, marketplace orders and cancelled orders do not earn points. Loyalty enrollment, balance, point history and redemption availability are dynamic and require account lookup.

## Gift promotions and bundles

A free gift or bundle offer is valid only when the campaign terms and checkout cart show the eligible combination. If the gift is missing from a dispatched order, route to Customer Experience with the order number and campaign context. Do not promise a replacement gift without an inventory and campaign check.

## Expired or unavailable promotion

The AI must not generate or guess coupon codes. If a campaign has expired or the promotion tool reports ineligibility, explain the specific verified reason when available. Requests for price matching, retroactive discounts, goodwill credits or exceptions require human review.

## Dynamic information warning

Active campaign dates, code validity, eligible SKU lists, customer-specific offers, point balances, redemption status and remaining promotion inventory are dynamic. Static RAG content provides rules only; it cannot establish current eligibility.
