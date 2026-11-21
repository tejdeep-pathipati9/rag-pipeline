---
document_id: "NS-CONN-2026"
title: "Connection Protection and Involuntary Rebooking Standard"
document_type: "policy"
version: "2.0"
effective_from: "2026-01-01"
status: "current"
owner: "Customer Operations"
source_kind: "synthetic"
fictional_airline: "Northstar Air"
---

# Connection Protection and Involuntary Rebooking Standard

> **Document control:** Customer Operations / Network Recovery. Approved 2025-12-15. Effective for travel on or after 2026-01-01. Review owner: Director of Airport Recovery. Applicability: Northstar-marketed, Northstar-operated domestic segments on a single ticket.

## 1. Purpose and decision ownership
This standard defines how Northstar Air protects a passenger traveling through an intermediate airport when disruption to an earlier segment makes the onward segment unattainable. An agent should not equate a missed connection with a canceled ticket or automatically conclude that the passenger is owed cash compensation. Determine itinerary protection, actual connection feasibility, and travel preference before proposing recovery. For refund conditions, refer to **NS-REF-2026 §3**.

### 1.1 Covered transportation
A *protected itinerary* includes at least two domestic Northstar-operated legs issued on the same ticket and reservation, with a connection sold as a continuous itinerary. The passenger's first leg must be delayed, canceled, or otherwise disrupted by Northstar operations before the onward flight's boarding cutoff. A booking reference by itself is insufficient: verify that both coupons appear under the same ticket record. Codeshare, interline, separate-ticket, and international itineraries are outside this pilot standard and must be referred to a specialist.

### 1.2 Missed connection determination
The normal test compares the actual inbound arrival and the earliest feasible time to reach the onward gate with the gate's recorded boarding close. Airport minimum-connection-time tables support but do not replace this observed test. Do not classify the connection as missed merely because the incoming flight is late; an onward departure may also have been delayed. If boarding status is unavailable, mark connection feasibility as **unverified**, not missed.

## 2. Recovery entitlements
### 2.1 No-additional-fare rebooking
For a verified protected missed connection caused by a preceding Northstar segment disruption, the passenger may be rebooked to the earliest available Northstar-operated itinerary serving the original ticketed destination at no additional fare. This Northstar contractual commitment applies to both airline-controllable and uncontrollable disruptions. Seat availability must be confirmed; the standard promises an eligible rebooking process, **not a particular flight or departure time**. Cabin equivalence is preferred, and an involuntary downgrade must be separately assessed under applicable refund rules.

### 2.2 Alternative itineraries
The agent must search same-day nonstop options, later connecting service, and next-day service in that order unless documented passenger preferences require otherwise. Never represent an unavailable seat as booked. A hold on an alternative flight must include an expiration time and must not silently constitute acceptance. External-carrier transfers require the interline desk's approval and are not guaranteed under this pilot policy.

### 2.3 Passenger choice
A passenger may accept, reject, or leave an offer unanswered. Record the status as `OFFERED`, `ACCEPTED`, `DECLINED`, or `EXPIRED` with timestamp and notification channel. Acceptance followed by completed travel can affect eligibility for a disruption-based ticket refund, as described in **NS-REF-2026 §3.4**. If a significant change triggers a refund right, an alternative offer must not be presented as the only permissible remedy.

### 2.4 Minimum connection time and operational feasibility
The booked connection time is an itinerary planning figure, not a guarantee that a late passenger can board once a departure is closed. For each interrupted itinerary, the agent compares the inbound flight's actual gate-arrival time, the onward flight's documented boarding cutoff, terminal or concourse transfer constraints, and any confirmed service hold. A connection is not considered available merely because the onward aircraft has not left the ground. The agent must record why the connection was feasible or missed using the operational timestamps and their timezone-qualified sources. If arrival and boarding records disagree, the disposition remains `NEEDS_REVIEW` until the conflicting event is explained; do not resolve an ambiguity by selecting whichever timestamp is more favorable.

### 2.5 Recovery inventory is a snapshot, not a promise
A rebooking search must record the availability snapshot time, origin and destination, offered segments, and whether the alternative still protects a reasonable connection. Inventory can change between query time and confirmation. An itinerary appearing in a search result is not the same as a confirmed reservation. Staff must distinguish `SEARCHED`, `OFFERED`, `ACCEPTED`, `TICKETED`, and `FLOWN`, and never state that the customer has been rebooked when only an offer exists. If no acceptable inventory is found, retain the underlying no-additional-fare recovery eligibility while recording `NO_CURRENT_INVENTORY`. The separate refund question must still be assessed under **NS-REF-2026 §3**.

### 2.6 Equivalent and non-equivalent transportation
When proposing alternatives, compare the final destination, departure station, connection count, travel date, and any documented constraints. A flight into a different metropolitan airport, a route adding a connection, or an itinerary arriving substantially later can have consequences under the separate refund framework, even if the customer is entitled to rebooking under this policy. A proposed itinerary is not automatically appropriate for a passenger who has documented accessibility assistance, mobility requirements, or a minor-traveler restriction. Flag the special handling; do not infer that a routing is acceptable from its ticket price or geographic proximity alone. A passenger may ask for another feasible routing rather than accept the first offer.

### 2.7 Decision record for a disrupted connection
Each decision should be reproducible from the recorded facts. Capture (a) original itinerary and ticket linkage; (b) whether the inbound Northstar operation caused the failed connection; (c) inbound and outbound operational times; (d) recovery alternatives and inventory timestamps; (e) passenger choice, if known; and (f) the current policy version. The absence of a final cause code does not by itself defeat no-fare rebooking, because §2.1 is cause-independent for protected missed connections. By contrast, a hotel recommendation made from this same record must request the classification and overnight facts required by **NS-CARE-2026 §4**. These are different decision paths using some shared evidence.

### 2.8 Communication during unsettled recovery
A passenger may ask the same question at a boarding gate, a phone-support desk, and a mobile rebooking channel. These channels can observe different snapshots of inventory and offer state. Staff should identify the current authoritative offer and communicate any cancellation or replacement of earlier proposals; they must not treat repeated offers as multiple distinct confirmations. The customer should know whether there is an active ticket, whether an alternate remains only a proposal, and what response is required. Where the customer has requested a refund, agents should avoid making new bookings without explicit authorization and review qualifying travel changes and passenger choice under **NS-REF-2026 §3**. This communication record is evidence for the customer-choice lifecycle, not an independent basis for awarding a refund.

A connection-recovery decision may therefore require several evidence sources: the booked segments, actual and scheduled flight events, a timestamped offer, and a passenger-choice event. The decision service should identify which source supplied each fact, rather than responding with a generic policy summary that hides operational uncertainty. The return value should distinguish `ELIGIBLE`, `NOT_ELIGIBLE`, `NEEDS_REVIEW`, and `OUT_OF_SCOPE` for the rebooking rule, while reporting separate operational fulfillment status in a dedicated field. This distinction supports audit and allows a later evaluator to identify whether the failure occurred in evidence retrieval, rule interpretation, or ticketing execution.

## 3. Overnight and care coordination
### 3.1 Connection recovery is not hotel eligibility
A no-charge rebooking entitlement does not by itself establish a hotel entitlement. Hotel and meal commitments are controlled by **NS-CARE-2026 §§3–5**, including disruption cause, overnight necessity, passenger residence, and authorization. The policy decision should report these as separate outcomes.

### 3.2 Timeline consistency
Use the *original final-destination arrival* from the issued itinerary and the *projected final-destination arrival* for a proposed alternative when assessing significant change. Compare timestamps in UTC, then present local times for readability. A three-hour inbound delay does not always mean a three-hour delay at the final destination; an overnight connection might cause a much greater difference.

### 3.3 Cause classification
Read the latest finalized classification from **NS-CAUSE-2026 §3**, not the first free-text airport comment. A pending classification can coexist with rebooking eligibility because rebooking in §2.1 does not depend on cause. The same uncertainty may prevent a definitive hotel outcome.

## 4. Exceptions and escalation
### 4.1 Passenger-caused missed connections
When the inbound flight arrived sufficiently early and the passenger missed boarding for unrelated personal reasons, this involuntary protection does not automatically apply. Obtain agent-reviewed evidence before marking a missed connection passenger-caused; do not infer it from a single scan event.

### 4.2 Accessibility or urgent support
Where a traveler requires disability assistance or urgent medical accommodation, route to a qualified service desk; do not force standard walking-time assumptions. The pilot's evaluation questions may contain such facts only as **escalation** cases, not automatic legal-eligibility determinations.

### 4.3 Conflicting evidence
When the flight report and booking record disagree, keep the rebooking decision at `NEEDS_REVIEW`, identify missing data, and open a traceable investigation. An archived historical case is useful for precedent but cannot override this standard.

## 5. Operational evidence and audit
A recovery review must capture ticket linkage, original arrival, inbound actual arrival, onward boarding cutoff, proposed alternative and passenger acceptance status. Apply the checks in §2 and **NS-REF-2026 §3** when the passenger declines continuation. Material corrections to a departure or arrival timestamp should create a new record revision rather than overwriting the earlier observation.

## 6. Example interpretations
| Situation | Rebooking under §2.1 | Hotel under this document? | Next action |
|---|---|---|---|
| Mechanical delay causes a protected missed connection | Eligible, subject to seats | Not determined here | Consult NS-CARE-2026 |
| Weather delay causes a protected missed connection | Eligible, subject to seats | Not determined here | Consult NS-CARE-2026 |
| Separate tickets purchased independently | Outside pilot scope | Not determined | Refer to specialist |
| Late inbound but onward boarding still open | Missed connection not established | Not determined | Verify boarding event |

## 7. Referenced controls
**NS-CAUSE-2026 §3** defines classified causes. **NS-CARE-2026 §4** determines overnight assistance. **NS-REF-2026 §3** addresses disruption-triggered refund rights. Sections 2.2–2.8 explain offers, passenger choice and confirmation. The Northstar documents are fictional training policies; real statutory rights must be checked against official sources.
