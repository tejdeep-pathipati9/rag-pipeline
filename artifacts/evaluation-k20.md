# Policy Q&A evaluation

Namespace: `policy-qa-recursive-v1` · Candidates per search: **20**
Reference date: 2026-11-20 · Questions: 15 · Service errors: 0

- Candidate pool recall: **96.7%**
- Recall@5: **54.4%**
- Final context recall: **96.7%**
- Answer checks: **100.0%**

Recall uses the listed gold sections. Accepted equivalent clauses may also support an answer. Section IDs alone do not prove that a complete clause was provided.

| Question | Pool recall | Recall@5 | Context recall | Answer check |
|---|---:|---:|---:|---|
| POL-01: My first flight was delayed by bad weather and I missed my connection. Both flights were on one Northstar ticket. Will you put me on another flight for free? | 100% | 100% | 100% | PASS |
| POL-02: I got a text offering me another flight. Does that mean I'm booked? | 100% | 0% | 100% | PASS |
| POL-03: When does Northstar pay for a hotel if I'm stuck overnight? | 100% | 100% | 100% | PASS |
| POL-04: I'm stuck overnight because of bad weather. Will Northstar pay for my hotel? | 100% | 0% | 100% | PASS |
| POL-05: The airline says a crew scheduling problem made me miss my connection. I'm stuck overnight away from home. Can I get a hotel? | 100% | 0% | 100% | PASS |
| POL-06: The new flight gets me to my destination three hours late. Can I get a refund if I turn it down? | 100% | 50% | 100% | PASS |
| POL-07: I took the replacement flight, but I arrived five hours late. Can I still get a full refund? | 100% | 100% | 100% | PASS |
| POL-08: The gate agent said weather, but the final investigation says it was a mechanical problem. Which explanation counts? | 100% | 50% | 100% | PASS |
| POL-09: My flights were booked on two separate tickets. Do I still get a free connection rebooking if the first flight is late? | 100% | 50% | 100% | PASS |
| POL-10: I'm stranded overnight at the airport in the city where I live. Will Northstar cover a room? | 100% | 0% | 100% | PASS |
| POL-11: Can I book a hotel myself and send Northstar the receipt? | 100% | 100% | 100% | PASS |
| POL-12: The agent says all the partner hotels are full. Does that mean I'm not eligible for a hotel anymore? | 100% | 100% | 100% | PASS |
| POL-13: Nobody has confirmed why my flight was delayed. Can I count on Northstar paying for a hotel? | 50% | 0% | 50% | PASS |
| POL-14: I missed my connection. Does that automatically mean I get my money back? | 100% | 67% | 100% | PASS |
| POL-15: I had a crew scheduling delay last year and had to stay overnight away from home. Would Northstar have paid for a hotel? | 100% | 100% | 100% | PASS |

## Questions

Expand a question to inspect its answer and gaps.

<details><summary>POL-01: My first flight was delayed by bad weather and I missed my connection. Both flights were on one Northstar ticket. Will you put me on another flight for free?</summary>

My first flight was delayed by bad weather and I missed my connection. Both flights were on one Northstar ticket. Will you put me on another flight for free?

**Missing gold sections in context:** None

**Missing expected information:** None

Yes — under the current standard (NS-CONN-2026 v2.0, effective 2026-01-01), a missed connection does not have to be the airline's fault. For a verified protected missed connection caused by a preceding Northstar segment disruption, you may be rebooked to the earliest available Northstar-operated itinerary to your original ticketed destination at no additional fare; this applies to both controllable and uncontrollable causes, including weather. "Protected" means at least two domestic Northstar-operated legs on the same ticket sold as one continuous itinerary (codeshare/interline/separate-ticket/international cases go to a specialist), and agents verify from operational timestamps that the connection was genuinely unreachable. The commitment is to an eligible rebooking process, not a specific flight or departure time, and seats must be confirmed. If the replacement itinerary is significantly changed, you may instead decline it and seek a refund under NS-REF-2026 §2.2. Weather-caused delays are excluded from standard meal and hotel benefits.

**Citations:** NS-CONN-2026#2.1, NS-CONN-2026#1.1, NS-CONN-2026#1.2, NS-CONN-2026#2.4, NS-REF-2026#2.1, NS-REF-2026#2.2, NS-CARE-2026#1.2, NS-CARE-2026#3.2

</details>

<details><summary>POL-02: I got a text offering me another flight. Does that mean I&#x27;m booked?</summary>

I got a text offering me another flight. Does that mean I'm booked?

**Missing gold sections in context:** None

**Review note:** The core answer is supported by current connection-policy clauses, but it unnecessarily also cites the 2025 care edition for a current question. Citation-ID validity does not check date applicability or claim-level support.

**Missing expected information:** None

Not by itself. Under Northstar's current policy (effective 2026-01-01), a proposed alternate flight is recorded as an *offer* until you accept it, and an unavailable seat must never be presented as booked. A hold on an alternative must carry an expiration time and does not silently count as acceptance. Offer states are tracked separately — CREATED, DELIVERED, VIEWED, ACCEPTED, DECLINED, EXPIRED and FLOWN — and staff may not infer your decision from an internal offer row; "OFFERED" is not "ACCEPTED," and acceptance is not the same as having flown. Connection protection promises an eligible rebooking process, not a particular flight or departure time. Agents should tell you whether there is an active ticket or only a proposal, and what response is needed. You may also ask for another feasible routing, and if a significant change triggers a refund right, the alternative cannot be presented as the only remedy.

**Citations:** NS-CONN-2026#2.1, NS-CONN-2026#2.2, NS-CONN-2026#2.3, NS-CONN-2026#2.6, NS-CONN-2026#2.8, NS-REF-2026#3.6, NS-REF-2026#3.3, NS-REF-2026#2.1, NS-REF-2026#2.2, NS-CARE-2025#2.1

</details>

<details><summary>POL-03: When does Northstar pay for a hotel if I&#x27;m stuck overnight?</summary>

When does Northstar pay for a hotel if I'm stuck overnight?

**Missing gold sections in context:** None

**Missing expected information:** None

Under the current policy (NS-CARE-2026, v2.1, effective 2026-01-01), Northstar provides an approved hotel only when all four conditions hold together: (1) you hold a valid Northstar disrupted itinerary; (2) the controlling disruption is airline-controlled; (3) practical onward travel genuinely requires an overnight wait at the affected airport; and (4) you are away from your home metropolitan area. These are cumulative, not alternatives.

"Overnight" means no reasonable onward Northstar option can be completed without staying into the next calendar day — a feasible late-night flight or a just-after-midnight departure doesn't automatically qualify. Crew-operational disruptions are included as airline-controlled since 2026. Weather and external air-traffic-control events are excluded; if the cause is unknown or pending, eligibility stays under review. Accommodation is normally issued as a voucher; self-booking requires prior written authorization of rate and dates to be reimbursable.

**Citations:** NS-CARE-2026#4.1, NS-CARE-2026#4.2, NS-CARE-2026#4.3, NS-CARE-2026#4.4, NS-CARE-2026#4.5, NS-CARE-2026#4.6, NS-CARE-2026#4.10, NS-CARE-2026#1.1

</details>

<details><summary>POL-04: I&#x27;m stuck overnight because of bad weather. Will Northstar pay for my hotel?</summary>

I'm stuck overnight because of bad weather. Will Northstar pay for my hotel?

**Missing gold sections in context:** None

**Missing expected information:** None

Under the current policy (NS-CARE-2026, v2.1, effective 2026-01-01), Northstar's hotel commitment applies only to airline-controlled disruptions — a final approved `MECHANICAL`, `CREW_OPERATIONAL`, or `AIRLINE_OPERATIONS` cause — plus a genuine overnight wait at the recovery airport and the passenger being away from their home metro area; all conditions must hold together. Weather and external ATC events are classified as uncontrollable and do not qualify for the routine hotel (or meal) benefit, so Northstar would not normally pay for your room. Staff may still help you find a hotel or offer discretionary assistance, but that is recorded as courtesy, not entitlement. Two caveats: if the final cause is still `UNKNOWN` or `MIXED_PENDING`, eligibility stays in review rather than being denied, and a mixed case turns on the documented controlling cause. No-additional-fare rebooking and any refund rights are assessed separately.

**Citations:** NS-CARE-2026#1.2, NS-CARE-2026#4.1, NS-CARE-2026#4.4, NS-CARE-2026#3.2, NS-CARE-2026#5, NS-REF-2026#2.1

</details>

<details><summary>POL-05: The airline says a crew scheduling problem made me miss my connection. I&#x27;m stuck overnight away from home. Can I get a hotel?</summary>

The airline says a crew scheduling problem made me miss my connection. I'm stuck overnight away from home. Can I get a hotel?

**Missing gold sections in context:** None

**Missing expected information:** None

Under the current 2026 policy, yes in principle — crew scheduling is now a qualifying cause. Effective 2026-01-01, a finalized `CREW_OPERATIONAL` cause (internal crew scheduling, reserve assignment or staffing) counts as an airline-controlled disruption, so it is included in the standard hotel commitment (NS-CARE-2026 §4.5; NS-CAUSE-2026 §2). Eligibility is conjunctive: you need a valid disrupted Northstar itinerary, an approved airline-controlled cause, a genuine overnight wait at the recovery airport (no feasible onward flight without staying into the next day), and you must be away from your home metro area (§4.1–§4.3). An informal remark that "crew scheduling" caused it isn't enough; the approved final classification controls, and a pending or mixed cause means the case is held for review (NS-CAUSE-2026 §3.4). Accommodation is normally issued as an approved hotel voucher; self-booking requires written rate authorization in advance (§4.6). Note this differed under the 2025 edition (NS-CARE-2025 §3.2).

**Citations:** NS-CARE-2026#4.5, NS-CARE-2026#4.1, NS-CARE-2026#4.2, NS-CARE-2026#4.3, NS-CARE-2026#4.6, NS-CARE-2026#5, NS-CAUSE-2026#2, NS-CAUSE-2026#3.4, NS-CARE-2025#3.2

</details>

<details><summary>POL-06: The new flight gets me to my destination three hours late. Can I get a refund if I turn it down?</summary>

The new flight gets me to my destination three hours late. Can I get a refund if I turn it down?

**Missing gold sections in context:** None

**Missing expected information:** None

Under the current refund policy (NS-REF-2026 v2.0, effective 2026-01-01), yes in principle. A replacement itinerary scheduled to arrive at your **final ticketed destination** at least three hours later than originally scheduled meets Northstar's domestic significant-change threshold. Where a domestic itinerary is canceled or significantly changed and you do not accept the changed itinerary, replacement flight, credit or other offered compensation, a refund may be required; declining an eligible rebooking does not forfeit that refund right, and the refund option should be explained rather than rebooking being treated as settled. Key conditions: the three hours must be measured at final destination (not just a late inbound leg), compared in UTC between the original ticket and the documented offer, and you must not travel on the substitute — a flown or partly used ticket is handled under unused-transportation/coupon rules, not a full change refund. Actual refund amounts depend on your ticket record.

**Citations:** NS-REF-2026#3.2, NS-REF-2026#2.2, NS-REF-2026#3.4, NS-REF-2026#3.5, NS-REF-2026#3.7, NS-REF-2026#1

</details>

<details><summary>POL-07: I took the replacement flight, but I arrived five hours late. Can I still get a full refund?</summary>

I took the replacement flight, but I arrived five hours late. Can I still get a full refund?

**Missing gold sections in context:** None

**Missing expected information:** None

Under the current refund policy (NS-REF-2026, effective 2026-01-01), the significant-change remedy is essentially a right to decline the replacement travel. Once you actually flew the delayed or replacement flight to your destination, a full refund of the ticket generally does not follow merely because you arrived late — even a long delay such as five hours. The policy's examples confirm this: a passenger who accepts rebooking and flies gets no full ticket refund under the change criterion alone. Other claims are assessed separately with their own evidence: an involuntary cabin downgrade, unused portions/coupons of the itinerary, baggage charges, or optional services you paid for but did not receive. If you had declined the replacement and the new itinerary arrived three or more hours later at your final destination, the refund pathway would have applied. This is fictional Northstar training policy, not a statement of your legal rights.

**Citations:** NS-REF-2026#3.4, NS-REF-2026#3.7, NS-REF-2026#5, NS-REF-2026#2.2, NS-REF-2026#3.2, NS-REF-2026#4.1

</details>

<details><summary>POL-08: The gate agent said weather, but the final investigation says it was a mechanical problem. Which explanation counts?</summary>

The gate agent said weather, but the final investigation says it was a mechanical problem. Which explanation counts?

**Missing gold sections in context:** None

**Missing expected information:** None

Under the current 2026 rules, the approved final investigation classification controls — not a gate agent's remark. A gate or dispatcher report is `PROVISIONAL`: useful for explaining why an investigation is open, but not a basis for granting or denying cause-dependent benefits, and a remark containing the word "weather" is not conclusive (NS-CAUSE-2026 §§2.1, 3.1). The cause lifecycle runs `REPORTED → INVESTIGATING → PROPOSED → FINAL_APPROVED`; benefits cite the latest valid final approval for the travel date, and a merely `PROPOSED` mechanical cause cannot override an approved weather determination (NS-CAUSE-2026 §3.8). So if the mechanical finding is final-approved, it governs; if it is still draft or `MIXED_PENDING`, eligibility stays `NEEDS_REVIEW` (NS-CARE-2026 §§4.4, 4.7, 4.11). Both observations and the transition must be preserved, not deleted (NS-CAUSE-2026 §3.6). Separately, refund rights under NS-REF-2026 §5 don't turn on whether the cause was weather or mechanical.

**Citations:** NS-CAUSE-2026#2.1, NS-CAUSE-2026#3.1, NS-CAUSE-2026#3.8, NS-CAUSE-2026#3.6, NS-CARE-2026#4.7, NS-CARE-2026#4.4, NS-CARE-2026#4.11, NS-REF-2026#5

</details>

<details><summary>POL-09: My flights were booked on two separate tickets. Do I still get a free connection rebooking if the first flight is late?</summary>

My flights were booked on two separate tickets. Do I still get a free connection rebooking if the first flight is late?

**Missing gold sections in context:** None

**Missing expected information:** None

Under the current Connection Protection and Involuntary Rebooking Standard (NS-CONN-2026, v2.0, effective 2026-01-01), the free (no-additional-fare) connection rebooking applies only to a *protected itinerary*: at least two domestic Northstar-operated legs issued on the **same ticket and reservation**, sold as a continuous itinerary. A shared booking reference is not enough — both coupons must appear under the same ticket record. Separate-ticket itineraries (as well as codeshare, interline and international ones) are expressly outside this pilot standard and must be referred to a specialist; the policy's example table lists "separate tickets purchased independently" as out of scope. So a late first flight on a separate ticket does not automatically entitle you to the §2.1 no-additional-fare rebooking. A specialist would review your case, and any refund question would be assessed separately under NS-REF-2026 §3. This is Northstar's fictional training policy, not a statement of legal rights.

**Citations:** NS-CONN-2026#1.1, NS-CONN-2026#2.1, NS-CONN-2026#6, NS-CONN-2026#7

</details>

<details><summary>POL-10: I&#x27;m stranded overnight at the airport in the city where I live. Will Northstar cover a room?</summary>

I'm stranded overnight at the airport in the city where I live. Will Northstar cover a room?

**Missing gold sections in context:** None

**Missing expected information:** None

Under the current policy (NS-CARE-2026, effective 2026-01-01), no — not as a standard entitlement. Hotel eligibility is conjunctive: you need a valid disrupted Northstar itinerary, an airline-controlled cause (MECHANICAL, CREW_OPERATIONAL or AIRLINE_OPERATIONS), a genuine overnight wait at the affected airport, and you must be away from your home metro area. A passenger whose verified home metropolitan area includes the disrupted overnight station is expressly excluded from the standard hotel commitment, even if the trip began elsewhere. The policy's own example table confirms: MECHANICAL + overnight + not away from home = not eligible (home-city restriction). If your residence isn't verified in the record, staff mark it NEEDS_REVIEW rather than guessing from airport proximity. Other care may still apply — e.g., a meal voucher after a 3+ hour airline-controlled wait, plus rebooking information. Any room beyond that would be discretionary goodwill, not an entitlement.

**Citations:** NS-CARE-2026#4.1, NS-CARE-2026#4.3, NS-CARE-2026#5, NS-CARE-2026#1.2, NS-CARE-2026#3.1

</details>

<details><summary>POL-11: Can I book a hotel myself and send Northstar the receipt?</summary>

Can I book a hotel myself and send Northstar the receipt?

**Missing gold sections in context:** None

**Missing expected information:** None

Under the current policy (NS-CARE-2026, v2.1, effective 2026-01-01), Northstar normally provides accommodation through an approved hotel voucher rather than reimbursing a hotel you choose yourself. If you book independently, you must first obtain written authorization that identifies the maximum reimbursable rate and the approved dates; an unrelated agent's verbal suggestion is not adequate proof. Simply submitting a receipt afterwards does not guarantee payment: being eligible for accommodation and whether a particular self-booked expense is reimbursable are two separate decisions. Eligibility itself requires all of §4.1's conditions (valid disrupted Northstar itinerary, airline-controlled cause, an operationally necessary overnight wait, and being away from your home metro area). Fulfillment is tracked separately (e.g., VOUCHER_AUTHORIZED, RECEIPT_PENDING), so an eligible decision does not certify a receipt has been accepted. Best practice: ask staff for a voucher, or get written rate authorization before booking.

**Citations:** NS-CARE-2026#4.6, NS-CARE-2026#4.1, NS-CARE-2026#4.8, NS-CARE-2026#4.11

</details>

<details><summary>POL-12: The agent says all the partner hotels are full. Does that mean I&#x27;m not eligible for a hotel anymore?</summary>

The agent says all the partner hotels are full. Does that mean I'm not eligible for a hotel anymore?

**Missing gold sections in context:** None

**Missing expected information:** None

No. Under the current policy (NS-CARE-2026, v2.1, effective 2026-01-01), eligibility and fulfillment are separate determinations. An `ELIGIBLE` hotel decision means you meet the airline's stated accommodation conditions (airline-controlled cause, genuine overnight necessity, away from your home metro area, proper authorization). It does not certify that a room has been booked or that a particular property is available. Fulfillment is tracked in its own states — NOT_REQUESTED, SEARCHING, VOUCHER_AUTHORIZED, VOUCHER_ISSUED, RECEIPT_PENDING, CLOSED. A fully booked partner hotel creates a fulfillment exception, not a retroactive denial of eligibility. The published handling is to retain eligibility and escalate the capacity problem: staff should document an alternative approved accommodation or escalate to an authorized passenger-care agent, while telling you accurately what has and has not been arranged. Note that self-booking reimbursement requires separate written authorization of the rate and dates.

**Citations:** NS-CARE-2026#4.8, NS-CARE-2026#4.11, NS-CARE-2026#4.1, NS-CARE-2026#4.6

</details>

<details><summary>POL-13: Nobody has confirmed why my flight was delayed. Can I count on Northstar paying for a hotel?</summary>

Nobody has confirmed why my flight was delayed. Can I count on Northstar paying for a hotel?

**Missing gold sections in context:** NS-CAUSE-2026#3.2

**Missing expected information:** None

Under the current policy (NS-CARE-2026, v2.1, effective 2026-01-01), a hotel is not automatic and cannot be promised while the cause is unconfirmed. Northstar provides an approved hotel only when all four conditions hold together: a valid disrupted Northstar itinerary; the controlling disruption is finally classified as airline-controlled (mechanical, airline operations, or — since 2026-01-01 — finalized crew-operational); practical onward travel requires an overnight wait at the affected airport; and you are away from your home metro area (§4.1, §4.5). Where the final cause is UNKNOWN, mixed/pending, or under investigation, eligibility stays NEEDS_REVIEW rather than approved or denied (§4.4); a provisional gate message is not the final classification (NS-CAUSE-2026 §3.1). Weather and external ATC events are excluded. Separately, no-additional-fare rebooking on a protected itinerary applies regardless of cause (NS-CONN-2026 §2.1). So: ask for the finalized cause determination; hotels are issued by voucher or prior written authorization (§4.6).

**Citations:** NS-CARE-2026#4.1, NS-CARE-2026#4.4, NS-CARE-2026#4.5, NS-CARE-2026#4.6, NS-CARE-2026#4.2, NS-CAUSE-2026#3.1, NS-CONN-2026#2.1, NS-CARE-2026#1

</details>

<details><summary>POL-14: I missed my connection. Does that automatically mean I get my money back?</summary>

I missed my connection. Does that automatically mean I get my money back?

**Missing gold sections in context:** None

**Missing expected information:** None

No. Under the current refund policy (NS-REF-2026 v2.0, effective 2026-01-01), a missed connection by itself is not a cancelled ticket and does not automatically create a refund right. Two separate things apply:

1) Rebooking: for a verified protected missed connection caused by a preceding Northstar segment disruption, you may be rebooked to the earliest available Northstar itinerary to your ticketed destination at no additional fare, whether the cause was mechanical or weather.

2) Refund: this arises where the itinerary is cancelled or significantly changed — measured by the change in scheduled arrival at your final ticketed destination (e.g. a three-hour domestic threshold, a different airport, an added connection) — and you decline the replacement travel. A late first leg alone doesn't prove a qualifying final-arrival change, and if you accept and fly the replacement, a full fare refund generally doesn't follow. Unused-coupon value is calculated separately.

**Citations:** NS-CONN-2026#1, NS-CONN-2026#2.1, NS-REF-2026#1.1, NS-REF-2026#2.2, NS-REF-2026#3.5, NS-REF-2026#3.7, NS-REF-2026#3.8, NS-REF-2026#4.1, NS-REF-2026#5

</details>

<details><summary>POL-15: I had a crew scheduling delay last year and had to stay overnight away from home. Would Northstar have paid for a hotel?</summary>

I had a crew scheduling delay last year and had to stay overnight away from home. Would Northstar have paid for a hotel?

**Missing gold sections in context:** None

**Missing expected information:** None

For a 2025 disruption ("last year" relative to 20 Nov 2026), the 2025 Passenger Care edition governs, and under it a crew-scheduling cause did not earn a hotel. Its standard overnight commitment covered only finally confirmed MECHANICAL or AIRLINE_OPERATIONS events where an overnight stay was unavoidable and the passenger was away from their home metro area; CREW_OPERATIONAL was expressly excluded from the routine commitment (§3.2, §5). Agents could ask a duty manager for discretionary help, and such courtesy bookings were logged separately from entitlement, so they don't prove eligibility (§3.5). Northstar's current 2026 policy does include finalized CREW_OPERATIONAL causes, but only for disruptions beginning 2026-01-01, so it doesn't apply retroactively. Note a metadata oddity: the 2025 edition is still labelled "current" although the 2026 edition is in force; if your travel date was actually in 2026, the newer rule would apply.

**Citations:** NS-CARE-2025#3.1, NS-CARE-2025#3.2, NS-CARE-2025#3.5, NS-CARE-2025#5, NS-CARE-2026#4.5, NS-CARE-2026#1

</details>
