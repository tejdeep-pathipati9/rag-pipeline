---
document_id: "CASE-CREW-2025"
title: "Historical Passenger Case — Crew Delay Under 2025 Policy"
document_type: "historical_case"
version: "1.0"
effective_from: "2025-11-12"
status: "current"
owner: "Historical Case Review"
source_kind: "synthetic"
fictional_airline: "Northstar Air"
case_id: "FR-097"
case_status: "CLOSED"
is_synthetic: true
---

# Historical Passenger Case — Crew Delay Under 2025 Policy

> **Synthetic closed historical case:** `FR-097`; travel date 2025-11-12, close date 2025-11-14. Preserves the rules actually applied at the travel date. Do not use this case's hotel outcome as the current standard for a 2026 incident.

## 1. Booking and disruption
A Northstar passenger traveling Portland, Maine to Austin through Charlotte held a single protected ticket. The inbound flight was held because an internal crew scheduling handoff failed and a reserve crew was not positioned on time. After the arrival delay, the passenger missed their onward flight and was offered the next available Northstar service the following day. The station was outside the traveler's home metropolitan area.

### 1.1 Approved operational cause
The original gate note described "crew availability." A later Network Operations Control review established the internal assignment error and finalized `CREW_OPERATIONAL`. The issue was not caused by external air-traffic restrictions, weather, or passenger action. The classification was final before the overnight service decision was made.

## 2. Service history
| Event | Time (local) | Outcome |
|---|---|---|
| Inbound service delayed | 11:10 | Internal crew report problem |
| Onward boarding closed | 13:20 | Connection no longer possible |
| Inbound arrived | 14:40 | Passenger referred to station recovery |
| Rebooking offered | 15:10 | No additional fare |
| Cause review finalized | 16:05 | `CREW_OPERATIONAL` |
| Hotel request reviewed | 16:30 | Standard 2025 hotel commitment did not cover crew category |
| Passenger accepted later flight | 17:05 | Departure next day |

## 3. Policy determination at the time
### 3.1 Rebooking
The passenger held protected travel on one ticket and missed the connection because of the delayed first leg, so the airline arranged alternative Northstar transportation at no extra fare under the then-applicable rebooking standard.

### 3.2 Hotel decision under the 2025 edition
The relevant historical accommodation authority was **NS-CARE-2025 §3.2**. That edition expressly excluded `CREW_OPERATIONAL` from the routine hotel commitment even when an overnight stay was necessary and the passenger was away from home. A customer-care manager could authorize a discretionary exception but no such approval was recorded in this case. The standard benefit was therefore marked not eligible.

### 3.3 Why the rule changed
The newer **NS-CARE-2026 §4.5** includes finalized crew-operational disruptions among qualifying controllable causes. That change applies to travel covered by the 2026 policy. This case is valuable for historical explanation but a wrong source for deciding a 2026 passenger's standard hotel entitlement. The rule difference is deliberate and must be interpreted using travel dates.

## 4. Refund status
The passenger accepted and completed the next-day alternative. They received no full fare refund under a significant-change theory after travel was completed. If an analyst asks whether the passenger could have chosen refund instead, the answer requires the relevant original versus offered arrival change and the passenger's then-applicable decision record, not merely the resolution narrative.

### 4.1 Applicable-date reconstruction
The case's date determines which passenger-care edition governs the hotel commitment. The archival reviewer confirms the disruption occurred in 2025, then applies **NS-CARE-2025 §3.2**, under which a crew-operational shortage did not qualify for the standard hotel benefit. The same approved cause occurring in 2026 would be handled differently under **NS-CARE-2026 §4.5**. The date is not background decoration: it changes the controlling policy. A system that searches only for the most recent document can misstate the historical outcome, while one that treats the archived policy as current can misstate a modern outcome.

### 4.2 Source version and retrieval provenance
The archived policy is intentionally kept in the source collection for audit reconstruction. Its existence does not make it current. A production-style resolver should compare the travel date and document effective range before selecting controlling authority. In the deliberately broken lab fixture, the archived policy's `status` metadata is incorrectly set to `current`, which allows an unsafe eligibility decision if the retrieval path relies on that flag. This exercise is a source lineage defect, not evidence that embedding similarity or cross-encoder ranking is intrinsically wrong.

### 4.3 Limits of incident analogy
Do not claim that a 2026 customer must be denied hotel assistance merely because this 2025 traveler was denied. Likewise, do not claim the 2025 traveler was entitled to a hotel simply because the later rule broadened coverage. The two passenger questions share terminology but differ in the policy regime that applies. If the disruption date or final classification cannot be verified, report the missing evidence. This case may be used to test whether a historical analogy is properly subordinate to dated, authoritative policy text.

## 5. Reviewer commentary
The final case note says: "No routine hotel voucher was issued under the applicable 2025 crew exclusion; agent gave hotel location information." This text can be retrieved for historical questions. If a retrieval system uses it to deny a hotel to a 2026 crew-delay traveler, the likely error is either inappropriate source selection or a flawed policy-status catalog, not an indication that the 2026 policy has the same rule.

## 6. Evidence labels and cross-references
| Question | Source to use |
|---|---|
| Why did this historical traveler not receive a hotel? | NS-CARE-2025 §3.2 |
| What is the rule for travel in 2026? | NS-CARE-2026 §4.5 |
| Does rebooking depend on the reason for delay? | Active connection-protection standard |
| Can a hotel decision substitute for refund decision? | No, examine separate refund conditions |

Related: **NS-CARE-2025 §§1–4**, **NS-CARE-2026 §4.5**, **NS-CAUSE-2026 §2** (classification concepts only, not retroactive policy).
