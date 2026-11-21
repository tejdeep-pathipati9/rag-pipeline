---
document_id: "NS-CAUSE-2026"
title: "Disruption Cause Classification and Investigation Standard"
document_type: "policy"
version: "1.4"
effective_from: "2026-01-01"
status: "current"
owner: "Network Operations Control"
source_kind: "synthetic"
fictional_airline: "Northstar Air"
---

# Disruption Cause Classification — NS-CAUSE-2026

Effective January 1, 2026. Owner: Network Operations Control. This fictional Northstar standard explains how approved causes are recorded for passenger-care decisions. An observed delay and its verified cause are different facts.

## 1. Purpose and scope
Determine the controlling cause of the affected disruption before assessing cause-dependent benefits. A gate announcement, airport display or passenger description may be useful evidence, but is not automatically an approved classification. Protected rebooking can proceed while the cause remains unresolved.

### 1.1 Required observations
Capture the affected flight, date, station, operational timeline, source records, analyst and approval time. Keep observed timestamps separate from when information entered a system. Do not assign a cause simply to produce a desired hotel decision.

## 2. Cause codes
Each code describes the verified cause, not whether a hotel has been booked. Meal and hotel conditions still come from NS-CARE-2026.

### 2.1 Airline-controlled causes
MECHANICAL means an aircraft defect or maintenance hold under carrier responsibility. CREW_OPERATIONAL means an internal crew scheduling, reserve assignment or staffing problem. AIRLINE_OPERATIONS means carrier-controlled gate, baggage-loading, aircraft rotation or dispatch planning. Approved examples include a confirmed failed component or an internal reserve-assignment error.

### 2.2 Uncontrollable and unresolved causes
WEATHER means external weather conditions. ATC_EXTERNAL means an external air-traffic restriction. UNKNOWN means verified information is insufficient. MIXED_PENDING means multiple material causes exist and a controlling cause has not been assigned. Unresolved is not the same as uncontrollable.

## 3. Investigation and approval
Use the latest applicable approved finding. Preserve previous observations so a reviewer can explain why a classification changed.

### 3.1 Preliminary report
An initial gate or dispatcher report is PROVISIONAL. It can explain why an investigation is open, but must not independently grant or deny cause-dependent hotel assistance. A confident description is not an approval event.

### 3.2 Cause not yet confirmed
UNKNOWN, MIXED_PENDING or an open investigation means NEEDS_REVIEW for hotel or meal decisions that depend on controllability. Request the approved cause rather than promising payment or treating uncertainty as a weather exclusion. Rebooking eligibility is assessed separately.

### 3.3 Final finding
An authorized analyst must identify the controlling cause, document the reasoning and sign the final revision. A finalized, approved mechanical finding can supersede an earlier provisional weather remark. Verify that the finding concerns the passenger's actual disrupted flight.

### 3.4 Mixed causes
When weather and an internal problem both contributed, identify which cause prevented timely operation during the relevant interval. Do not count keywords or assume any weather mention excludes assistance. Keep MIXED_PENDING when the evidence cannot resolve the controlling cause.

### 3.5 Causal sequence
Weather may delay an aircraft before a later crew problem prevents departure. A maintenance note may concern a different aircraft after a swap. Compare the chronology and affected segment; the last event mentioned is not necessarily the controlling cause.

### 3.6 Evidence precedence
The latest authorized, signed final investigation takes precedence over preliminary gate comments. Preserve the earlier observation, its timestamp and the approved revision explaining the change. Operational timestamps establish when events occurred; they do not by themselves establish why. Never overwrite an earlier record to hide a changed decision.

### 3.7 Timestamp conflicts
Compare timezone-aware or UTC timestamps from reconciled operational records. A later ingestion time is not proof that an event happened later. If material times conflict, seek review rather than selecting the most convenient value.

### 3.8 Investigation states
The lifecycle is REPORTED, INVESTIGATING, PROPOSED and FINAL_APPROVED. PROPOSED is a draft awaiting authorized approval; it cannot override a valid approved finding. REOPENED means new evidence requires review of the earlier result. Keep the status and cause code as separate fields.

## 4. Applying the cause
Mechanical, crew-operational and airline-operations causes can satisfy the current hotel controllability requirement, but overnight necessity and residence conditions still apply. Weather and external ATC do not satisfy standard care coverage. Cause is not a prerequisite for protected rebooking or a qualifying disruption refund.

## 5. Example
A gate agent initially reports weather. An authorized investigation later confirms an internal crew scheduling failure after the restriction ended. Use the approved crew classification, retain the original weather observation and reassess any cause-dependent benefit under the applicable policy edition.

## 6. Communication
Explain the approved finding, approval status and any missing evidence. Refer to NS-CARE-2026 for meals and hotels, NS-CONN-2026 for protected rebooking and NS-REF-2026 for refunds. Classification alone never proves that a service was delivered.
