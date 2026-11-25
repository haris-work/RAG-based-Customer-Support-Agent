# Payment and Billing

## Accepted payment methods

The fictional direct storefront is configured to accept major credit and debit cards, eligible digital wallets supported at checkout, and NovaTech gift cards. Availability depends on checkout region, device and payment-provider support. Buy-now-pay-later options are not defined in this training knowledge base; the AI must not claim they are offered. Marketplace purchases use the marketplace's available payment methods.

## Authorization versus capture

A payment authorization reserves or verifies funds; it is not necessarily a completed capture. A pending authorization may later disappear or convert into a posted charge depending on the issuer and order flow. The AI must retrieve the actual payment state before explaining an individual transaction.

## Failed or declined payment

The customer should confirm the billing address and payment method details in the secure checkout interface, check with the issuer, and retry only after verifying that no duplicate order was created. Do not ask the customer to send card details in chat or email. A bank decline reason may not be shared with NovaTech; the issuer is the authority for account-specific declines.

## Duplicate or unexpected charge

Ask for the order number, approximate date, amount and last four digits only if the approved payment workflow specifically supports this minimal reference. Never request the full card number or CVV. Two pending entries may represent an authorization and a capture, but the AI must not assume that. Finance must reconcile against provider records.

## Taxes and invoices

Applicable sales tax is calculated at checkout using the destination and tax rules applied by the commerce platform. The final order confirmation/receipt is the source for the transaction's tax breakdown. The AI may explain where to find the receipt but must not calculate or guarantee an individual tax amount. Invoice or tax-exemption requests require Finance review and any required documentation through a secure channel.

## Gift cards

Gift-card balance and redemption state are dynamic. The AI must use the approved gift-card lookup tool or direct the customer to the secure balance/check-out page. Never invent a balance or ask the customer to post a full gift-card code publicly.

## Payment security boundaries

NovaTech's support agent is not a payment-card collection channel. Do not request or store full card numbers, CVV, PINs, bank login credentials, passwords, OTPs or recovery codes. Customers should enter payment information only in the secure checkout or payment-provider interface. Do not claim PCI certification or any other compliance certification in this fictional scenario.

## Billing disputes

For a charge the customer does not recognize, a duplicate transaction, a refund that failed, a mismatch between receipt and bank statement or a suspected fraudulent purchase, route to Finance. For suspected account takeover or compromised payment details, also route to Trust & Safety under `16_human_escalation_policy.md`.

## Dynamic data

Payment authorization/capture/refund state, payment-provider reference, gift-card balance, tax receipt, billing address and fraud review are dynamic. They must come from an authorized integration and verified customer context.
