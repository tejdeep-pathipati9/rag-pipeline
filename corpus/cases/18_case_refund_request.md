---
document_id: "CASE-REF-2026"
title: "Resolved Passenger Case — Declined Rebooking and Refund Review"
document_type: "historical_case"
version: "1.0"
effective_from: "2026-09-06"
status: "current"
owner: "Historical Case Review"
source_kind: "synthetic"
fictional_airline: "Northstar Air"
case_id: "FR-207"
case_status: "CLOSED"
is_synthetic: true
---

# Resolved Passenger Case — Declined Rebooking and Refund Review

> **Synthetic closed case:** `FR-207`, travel date 2026-09-06, closed 2026-09-10. Purpose: separate a passenger's choice of refund from the existence of a no-extra-fare rebooking option. All identities and payment values are fictional.

## 1. Original itinerary
The passenger had a single Northstar ticket from Baltimore to Sacramento through Charlotte. The inbound reached Charlotte late after an airline-controlled aircraft rotation problem; the passenger missed the onward flight. The original itinerary was scheduled to arrive in Sacramento at 17:15 local time on September 6. The next feasible Northstar offer would arrive at 09:30 on September 7, more than sixteen hours later. Original and offered timestamps were preserved in the ticketing event record.

### 1.1 Operational offer
The recovery agent proposed next-day travel at no additional fare, correctly applying **NS-CONN-2026 §2.1**. The passenger received an explicit notice that an applicable refund could be available if they declined to continue after a qualifying significant change. An offer event recorded `OFFERED`, followed by a separate passenger message documenting `DECLINED`.

## 2. Event timeline
| Event | Local time | Source action |
|---|---|---|
| Inbound delay confirmed | 14:10 | Flight movement record |
| Onward service missed | 16:25 | Connection event |
| Next-day offer created | 17:05 | `OFFERED` |
| Passenger rejected replacement | 17:41 | `DECLINED` from authenticated contact |
| Refund qualification checked | 18:00 | Final-arrival difference evaluated |
| Unused coupon value reconciled | Next business day | Ticket accounting review |
| Refund submitted to processor | 2026-09-08 | Merchant-of-record record |

## 3. Separate benefit assessments
### 3.1 Rebooking
The passenger qualified to receive an alternative Northstar itinerary at no extra fare. That statement remained correct even though the passenger rejected the particular offered flight. Eligibility is about what the airline offered under the connection rule, not whether the customer ultimately exercised that choice.

### 3.2 Refund qualification
The substitute journey would have reached the final destination well after the three-hour domestic significant-change benchmark. The passenger explicitly declined the alternative and did not travel the unused onward coupon. The refund review therefore identified a qualifying pathway under **NS-REF-2026 §§2–4** with reference to **DOT-REF-SNAPSHOT §§2–3**. Ticket accounting computed the unused value; no automated language model estimated the fare allocation.

### 3.3 Hotel decision
Although the rotation problem was airline-controlled and overnight travel might otherwise have triggered review, the customer elected to end the uncompleted journey. The case was closed under the refund workflow without issuing a hotel voucher. This historical *outcome* is not proof that every passenger choosing a refund is categorically disqualified from a hotel; such a categorical rule does not appear in the Northstar hotel policy.

## 4. What the customer was told
The confirmed customer message explained that rebooking was available at no extra fare, that the passenger had chosen the refund path instead, and that the value of unused transportation would be returned to the original form of payment according to applicable processing rules. The communication did not promise both a flown replacement flight and a refund for the same transportation.

### 4.1 Why the offer state matters
The operations system recorded an alternate itinerary, but an offer existing in a database is not proof that the passenger agreed to travel on it. The reviewer checked the time the offer was delivered, the passenger's recorded choice, and whether the replacement itinerary was actually flown. This ordering matters because the refund pathway depends on the qualifying change and the passenger's response. A model that reads only a narrative sentence such as 'rebooking arranged' may incorrectly assume the ticket was used. Distinct `OFFERED`, `ACCEPTED`, `TICKETED`, and `FLOWN` events should remain accessible through their original record identifiers.

### 4.2 Partial-travel accounting
The passenger had already traveled on the first segment before the connection problem arose. This makes the value of the unused onward journey a separate calculation from establishing refund eligibility. The case supports a conclusion about the appropriate refund pathway; it does not authorize a fabricated dollar amount. The ticketing ledger and merchant-of-record data determine which party processes the payment and how the unused portion is valued. When those fields are missing, the correct explanation is that the refundable amount is pending, not that the whole original purchase must be paid back.

### 4.3 Distinguishing refund rights from hotel commitments
A passenger may qualify for a refund because a replacement itinerary arrives significantly later even when the airline's voluntary hotel benefit is unavailable. The cause classification that matters for hotel eligibility need not determine the federal refund pathway. This case therefore contains intentionally separate decision tracks: missed-connection protection, accommodation eligibility, and passenger-choice-based refund analysis. The engine should produce a cited result for each track rather than collapsing them into a single favorable or unfavorable judgment.

## 5. Audit and provenance
The case retains the original scheduled arrival, substituted final arrival, the offer ID, authenticated rejection event, unused coupon status, merchant of record, payment type, and final settlement reference. A source-retrieval engine should distinguish *refund eligibility*, *refund amount calculated*, and *refund successfully issued* as three states. Only the last requires a settlement confirmation.

## 6. Connections to the live case fixture
The separate active case **FR-214** has a similar long final-arrival change but only an `OFFERED` rebooking and no rejection yet. Importing the `DECLINED` outcome from this historical case into FR-214 would be a factual error. Related references: **NS-CONN-2026 §2**, **NS-REF-2026 §3**, **SOP-REFUND §§2–4**, and **DOT-REF-SNAPSHOT §3**.
