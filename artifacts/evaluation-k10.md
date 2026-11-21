# Policy Q&A evaluation

Namespace: `policy-qa-recursive-v1` · Candidates per search: **10**
Reference date: 2026-11-20 · Questions: 15 · Service errors: 0

- Candidate pool recall: Not recorded
- Recall@5: **54.4%**
- Final context recall: **77.8%**
- Answer checks: **93.3%**

Recall uses the listed gold sections. Accepted equivalent clauses may also support an answer. Section IDs alone do not prove that a complete clause was provided.

| Question | Pool recall | Recall@5 | Context recall | Answer check |
|---|---:|---:|---:|---|
| POL-01: My first flight was delayed by bad weather and I missed my connection. Both flights were on one Northstar ticket. Will you put me on another flight for free? | Not recorded | 100% | 100% | PASS |
| POL-02: I got a text offering me another flight. Does that mean I'm booked? | Not recorded | 0% | 100% | PASS |
| POL-03: When does Northstar pay for a hotel if I'm stuck overnight? | Not recorded | 100% | 100% | PASS |
| POL-04: I'm stuck overnight because of bad weather. Will Northstar pay for my hotel? | Not recorded | 0% | 100% | PASS |
| POL-05: The airline says a crew scheduling problem made me miss my connection. I'm stuck overnight away from home. Can I get a hotel? | Not recorded | 0% | 0% | PASS |
| POL-06: The new flight gets me to my destination three hours late. Can I get a refund if I turn it down? | Not recorded | 50% | 100% | PASS |
| POL-07: I took the replacement flight, but I arrived five hours late. Can I still get a full refund? | Not recorded | 100% | 100% | PASS |
| POL-08: The gate agent said weather, but the final investigation says it was a mechanical problem. Which explanation counts? | Not recorded | 50% | 50% | PASS |
| POL-09: My flights were booked on two separate tickets. Do I still get a free connection rebooking if the first flight is late? | Not recorded | 50% | 100% | PASS |
| POL-10: I'm stranded overnight at the airport in the city where I live. Will Northstar cover a room? | Not recorded | 0% | 50% | PASS |
| POL-11: Can I book a hotel myself and send Northstar the receipt? | Not recorded | 100% | 100% | PASS |
| POL-12: The agent says all the partner hotels are full. Does that mean I'm not eligible for a hotel anymore? | Not recorded | 100% | 100% | PASS |
| POL-13: Nobody has confirmed why my flight was delayed. Can I count on Northstar paying for a hotel? | Not recorded | 0% | 0% | PASS |
| POL-14: I missed my connection. Does that automatically mean I get my money back? | Not recorded | 67% | 67% | PASS |
| POL-15: I had a crew scheduling delay last year and had to stay overnight away from home. Would Northstar have paid for a hotel? | Not recorded | 100% | 100% | FAIL |

## Questions

Expand a question to inspect its answer and gaps.

<details><summary>POL-01: My first flight was delayed by bad weather and I missed my connection. Both flights were on one Northstar ticket. Will you put me on another flight for free?</summary>

My first flight was delayed by bad weather and I missed my connection. Both flights were on one Northstar ticket. Will you put me on another flight for free?

**Missing gold sections in context:** None
**Missing expected information:** None

Under the current policy (NS-CONN-2026, v2.0, effective 2026-01-01), yes in principle — weather does not disqualify you. For a verified protected missed connection caused by a preceding Northstar segment, Northstar rebooks you to the earliest available Northstar-operated itinerary to your original ticketed destination at no additional fare, and this applies to both airline-controllable and uncontrollable (e.g., weather) disruptions. Conditions: at least two domestic Northstar-operated legs on the same ticket sold as a continuous itinerary (codeshare, interline, separate-ticket and international itineraries go to a specialist), and the connection must actually be verified as missed against the onward gate's boarding close. The commitment is to an eligible rebooking process, not a specific flight or departure time; seats must be confirmed. Separately, weather-only delays are excluded from standard meal vouchers, and hotels require an airline-controlled cause. Refund rights (e.g., a 3-hour final-destination arrival change) are assessed separately.

**Citations:** NS-CONN-2026#2.1, NS-CONN-2026#1.1, NS-CONN-2026#1.2, NS-CARE-2026#3.2, NS-CARE-2026#4.1, NS-REF-2026#3.2

</details>

<details><summary>POL-02: I got a text offering me another flight. Does that mean I&#x27;m booked?</summary>

I got a text offering me another flight. Does that mean I'm booked?

**Missing gold sections in context:** None
**Missing expected information:** None

No — under the current policy (effective 2026-01-01), a text proposing an alternate flight is an offer, not a confirmed booking. Offers are tracked separately as OFFERED, ACCEPTED, DECLINED, or EXPIRED, and "OFFERED" without a response is not the same as "ACCEPTED." Staff must never represent an unavailable seat as booked, and any hold on an alternative flight must carry an expiration time and cannot silently count as your acceptance. Even accepting doesn't mean you flew it — ACCEPTED and FLOWN stay distinct. Because gate, phone and app channels can show different snapshots, you're entitled to be told which offer is currently authoritative, whether an active ticket exists, and what response is needed. You may also ask for another feasible routing, and if a cancellation or significant change applies, a refund option must be explained rather than treating rebooking as settled.

**Citations:** NS-CONN-2026#2.2, NS-CONN-2026#2.3, NS-CONN-2026#2.6, NS-CONN-2026#2.8, NS-REF-2026#2.1, NS-REF-2026#2.2, NS-REF-2026#3.3

</details>

<details><summary>POL-03: When does Northstar pay for a hotel if I&#x27;m stuck overnight?</summary>

When does Northstar pay for a hotel if I'm stuck overnight?

**Missing gold sections in context:** None
**Missing expected information:** None

Under the current policy (NS-CARE-2026, v2.1, effective 2026-01-01), a hotel is provided only when all four conditions hold together: (1) you hold a valid Northstar disrupted itinerary; (2) the controlling disruption is airline-controlled (§1.2); (3) practical onward travel requires an overnight wait at the affected airport; and (4) you are away from your home metropolitan area. These are cumulative, not alternatives. An "overnight wait" means no reasonable onward Northstar option can be completed without staying at the recovery station into the next calendar day — a feasible late-night flight does not count, and neither does a mere timezone date change. If your home metro area includes the disrupted station, you are excluded. Weather and external air-traffic-control events do not qualify for the routine hotel commitment, and if the cause is unknown, mixed or under investigation, eligibility stays in review pending the final classification.

**Citations:** NS-CARE-2026#4.1, NS-CARE-2026#4.2, NS-CARE-2026#4.3, NS-CARE-2026#4.4

</details>

<details><summary>POL-04: I&#x27;m stuck overnight because of bad weather. Will Northstar pay for my hotel?</summary>

I'm stuck overnight because of bad weather. Will Northstar pay for my hotel?

**Missing gold sections in context:** None
**Missing expected information:** None

Under the current policy (NS-CARE-2026, v2.1, effective 2026-01-01), Northstar's overnight hotel commitment is voluntary and applies only when all conditions in §4.1 hold: a valid disrupted Northstar itinerary, an airline-controlled controlling cause (mechanical, airline operations, and since 2026 also finalized crew-operational), a genuine overnight wait at the affected airport, and the passenger being away from their home metro area. Weather and external air-traffic-control events do not qualify for the routine hotel commitment, so a purely weather-caused overnight is normally not paid for by Northstar. Staff may still help you find local hotels, and any assistance given is goodwill/courtesy rather than an entitlement. Two caveats: if the cause is mixed, unknown or still under investigation, eligibility is held as NEEDS_REVIEW pending the final documented controlling cause (see NS-CAUSE-2026 §3.4), and any self-booked room needs prior written authorization to be reimbursable.

**Citations:** NS-CARE-2026#1, NS-CARE-2026#4.1, NS-CARE-2026#4.2, NS-CARE-2026#4.4, NS-CARE-2026#4.5, NS-CARE-2026#4.6, NS-CARE-2026#3.2

</details>

<details><summary>POL-05: The airline says a crew scheduling problem made me miss my connection. I&#x27;m stuck overnight away from home. Can I get a hotel?</summary>

The airline says a crew scheduling problem made me miss my connection. I'm stuck overnight away from home. Can I get a hotel?

**Missing gold sections in context:** NS-CARE-2026#4.5
**Missing expected information:** None

Under the current policy (NS-CARE-2026, effective 2026-01-01), a crew scheduling event is treated as an airline-controlled disruption: `CREW_OPERATIONAL` is listed alongside `MECHANICAL` and `AIRLINE_OPERATIONS` as a controllable cause, so it can qualify for a hotel — unlike the 2025 edition, which excluded crew causes from the routine overnight commitment.

Eligibility is conjunctive: (1) a valid Northstar disrupted itinerary; (2) the final approved controlling cause is airline-controlled; (3) practical onward travel truly requires waiting at the recovery airport into the next calendar day (a feasible late-night flight can defeat this); and (4) you are away from your home metropolitan area. Hotel provision is also subject to approved/participating inventory and authorized issuance.

The cause must come from the finalized classification record, not an informal comment; if it is still `UNKNOWN`, the hotel decision is held for review. I cannot confirm your specific case or arrange a room.

**Citations:** NS-CARE-2026#1.2, NS-CARE-2026#4.1, NS-CARE-2026#4.2, NS-CARE-2026#4.3, NS-CARE-2026#5, NS-CARE-2025#3.2, NS-CARE-2025#3.5, NS-CONN-2026#3.3

</details>

<details><summary>POL-06: The new flight gets me to my destination three hours late. Can I get a refund if I turn it down?</summary>

The new flight gets me to my destination three hours late. Can I get a refund if I turn it down?

**Missing gold sections in context:** None
**Missing expected information:** None

Under the current refund policy (NS-REF-2026 v2.0, effective 2026-01-01), yes in principle. A domestic itinerary scheduled to arrive at your **final ticketed destination** at least three hours later than originally scheduled meets Northstar's significant-change threshold, so a three-hour-later arrival qualifies. Where a domestic itinerary is canceled or significantly changed and you do not accept the changed itinerary, replacement flight, credit, or other offered compensation, the applicable framework may require a refund; declining an eligible rebooking does not forfeit that refund right, and the refund option should be explained rather than treating rebooking as settled. Two cautions: the three hours must be measured at the final destination (in UTC), not on an inbound leg; and if you actually fly the replacement, a full refund generally does not follow under the significant-change remedy. Your decision should be recorded as DECLINED rather than left unanswered.

**Citations:** NS-REF-2026#3.2, NS-REF-2026#2.2, NS-REF-2026#3.5, NS-REF-2026#3.4, NS-REF-2026#3.3, NS-CONN-2026#2.3

</details>

<details><summary>POL-07: I took the replacement flight, but I arrived five hours late. Can I still get a full refund?</summary>

I took the replacement flight, but I arrived five hours late. Can I still get a full refund?

**Missing gold sections in context:** None
**Missing expected information:** None

Under the current refund policy (NS-REF-2026, v2.0, effective 2026-01-01), the answer is generally no. A passenger who actually flew the significantly delayed or replacement flight to the destination cannot obtain a full refund of transportation already used under the significant-change remedy alone — the fact that arrival was late (even by five hours, above the three-hour domestic arrival-change threshold) does not by itself produce a full ticket refund once travel is completed. The policy treats "accepted," "flown," and "partially used" as distinct states, and the published example confirms: passenger accepts rebooking and flies = no full ticket refund under change alone. Separate, partial remedies may still apply and are assessed on their own evidence and rules: an involuntary cabin downgrade, unused portions/coupons of the itinerary, and baggage or optional-service charges. Any amount would be computed from ticket-value accounting records, not assumed.

**Citations:** NS-REF-2026#3.4, NS-REF-2026#3.7, NS-REF-2026#3.2, NS-REF-2026#5, NS-REF-2026#4.1

</details>

<details><summary>POL-08: The gate agent said weather, but the final investigation says it was a mechanical problem. Which explanation counts?</summary>

The gate agent said weather, but the final investigation says it was a mechanical problem. Which explanation counts?

**Missing gold sections in context:** NS-CAUSE-2026#3.3
**Missing expected information:** None

Under the current 2026 rules (as of 2026-11-20), the approved final investigation classification controls, not the gate agent's remark. A first airport or dispatcher report is `PROVISIONAL` and preliminary — it explains why an investigation is open, and an announcement containing the word "weather" is not conclusive. The controlling cause for benefit eligibility is the latest *approved* investigation classification (lifecycle `REPORTED → INVESTIGATING → PROPOSED → FINAL_APPROVED`), so once the mechanical cause is finalised and approved, it supersedes the earlier weather label. Two cautions: a merely `PROPOSED` mechanical cause cannot automatically override an approved weather determination, and if the case is still `MIXED_PENDING` or unresolved, passenger-care entitlement stays `NEEDS_REVIEW`. Both observations and the transition between them must be preserved, with the approval timestamp recorded; the earlier assertion is not deleted. Any courtesy assistance given while the case was open stays distinct from a confirmed entitlement.

**Citations:** NS-CARE-2026#4.7, NS-CARE-2026#4.4, NS-CARE-2026#4.11, NS-CAUSE-2026#3.1, NS-CAUSE-2026#3.8, NS-CAUSE-2026#3.6, NS-CAUSE-2026#2.1

</details>

<details><summary>POL-09: My flights were booked on two separate tickets. Do I still get a free connection rebooking if the first flight is late?</summary>

My flights were booked on two separate tickets. Do I still get a free connection rebooking if the first flight is late?

**Missing gold sections in context:** None
**Missing expected information:** None

Under the current Connection Protection and Involuntary Rebooking Standard (NS-CONN-2026 v2.0, effective 2026-01-01), the no-additional-fare connection rebooking in §2.1 applies only to a *protected itinerary*: at least two domestic Northstar-operated legs issued on the **same ticket and reservation**, sold as a continuous connection. A shared booking reference is not enough — both coupons must appear under the same ticket record. Separate-ticket itineraries (like codeshare, interline and international ones) are expressly outside this pilot standard and must be referred to a specialist; the policy's worked examples list "separate tickets purchased independently" as out of scope, with hotel entitlement also undetermined. So the free connection rebooking is not guaranteed for two separate tickets; a specialist decides what, if anything, can be offered. Separately, any refund question is assessed under NS-REF-2026 §3, and overnight assistance under NS-CARE-2026 §4.

**Citations:** NS-CONN-2026#1.1, NS-CONN-2026#2.1, NS-CONN-2026#6, NS-CONN-2026#7

</details>

<details><summary>POL-10: I&#x27;m stranded overnight at the airport in the city where I live. Will Northstar cover a room?</summary>

I'm stranded overnight at the airport in the city where I live. Will Northstar cover a room?

**Missing gold sections in context:** NS-CARE-2026#4.9
**Missing expected information:** None

Under the current policy (NS-CARE-2026, v2.1, effective 2026-01-01), Northstar's standard overnight hotel commitment requires **all** of four facts: a valid disrupted Northstar itinerary; an airline-controlled cause (`MECHANICAL`, `CREW_OPERATIONAL`, or `AIRLINE_OPERATIONS`); a genuine overnight wait at the affected airport; and the passenger being away from their verified home metropolitan area. These are conjunctive, not alternatives. Section 4.3 states expressly that a passenger whose verified home metro area includes the disrupted overnight station is excluded from the standard hotel commitment, even if the trip began elsewhere. The assistance table confirms this: a mechanical overnight with "away from home = No" is "Not eligible; home-city restriction." So if the airport is in your home metro area, a room is not a routine entitlement, though staff may offer information or discretionary/goodwill help, which must not be described as an entitlement. Meal assistance is assessed separately under §3.1.

**Citations:** NS-CARE-2026#4.1, NS-CARE-2026#4.3, NS-CARE-2026#1.2, NS-CARE-2026#5, NS-CARE-2026#3.1

</details>

<details><summary>POL-11: Can I book a hotel myself and send Northstar the receipt?</summary>

Can I book a hotel myself and send Northstar the receipt?

**Missing gold sections in context:** None
**Missing expected information:** None

Under the current policy (NS-CARE-2026, v2.1, effective 2026-01-01), Northstar normally provides accommodation through an approved hotel voucher rather than reimbursement of a self-booked room. If you book independently, you must first obtain **written authorization** that identifies the maximum reimbursable rate and the approved dates; a verbal suggestion from an unrelated agent is not adequate proof. Note two separate decisions: whether you are eligible for accommodation at all (§4.1 — valid disrupted Northstar itinerary, airline-controlled cause, overnight wait required at the affected airport, and away from your home metro area), and whether a particular self-booked expense is reimbursable. An eligibility determination does not certify that a room was booked or that a receipt has been accepted; fulfillment moves through states such as VOUCHER_AUTHORIZED, VOUCHER_ISSUED and RECEIPT_PENDING. Self-booking without written rate authorization is flagged for review.

**Citations:** NS-CARE-2026#4.6, NS-CARE-2026#4.1, NS-CARE-2026#4.8, NS-CARE-2026#4.11

</details>

<details><summary>POL-12: The agent says all the partner hotels are full. Does that mean I&#x27;m not eligible for a hotel anymore?</summary>

The agent says all the partner hotels are full. Does that mean I'm not eligible for a hotel anymore?

**Missing gold sections in context:** None
**Missing expected information:** None

No. Under the current policy (NS-CARE-2026, effective 2026-01-01), eligibility and fulfillment are separate determinations. Eligibility depends on the §4.1 conjunctive test: a valid disrupted Northstar itinerary, an airline-controlled controlling cause, a genuine overnight wait required at the affected airport, and being away from your home metro area. Whether a partner property actually has rooms is a fulfillment question, tracked through states such as NOT_REQUESTED, SEARCHING, VOUCHER_AUTHORIZED, VOUCHER_ISSUED, RECEIPT_PENDING and CLOSED. A fully booked partner hotel creates a fulfillment exception, not a retroactive denial of eligibility. The published guidance is that staff should document an alternative approved accommodation or escalate the capacity problem to an authorized passenger-care agent, while telling you accurately what has and has not been arranged. If you book independently, you need written authorization specifying the maximum reimbursable rate and approved dates; a verbal suggestion is not sufficient proof.

**Citations:** NS-CARE-2026#4.8, NS-CARE-2026#4.1, NS-CARE-2026#4.11, NS-CARE-2026#4.6

</details>

<details><summary>POL-13: Nobody has confirmed why my flight was delayed. Can I count on Northstar paying for a hotel?</summary>

Nobody has confirmed why my flight was delayed. Can I count on Northstar paying for a hotel?

**Missing gold sections in context:** NS-CARE-2026#4.4, NS-CAUSE-2026#3.2
**Missing expected information:** None

Not yet — under the current 2026 edition, a hotel is not automatic. NS-CARE-2026 §4.1 is conjunctive: Northstar provides an approved hotel only when all four facts hold — a valid disrupted Northstar itinerary; a controlling disruption classified as airline-controlled; practical onward travel requiring an overnight wait at the affected airport; and the passenger being away from their home metropolitan area. Weather or external-ATC causes fall outside the standard benefit, and agents may give only clearly labelled courtesy assistance (§3.2). While the cause is still unconfirmed, the case stays in review rather than defaulting either way; the cause label must come from an approved operations record, and preliminary gate remarks or a display showing "DELAYED" without a cause don't settle it (NS-CAUSE-2026 §3.6). Overnight necessity is judged on realistic boarding/transit constraints, not delay length alone (§4.2, §4.10). So no, you can't count on it yet.

**Citations:** NS-CARE-2026#4.1, NS-CARE-2026#3.2, NS-CARE-2026#4.2, NS-CARE-2026#4.10, NS-CAUSE-2026#3.6, NS-CARE-2026#1

</details>

<details><summary>POL-14: I missed my connection. Does that automatically mean I get my money back?</summary>

I missed my connection. Does that automatically mean I get my money back?

**Missing gold sections in context:** NS-REF-2026#2.2
**Missing expected information:** None

No. Under the current policies (effective 2026-01-01), a missed connection by itself is not a refund trigger. A missed connection is not treated as a canceled ticket or automatic cash compensation (NS-CONN-2026 §1), and the statement "I missed my connection" alone does not establish either a three-hour change in arrival at your final ticketed destination or a decision to decline onward transport (NS-REF-2026 §1.1). What you do get, for a verified protected missed connection caused by a preceding Northstar segment, is rebooking to the earliest available Northstar itinerary to your ticketed destination at no additional fare, regardless of whether the cause was mechanical or weather (NS-CONN-2026 §2.1). A refund pathway opens only if the replacement itinerary involves a significant change — measured at the final destination, not the delayed leg — or another qualifying change, and you decline the onward travel (NS-REF-2026 §§3.5, 3.8, 5). If you fly the rebooking, no full ticket refund arises from the change alone; refunds of unused portions are calculated from ticket accounting records (NS-REF-2026 §§5, 4.1).

**Citations:** NS-CONN-2026#1, NS-CONN-2026#2.1, NS-REF-2026#1.1, NS-REF-2026#3.5, NS-REF-2026#3.8, NS-REF-2026#5, NS-REF-2026#4.1

</details>

<details><summary>POL-15: I had a crew scheduling delay last year and had to stay overnight away from home. Would Northstar have paid for a hotel?</summary>

I had a crew scheduling delay last year and had to stay overnight away from home. Would Northstar have paid for a hotel?

**Missing gold sections in context:** None
**Review note:** Phrase-match false negative: the answer correctly says the 2025 policy did not include crew-caused overnights, but the expected phrase list does not include did not include or fell outside.
**Missing expected information:** historical exclusion

For travel in 2025 ("last year" relative to 20 Nov 2026), the 2025 Passenger Care edition governs, and it did **not** include crew-caused overnights in the routine hotel commitment. A disruption whose final approved primary cause was `CREW_OPERATIONAL` fell outside Northstar's standard overnight-hotel promise, even when operationally attributable to Northstar. Agents could ask a duty manager for discretionary assistance, or escalate exceptional accessibility/safety needs, but any such booking was a documented courtesy, not an entitlement — so another passenger's hotel in the same situation doesn't prove eligibility. The standard 2025 benefit covered only verified `MECHANICAL` or `AIRLINE_OPERATIONS` disruptions with an unavoidable overnight away from the home metro area. Note the change: from 1 January 2026, crew-operational disruptions are eligible if the overnight and away-from-home conditions are met. One caveat: the 2025 edition is still labelled "current" in its metadata despite the 2026 edition being in force.

**Citations:** NS-CARE-2025#3.2, NS-CARE-2025#3.5, NS-CARE-2025#3.1, NS-CARE-2025#3.4, NS-CARE-2026#4.1, NS-CARE-2026#5, NS-CARE-2026#1

</details>
