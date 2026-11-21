# Policy Q&A evaluation

Namespace: `policy-qa-parent-child-200-40-v1` · Candidates per search: **20**
Reference date: 2026-11-20 · Questions: 15 · Service errors: 0

- Candidate pool recall: **93.3%**
- Ranked chunk recall@5: **64.4%**
- Ranked chunk recall@10: **71.1%**
- First-five context-entry recall: **91.1%**
- Final context recall: **94.4%**
- Answer checks: **100.0%**

Recall uses the listed gold sections. Accepted equivalent clauses may also support an answer. Parent expansion creates larger context entries; their recall@5 is not a chunk-ranking score. Section IDs alone do not prove a complete clause was provided.

| Question | Pool recall | Chunk recall@5 | Chunk recall@10 | Context | Answer check |
|---|---:|---:|---:|---:|---|
| POL-01: My first flight was delayed by bad weather and I missed my connection. Both flights were on one Northstar ticket. Will you put me on another flight for free? | 100% | 100% | 100% | 100% | PASS |
| POL-02: I got a text offering me another flight. Does that mean I'm booked? | 0% | 0% | 0% | 100% | PASS |
| POL-03: When does Northstar pay for a hotel if I'm stuck overnight? | 100% | 100% | 100% | 100% | PASS |
| POL-04: I'm stuck overnight because of bad weather. Will Northstar pay for my hotel? | 100% | 100% | 100% | 100% | PASS |
| POL-05: The airline says a crew scheduling problem made me miss my connection. I'm stuck overnight away from home. Can I get a hotel? | 100% | 0% | 0% | 100% | PASS |
| POL-06: The new flight gets me to my destination three hours late. Can I get a refund if I turn it down? | 100% | 50% | 50% | 100% | PASS |
| POL-07: I took the replacement flight, but I arrived five hours late. Can I still get a full refund? | 100% | 100% | 100% | 100% | PASS |
| POL-08: The gate agent said weather, but the final investigation says it was a mechanical problem. Which explanation counts? | 100% | 50% | 50% | 100% | PASS |
| POL-09: My flights were booked on two separate tickets. Do I still get a free connection rebooking if the first flight is late? | 100% | 50% | 100% | 100% | PASS |
| POL-10: I'm stranded overnight at the airport in the city where I live. Will Northstar cover a room? | 100% | 50% | 50% | 100% | PASS |
| POL-11: Can I book a hotel myself and send Northstar the receipt? | 100% | 100% | 100% | 100% | PASS |
| POL-12: The agent says all the partner hotels are full. Does that mean I'm not eligible for a hotel anymore? | 100% | 100% | 100% | 100% | PASS |
| POL-13: Nobody has confirmed why my flight was delayed. Can I count on Northstar paying for a hotel? | 100% | 0% | 50% | 50% | PASS |
| POL-14: I missed my connection. Does that automatically mean I get my money back? | 100% | 67% | 67% | 67% | PASS |
| POL-15: I had a crew scheduling delay last year and had to stay overnight away from home. Would Northstar have paid for a hotel? | 100% | 100% | 100% | 100% | PASS |

## Questions

Expand a question to inspect its answer and gaps.

<details><summary>POL-01: My first flight was delayed by bad weather and I missed my connection. Both flights were on one Northstar ticket. Will you put me on another flight for free?</summary>

My first flight was delayed by bad weather and I missed my connection. Both flights were on one Northstar ticket. Will you put me on another flight for free?

**Missing gold sections in context:** None

**Review note:** The core rebooking answer uses the current connection policy, but its extra meal-voucher statement cites the 2025 care policy for a current question. Date applicability and claim-level citation support are not checked by citation-ID validation.

**Missing expected information:** None

Under the current Connection Protection standard (NS-CONN-2026, v2.0, effective 2026-01-01), yes in principle. For a verified protected missed connection — at least two domestic Northstar-operated legs on the same ticket and reservation, sold as a continuous itinerary, where the first leg was disrupted before the onward flight's boarding cutoff — Northstar rebooks you to the earliest available Northstar-operated itinerary to your original ticketed destination at no additional fare. This commitment is cause-independent: it applies to both airline-controllable and uncontrollable disruptions, so weather does not remove it. However, it promises an eligible rebooking process, not a specific flight or time; seats must actually be confirmed, and an offer is not a booking until ticketed. Codeshare, interline, separate-ticket and international itineraries fall outside this standard. Separately, if the replacement arrives much later, you may instead have a refund right under NS-REF-2026 §3. Note weather delays are excluded from standard meal vouchers.

**Citations:** NS-CONN-2026#1.1, NS-CONN-2026#1.2, NS-CONN-2026#2.1, NS-CONN-2026#2.2, NS-CONN-2026#2.5, NS-REF-2026#3.2, NS-CARE-2025#2.2

</details>

<details><summary>POL-02: I got a text offering me another flight. Does that mean I&#x27;m booked?</summary>

I got a text offering me another flight. Does that mean I'm booked?

**Missing gold sections in context:** None

**Missing expected information:** None

No — a text proposing an alternate flight is an offer, not a confirmed reservation. Northstar's connection standard requires staff to distinguish the states `SEARCHED`, `OFFERED`, `ACCEPTED`, `TICKETED` and `FLOWN`, and never to say a customer has been rebooked when only an offer exists; inventory in a search snapshot can change before confirmation. A hold on an alternative flight must carry an expiration time and must not silently count as acceptance, and an unavailable seat may never be presented as booked. You may accept, decline, or leave the offer unanswered; the status is logged with a timestamp and channel. Because gate, phone and app channels can show different snapshots, you can ask which offer is currently authoritative and whether an actual ticket exists. Declining an eligible replacement does not by itself forfeit any refund right, which is assessed separately.

**Citations:** NS-CONN-2026#2.5, NS-CONN-2026#2.2, NS-CONN-2026#2.3, NS-CONN-2026#2.8, NS-REF-2026#2.1, NS-REF-2026#2.2

</details>

<details><summary>POL-03: When does Northstar pay for a hotel if I&#x27;m stuck overnight?</summary>

When does Northstar pay for a hotel if I'm stuck overnight?

**Missing gold sections in context:** None

**Missing expected information:** None

Under the current policy (NS-CARE-2026, effective 2026-01-01), Northstar pays for an approved hotel only when all four conditions hold together: (1) you hold a valid disrupted Northstar itinerary; (2) the final approved root cause is airline-controlled — MECHANICAL, CREW_OPERATIONAL or AIRLINE_OPERATIONS; (3) no reasonable onward Northstar option can be completed without staying at the recovery airport into the next calendar day; and (4) the overnight station is outside your verified home metro area. Weather and external ATC events are excluded (courtesy help only), and an UNKNOWN or MIXED_PENDING cause stays in NEEDS_REVIEW. Crew-caused disruptions have been covered since 2026-01-01; under the archived 2025 edition they were excluded. Accommodation is normally issued as a voucher; self-booking needs prior written authorization of rate and dates. Note: the 2025 edition is still tagged "current" in metadata despite being superseded — a source labelling conflict.

**Citations:** NS-CARE-2026#1.2, NS-CARE-2026#4.1, NS-CARE-2026#4.2, NS-CARE-2026#4.3, NS-CARE-2026#4.4, NS-CARE-2026#4.5, NS-CARE-2026#4.6, NS-CARE-2025#3.2, NS-CARE-2025#3.8

</details>

<details><summary>POL-04: I&#x27;m stuck overnight because of bad weather. Will Northstar pay for my hotel?</summary>

I'm stuck overnight because of bad weather. Will Northstar pay for my hotel?

**Missing gold sections in context:** None

**Missing expected information:** None

Under the current edition (NS-CARE-2026, effective 2026-01-01), no — weather is not covered. Northstar's hotel commitment applies only to "airline-controlled" disruptions whose final approved cause is MECHANICAL, CREW_OPERATIONAL or AIRLINE_OPERATIONS; WEATHER and external ATC events are classified as uncontrollable and are excluded from the routine hotel (and meal) commitment. Staff may help with information or offer discretionary/courtesy assistance, but that is not an entitlement and must be labelled as courtesy rather than policy.

Two caveats: the controlling cause is the latest *approved* investigation classification, not a gate announcement — if a delay first reported as weather is finally classified as mechanical, eligibility is reassessed; while the cause is UNKNOWN or MIXED_PENDING the case stays NEEDS_REVIEW. Even for a covered cause, an overnight wait away from your home metro area and authorization would also be required.

**Citations:** NS-CARE-2026#1.2, NS-CARE-2026#4.1, NS-CARE-2026#4.4, NS-CARE-2026#4.7, NS-CARE-2026#3.2, NS-CARE-2026#4.3

</details>

<details><summary>POL-05: The airline says a crew scheduling problem made me miss my connection. I&#x27;m stuck overnight away from home. Can I get a hotel?</summary>

The airline says a crew scheduling problem made me miss my connection. I'm stuck overnight away from home. Can I get a hotel?

**Missing gold sections in context:** None

**Missing expected information:** None

Under the current policy (NS-CARE-2026, effective 2026-01-01), a crew-caused disruption can qualify. A finalized `CREW_OPERATIONAL` cause is treated as airline-controlled (§1.2, §4.5). Hotel eligibility is conjunctive: you hold a valid disrupted Northstar itinerary; the final approved cause is airline-controlled; continuing travel genuinely requires waiting at the recovery airport into the next calendar day; and the overnight station is outside your verified home metro area (§4.1–§4.3). If the cause is still pending/unknown, the case is held for review (§4.4). Accommodation is normally issued as an approved hotel voucher; self-booking needs written authorization of dates and maximum rate (§4.6). Eligibility is separate from fulfillment — being eligible doesn't mean a room has been booked (§4.8). Note: the archived 2025 edition excluded crew-related causes (NS-CARE-2025 §3.2) and is labeled "current" in metadata despite being superseded; it applies only to 2025 travel dates.

**Citations:** NS-CARE-2026#1.2, NS-CARE-2026#4.1, NS-CARE-2026#4.2, NS-CARE-2026#4.3, NS-CARE-2026#4.4, NS-CARE-2026#4.5, NS-CARE-2026#4.6, NS-CARE-2026#4.8, NS-CARE-2026#5, NS-CARE-2025#3.2, NS-CARE-2025#3.8

</details>

<details><summary>POL-06: The new flight gets me to my destination three hours late. Can I get a refund if I turn it down?</summary>

The new flight gets me to my destination three hours late. Can I get a refund if I turn it down?

**Missing gold sections in context:** None

**Missing expected information:** None

Under Northstar's current refund standard (NS-REF-2026, v2.0, effective 2026-01-01), yes in principle. A replacement itinerary scheduled to arrive at your **final ticketed destination** at least three hours later than your original schedule meets the domestic significant-change threshold. If you decline that changed itinerary and don't accept a replacement flight, travel credit or other compensation, the refund pathway applies — and declining an eligible rebooking does not forfeit that right. The cause matters not: weather-related disruptions qualify just as mechanical ones do.

Key conditions: the three hours is measured at final destination (compared in UTC from the original ticket and the documented offer), not on the inbound leg. If you have already flown part of the journey, only the unused transportation is refunded, per coupon accounting; if you fly the replacement, no full refund follows. The refund amount itself requires the ticket-value record.

**Citations:** NS-REF-2026#3.2, NS-REF-2026#2.2, NS-REF-2026#3.5, NS-REF-2026#3.7, NS-REF-2026#3.4, NS-REF-2026#5, NS-REF-2026#1.1

</details>

<details><summary>POL-07: I took the replacement flight, but I arrived five hours late. Can I still get a full refund?</summary>

I took the replacement flight, but I arrived five hours late. Can I still get a full refund?

**Missing gold sections in context:** None

**Missing expected information:** None

Under the current refund policy (NS-REF-2026, v2.0, effective 2026-01-01), the answer is generally no. A passenger who actually travelled on the significantly delayed or replacement flight cannot obtain a full ticket refund under the significant-change remedy alone, because the transportation was used — even if final arrival was several hours late. The three-hour arrival-change threshold matters only when you decline the changed itinerary; the refund right exists as an alternative to travelling, not in addition to it. Partial refunds can still apply as separate issues with their own evidence: an involuntary cabin downgrade, unused coupons/segments, or refundable baggage and optional-service fees. Any unused-portion amount is calculated from ticket accounting records, not as a full fare refund, and eligible refunds go to the original form of payment (about 7 business days for credit cards, 20 calendar days otherwise).

**Citations:** NS-REF-2026#3.4, NS-REF-2026#3.7, NS-REF-2026#3.2, NS-REF-2026#5, NS-REF-2026#4.1, NS-REF-2026#4.2

</details>

<details><summary>POL-08: The gate agent said weather, but the final investigation says it was a mechanical problem. Which explanation counts?</summary>

The gate agent said weather, but the final investigation says it was a mechanical problem. Which explanation counts?

**Missing gold sections in context:** None

**Missing expected information:** None

The approved final investigation classification controls, not the gate agent's preliminary remark. Northstar treats the first airport/gate statement as provisional: it may explain why an investigation is open, but it does not replace the investigation's final classification (NS-CARE-2026 §4.4, §4.7; NS-CAUSE-2026 §3.1, §3.6). So if an authorized analyst has finalized and approved a MECHANICAL cause, that supersedes the earlier weather label; both observations and the transition between them should be preserved in the record, not deleted (NS-CAUSE-2026 §3.6, §5). Important caveats: a merely PROPOSED or draft mechanical finding cannot silently override an approved determination (NS-CAUSE-2026 §3.8; NS-CARE-2026 §4.7), and if the cause is still UNKNOWN or MIXED_PENDING, cause-dependent benefits stay NEEDS_REVIEW. MECHANICAL is airline-controlled, which satisfies the controllability element for meal/hotel care; other conditions (overnight necessity, home-metro status, approval) still apply (NS-CAUSE-2026 §2, §4; NS-CARE-2026 §4.1).

**Citations:** NS-CARE-2026#4.4, NS-CARE-2026#4.7, NS-CARE-2026#4.1, NS-CAUSE-2026#3.1, NS-CAUSE-2026#3.6, NS-CAUSE-2026#3.8, NS-CAUSE-2026#2, NS-CAUSE-2026#4, NS-CAUSE-2026#5

</details>

<details><summary>POL-09: My flights were booked on two separate tickets. Do I still get a free connection rebooking if the first flight is late?</summary>

My flights were booked on two separate tickets. Do I still get a free connection rebooking if the first flight is late?

**Missing gold sections in context:** None

**Missing expected information:** None

Under the current standard (NS-CONN-2026 v2.0, effective 2026-01-01), the no-additional-fare connection rebooking applies only to a "protected itinerary": at least two domestic Northstar-operated legs issued on the same ticket and reservation, sold as a continuous itinerary. A shared booking reference is not enough — both coupons must appear under the same ticket record. Separate-ticket itineraries (like yours), as well as codeshare, interline and international travel, are expressly outside this pilot standard and must be referred to a specialist, who would decide what, if anything, can be offered. The example table confirms: "Separate tickets purchased independently — outside pilot scope — refer to specialist." Note also that a late inbound flight alone does not establish a missed connection; the onward flight's boarding cutoff matters. Any refund question is assessed separately under NS-REF-2026. Nothing here is a booking or guarantee.

**Citations:** NS-CONN-2026#1.1, NS-CONN-2026#1.2, NS-CONN-2026#2.1, NS-CONN-2026#6, NS-REF-2026#1

</details>

<details><summary>POL-10: I&#x27;m stranded overnight at the airport in the city where I live. Will Northstar cover a room?</summary>

I'm stranded overnight at the airport in the city where I live. Will Northstar cover a room?

**Missing gold sections in context:** None

**Missing expected information:** None

Under the current policy (NS-CARE-2026, effective 2026-01-01), no — a standard hotel is not provided when the overnight station is in your own home metro area. Hotel eligibility is conjunctive: you need a valid disrupted Northstar itinerary, a final approved airline-controlled cause (mechanical, crew operational, or airline operations), a genuine operational need to wait at that airport into the next calendar day, and you must be away from your verified home metropolitan area. The home-city restriction applies even if your trip began elsewhere, so a passenger stranded at an airport within their own metro area is excluded from the standard accommodation commitment. Home-metro status is judged from a verified residence field, not billing address or area code; if residence sources conflict, the condition is marked unresolved pending verification. Meal vouchers are assessed separately: an airline-controlled wait of three or more consecutive hours can still qualify.

**Citations:** NS-CARE-2026#4.1, NS-CARE-2026#4.3, NS-CARE-2026#4.9, NS-CARE-2026#1.2, NS-CARE-2026#3.1

</details>

<details><summary>POL-11: Can I book a hotel myself and send Northstar the receipt?</summary>

Can I book a hotel myself and send Northstar the receipt?

**Missing gold sections in context:** None

**Missing expected information:** None

Under the current policy (NS-CARE-2026, effective 2026-01-01), Northstar normally provides accommodation through an approved hotel voucher rather than reimbursing a hotel you arrange yourself. If you book independently, you must first obtain written authorization that identifies the maximum reimbursable rate and the approved dates; an unrelated agent's verbal suggestion is not adequate proof. Without that written authorization, a receipt submitted afterwards is not guaranteed to be reimbursed. Note also that being eligible for accommodation and whether a particular self-booked expense is reimbursable are two separate decisions: an "eligible" determination does not certify that a room was booked or that a receipt has been accepted (fulfillment states run from NOT_REQUESTED through RECEIPT_PENDING and CLOSED). Underlying eligibility still requires a valid disrupted itinerary, an airline-controlled cause, a genuine overnight wait, and that you are away from your home metro area.

**Citations:** NS-CARE-2026#4.6, NS-CARE-2026#4.8, NS-CARE-2026#4.1

</details>

<details><summary>POL-12: The agent says all the partner hotels are full. Does that mean I&#x27;m not eligible for a hotel anymore?</summary>

The agent says all the partner hotels are full. Does that mean I'm not eligible for a hotel anymore?

**Missing gold sections in context:** None

**Missing expected information:** None

No. Under the current policy (NS-CARE-2026, effective 2026-01-01), hotel *eligibility* and hotel *fulfillment* are separate decisions. Eligibility depends only on the conjunctive conditions in §4.1: a valid disrupted Northstar itinerary, a final approved airline-controlled cause, a genuine overnight wait at the affected airport, and the passenger being away from their verified home metro area. A fully booked partner hotel is a fulfillment exception, not a retroactive denial of eligibility (§4.8). Fulfillment has its own states (NOT_REQUESTED, SEARCHING, VOUCHER_AUTHORIZED, VOUCHER_ISSUED, RECEIPT_PENDING, CLOSED), and staff should document an alternative approved accommodation or escalate the capacity problem to an authorized passenger-care agent while telling you accurately what has and has not been arranged. If you book your own room, you need advance written authorization stating the maximum reimbursable rate and approved dates; an agent's verbal suggestion is not sufficient (§4.6).

**Citations:** NS-CARE-2026#4.8, NS-CARE-2026#4.1, NS-CARE-2026#4.6, NS-CARE-2026#4.11

</details>

<details><summary>POL-13: Nobody has confirmed why my flight was delayed. Can I count on Northstar paying for a hotel?</summary>

Nobody has confirmed why my flight was delayed. Can I count on Northstar paying for a hotel?

**Missing gold sections in context:** NS-CAUSE-2026#3.2

**Missing expected information:** None

Not yet — under the current policy (NS-CARE-2026, effective 2026-01-01), a hotel is not promised while the cause is unresolved. Northstar provides an approved hotel only when all four conditions hold together: a valid disrupted Northstar itinerary; the controlling disruption is airline-controlled (final approved cause of MECHANICAL, CREW_OPERATIONAL or AIRLINE_OPERATIONS); practical onward travel requires an overnight wait at the affected airport; and the passenger is away from their verified home metro area. Where the final cause is UNKNOWN, MIXED_PENDING or still under investigation, eligibility stays NEEDS_REVIEW; a gate announcement does not substitute for the approved investigation classification, and weather or external ATC causes are excluded. Staff may offer courtesy assistance during an unresolved case, but that is discretionary, not an entitlement. Even an ELIGIBLE decision is separate from fulfilment — it does not mean a room has been booked.

**Citations:** NS-CARE-2026#4.1, NS-CARE-2026#4.4, NS-CARE-2026#4.7, NS-CARE-2026#4.8, NS-CARE-2026#1.2, NS-CARE-2026#4.2

</details>

<details><summary>POL-14: I missed my connection. Does that automatically mean I get my money back?</summary>

I missed my connection. Does that automatically mean I get my money back?

**Missing gold sections in context:** NS-REF-2026#2.2

**Missing expected information:** None

No. Under the current policies (effective 2026-01-01), a missed connection is not treated as a canceled ticket and does not by itself create a refund right. On a protected single-ticket domestic Northstar itinerary, a verified missed connection caused by a preceding Northstar disruption entitles you to rebooking on the earliest available Northstar flight to your ticketed destination at no additional fare — for both controllable and uncontrollable causes, subject to seats (NS-CONN-2026 §2.1). A refund is assessed separately: typically if the flight was canceled, or if the replacement itinerary arrives at your final destination at least three hours later (or has another qualifying change) and you decline the alternative. The comparison uses final-destination arrival, not the inbound leg. If you accept rebooking and fly, a full refund generally does not follow; unused portions may be refunded using ticket accounting, to the original form of payment.

**Citations:** NS-CONN-2026#1, NS-CONN-2026#2.1, NS-CONN-2026#2.3, NS-REF-2026#1.1, NS-REF-2026#3.1, NS-REF-2026#3.2, NS-REF-2026#3.4, NS-REF-2026#3.5, NS-REF-2026#4.1, NS-REF-2026#4.2, NS-REF-2026#5

</details>

<details><summary>POL-15: I had a crew scheduling delay last year and had to stay overnight away from home. Would Northstar have paid for a hotel?</summary>

I had a crew scheduling delay last year and had to stay overnight away from home. Would Northstar have paid for a hotel?

**Missing gold sections in context:** None

**Missing expected information:** None

Taking "last year" as 2025 (relative to 2026-11-20), the 2025 edition governs. Under NS-CARE-2025, the routine hotel commitment applied only to a final confirmed MECHANICAL or AIRLINE_OPERATIONS cause, where an overnight stay away from your home metro area was operationally necessary. A disruption whose final primary cause was CREW_OPERATIONAL was expressly excluded from that standard commitment; agents could ask a duty manager for discretionary assistance, but that courtesy was not an entitlement. From 2026-01-01, NS-CARE-2026 §4.5 includes finalized CREW_OPERATIONAL causes, subject to the same overnight, residence and authorization conditions — so a 2026 crew delay would be treated differently. Note a metadata oddity: the archived 2025 edition is still tagged "current" even though it was superseded on 2026-01-01; the event date controls. Eligibility also depends on the approved cause classification and verified home metro.

**Citations:** NS-CARE-2025#1.2, NS-CARE-2025#3.1, NS-CARE-2025#3.2, NS-CARE-2025#3.5, NS-CARE-2025#3.8, NS-CARE-2025#5, NS-CARE-2026#4.1, NS-CARE-2026#4.5

</details>
