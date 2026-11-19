---
document_id: "CASE-MECH-2026"
title: "Resolved Passenger Case — Mechanical Delay and Overnight Hotel"
document_type: "historical_case"
version: "1.0"
effective_from: "2026-05-08"
status: "current"
owner: "Historical Case Review"
source_kind: "synthetic"
fictional_airline: "Northstar Air"
case_id: "FR-181"
case_status: "CLOSED"
is_synthetic: true
---

# Resolved Passenger Case — Mechanical Delay and Overnight Hotel

> **Synthetic closed case:** `FR-181`, travel date 2026-05-08; close date 2026-05-10. Created as a training example for incident comparison, not as authoritative policy. Passenger and ticket details are fictional. Outcome was reviewed under the 2026 Northstar policy.

## 1. Passenger itinerary and reported problem
A passenger booked on a single Northstar ticket from Raleigh to Seattle via Chicago missed the onward flight after an aircraft hydraulic inspection delayed the first segment. The inbound reached Chicago at 18:05 local time; the connecting flight's boarding closed at 17:20. An airport agent confirmed no Northstar service with an available seat could reach Seattle the same day. The next offered flight departed at 07:35 the following morning. The passenger's recorded home metro was Raleigh, not Chicago.

## 2. Sequence of events
| Timestamp (local) | Observation |
|---|---|
| 14:25 | Inbound aircraft held for maintenance inspection |
| 16:45 | Original connection would already have departed |
| 18:05 | Passenger arrived at Chicago recovery desk |
| 18:25 | Agent verified one-ticket protected connection |
| 18:42 | Cause analyst approved `MECHANICAL` classification |
| 19:10 | Next-day rebooking option offered |
| 19:32 | Passenger accepted rebooking |
| 20:05 | Authorized hotel voucher issued |

### 2.1 Connection protection decision
The passenger held two segments on a single ticket, and the inbound arrival occurred after onward boarding closed. The case met **NS-CONN-2026 §§1.1–2.1**, so the agent offered replacement travel without extra fare, subject to seat confirmation. The flight was booked only after acceptance; the early offer did not itself constitute a ticket change.

### 2.2 Hotel assessment
The cause was finalized as `MECHANICAL`, the passenger was away from home, and same-day travel was infeasible. These facts jointly satisfied **NS-CARE-2026 §4.1**. A voucher was issued through **SOP-HOTEL §3.2**, and the voucher record contained its own number and authorization timestamp. This distinguishes a benefit decision from actual provision of assistance.

## 3. Refund review
The offered arrival was more than three hours later than originally ticketed. The customer asked whether a cash refund was possible, but ultimately accepted and completed the alternate flight. The agent explained the options using **NS-REF-2026 §§2–3**. No full ticket-price refund was issued under the significant-change pathway after completed travel. The passenger did not report any involuntary cabin downgrade.

### 3.1 Why this case is only precedent
A new passenger with the same phrases "hydraulic inspection" and "overnight" could still be ineligible for a routine hotel if their home metro were Chicago, or could have a pending decision if the cause remained provisional. A retrieval system should not copy this case's final result without comparing its facts to the new booking.

## 4. Evidence and resolution
| Resolution component | Recorded result | Supporting source |
|---|---|---|
| Protected rebooking | Eligible and completed | NS-CONN-2026 §2.1 |
| Standard hotel | Eligible and voucher issued | NS-CARE-2026 §§4.1–4.6 |
| Full disruption refund | Not issued after alternate travel flown | NS-REF-2026 §3.4 |
| Cause | `MECHANICAL / FINAL` | Case cause investigation |

### 4.1 Evidence package used by the reviewer
The reviewer assembled the original segment linkage, the approved mechanical classification, the arrival-time record establishing the missed connection, the available-flight snapshot, and the home metropolitan area assertion. Each element served a distinct purpose. The flight timeline established that the missed connection was caused by the disrupted inbound operation. The cause determination supplied the carrier-control condition for accommodation. The later offer established whether an overnight stay was necessary. The residence field established whether the passenger was away from home. None of these facts alone would have been sufficient to grant every benefit.

### 4.2 Why similar cases can lead to different answers
A separate weather-delayed passenger could also experience an overnight connection in the same airport, but Northstar's routine hotel commitment would not apply under the same rule. Another passenger whose home metro included the affected station could be excluded even when the cause was mechanical. A third traveler might have no available onward seats yet still be eligible for no-charge rebooking when capacity appears. These distinctions are documented to prevent a case-similarity retriever from treating a previously granted hotel as proof of eligibility in another case.

### 4.3 Counterfactual checks
For training, consider changing only the approved cause to `WEATHER` while holding the itinerary and residence fixed: rebooking eligibility under **NS-CONN-2026 §2.1** remains, but standard hotel assistance under **NS-CARE-2026 §4.4** changes. If instead the next practical connection can be completed without overnight waiting, the hotel decision changes under §4.2. These are controlled counterfactuals, not alternate facts about the real historical case. A retrieval experiment should preserve the distinction between source record and evaluator-created scenario.

## 5. Reviewer notes
The initial agent drafted a generic message promising "compensation" but the reviewer replaced it with separate rebooking, hotel and refund statements. The correction was made to avoid conflating accommodation with airfare repayment. The final case record preserved the passenger's choices and timestamps; future evaluation should compare required evidence and not merely keyword overlap.

## 6. Cross-references
**NS-CONN-2026 §2**, **NS-CARE-2026 §4**, **NS-REF-2026 §3**, **SOP-HOTEL §3**, and **NS-CAUSE-2026 §3**.
