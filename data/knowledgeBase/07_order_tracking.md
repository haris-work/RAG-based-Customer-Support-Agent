# Order Tracking and Order Changes

## Order lifecycle

The following are standard lifecycle labels. An individual order's actual state must be retrieved from the authorized order-management system.

1. **Order received:** Checkout submission is recorded; not yet proof of payment capture or shipment.
2. **Payment review:** Authorization, payment validation and fraud screening are in progress.
3. **Processing:** The order is queued for picking and packing.
4. **Partially fulfilled:** One or more items shipped separately; other items may remain in processing.
5. **Shipped / carrier accepted:** A carrier has accepted the parcel and a tracking reference is available.
6. **In transit:** Carrier scans show movement through its network.
7. **Out for delivery:** Carrier indicates the parcel is scheduled for a delivery attempt that day; this is not a guarantee.
8. **Delivered:** Carrier reports delivery. If the customer cannot locate it, use the delivered-but-not-received procedure.
9. **Exception / delayed:** Carrier reports an address, weather, routing or other exception requiring review.
10. **Cancelled:** The order system confirms cancellation. A request to cancel is not itself a completed cancellation.

## Confirmation and tracking notifications

A confirmation email is normally sent after the order is accepted by checkout. A separate shipment email is sent when a parcel is fulfilled and a carrier tracking reference is assigned. Email delivery may be delayed or filtered. Customers can also sign in to the fictional account area and open Order History. The AI must not invent an order number or tracking URL.

## Retrieving an individual order

If an authorized integration is available:

1. Ask for the order number and the email used at checkout.
2. Submit those values only to the approved order lookup/authentication action.
3. Follow the tool's verification result. Do not reveal personal or order details if verification fails.
4. Summarize only fields returned by the tool and state the time of the latest scan when supplied.
5. If the lookup tool is unavailable or returns no matching order, explain that the record cannot be verified and create a human-support request if possible.

Never request a password, full card number, CVV, OTP or recovery code. Guest-checkout customers may still receive order help after secure verification.

## Processing delays

Standard processing is generally 1–2 business days after payment authorization and fraud screening. A longer processing period may occur when an item is backordered, a payment needs review, an address requires correction or a holiday closure intervenes. The AI may explain the standard timeframe but must use a live order lookup to say whether an individual order has shipped.

## Missing tracking email

Ask the customer to check spam/promotions folders and confirm whether the checkout email was entered correctly. Do not ask them to share account passwords. If the order system shows a shipment but the email is missing, provide the verified tracking link through the authenticated channel or escalate to Order Operations.

## Address corrections and order edits

- Before fulfillment begins, Order Operations may be able to correct an address or edit an order, subject to payment reauthorization and fraud checks.
- Once picking/packing begins, changes are not guaranteed.
- Once the carrier accepts the parcel, NovaTech generally cannot change the delivery address. The customer may contact the carrier using its official service options, but the AI must not promise a successful intercept.
- The AI must not directly change address, item, quantity or shipping service without an authorized tool that confirms the change.

## Cancellations

Customers may request cancellation while an order is still in a cancellable state. If the order is already packed or handed to the carrier, cancellation may not be possible; the customer may need to follow the return procedure after delivery. A cancellation request must be checked against the order system. Do not tell a customer that an order is cancelled until the tool confirms the final state.

## Delayed shipment

Compare the live tracking status with the stated service estimate: 5–7 business days for contiguous standard, 2–3 for contiguous expedited, and 7–10 for Alaska/Hawaii standard, all after carrier acceptance. If it is more than 2 business days beyond the end of the applicable estimate without delivery, route to Logistics for investigation. Do not count processing time as carrier transit.

## Delivered but not received

Ask the customer to:
1. Check the delivery location, porch, side entrance, parcel locker, mailroom or reception desk.
2. Ask household members or building staff whether they accepted the parcel.
3. Check whether the carrier provided a delivery photo or location note.
4. Allow until the end of the next business day if the scan is very recent, because some premature “delivered” scans resolve shortly after.

If still missing, collect the order number, delivery address confirmation through secure verification, carrier status/time, and any relevant observations. Escalate to Logistics. Do not accuse the customer or carrier, promise a replacement/refund, or declare theft. Suspected theft and high-value claims require human investigation.

## Damaged or wrong item on arrival

Ask the customer to stop using an unsafe or visibly damaged electrical product. For a wrong or damaged item, collect the order number and a description; request photos only through an approved secure upload channel. If reported within 10 calendar days after delivery, a prepaid return label may be provided after review. See `08_returns_exchanges.md`.

## Marketplace orders

For orders purchased through a third-party marketplace, guide the customer to that marketplace's order page and messaging/return workflow. Marketplace policies can differ and may control the transaction. Do not promise that a direct-store adjustment can be applied to a marketplace order.

## Data boundary

Order number format, payment state, fulfillment state, carrier name, tracking number, tracking events, delivery proof, address and customer identity are dynamic data. All must come from a verified system result; none may be fabricated for examples or production responses.
