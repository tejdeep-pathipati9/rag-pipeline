---
document_id: "NS-CARE-2026"
title: "Passenger Care, Meal Assistance and Overnight Accommodation"
document_type: "policy"
version: "2.1"
effective_from: "2026-01-01"
status: "current"
owner: "Customer Experience Operations"
source_kind: "synthetic"
fictional_airline: "Northstar Air"
---

# Passenger Care, Meal Assistance and Overnight Accommodation

> **Document control:** Customer Experience Operations. Approved 2025-12-20, effective for disruptions beginning 2026-01-01. Version 2.1. Applies to Northstar-operated domestic itineraries. Related documents: **NS-CAUSE-2026**, **NS-CONN-2026**, **SOP-HOTEL**.

## 1. Purpose and relationship to other obligations
This policy defines Northstar Air's voluntary customer-care commitments during operational disruption. It is separate from governmental refund requirements and separate from the promise to rebook protected connecting itineraries. Agents must not describe the hotel commitment as a universally mandated federal benefit. A passenger's right to reject an eligible rebooking and receive a refund is assessed independently under **NS-REF-2026**.

### 1.1 Scope
The policy applies to Northstar passengers physically present at a U.S. airport while affected by delayed or canceled Northstar-operated domestic travel. An overnight connection caused by a late incoming Northstar flight can qualify. The entitlement is evaluated at the airport where the passenger must wait, rather than automatically at the scheduled final destination.

### 1.2 Terms
*Airline-controlled disruption* is one whose **final approved** root-cause classification is `MECHANICAL`, `CREW_OPERATIONAL`, or `AIRLINE_OPERATIONS` under **NS-CAUSE-2026 §2**. *Uncontrollable disruption* is `WEATHER` or `ATC_EXTERNAL`. `UNKNOWN` and `MIXED_PENDING` mean the controlling classification is not yet established. *Away from home* means the overnight station is not within the passenger's verified home metropolitan area; simple street-address matching is not required in this training environment.

## 2. General care and communications
### 2.1 Rebooking information
An eligible traveler should receive a realistic rebooking offer and a clear explanation of its deadline. **NS-CONN-2026 §2.1** governs no-additional-fare rebooking. Neither the presence nor the absence of available seats determines whether a hotel benefit is owed, although the next practical departure may determine whether an overnight stay is necessary.

### 2.2 Basic assistance
Staff should explain where to receive schedule updates, how to preserve receipts, and how to seek accessible assistance. These are operational services and not a promise of cash delay compensation. When facts are incomplete, record which investigation or approval is pending rather than issuing a categorical denial.

## 3. Meals and extended waiting
### 3.1 Meal commitment
When a disruption classified as airline-controlled forces a passenger to wait **three consecutive hours or more** beyond the originally scheduled onward departure at the recovery airport, Northstar offers one meal voucher per affected meal period under its fictional customer-care commitment. This threshold is an internal Northstar rule; it is not presented as a universal federal requirement.

### 3.2 Exclusions and timing
A weather-only or external-ATC delay does not qualify under §3.1, though staff may provide a discretionary voucher that must be labeled `COURTESY`, not `ENTITLEMENT`. Do not double-count waiting time when two successive offers replace each other. When the cause remains `UNKNOWN`, return `NEEDS_REVIEW` for meal eligibility and identify the pending cause record.

## 4. Overnight accommodation
### 4.1 Primary eligibility
Northstar provides an approved hotel accommodation when **all** of these facts hold: the traveler has a valid Northstar disrupted itinerary; the controlling disruption is airline-controlled under §1.2; practical onward travel requires an overnight wait at the affected airport; and the passenger is away from their home metropolitan area under §1.2. This is a conjunctive rule, not four alternative reasons to provide a hotel.

### 4.2 What counts as overnight
An overnight wait exists when no reasonable onward Northstar option can be completed without remaining at the recovery station into the following calendar day, based on the documented available-flight snapshot and boarding constraints. A late-night flight may still avoid an overnight stay if it is operationally feasible. Do not infer overnight eligibility solely from a calendar date change in a passenger's device timezone.

### 4.3 Home-city restriction
A passenger whose verified home metro area includes the disrupted overnight station is excluded from the standard hotel commitment, even if the trip began elsewhere. Home-city status is an itinerary fact, not a proxy for citizenship, nationality, or billing country. If residence is missing, record `NEEDS_REVIEW` rather than guessing from airport proximity.

### 4.4 Uncontrollable and unresolved causes
Weather and external air-traffic-control events do not qualify under Northstar's routine hotel commitment. When the final cause is `UNKNOWN`, `MIXED_PENDING`, or under investigation, eligibility remains `NEEDS_REVIEW`. A preliminary gate announcement does not replace the investigation's final classification. For mixed causes, consult **NS-CAUSE-2026 §3.4** for the documented controlling cause; do not assume every occurrence of weather automatically excludes all assistance.

### 4.5 Crew-related disruption
A **finalized `CREW_OPERATIONAL` cause is included** among airline-controlled disruptions effective 2026-01-01. The same criteria for overnight necessity, residence, and approval apply. This inclusion is part of the current Northstar commitment and is relevant to version-sensitive historical inquiries.

### 4.6 Authorization and self-booking
Northstar generally issues accommodation through an approved hotel voucher under **SOP-HOTEL §3**. A passenger who books independently must obtain written authorization identifying the maximum reimbursable rate and approved dates; an unrelated agent's verbal suggestion is not adequate proof. An eligible passenger's benefit determination and whether a particular self-booked hotel expense is reimbursable are two distinct decisions.

### 4.7 Evidence precedence and a changing cause investigation
The controlling cause used for benefit eligibility is the latest *approved* investigation classification, not the most recent free-text comment. If a gate notice initially calls a late arrival weather-related but an authorized investigation later finalizes a mechanical failure, record both observations and the transition between them. The decision should identify the final classification record and its approval timestamp. If an unapproved draft appears later than the approved finding, do not allow it to silently reverse eligibility. Staff may offer courtesy assistance during an unresolved case, but must keep discretionary services distinct from a confirmed entitlement. Consult **NS-CAUSE-2026 §§3.2–3.4** for mixed and evolving investigations.

### 4.8 Distinguish eligibility from fulfillment
An `ELIGIBLE` hotel decision means the traveler satisfies the airline's stated accommodation conditions. It does not certify that the agent has booked a room, that a specific property is available, or that a receipt has been accepted for reimbursement. Fulfillment has separate states: `NOT_REQUESTED`, `SEARCHING`, `VOUCHER_AUTHORIZED`, `VOUCHER_ISSUED`, `RECEIPT_PENDING`, and `CLOSED`. A fully booked partner hotel may create a fulfillment exception, not a retroactive denial of the underlying eligibility. The fulfillment team should document an alternative approved accommodation or escalate capacity problems under **SOP-HOTEL §3**, while giving the customer accurate information about what has and has not been arranged.

### 4.9 Residence and station interpretation
For this fictional policy, home metro refers to the passenger's verified metropolitan area, not necessarily the airport code on the first segment. A traveler may be connecting through an airport near their residence after beginning a trip elsewhere; in that case the home-city restriction may still apply. Conversely, a traveler who originally departed from Boston but now resides elsewhere is not automatically local to Boston. Billing address, payment card location, nationality, and telephone area code are not appropriate substitutes for a verified home-metro field. If sources disagree, set the location condition to `UNRESOLVED` and request authorized verification rather than choosing an arbitrary address. The answer should state that the residence requirement, rather than the mechanical cause, is the unresolved eligibility gate.

### 4.10 Late departures versus genuine overnight necessity
A scheduled departure just after midnight does not invariably require a hotel. Agents should look at realistic boarding and transit constraints and whether continuing travel requires remaining at the affected airport into a following day. A flight that remains boardable without an extended overnight wait may not satisfy §4.2. Likewise, a nominally same-day rebooking can still be impractical if the passenger cannot reach the departure airport or has no viable connection. The operational record must explain the chosen overnight determination, citing the offer and disruption timestamps. This is why the hotel policy cannot be applied using only a delay-duration number.

### 4.11 Borderline examples for review
| Situation | Correct handling | Evidence that matters |
|---|---|---|
| Mechanical failure, next-day onward flight, verified out-of-town traveler | Evaluate as eligible under §4.1 | Final cause, next feasible offer, home metro |
| Crew operational shortage, same itinerary, 2026 disruption | Apply the current crew-inclusion rule in §4.5 | Effective date and approved cause |
| Weather initially reported, final mechanical classification approved | Use approved final classification | Versioned investigation record |
| Cause still `MIXED_PENDING` despite a hotel request | Return `NEEDS_REVIEW` for entitlement | Current investigation state |
| Eligible traveler self-books without written rate authorization | Separate eligibility from expense reimbursement | Authorization and receipt record |
| Hotel is unavailable in approved inventory | Retain eligibility; escalate fulfillment | Hotel capacity / voucher audit |

These examples are training interpretations of Northstar's fictional commitment. They are not a comprehensive replacement for §4.1–§4.6, and they do not establish federal refund rights. The answer generator must cite the actual controlling eligibility clauses rather than treating this table as an independent source of authority.

## 5. Assistance and evidence table
| Classification | Overnight at recovery airport | Away from home | Standard hotel result | Reference |
|---|---|---|---|---|
| `MECHANICAL` | Yes | Yes | Eligible, subject to approved inventory | §4.1 |
| `CREW_OPERATIONAL` | Yes | Yes | Eligible under 2026 rule | §4.5 |
| `WEATHER` | Yes | Yes | Not eligible under airline commitment | §4.4 |
| `AIRLINE_OPERATIONS` | No | Yes | Not eligible; no overnight necessity | §4.2 |
| `MECHANICAL` | Yes | No | Not eligible; home-city restriction | §4.3 |
| `UNKNOWN` | Yes | Yes | Needs review pending classification | §4.4 |

### 5.1 Accessibility and exceptional assistance
Agents must offer a trained human-review path for accessibility accommodations or safety needs that don't fit the standard voucher process. The simulator should not generate a legal conclusion from a generic policy paragraph when the case requires specialized handling.

### 5.2 Documentation
Record the claim ID, final cause source and revision, home metro indicator, available onward schedule, overnight determination, voucher authorization status, and citations. Preserve the answer as `ELIGIBLE`, `NOT_ELIGIBLE`, `NEEDS_REVIEW`, or `OUT_OF_SCOPE`. Never store "yes" without explaining which conditions were satisfied.

## 6. Cross-references and precedence
Use **NS-CAUSE-2026 §§2–3** to establish control and **NS-CONN-2026 §2** to establish protected rebooking. Use **SOP-HOTEL §§2–5** to issue approved vouchers. Refund eligibility is independently controlled by **NS-REF-2026 §3** and applicable DOT rules. Historical cases, including records governed by a 2025 policy, are descriptive precedent rather than current entitlement authority.
