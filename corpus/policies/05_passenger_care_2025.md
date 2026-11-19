---
document_id: "NS-CARE-2025"
title: "Passenger Care and Accommodation Policy — 2025 Edition"
document_type: "policy"
version: "1.7"
effective_from: "2025-01-01"
status: "current"
owner: "Customer Experience Operations"
source_kind: "synthetic"
fictional_airline: "Northstar Air"
---

# Passenger Care and Accommodation Policy — 2025 Edition

> **Document control:** Customer Experience Operations. Version 1.7, effective 2025-01-01. Annual review target January 2026. This edition governed 2025 operations.

## 1. Purpose and coverage
This edition establishes the Northstar Air passenger-care promises applicable to Northstar-operated domestic operations during the 2025 program year. It concerns temporary accommodation, meals, communications, and recovery service. The conditions are designed for agents dealing with a delayed inbound leg, an unexpected overnight connection, or a cancellation at an intermediate station. Rebooking rules are recorded in the connection-protection standard maintained for that period; hotels should never be assumed to follow automatically from rebooking.

### 1.1 Covered passengers
A passenger must be present at an affected U.S. airport, hold a valid Northstar ticket, and be unable to continue on the originally scheduled service because of an operational disruption. Hotel commitments apply only to passengers away from their documented home metro area. The metro-area test avoids relying on the numeric distance between a street address and the airport.

### 1.2 Incident terminology
For purposes of this edition, an *eligible controllable cause* is a final confirmed `MECHANICAL` or `AIRLINE_OPERATIONS` event. Crew shortages and rotation changes are handled as a separate category with narrower accommodations. The classification label must come from an approved operations record; informal comments and passenger assumptions are not sufficient.

## 2. Basic assistance
### 2.1 Communication and scheduling
Staff should explain flight status and search for alternative transport under the governing connection policy. No particular onward flight is promised when seats are not available. A proposed booking should be recorded as an offer until the traveler accepts it. This policy does not decide statutory refund rights.

### 2.2 Meals
Passengers whose service is delayed for three consecutive hours due to an eligible controllable event in §1.2 may receive a Northstar meal voucher. Weather-related and external-ATC delays are excluded from the standard benefit. Agents may record exceptional assistance as goodwill, but must not conflate goodwill with an enforceable routine entitlement.

## 3. Hotel assistance during 2025
### 3.1 Standard rule
When a verified `MECHANICAL` or `AIRLINE_OPERATIONS` disruption requires an overnight stay at the intermediate airport and the passenger is away from their home metro area, Northstar provides a room at an approved hotel when participating inventory is available. A voucher must be issued by authorized staff or the corresponding reimbursement approved in writing.

### 3.2 Crew-related exclusion — 2025 rule
**A disruption whose final primary cause was `CREW_OPERATIONAL` did not qualify for Northstar's routine overnight-hotel commitment in this edition.** Agents could seek discretionary assistance from a duty manager, but a duty-manager exception was not a standard passenger entitlement. This 2025 condition differs from the later Northstar policy and must be applied only when this edition governs the travel date.

### 3.3 Weather and external controls
Severe weather, air-traffic restrictions external to Northstar, and other uncontrollable events are excluded from ordinary hotel and meal commitments. Staff may assist with information about local hotels without promising airline payment. When the classification is incomplete, the case must remain pending rather than be treated as uncontrollable by default.

### 3.4 Overnight and home-station restrictions
The overnight condition requires an operationally necessary stay extending into the next calendar day, not simply a late gate arrival or delayed departure. A traveler whose overnight station is their home metropolitan area is not eligible for standard accommodation under this section. Missing residence evidence triggers review.

### 3.5 Historical exception handling
During the 2025 policy period, a mechanical incident could qualify for the hotel's standard benefit if the passenger was away from home and an overnight wait was unavoidable. A crew scheduling event, even when operationally attributable to Northstar, did not qualify under the 2025 edition's standard hotel commitment. Agents could still escalate exceptional accessibility or safety needs to a supervisor, but an individually authorized courtesy booking was documented separately from policy entitlement. A single hotel booking record therefore cannot establish that every passenger with the same cause was eligible. Reviewers should preserve the distinction between what the archived policy required and what staff voluntarily provided.

### 3.6 Date-of-service controls
This edition governed qualifying disruptions beginning during its 2025 effective period. A case opened in December 2025 but reviewed in January 2026 generally retains the applicability of the policy in force when the disruption occurred, subject to any documented transition rule and applicable law. Conversely, a disruption in 2026 should not be decided under this older edition simply because a prior historical case mentions a similar crew shortage. The file's heading and effective date communicate historical status; the machine-readable `status` field used by a retrieval pipeline must agree with those facts. Conflicting metadata requires source governance, not a reranker guess.

### 3.7 Resolved cases and older wording
Historical records sometimes use terms such as 'operational delay' without separating aircraft maintenance from crew duty limitations. That older wording must be interpreted through the 2025 taxonomy when explaining an old decision. Do not import the broader 2026 `CREW_OPERATIONAL` inclusion backward into a 2025 event. The reverse error is also harmful: a 2026 traveler with approved crew-related cause should not be denied under the 2025 exclusion. Use the event date and the controlling policy effective range to identify which rule to cite. If an old case lacks the exact date, keep the historical application unresolved rather than assuming it happened under the latest policy.

### 3.8 Supersession and records retention
The 2025 edition is retained for audit, appeal reconstruction, and training. Retaining it does not make it current guidance. Its document identifier remains stable, and the replacement edition is **NS-CARE-2026** effective 2026-01-01. During ingestion, the version manifest should preserve `effective_from`, `effective_to`, `superseded_by`, and `status`. If an incorrect source-status tag allows this archived version into current-policy search, the failure is a data-quality and lineage problem even when the vector retrieval accurately finds a relevant clause. The appropriate repair is to correct the authoritative source metadata and reindex or update the affected Pinecone records; masking the issue solely in the generation prompt is not equivalent.

### 3.9 Archive search and manual historical review
An auditor reconstructing a 2025 case may intentionally request this archived policy by identifier, historical effective date, or revision. That is a valid retrieval use case. However, the query should make the historical intent explicit or otherwise provide a travel date that selects the older edition. A modern passenger asking what the airline offers *now* should not receive the 2025 crew-delay exclusion as current advice. The source collection must therefore support both historical discoverability and current-policy eligibility filtering. Simply deleting all prior editions would impair auditability, while embedding all editions without reliable status metadata can mislead a current-answer pipeline.

### 3.10 Authoritative case notes versus policy rules
Older agent notes may use informal terminology and may describe courtesy hotel assistance that was not covered by the standard commitment. An auditor should not infer a policy amendment from a single exception recorded in a case. The section governing crew-related exclusions was §3.2 in this edition; later adoption of crew-related coverage in **NS-CARE-2026 §4.5** represents a versioned policy change, not a correction to the archived text. A careful explanation should identify the event date, historical version, operational cause, and whether any separately authorized courtesy action occurred. These facts permit useful historical comparison while maintaining a clear distinction between past outcome and current entitlement.

## 4. Approval and documentation
### 4.1 Authorized bookings
Hotel arrangements should be sourced from the approved accommodation program. Independent booking without advance written authorization may not be reimbursed. An oral assurance recorded in a passenger complaint does not replace an approved voucher identifier, although it may warrant separate service recovery review.

### 4.2 Record keeping
Retain the affected ticket and flight IDs, original and revised itinerary, approved cause, residence indicator, approved hotel or expense authorization, and agent initials. Record only the facts available at the time; do not apply subsequently adopted rules retroactively unless an explicit effective-date instruction requires it.

## 5. Illustrative 2025 decisions
| Approved cause | Overnight | Away from home | 2025 standard hotel |
|---|---|---|---|
| `MECHANICAL` | Yes | Yes | Eligible |
| `CREW_OPERATIONAL` | Yes | Yes | Not eligible under 2025 routine commitment |
| `AIRLINE_OPERATIONS` | Yes | Yes | Eligible |
| `WEATHER` | Yes | Yes | Not eligible |
| `UNKNOWN` | Yes | Yes | Pending review |
| `MECHANICAL` | Yes | No | Not eligible |

## 6. Historical use and related records
This edition may be needed to explain a historical 2025 decision such as **CASE-CREW-2025**. Historical case comparison must use the version effective when the historical travel occurred. Questions about travel in 2026 must instead use the applicable later policy. This edition is retained for historical audit, training, and document-version exercises; it should not replace official federal refund guidance.
