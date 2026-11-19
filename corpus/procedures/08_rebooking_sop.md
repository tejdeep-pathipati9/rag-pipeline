---
document_id: "SOP-REBOOK"
title: "Station Agent SOP — Protected Connection Rebooking"
document_type: "sop"
version: "1.3"
effective_from: "2026-01-01"
status: "current"
owner: "Station Recovery Desk"
source_kind: "synthetic"
fictional_airline: "Northstar Air"
---

# Station Agent SOP — Protected Connection Rebooking

> **Controlled procedure:** Station Recovery Desk, revision 1.3, effective 2026-01-01. Governing rule: **NS-CONN-2026**. Use only for one-ticket Northstar domestic connections; other itineraries require specialist routing. This SOP describes actions, not independent passenger rights.

## 1. Trigger and safety boundary
Open this workflow when a protected passenger reports that a preceding Northstar flight delay or cancellation has made an onward connection infeasible. The agent must validate the booking before moving the traveler's reservation. The agent must not cancel coupons, issue a refund, or commit a hotel before collecting the required evidence for that separate decision. A proposed replacement flight is not a ticketed reservation until the booking system reports confirmation.

### 1.1 Required inputs
Capture `booking_id`, ticket coupons, passenger travel date, inbound flight and actual gate arrival, onward flight boarding cutoff, final destination, accessibility assistance indicator if relevant, and current offer status. Match the booking identifiers in **OPS-BOOK-214** to flight evidence in **OPS-FLIGHT-214**. Missing IDs should result in an intake clarification rather than speculative lookup.

## 2. Diagnostic path
### 2.1 Confirm protected itinerary
Verify that both segments are on one ticket and operated by Northstar. If not, assign `OUT_OF_SCOPE` and forward to an interline or separate-ticket desk. Do not imply that the passenger has no rights outside the pilot: this is a limitation of the simulated workflow.

### 2.2 Confirm missed connection
Compare inbound actual gate arrival, expected transfer feasibility, and onward boarding close. If boarding could still have been reached, mark `NOT_CONFIRMED` pending gate review. If the onward service itself was delayed enough to preserve the connection, the passenger may not need replacement travel at all. Time calculations should use UTC internally.

### 2.3 Retrieve current schedule availability
Search same-day Northstar options to the original destination, then next-day flights where necessary. Record which snapshot supplied each seat count. An expired availability record is not bookable evidence. Never tell a passenger that a hypothetical example flight is available in a real airline booking system.

## 3. Recovery decision branches
| Decision | Next action | Related authority |
|---|---|---|
| One-ticket protected connection, missed | Offer earliest feasible Northstar itinerary, no extra fare | NS-CONN-2026 §2.1 |
| Protected but no seat currently available | Record no-seat state, search later options, escalate if needed | NS-CONN-2026 §2.2 |
| Separate tickets | Refer to specialist, avoid automatic same-ticket promise | NS-CONN-2026 §1.1 |
| Inbound late but connection still boardable | Confirm live gate status before changing itinerary | NS-CONN-2026 §1.2 |
| Classification `UNKNOWN` | Proceed with eligible rebooking; defer cause-dependent hotel | NS-CONN-2026 §3.3 |

### 3.1 Presenting alternatives
Describe each offer with flight ID, departure and arrival local timestamps, original destination, cabin, seat status, and acceptance deadline. An offer must not be described as guaranteed until reservation confirmation. If final-arrival change is substantial, disclose that a refund may be an option under **NS-REF-2026 §3**.

### 3.2 Capturing passenger choice
Store `OFFERED`, `ACCEPTED`, `DECLINED`, or `EXPIRED`, with a timestamp and channel. If the passenger is undecided, retain `OFFERED`. A passive lack of response cannot be reinterpreted as a completed acceptance. When an offer expires, append an event rather than editing earlier status history out of existence.

### 3.3 Offer assembly and record linkage
Every proposed alternate itinerary must carry a stable offer identifier linked to the original booking and the disruption that caused the failed connection. The rebooking agent should verify segment order, transfer time, origin and destination, departure and arrival timestamps, and the offer's inventory-observation timestamp. When multiple options are generated, the system should not mistake the first returned search result for the customer's chosen itinerary. If a routing includes an unfamiliar intermediate station or a later travel date, the passenger must be told what changed. Keep the offered routing in a structured record; the knowledge index can store an explanatory summary but must not become the authoritative seat inventory.

### 3.4 Provisional offers and confirmation
Use separate states for `SEARCHED`, `OFFERED`, `ACCEPTED`, `TICKETED`, and `FLOWN`. An offer can expire before the passenger responds. When the customer accepts, revalidate inventory and obtain an actual ticketing confirmation before announcing that travel has been secured. If a second agent sends a different itinerary, preserve both offers with their timestamps and identify which, if either, was accepted. A missing response must not be silently interpreted as rejection or consent. This distinction also controls the separate refund decision in **NS-REF-2026 §3.3**.

### 3.5 Decision-tree examples
| Observed facts | Rebooking action | Separate unresolved issue |
|---|---|---|
| Protected single-ticket connection missed after mechanical delay | Search alternative without additional fare | Hotel depends on overnight, cause, residence |
| Protected connection missed after weather disruption | Search alternative without additional fare | Weather may exclude standard hotel benefit |
| First segment late but connection still boarded successfully | No missed-connection recovery triggered | Ordinary schedule notice may remain relevant |
| Ticket linkage cannot be verified | Route to human review | Do not assume protected connection |
| Alternative offered, passenger decision unknown | Keep offer pending | Do not claim accepted travel or settled refund |

The examples illustrate operational routing, not a complete entitlement codebook. Record the controlling policy clause and the case evidence that establishes each branch.

## 4. Cross-service handoffs
### 4.1 Hotel and meal eligibility
If the next feasible departure creates an overnight wait, invoke **SOP-HOTEL §§2–3** with case facts, but do not mark hotel `ELIGIBLE` before confirming controllable cause and away-from-home status. For meals, measure the relevant waiting interval per **NS-CARE-2026 §3**.

### 4.2 Refund alternative
If the passenger declines replacement travel or asks whether cancellation entitles them to a cash refund, hand the recorded offer and original arrival evidence to **SOP-REFUND §2**. A no-extra-fare offer must not suppress a qualifying refund assessment.

### 4.3 Escalation for uncertain data
If the ticket status and flight report are contradictory, open an evidence-reconciliation task with stable IDs. If cause classification alone is pending, continue the rebooking procedure while setting hotel eligibility to `NEEDS_REVIEW`.

## 5. Required audit trail and example
For synthetic booking `NS7KQ2`, record that delayed inbound `NS420` reached Charlotte after onward boarding for `NS811` had closed. Offer `OFR-214` for the following morning without additional fare if the simulated inventory indicates a seat. Record a separate passenger-choice field; do not invent an acceptance.

The final structured response should contain the protected-itinerary decision, missed-connection evidence, rebooking eligibility, offer ID if present, and links to the policy sections used. It should not claim to have modified a real reservation or made a live booking.

## 6. Related documentation
**NS-CONN-2026 §§1–4**, **NS-CARE-2026 §4**, **NS-REF-2026 §3**, **OPS-BOOK-214**, **OPS-FLIGHT-214**, and **OPS-OFFER-214**.
