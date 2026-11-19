---
document_id: "CASE-WX-2026"
title: "Resolved Passenger Case — Weather-Related Connection Loss"
document_type: "historical_case"
version: "1.0"
effective_from: "2026-07-21"
status: "current"
owner: "Historical Case Review"
source_kind: "synthetic"
fictional_airline: "Northstar Air"
case_id: "FR-192"
case_status: "CLOSED"
is_synthetic: true
---

# Resolved Passenger Case — Weather-Related Connection Loss

> **Synthetic closed case:** `FR-192`, travel date 2026-07-21; close date 2026-07-23. This is historical evidence and not a policy document. Purpose: demonstrate that a missed connection and overnight wait do not guarantee identical hotel outcomes.

## 1. Situation
A passenger traveling from Denver to Baltimore through Charlotte on a protected Northstar itinerary missed the second flight when thunderstorms caused a ground stop affecting the inbound aircraft. The final approved disruption category was `WEATHER`, based on operations and airport restriction data. The passenger's verified home metro was Denver. All acceptable next-day onward alternatives were outside the original travel day.

### 1.1 Similarity to other cases
The passenger's practical problem looked similar to a mechanical-delay case: long wait, missed connection, next-day flight, and a request for a hotel. A semantic retriever might rank **CASE-MECH-2026** highly because the phrasing overlaps. The decisive difference is the approved cause, not the emotional severity of the disruption or the existence of an overnight itinerary.

## 2. Reconstructed chronology
| Time (EDT) | Event |
|---|---|
| 12:15 | Weather restriction advisory for the region |
| 13:05 | Flight held due to airport ground stop |
| 16:20 | Original onward flight boarded and departed |
| 18:05 | Delayed inbound reached CLT |
| 18:40 | Agent recorded protected missed connection |
| 19:00 | Next-day Northstar option offered |
| 19:35 | Passenger declined the initial morning offer, asked for later choice |
| 20:05 | Cause finalized `WEATHER` |

## 3. Three independent decisions
### 3.1 Rebooking
The traveler had one ticket and missed the onward flight as a direct result of the late inbound. Rebooking remained eligible without additional fare under **NS-CONN-2026 §2.1**, even though the disruption was weather-related. A flight offer had to be accepted and confirmed before the passenger could be described as rebooked.

### 3.2 Hotel assistance
Northstar's voluntary accommodation policy required an approved airline-controlled cause. With `WEATHER / FINAL`, the standard hotel benefit did **not** apply under **NS-CARE-2026 §4.4**. Staff provided a list of hotels, but did not issue a Northstar-paid voucher. The absence of the hotel commitment did not cancel the rebooking offer.

### 3.3 Refund pathway
The case record initially lacked a final agreed alternative and did not establish a completed refund. The later itinerary's projected final arrival was substantially later than originally scheduled. The passenger could consider an applicable disruption refund if the qualifying change and passenger-choice conditions were satisfied under **NS-REF-2026 §3** and **DOT-REF-SNAPSHOT**. A weather cause by itself is not a reason to deny a qualifying refund.

## 4. Resolution and service note
The passenger eventually accepted a later next-day Northstar service and traveled. The case was closed with a no-additional-fare rebooking, no routine Northstar hotel voucher, and no full ticket refund under the significant-change remedy after travel. A courtesy agent assisted the traveler in locating local lodging; that help was not categorized as an accommodation entitlement.

### 4.1 Supporting evidence and limitations
The weather classification was not inferred solely from a passenger's description of rain at the airport. The reviewed record included a finalized disruption determination and relevant operational timeline. The late first leg and missed connection supported the no-fare rebooking assessment. The subsequent flight offer supported the timeline comparison for the separate refund pathway. No single chunk containing the word 'weather' could safely determine the entire passenger resolution; different services depended on different evidence.

### 4.2 Historical similarity trap
This case initially looks like a mechanical-delay case: both travelers are away from home, have protected connections, and face an overnight wait. A nearest-neighbor search over free-text incident summaries might retrieve the mechanical case first because most of the observable symptoms match. The decisive difference is the final controlling disruption cause, not simply the number of matching words. The case record is illustrative precedent; an engine must still cite the current hotel's underlying eligibility and exclusion clauses before providing a recommendation.

### 4.3 Counterfactual investigation
Had an approved later investigation overturned the weather classification and concluded the controlling event was a mechanical defect, the hotel analysis would require reassessment under the current **NS-CARE-2026 §4**. That does not mean an unapproved comment or speculative hypothesis should reverse the documented result. A good resolver should display the final cause version and identify any new record needed to justify a revised entitlement decision. It should not retroactively rewrite the original historical case while exploring this scenario.

## 5. Lessons for retrieval
A model answering "what happened last time?" may cite this case. A model answering "what am I entitled to now?" must cite the active policy and current passenger facts. Similar cases may generate troubleshooting hypotheses, but their outcomes must not be promoted to rules. Distinguish `WEATHER` from `UNKNOWN`: finalized bad weather supports a negative routine-hotel result, while an unresolved cause supports further review.

## 6. Related sources
**NS-CONN-2026 §2.1**, **NS-CARE-2026 §4.4**, **NS-REF-2026 §3**, **NS-CAUSE-2026 §§2–3**, **CASE-MECH-2026** for contrast.
