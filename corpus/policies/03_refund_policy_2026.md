---
document_id: "NS-REF-2026"
title: "Flight Disruption Refund Eligibility and Passenger Choice"
document_type: "policy"
version: "2.0"
effective_from: "2026-01-01"
status: "current"
owner: "Ticketing Compliance"
source_kind: "synthetic"
fictional_airline: "Northstar Air"
---

# Flight Disruption Refund Eligibility and Passenger Choice

> **Document control:** Ticketing Compliance. Version 2.0, effective 2026-01-01 for relevant travel. Domestic Northstar-operated pilot. This training policy summarizes Northstar workflow and defers to applicable federal law for minimum refund rights.

## 1. Scope, authority and exclusions
This standard governs the determination of whether a passenger with a disrupted domestic Northstar itinerary may receive a refund rather than continue on changed or substitute transportation. Its central distinction is between (a) Northstar's contractual no-charge rebooking service and (b) refund rights arising from cancellation or significant itinerary changes. The two options must not be collapsed into one answer. For primary federal reference, use the current dated snapshot **DOT-REF-SNAPSHOT §§1–4**, and when required consult the official DOT page linked in that source.

### 1.1 Evidence required
Obtain ticket coupon status, original and proposed final-destination arrival timestamps, carrier cancellation status, the status of each travel offer, whether the passenger traveled, and merchant of record. A passenger's statement "I missed my connection" alone does not establish either a three-hour destination arrival change or a decision to decline onward transportation.

## 2. Distinguish travel choices
### 2.1 No-cost rebooking
**NS-CONN-2026 §2.1** may offer no-additional-fare alternate travel whether the preceding disruption was mechanical or weather-related. Accepting an offer does not mean the passenger has flown it; preserve `ACCEPTED` and `FLOWN` as separate states.

### 2.2 Refund instead of alternative travel
Where a domestic itinerary is canceled or significantly changed and the passenger does not accept the changed itinerary, replacement flight, credit, or other offered compensation, the applicable federal framework may require a refund. A passenger can reject an eligible replacement without forfeiting the otherwise applicable refund right. The airline should explain the refund option before treating rebooking as settled.

## 3. Significance and conditions
### 3.1 Cancellation
A canceled covered flight is a qualifying disruption irrespective of whether weather or airline operations caused it, provided the passenger does not travel on an accepted substitute and satisfies the relevant refund conditions. Classification is **not** a prerequisite for a federal cancellation refund.

### 3.2 Domestic arrival-change threshold
A changed itinerary scheduled to arrive at the **final destination** at least **three hours later** than originally scheduled meets one important domestic significant-change criterion described by DOT. A domestic itinerary scheduled to depart the origin at least three hours earlier is another. Evaluate these in UTC from original ticket and documented offer. Do not apply a three-hour threshold to the inbound leg in place of final arrival. Other qualifying changes, such as a different origin/destination airport or an additional connection, may also apply; see **DOT-REF-SNAPSHOT §2**.

### 3.3 Passenger decision
When an eligible qualifying disruption occurs, track whether the traveler rejected a replacement, explicitly chose a refund, accepted travel credit, or completed travel. `OFFERED` without response is **not** synonymous with `ACCEPTED`. For a nonresponse case, follow the applicable notification and departure events under **DOT-REF-SNAPSHOT §3.3**; do not assert automatic refund completion based merely on an unexpired offer.

### 3.4 Travel completed
A passenger who actually took the significantly delayed or replacement flight generally cannot obtain a full refund for transportation already used under the significant-change remedy alone. A separate partial refund may apply for an involuntary cabin downgrade or unused portions. The distinction between *accepted*, *flown*, and *partially used* is mandatory. See **SOP-REFUND §3.4**.

### 3.5 Journey-level assessment, not leg-level shortcut
For a connecting itinerary, the arrival-change calculation uses the scheduled arrival at the *final ticketed destination*. A first leg arriving four hours late does not automatically establish that the replacement itinerary arrives four hours late; the passenger might make a later connection that limits the final change. Equally, a relatively small inbound delay might cause a missed connection and push final arrival into the next day. Record the original itinerary, the proposed replacement itinerary, and each timestamp with its timezone. If the revised arrival is absent, the engine may identify a missed connection and rebooking eligibility but must not invent a final-destination change to grant the significant-change refund pathway.

### 3.6 Offer and acceptance lifecycle
A rebooking offer can exist in an operations system before the passenger sees it. Evidence must distinguish `CREATED`, `DELIVERED`, `VIEWED`, `ACCEPTED`, `DECLINED`, `EXPIRED`, and `FLOWN`. Staff should not infer a passenger decision from an internal offer row. A delivery failure or missing acknowledgment is a question about notification state, not proof of consent. If acceptance is recorded in two systems at different times, verify the authoritative event and avoid silently choosing one. Refund disposition may remain `NEEDS_PASSENGER_DECISION` while the eligibility conditions are otherwise met. The separate ticket-accounting task must not be confused with the yes/no right to decline qualifying alternate travel.

### 3.7 Ticket consumption, partial journeys, and money
When a passenger has flown the first leg of a protected connection and declines a qualifying replacement for the remaining journey, the refund of unused transportation differs from an entirely unused itinerary. Coupon accounting must identify which segment has been consumed and whether associated fees are refundable. The RAG response should avoid assigning a dollar amount without the ticket-value record. If the traveler has taken a replacement flight to the destination, full transportation refund under the disruption-change remedy generally does not follow simply because arrival was late. Any additional rights related to baggage charges, optional services, or a cabin downgrade must be evaluated as distinct issues with their own evidence and rules.

### 3.8 Other potentially significant changes
A domestic three-hour arrival threshold is not the only significant-change criterion. Under the applicable DOT framework, a change in destination airport, an additional connection, or a qualifying downgrade may be relevant. These conditions must be checked against the official dated reference rather than treated as invented Northstar entitlements. A request such as 'My itinerary now routes through two airports' cannot be decided solely from the delay-duration field. The engine should retrieve the specific rule, collect the original and changed itineraries, and explain which comparison remains incomplete when necessary. If a new government interpretation is published, source versioning should preserve the guidance in force for the relevant assessment.

### 3.9 Example evidence completeness checklist
| Decision dimension | Preferred evidence | Mistake to avoid |
|---|---|---|
| Significant arrival change | Original and replacement final-arrival timestamps | Comparing only first-leg arrival |
| Cancellation | Carrier flight status and notice | Treating a delay as a cancellation |
| Passenger decline | Delivered offer and passenger response | Treating no response as rejection prematurely |
| Transportation consumed | Ticket coupon ledger | Promising an entire ticket refund after travel |
| Amount | Accounting source for unused travel | Deriving money from chunk similarity |
| Authority | Applicable DOT rules and current carrier policy | Letting an old historical case override current obligations |

The assistant should report each supported condition and missing gate independently. If the refund right is established but money cannot yet be computed, a qualified answer is better than an invented currency amount.

## 4. Refund amount and processing
### 4.1 Remaining ticket value
For a passenger who completed the first segment but declined qualifying onward transport, calculate the refund of the unused ticket portion using ticket accounting records, rather than simply refunding the entire fare. For an entirely unused qualifying itinerary, evaluate a full ticket-price refund under applicable rules. The lab does not compute real commercial proration; if the value of unused coupons is missing, return `ELIGIBLE_AMOUNT_PENDING` for money while resolving the eligibility question separately.

### 4.2 Source and timing of payment
Eligible refunds should be made to the original form of payment according to DOT requirements. Published DOT guidance discusses **seven business days for credit-card payments and twenty calendar days for certain other payment methods** after relevant triggering events; verify precise obligations in **DOT-REF-SNAPSHOT §3** rather than improvising dates. Booking via an agent may affect which entity is merchant of record.

### 4.3 Alternative compensation
A voucher or travel credit is not automatically equivalent to a cash refund. Record whether it was explicitly accepted and retain the actual offer text and notification time. Do not mark a refund request closed merely because a voucher was generated internally.

## 5. Conditional examples
| Disruption and choice | Refund assessment | Explanation |
|---|---|---|
| Mechanical missed connection; next arrival 20 hours later; passenger rejects rebooking | Qualifying refund pathway | Final arrival change, not mechanical cause, drives analysis |
| Weather missed connection; next arrival 20 hours later; passenger rejects rebooking | Qualifying refund pathway | Weather does not remove the qualifying-disruption refund right |
| Mechanical delay; passenger accepts rebooking and flies | No full ticket refund under change alone | Passenger completed travel |
| 45-minute final arrival difference; passenger declines for convenience | Not established under significant-delay criterion alone | Check other changes and fare conditions |
| Offer sent, response unknown, flight not yet departed | Pending passenger decision | Do not invent rejection |

## 6. Conflict handling and citations
If refund policy language conflicts with an official federal requirement, applicable law controls; flag the conflict instead of silently applying a less protective fictional rule. Never cite DOT airline commitments as a refund statute. Produce decisions with citations to the applicable clause and the independent evidence record that establishes the condition. If ticket, payment, or offer states disagree, respond `NEEDS_REVIEW` and state the specific missing or contradictory field.

## 7. Related documents
**NS-CONN-2026 §2**, **NS-CARE-2026 §4**, **SOP-REFUND §§2–5**, **OPS-OFFER-214**, and **DOT-REF-SNAPSHOT §§1–4**. This document is fictional and should never be presented as an actual carrier's contract.
