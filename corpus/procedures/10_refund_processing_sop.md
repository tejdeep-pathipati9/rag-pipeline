---
document_id: "SOP-REFUND"
title: "Ticketing SOP — Disruption Refund Review and Settlement"
document_type: "sop"
version: "1.2"
effective_from: "2026-01-01"
status: "current"
owner: "Ticketing Compliance"
source_kind: "synthetic"
fictional_airline: "Northstar Air"
---

# Ticketing SOP — Disruption Refund Review and Settlement

> **Controlled procedure:** Ticketing Compliance, version 1.2, effective 2026-01-01. Source authority: **NS-REF-2026** and applicable official DOT refund guidance. This process supports factual case review; no real payment or booking transaction is executed by FlightResolve.

## 1. Intake and evidence boundaries
Start a refund review after the traveler asks to stop traveling, rejects an offered alternative, or presents a disrupted itinerary that may require an automatic refund. Gather the original ticket and coupon values, passenger travel status, all notification and offer events, and original versus proposed final-destination arrival. Do not infer that the passenger rejected travel merely because they asked a question about refunds.

### 1.1 Required identifiers
Capture case ID, booking reference, individual ticket number, coupon status, merchant of record, payment method category, and refund-related offer IDs. A booking reference without underlying ticket-state evidence is not sufficient to calculate money to be returned. The sample record set includes **OPS-BOOK-214** and **OPS-OFFER-214**.

## 2. Qualification gates
### 2.1 Cancellation or significant change
Check the actual cancellation record or qualifying change criteria, including domestic final-arrival change of at least three hours, earlier origin departure of at least three hours, and other listed changes. Use **NS-REF-2026 §3** and **DOT-REF-SNAPSHOT §2**. Do not mistake a two-hour incoming flight delay for final-itinerary arrival change, or vice versa.

### 2.2 Passenger decision gate
Determine whether alternative travel was `OFFERED`, `ACCEPTED`, `DECLINED`, `EXPIRED`, or `FLOWN`. Record the source event and timestamp. An open offer with no response cannot be converted into acceptance, and an accepted offer does not necessarily mean the passenger actually flew. If the offer is unexpired and the passenger choice remains unknown, return `DECISION_PENDING` and explain the missing information.

### 2.3 Refund claim outcome
If a qualifying disruption occurred and the passenger rejected alternatives or otherwise meets the applicable automatic refund trigger, continue settlement. If the passenger completed the replacement journey, do not issue a full ticket-price refund solely for the schedule change. If the itinerary change is below the relevant criteria and no other trigger is found, check fare terms or escalate; do not assert federal refund eligibility from dissatisfaction alone.

## 3. Ticket value calculation
### 3.1 Unused travel
Identify unused coupons and associated paid value. A customer who already traveled BOS to CLT but declined CLT to SFO does not automatically have the same refund amount as someone who never departed BOS. The pilot's RAG layer does not invent a dollar amount: use explicit accounting data or return `AMOUNT_PENDING`.

### 3.2 Optional charges
Check whether separate optional service fees for unused services are documented. Those are out of the pilot's main three-way eligibility classifier, but a real ticketing workflow should preserve them as separate questions rather than blending them into ticket value.

### 3.3 Merchant of record
The airline or ticket agent that collected payment may determine which party must issue the applicable refund. If this field is missing, the existence of an eligibility right can be reported while the processing path remains unresolved.

### 3.4 Already flown or downgraded
If travel was completed, do not issue the full fare back under significant change alone. An involuntary downgrade may have a different refund calculation, and a fully refundable fare may have separate contractual conditions. Route such cases to the appropriate adjustment workflow.

### 3.5 Distinguishing eligibility from the payable amount
A refund reviewer should not block a clear eligibility decision simply because the value of an unused ticket coupon is still being calculated. The case can carry an established refund pathway and a separate `AMOUNT_PENDING` task. The amount calculation belongs to ticket accounting, not to document retrieval. For a two-leg journey where the first leg was flown, use remaining coupon status rather than treating the entire fare as unconsumed. Preserve the booking channel and merchant-of-record fields because refund initiation and processing obligations may involve the seller rather than only the operating airline.

### 3.6 Evidence consistency for declined alternatives
A customer service note saying 'passenger wants refund' may be useful but is not by itself a complete transaction history. Compare the note against the offer lifecycle, ticket coupon record, and notification history. An offer that was only created internally is not proof the passenger accepted it. An alternative marked `ACCEPTED` but never ticketed requires investigation before being represented as completed travel. The engine should separate what it can establish from the documents—such as significant final-arrival change—from what it still needs, such as confirmed passenger decision.

### 3.7 Reconciliation examples
| Evidence configuration | Workflow result | Warning |
|---|---|---|
| Qualifying major change, alternative declined, unused onward coupon | Initiate applicable unused-travel refund | Amount may require ticket ledger |
| Qualifying change, alternative accepted and flown | Do not initiate full transportation refund under this pathway | Check other distinct entitlements only if raised |
| Qualifying change, offer created but passenger choice absent | Await applicable notification and choice conditions | Do not invent acceptance or refusal |
| No significant-change criterion established | Escalate only if another eligibility ground exists | Do not use leg delay as final-arrival delay |
| Contradictory ticket and offer states | Manual reconciliation | Record conflicting source IDs |

This SOP describes processing, not an independent source of federal entitlements. Resolve any conflict against the official applicable DOT rule and document the precedence decision.

## 4. Payment and communication
### 4.1 Refund notice
Explain eligibility, documented passenger choice, value calculation status, merchant-of-record responsibility, and the expected return method. DOT's consumer guidance outlines seven business days for credit-card purchases and twenty calendar days for other certain payment forms after appropriate triggering events. Do not calculate a deadline until the trigger and payment method are known.

### 4.2 No accidental cancellations
A simulated CLI query must never cancel a passenger's travel, withdraw a booking offer, or issue a payment. It may describe the steps an authorized agent would perform. An actual settlement would require a transaction ID, approval event, and idempotent payment processing.

### 4.3 Reconciliation
If the ticket states and offer log conflict, open a reconciliation task rather than selecting whichever record is easiest to retrieve. If the refund rule and carrier hotel rule appear to conflict, evaluate them separately: the two documents govern different benefits.

## 5. Decision table
| Evidence | Decision | Next step |
|---|---|---|
| Significant final arrival change, replacement declined | Refund-eligible pathway | Value of unused coupons |
| Significant change, alternative offered but decision unknown | Pending | Record passenger decision / applicable trigger |
| Significant change, replacement flown | No full refund under change alone | Check partial exceptions if any |
| Weather cancellation, no alternative accepted | Qualifying refund pathway | Do not deny because of weather |
| No significant change, no cancellation, no refundable fare evidence | Not established | Ask for additional eligibility basis |

## 6. Audit and related documents
Return a structured decision plus supporting clause citations, source revision IDs, offer state, amount status, and any missing fields. Sources: **NS-REF-2026 §§2–4**, **DOT-REF-SNAPSHOT §§2–3**, **SOP-REBOOK §3**, and **OPS-OFFER-214**.
