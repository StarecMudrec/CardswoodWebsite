# Can the payment be cancelled if item granting fails?

## Current integration: MONETA.Assistant / PayAnyWay

Your site uses **MONETA.Assistant** (PayAnyWay): the flow is “request form → user pays → **Pay URL** callback”. The docs you have are:

- **MONETA.Assistant.ru.pdf** – request on payment, Pay URL, Check URL (no refund API).
- **merchium.pdf** – PayAnyWay setup (no refund API).
- **cmsspecification (1).pdf** – Check/Pay URL and receipt format (no refund API).

In this flow **there is no API to cancel or refund a payment from your backend**. Refunds are done **manually** in the PayAnyWay / Moneta.Ru back office (личный кабинет).

So **with the current integration, payment cannot be cancelled automatically** when notification or item granting fails. You keep the money; you handle failed cases by:

- Granting items manually, or  
- Refunding manually in the PayAnyWay back office, if you decide to refund.

---

## If you add MONETA.MerchantAPI v2

**MONETA.MerchantAPI.v2.ru.pdf** describes a **different** API (SOAP/JSON, Merchant API, not Assistant):

- **Refund** – возврат средств.
- **CancelTransaction** – отмена операции.

So **yes, payment can be cancelled/refunded programmatically**, but only if you:

1. Have **Merchant API v2** access (credentials, not just MNT_ID + integrity code).
2. Add a **separate** integration that:
   - Uses the **operation/payment id** you already store (`payanyway_payment_id` / MNT_OPERATION_ID).
   - Calls **Refund** (or **CancelTransaction**, depending on the API and state of the payment) when:
     - Notification to the bot fails after all retries, or  
     - Your “item granting” step fails and you decide to refund.

Then you could, for example:

- On **notification_status == "failed"** (and optionally after a short delay or manual flag): call Merchant API **Refund** for that order’s `payanyway_payment_id`.
- Or run a periodic job that finds paid orders with failed notification and calls Refund for them.

---

## Summary

| Question | Answer |
|----------|--------|
| Can payment be cancelled if **notification** fails (current code)? | **No.** With PayAnyWay/MONETA.Assistant only, there is no cancel/refund API. Refunds are manual in ЛК. |
| Can payment be cancelled if **item granting** fails? | Same: **no** with current integration. |
| Can it ever be cancelled automatically? | **Yes**, if you add **MONETA.MerchantAPI v2** and call **Refund** (or **CancelTransaction**) when granting fails or notification fails and you want to refund. |

So: **with your current setup, payment cannot be cancelled automatically** when item granting (or notification) fails; you handle it manually. To support **automatic** cancel/refund on failure, you need Merchant API v2 and an integration that calls Refund when appropriate.
