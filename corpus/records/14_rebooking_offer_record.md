---
document_id: "OPS-OFFER-214"
title: "Recovery Offer and Passenger Decision Log — FR-214"
document_type: "operational_record"
version: "r1"
effective_from: "2026-10-14"
status: "current"
owner: "Station Recovery Desk"
source_kind: "synthetic"
fictional_airline: "Northstar Air"
case_id: "FR-214"
record_type: "travel_offer"
is_synthetic: true
offer_status: "OFFERED"
---

# Recovery Offer and Passenger Decision Log — FR-214

> **Synthetic service log:** Case FR-214 / reservation NS7KQ2. Exported 2026-10-14T19:00:00Z. Offer logs are immutable events; the latest derived state is **OFFERED / response pending**. This record does not represent a live airline booking or seat availability promise.

## 1. Original travel baseline
The original scheduled final destination was SFO at **2026-10-14 14:10 PDT** on `NS811`, as recorded in **OPS-BOOK-214 §2**. The incoming `NS420` arrived too late for that connection, according to **OPS-FLIGHT-214**. The original flight coupon `SEG-214-B` remained unused at the export time.

## 2. Proposed recovery itinerary
| Field | Value |
|---|---|
| Offer ID | `OFR-214` |
| Alternative flight | `NS815` CLT → SFO |
| Proposed departure | 2026-10-15 08:15 EDT |
| Proposed final arrival | 2026-10-15 10:40 PDT |
| Original final arrival | 2026-10-14 14:10 PDT |
| Proposed final-arrival delta | +20 hours 30 minutes |
| Candidate seat status | One synthetic seat shown as available at 14:10 EDT |
| Price condition | No additional fare under eligible rebooking |
| Offer type | Alternative travel, not confirmed reservation |
| Offer expiry | 2026-10-14 20:00 EDT |
| Response status at export | `OFFERED`; no acceptance or rejection |

### 2.1 The distinction between offer and confirmed ticket
The candidate inventory snapshot is a record of what the agent saw, not proof that a seat was held or ticketed. The offer message explains what the passenger may accept, but the log contains no acceptance event and no replacement coupon issuance. Any RAG response saying "You are booked on NS815" would be unsupported.

### 2.2 Final-destination arrival comparison
The next-day arrival at SFO is 20h30 after the original scheduled SFO arrival. This is materially different from the inbound segment's 2h45 late arrival to Charlotte. The first difference is relevant to a domestic significant-change refund evaluation under **NS-REF-2026 §3.2**. The second is useful for connection feasibility but must not replace the first.

## 3. Event log
| Event ID | UTC time | Type | Details |
|---|---|---|---|
| `OFE-214-01` | 2026-10-14T18:10Z | INVENTORY_SNAPSHOT | No same-day usable onward Northstar seat |
| `OFE-214-02` | 2026-10-14T18:20Z | OFFER_CREATED | `OFR-214` proposes NS815 next morning |
| `OFE-214-03` | 2026-10-14T18:25Z | OFFER_DELIVERED | Email/SMS notification sent |
| `OFE-214-04` | 2026-10-14T19:00Z | EXPORT | No response yet recorded |

### 3.1 No synthetic acceptance
At export time, the passenger has not accepted, rejected, or traveled on the replacement flight. Therefore a recovery engine may say "Rebooking is offered" and "A qualifying refund pathway may be available if the passenger declines," but may not assert that a refund has already been triggered and processed. The offer has not yet expired at 19:00Z.

### 3.2 Overnight impact
The proposed departure is next day at CLT. When combined with the inventory snapshot, it supports an overnight-stay finding for **NS-CARE-2026 §4.2**. Home metro and approved cause come from other records. This log intentionally does not include a hotel voucher because no accommodation authorization is represented in this record.

## 4. Passenger messaging excerpt
> We can offer a Northstar flight from Charlotte to San Francisco departing tomorrow morning at no extra fare, subject to confirmation before the offer expires. Please tell us whether you wish to continue travel. You can ask an agent about refund rights if you prefer not to take alternative transportation. This message is an offer, not a confirmed ticket.

## 5. Audit fields and references
The authoritative fields are `offer_id`, alternative segments, departure/arrival time, `response_status`, `sent_at`, `expires_at`, and confirmation status. See **SOP-REBOOK §3.2**, **NS-CONN-2026 §2.3**, **NS-REF-2026 §3.3**, and **DOT-REF-SNAPSHOT §3.3**. An external flight search is outside this corpus.
