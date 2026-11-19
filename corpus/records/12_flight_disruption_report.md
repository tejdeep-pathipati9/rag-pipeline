---
document_id: "OPS-FLIGHT-214"
title: "Flight Movement and Connection Loss Report — FR-214"
document_type: "operational_record"
version: "r2"
effective_from: "2026-10-14"
status: "current"
owner: "Flight Movement Operations"
source_kind: "synthetic"
fictional_airline: "Northstar Air"
case_id: "FR-214"
record_type: "flight_events"
is_synthetic: true
---

# Flight Movement and Connection Loss Report — FR-214

> **Synthetic operational export:** Flight Movement Operations, revision `FLT-214-r2`, produced 2026-10-14T19:15:00Z. Covers `NS420` inbound and connecting service `NS811`. The report records movements and effects, not the approved underlying cause classification.

## 1. Flight and station identifiers
| Field | Inbound | Onward |
|---|---|---|
| Flight | `NS420` | `NS811` |
| Segment | `SEG-214-A` | `SEG-214-B` |
| Operating date | 2026-10-14 | 2026-10-14 |
| Route | BOS → CLT | CLT → SFO |
| Status | Completed late | Departed as scheduled; passenger missed connection |
| Original scheduled departure | 08:10 EDT BOS | 11:35 EDT CLT |
| Original scheduled arrival | 10:35 EDT CLT | 14:10 PDT SFO |
| Recorded boarding cutoff | Not applicable here | 11:20 EDT CLT |

## 2. Verified event timeline
| Event ID | Timestamp | Local / UTC | Fact |
|---|---|---|---|
| `EVT-214-01` | 2026-10-14 08:10 EDT | 12:10Z | Original `NS420` departure time passed |
| `EVT-214-02` | 2026-10-14 08:36 EDT | 12:36Z | Maintenance inspection underway; provisional remark posted |
| `EVT-214-03` | 2026-10-14 10:50 EDT | 14:50Z | `NS420` departed BOS after maintenance release |
| `EVT-214-04` | 2026-10-14 11:20 EDT | 15:20Z | `NS811` boarding closed at CLT |
| `EVT-214-05` | 2026-10-14 11:35 EDT | 15:35Z | `NS811` departed CLT |
| `EVT-214-06` | 2026-10-14 13:20 EDT | 17:20Z | `NS420` arrived at CLT gate |
| `EVT-214-07` | 2026-10-14 13:42 EDT | 17:42Z | Recovery desk opened protected-connection case |

### 2.1 Connection infeasibility
The inbound arrived two hours after the onward boarding cutoff. Even before allowing walking and gate-transfer time, the passenger could not board `NS811` based on these event times. This report supports the missed-connection determination under **NS-CONN-2026 §1.2** and explains why the original segment remains `OPEN_UNUSED` in **OPS-BOOK-214**.

### 2.2 Flight delay magnitude
Original inbound CLT arrival was 10:35 EDT and verified actual gate arrival was 13:20 EDT, an inbound arrival difference of **2 hours 45 minutes**. This figure is intentionally different from the projected final-destination arrival difference of the next-day rebooking. The refund test must use the relevant original and proposed *final-destination* schedule rather than reusing 2h45.

## 3. Passenger impact and alternative inventory
As of a fictional inventory snapshot at 14:10 EDT, no usable same-day Northstar onward seat met the connection and boarding constraints. A next-day CLT → SFO Northstar service was proposed for 2026-10-15. This report establishes the operational reason a next-day option was considered but does **not** establish that it was accepted or ticketed. See **OPS-OFFER-214**.

### 3.1 Overnight finding
An overnight station wait is operationally necessary based on the stated available-flight snapshot. This is one element of hotel eligibility; passenger residence and approved cause must still be evaluated separately. A published timetable is not equivalent to confirmed inventory.

## 4. Cause evidence boundary
An early airport remark mentioned a component inspection. Flight Movement Operations does not approve a final root cause. The distinct **OPS-CAUSE-214** investigation finalizes `MECHANICAL` after validating maintenance records. A question about *why* the flight was late should cite that investigation, not just the movement timestamps.

## 5. Audit handling
Append corrected observations with their event IDs if later reconciliation changes arrival or departure times. Do not revise the original ticketed arrival baseline to match the rescheduled service; doing so would erase evidence needed to evaluate disruption significance. Event times are saved in UTC even when displayed in local time above.

## 6. Cross-references
**OPS-BOOK-214 §2**, **OPS-CAUSE-214 §3**, **OPS-OFFER-214 §2**, **NS-CONN-2026 §§1–3**, **NS-CARE-2026 §4.2**.
