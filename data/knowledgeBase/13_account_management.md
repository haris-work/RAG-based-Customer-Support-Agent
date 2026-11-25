# Customer Account Management

## Account registration

Customers may create an account using an email address and a password set directly in the secure storefront. They should use a unique password and avoid sharing account access. The AI must never ask the customer to disclose a password or create one on their behalf.

## Sign-in and password reset

Use the storefront's “Forgot password” flow. The system sends a reset link to the registered email address if the account exists. For security, the AI should not reveal whether an arbitrary email address has an account unless an authenticated lookup explicitly permits it. Reset links and verification codes are private; customers should not paste them into chat.

## Email address changes

Email changes require authentication through the account security workflow. The AI may explain where the setting is located but may not change the address based only on a chat request. If the customer cannot access the old email or suspects account compromise, route to Trust & Safety.

## Guest checkout

Customers can place eligible direct-store orders as guests. They may use the order number and checkout email for secure order verification. A guest order does not automatically create an account. Do not ask the customer to create an account as a condition of support.

## Order history

Signed-in customers can view order history and available tracking/return actions in the account area. Guest customers should use the secure order lookup link in the confirmation email or request support verification. The AI must not reveal order details before verification.

## Account deletion and privacy requests

A customer may request account deletion or a copy/correction of personal data through the privacy request process. The request must be identity-verified and reviewed by the privacy owner; some transaction records may need to be retained for legitimate business, accounting, fraud-prevention or legal reasons. Do not promise immediate or total erasure. Route requests to Privacy using `17_privacy_security.md`.

## Locked or suspicious account

Repeated failed sign-ins, unfamiliar activity, an unexpected password-reset message or changed contact details may indicate compromise. Advise the customer to use the official password-reset route from the known storefront, secure their email account and contact support through the official channel. Do not ask for OTPs or recovery codes. Escalate suspected takeover to Trust & Safety.

## Customer authentication boundary

An order number plus checkout email may be used as lookup inputs but does not, by itself, authorize disclosure of all personal information. Follow the approved verification workflow and disclose only information needed to resolve the case. Never collect passwords, full card details, CVV, government ID numbers or one-time credentials in chat.
