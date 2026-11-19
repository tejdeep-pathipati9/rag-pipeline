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

# Disruption Cause Classification and Investigation Standard

> **Document control:** Network Operations Control (NOC). Version 1.4, effective 2026-01-01. Approved for the domestic Northstar passenger-care pilot. Source-of-truth for cause status is the last finalized investigation revision, not a gate message.

## 1. Scope and rationale
This standard defines how operational events are recorded and classified before downstream benefit policies use them. The connection-rebooking commitment does not require cause classification, but accommodation and meals do. An investigator must distinguish an observed symptom, a possible contributing factor, and the confirmed primary cause. A flight's arrival delay can have several contributing conditions without all of them qualifying as the controlling cause.

### 1.1 Required observations
Each investigation identifies the flight and date, leg and station, original and actual timestamps, operational timeline, initial event codes, known evidence, disputed facts, analyst, and approval time. If the cause is not verified, retain an unresolved state. The record may be updated as maintenance and operations data arrive; earlier revisions must remain inspectable.

## 2. Classification taxonomy
| Code | Meaning | Control classification | Example evidence |
|---|---|---|---|
| `MECHANICAL` | Aircraft defect or maintenance hold under carrier responsibility | Airline-controlled | Maintenance release delayed by component inspection |
| `CREW_OPERATIONAL` | Internal crew scheduling, reserve assignment, or staffing | Airline-controlled | Reserve crew report not met after planning error |
| `AIRLINE_OPERATIONS` | Gate, baggage-loading, aircraft rotation or dispatch planning | Airline-controlled | Aircraft positioned at wrong gate |
| `WEATHER` | Weather conditions beyond carrier control | Uncontrollable | Airport restriction for storms |
| `ATC_EXTERNAL` | External air-traffic restriction | Uncontrollable | Ground stop imposed by ATC |
| `UNKNOWN` | Insufficient verified information | Unresolved | Initial delay code only |
| `MIXED_PENDING` | Multiple material causes, controlling cause not assigned | Unresolved | Weather plus crew effects still under review |

### 2.1 Classification is not a keyword task
An airport remark containing the word "weather" is not conclusive if the verified delay was caused by a later internal crew scheduling failure. Likewise, "maintenance checked" in a log does not automatically establish a mechanical delay. The approved primary-cause field must be supported by the chronology and signed by an authorized analyst.

### 2.2 Conflicting timestamps
When two systems disagree about actual gate arrival, use the flight operations reconciled timestamp and preserve the original conflicting values. Do not overwrite an observation to force the eligibility outcome desired by a customer or agent. Time arithmetic should be performed on zone-aware timestamps.

## 3. Investigation state machine
### 3.1 Initial report
The first airport or dispatcher event is `PROVISIONAL`. It may contain an unverified description and is suitable for explaining why the investigation is open, not for denying or granting discretionary hotel benefits. Downstream systems should record the provisional status separately from the current primary classification.

### 3.2 Under investigation
When significant contradictions exist, assign `UNKNOWN` or `MIXED_PENDING`, attach evidence IDs and a next review time, and return `NEEDS_REVIEW` for decisions that depend on controllability. Do not choose a negative classification merely because it is operationally convenient.

### 3.3 Finalization
A classification becomes `FINAL` when an authorized analyst identifies the controlling cause, records rationale, and signs the revision. The finalized revision includes `revision_id`, `finalized_at`, `primary_cause`, and a stable link to contributing observations. Passenger-care eligibility may then be re-evaluated.

### 3.4 Mixed causes and controlling cause
When weather and an internal condition both contributed, investigators must determine which cause independently prevented the flight's timely operation during the relevant interval. If the evidence cannot support that determination, keep `MIXED_PENDING`. A weather notice alone is not a universal veto on accommodation, and a crew label alone is not a universal guarantee; the approved cause controls the applicable airline commitment.

### 3.5 Multiple contributing factors and controlling cause
An event may have more than one real contributing factor. A maintenance delay can cause a crew to exceed a duty window; severe weather may have delayed the same aircraft earlier in the day; a later ground stop may then prevent recovery. The classification is not determined by counting how many logs mention each factor. Investigators should establish the controlling cause for the specific missed connection using an ordered, timestamped incident narrative. If the causal chain cannot be resolved, retain `MIXED_PENDING` until a qualified reviewer makes a final determination. The booking team can continue no-cost recovery under **NS-CONN-2026 §2.1**, while passenger-care entitlement may remain unresolved under **NS-CARE-2026 §4.4**.

### 3.6 Evidence source hierarchy
Automated flight events establish that something happened at a particular time, but do not always explain why. An airport display may show `DELAYED` without cause; a gate-agent remark may be preliminary; an aircraft maintenance record may show a confirmed defect; and the final investigation may supersede all earlier cause labels. Each item must retain its observation timestamp, source system, and approval state. The approved cause record should point back to its supporting artifacts. When a cause is corrected, preserve the previous value, who approved the revision, and why the correction was made. Do not delete the earlier assertion; preserving it is necessary for a reproducible explanation of past decisions.

### 3.7 UTC timeline reconstruction
Mixed local-time inputs frequently create misleading narratives during cross-time-zone itineraries. Record scheduled, estimated, actual, and source-ingestion timestamps separately in ISO 8601 with timezone offsets or UTC. A report entered at 23:30 local time can be later than a flight event stamped 00:10 in a different timezone; sorting raw clock strings is not acceptable. Also distinguish when an observation occurred from when the underlying system learned about it. The ingestion time of a corrected weather report must not be mistaken for the time the weather affected departure operations. The operational evidence store, rather than the embedding model, should perform timestamp normalization and chronology reconstruction.

### 3.8 State transitions and approvals
The normal cause lifecycle is `REPORTED → INVESTIGATING → PROPOSED → FINAL_APPROVED`, with `REOPENED` allowed if a material correction is necessary. Benefits that depend on cause should cite the latest valid final approval for the travel date. A `PROPOSED` mechanical cause might be useful for escalation, but cannot automatically override a previously approved weather determination. A reopened investigation should produce a fresh review requirement if entitlement would change. The system may identify the conflicting entries, but it should not fabricate an approval event or resolve an aviation operational dispute using only narrative similarity.

### 3.9 Contrastive examples
| Observation set | Plausible final code | Why further evidence may matter |
|---|---|---|
| Defective valve confirmed by maintenance, departure held for repair | `MECHANICAL` | Repair log must refer to the affected flight |
| Crew unavailable due to airline scheduling | `CREW_OPERATIONAL` | Need to distinguish a weather-driven crew displacement |
| Airport runway closed due to storm | `WEATHER` | Downstream operations delays do not automatically change primary cause |
| External air traffic restriction without carrier-controlled origin | `ATC_EXTERNAL` | Verify authoritative restriction event |
| Severe weather and a maintenance failure both appear relevant | `MIXED_PENDING` until approved | A single keyword cannot establish controlling cause |

These examples are intended to prevent false certainty. A classification answer should cite approved case evidence and the taxonomy, not just quote a policy definition.

### 3.10 Review checks for apparently contradictory reports
Before approving a final cause, the reviewer should check whether competing observations concern the same flight, the same operational leg, and the same time interval. A weather alert from the arrival airport may be real yet irrelevant to the original cause of the missed connection. A maintenance note may belong to a different tail number after an aircraft swap. A crew scheduling report may record the final departure delay without establishing what originally triggered the crew problem. The investigation must capture these distinctions in the written rationale, citing exact evidence identifiers and why the chosen controlling cause best fits the incident. A missing link between the evidence and the disrupted segment is a reason for `NEEDS_REVIEW`, not a reason to promote the most confidently worded narrative.

### 3.11 Classification output contract
An approved classification response should contain the flight and disruption identifiers, current code, approval status, approval timestamp, source references, and any superseded finding IDs. Downstream services should consume the code only after verifying that it belongs to the correct affected itinerary and has a valid approval state. For customer communications, report the human-readable meaning of the code without claiming that it independently establishes a rebooking, hotel, or refund result. Those decisions must be made under their respective policies. If a later revision is approved, record the review transition, recalculate any cause-dependent entitlement affected by the change, and preserve the original recommendation as an auditable earlier decision.

## 4. Rule-use implications
**NS-CARE-2026 §§3–4** uses the final cause for meal and hotel eligibility. `MECHANICAL`, `CREW_OPERATIONAL`, and `AIRLINE_OPERATIONS` can meet the controllability element; `WEATHER` and `ATC_EXTERNAL` do not. `UNKNOWN` and `MIXED_PENDING` yield an unresolved benefit decision, unless other mandatory constraints independently establish ineligibility. Rebooking under **NS-CONN-2026 §2.1** can proceed while the cause is unresolved. Refund obligations under **NS-REF-2026 §3** cannot be denied solely because a delay is attributed to weather.

## 5. Investigation record example
A flight initially tagged `WEATHER` at 09:20 may be revised to `CREW_OPERATIONAL` after the weather restriction is lifted and dispatch records establish an internal reserve assignment failure. That is not two simultaneous final causes. The dataset should preserve both events with effective timestamps and make the newer approved revision authoritative. The example illustrates change over time, not a reason to manufacture an inconsistency in every record.

## 6. Audit and cross-references
Maintain immutable observation IDs, analyst sign-off, evidence attachment hashes, and revision sequence. See **OPS-CAUSE-214** for the active case and **SOP-HOTEL §2.3** for handling pending decisions. Classification documents must never be used as substitutes for primary flight operation records or airline refund terms.
