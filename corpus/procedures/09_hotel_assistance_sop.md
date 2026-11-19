---
document_id: "SOP-HOTEL"
title: "Station Agent SOP — Overnight Hotel Authorization"
document_type: "sop"
version: "1.6"
effective_from: "2026-01-01"
status: "current"
owner: "Airport Customer Care"
source_kind: "synthetic"
fictional_airline: "Northstar Air"
---

# Station Agent SOP — Overnight Hotel Authorization

> **Controlled procedure:** Airport Customer Care, revision 1.6, effective 2026-01-01. Entitlement authority: **NS-CARE-2026 §4**. Operational companion to rebooking SOP. An authorization decision requires facts beyond the passenger's own disruption description.

## 1. Trigger and prerequisite checklist
Start after a missed connection, cancellation, or protected overnight disruption has been documented. This workflow does not determine whether a connection is protected; consult **NS-CONN-2026** first. Confirm the passenger's travel date, recovery airport, place of residence, available onward departure, and final cause classification. Preserve each input's source document and revision ID so another reviewer can reproduce the decision.

### 1.1 Minimum evidence
The hotel determination requires four fields: a valid disrupted Northstar itinerary, `overnight_required`, `away_from_home`, and `final_primary_cause`. A traveler may show a rebooking confirmation yet fail the home-city test. Likewise, a passenger with an overnight stay caused solely by weather is not routine-hotel eligible under the fictional Northstar policy.

### 1.2 Data freshness
Check whether the proposed rebooking offer is still active; if a same-day flight became available, overnight necessity may have changed. Check that the cause report is `FINAL`. A preliminary cause note does not authorize a categorical denial. Do not use historical cases as substitutes for missing live facts.

## 2. Eligibility workflow
### 2.1 Verify disruption and station
Cross-check the affected flight and station against the passenger's booking. Record where the passenger must spend the night. A connecting traveler whose home metro equals that station is not eligible for standard accommodation even when the journey originated at another airport.

### 2.2 Verify overnight necessity
Use the last valid availability snapshot and the actual rebooking proposal to determine whether the passenger must remain at the station into the next day. A late departure before midnight does not necessarily create an overnight need. An offer that is merely speculative is insufficient evidence to deny accommodation.

### 2.3 Resolve cause status
Read the latest approved primary cause under **NS-CAUSE-2026 §3.3**. For `MECHANICAL`, `CREW_OPERATIONAL`, or `AIRLINE_OPERATIONS`, continue eligibility checks. For `WEATHER` or `ATC_EXTERNAL`, return `NOT_ELIGIBLE` under standard policy while offering hotel-search information. For `UNKNOWN` and `MIXED_PENDING`, return `NEEDS_REVIEW`, assign an owner, and preserve an open investigation link. The 2026 crew rule is explicit in **NS-CARE-2026 §4.5**.

### 2.4 Apply conditions together
Only mark `ELIGIBLE` if the valid disrupted itinerary, overnight condition, away-from-home status, and qualifying final cause all hold. If one required fact is missing and no independent exclusion is confirmed, return `NEEDS_REVIEW`. A missing cause should not be silently treated as either mechanical or weather.

## 3. Authorized hotel flow
### 3.1 Room inventory
Select a participating hotel with documented room availability for the needed date. Record quoted rate, tax treatment, passenger count, and hotel-shuttle details. Inventory may be unavailable even when the benefit is owed; report `ELIGIBLE_INVENTORY_PENDING` rather than incorrectly declaring the traveler ineligible.

### 3.2 Voucher issuance
Record voucher ID, issued time, covered nights, authorized party, and delivery channel. Vouchers are promises for the specified accommodation only; they do not automatically cover any unrelated meal, transport, or personal expense.

### 3.3 Self-booked accommodation
When no approved room can be arranged or exceptional circumstances require independent booking, issue written authorization with a rate ceiling before the passenger books. A traveler who is generally hotel eligible can still have an independently booked expense disallowed if authorization was never granted. Separate **benefit eligibility** from **expense reimbursement** in the answer.

### 3.4 Fulfillment must not override the eligibility decision
An approved eligibility determination does not mean accommodation has been booked. The agent must verify partner property availability, expected check-in, room accessibility needs, transport arrangements where applicable, and voucher constraints. If room inventory is exhausted, escalate fulfillment while preserving the prior eligibility result. Conversely, a room appearing in the reservation portal does not establish that the passenger qualifies. Keep these states separate so downstream reports distinguish 'eligible but not fulfilled' from 'not eligible'. Duplicate voucher attempts must be checked against the case and authorization IDs before issuing another commitment.

### 3.5 Receipt-driven claims and authorization limits
When a passenger independently books accommodation, verify the prior written authorization referenced by **NS-CARE-2026 §4.6**, the approved dates, spending cap, guest identity, and itemized receipt. Do not infer that a receipt is reimbursable merely because its lodging date matches an overnight delay. If authorization is missing, the eligibility decision can remain correct while the expense request is routed to an appropriate reviewer. The system should explain that it is evaluating two questions: whether accommodation assistance is owed under policy and whether a particular expense was authorized under the reimbursement process.

### 3.6 Example escalation paths
| Scenario | Entitlement status | Fulfillment / review action |
|---|---|---|
| Final mechanical cause, verified overnight, away from home | Eligible | Search and authorize hotel voucher |
| Same facts, hotel inventory exhausted | Eligible | Escalate accommodation placement; preserve failed search log |
| Final weather cause | Not eligible under routine Northstar commitment | Explain restriction; discretionary aid must be tagged courtesy |
| Cause unresolved | Needs review | Request approved investigation classification |
| Residence unknown | Needs review | Verify home metropolitan area |
| Authorized self-booking with receipt not yet submitted | Eligible | Await receipt before expense disposition |

These rows are workflow examples; entitlement reasoning remains governed by **NS-CARE-2026 §4**. Every case output should retain both the policy citation and the operational records used to establish the facts.

## 4. Exception handling and escalation
| Case | Result | Reason |
|---|---|---|
| Finalized crew scheduling delay, overnight, away from home | Eligible under 2026 policy | NS-CARE-2026 §4.5 |
| Mechanical delay, overnight, home metro | Not eligible under standard policy | NS-CARE-2026 §4.3 |
| Weather-only overnight | Not eligible under standard policy | NS-CARE-2026 §4.4 |
| Unknown final cause | Needs review | NS-CAUSE-2026 §3.2 |
| Qualifying facts, no participating hotel rooms | Eligible; inventory pending | §3.1 |
| Eligible passenger independently paid without prior approval | Benefit eligible; reimbursement review | §3.3 |

### 4.1 Special support
For an accessibility, safety, or medical support issue, consult a trained agent; the basic voucher flow cannot substitute for case-specific assistance. The RAG assistant should return a human handoff if the necessary policy scope is absent.

### 4.2 Document revision mismatch
If the record references **NS-CARE-2025 §3.2** for travel on or after 2026-01-01, compare the effective policy versions before reaching an outcome. Do not accept an archived rule merely because its text appears to match the query. The on-call hotel agent should flag the mismatch for policy catalog remediation.

## 5. Audit output
Record `hotel_decision`, evidence per eligibility condition, current cause revision, date of policy authority, voucher or authorization ID, and missing conditions. The output must say why a decision is pending and avoid asserting that the passenger has received a voucher when only eligibility was assessed.

## 6. Related documentation
**NS-CARE-2026 §§1,3–5**, **NS-CAUSE-2026 §3**, **NS-CONN-2026 §3**, **OPS-CAUSE-214**, **OPS-OFFER-214**, and **CASE-CREW-2025** for historical-only comparison.
