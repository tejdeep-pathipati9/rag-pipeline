---
document_id: "OPS-BOOK-214"
title: "Passenger Booking and Ticket Ledger — FR-214"
document_type: "operational_record"
version: "r3"
effective_from: "2026-10-14"
status: "current"
owner: "Ticketing Systems"
source_kind: "synthetic"
fictional_airline: "Northstar Air"
case_id: "FR-214"
record_type: "booking"
is_synthetic: true
---

# Passenger Booking and Ticket Ledger — FR-214

> **Synthetic booking export:** This is a fictional, deterministic test fixture, not live reservation data. Record revision `BOOK-214-r3`; exported 2026-10-14T19:00:00Z. Owner: Ticketing Systems. The same IDs are used in OPS-FLIGHT-214, OPS-CAUSE-214 and OPS-OFFER-214. All names and ticket numbers are invented.

## 1. Passenger and itinerary key
| Field | Value |
|---|---|
| Case ID | `FR-214` |
| Passenger display name | Morgan Lee (fictional) |
| Reservation reference | `NS7KQ2` |
| Ticket ID | `016-9000002140` (synthetic) |
| Ticket structure | Single ticket; two Northstar-operated domestic flight coupons |
| Ticket issued | 2026-09-19T16:30:00Z |
| Passenger home metro | Boston, MA |
| Recovery airport | Charlotte Douglas (CLT), NC |
| Final destination | San Francisco (SFO), CA |
| Currency / payment | USD / credit-card purchase |
| Merchant of record | Northstar Air (synthetic) |
| Passenger notification consent | Email and SMS |

## 2. Original ticketed itinerary
| Segment | Carrier | Route | Scheduled departure | Scheduled arrival | Coupon status at export |
|---|---|---|---|---|---|
| `SEG-214-A` / `NS420` | Northstar Air | BOS → CLT | 2026-10-14 08:10 EDT | 2026-10-14 10:35 EDT | FLOWN |
| `SEG-214-B` / `NS811` | Northstar Air | CLT → SFO | 2026-10-14 11:35 EDT | 2026-10-14 14:10 PDT | OPEN_UNUSED |

### 2.1 Connection and boarding facts
Original connection time at CLT was 60 minutes. The onward `NS811` boarding cutoff was recorded as 11:20 EDT. The inbound `NS420` reached its arrival gate at 13:20 EDT, after the original onward flight had already departed. The full departure history is in **OPS-FLIGHT-214 §2**; this ticket export alone does not prove why `NS420` was delayed.

### 2.2 Original final-arrival baseline
The final destination originally scheduled arrival is **2026-10-14 14:10 PDT**, equivalent to 21:10 UTC. This baseline is important for the domestic three-hour significant-change assessment. Do not use the inbound CLT arrival, or confuse PDT with EDT, when comparing an offered final arrival.

## 3. Ticket entitlement facts
The two coupons were issued on a single ticket, making the missed connection a candidate for protection under **NS-CONN-2026 §1.1**. The first leg was flown. Therefore, if the traveler later rejects a qualifying alternative, the refund calculation must consider the unused onward coupon rather than blindly returning the original full itinerary price. No unused-coupon dollar amount is included in this export; amount calculation should remain pending.

### 3.1 Travel choice snapshot
At the export timestamp, no confirmed replacement segment was ticketed. An alternative was sent but not yet accepted; the authoritative offer-state event history appears in **OPS-OFFER-214**. Treat the customer's ultimate decision as `UNKNOWN_AT_EXPORT`, not as rejected or accepted. A customer query about refund options does not itself change this status.

### 3.2 Residence field interpretation
For the simulated hotel eligibility test, CLT is outside the passenger's verified home metro. The booking's billing address is intentionally not included. Use the `home_metro` business field rather than inferring residence from the itinerary origin; a traveler can begin a journey away from home.

## 4. Provenance and data-contract notes
System-of-record fields are passenger ID, ticket ID, coupon status and original itinerary. The flight disruption report controls actual flight times; the approved investigation controls delay cause; the offer log controls current rebooking-offer status. If the sources disagree, do not silently prefer the most recently retrieved text. Join on case and flight identifiers and report discrepancies.

## 5. Related evidence
**OPS-FLIGHT-214 §2**, **OPS-CAUSE-214 §§2–3**, **OPS-OFFER-214 §§2–3**. Relevant policies: **NS-CONN-2026 §§1–3**, **NS-CARE-2026 §4**, **NS-REF-2026 §4.1**.
