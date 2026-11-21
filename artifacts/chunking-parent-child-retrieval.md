# Policy Q&A evaluation

Namespace: `policy-qa-parent-child-200-40-v1` · Candidates per search: **20**
Reference date: 2026-11-20 · Questions: 15 · Service errors: 0

- Candidate pool recall: **93.3%**
- Ranked chunk recall@5: **64.4%**
- Ranked chunk recall@10: **71.1%**
- First-five context-entry recall: **91.1%**
- Final context recall: **94.4%**
- Answer checks: **Not run (retrieval only)**

Recall uses the listed gold sections. Accepted equivalent clauses may also support an answer. Parent expansion creates larger context entries; their recall@5 is not a chunk-ranking score. Section IDs alone do not prove a complete clause was provided.

| Question | Pool recall | Chunk recall@5 | Chunk recall@10 | Context | Answer check |
|---|---:|---:|---:|---:|---|
| POL-01: My first flight was delayed by bad weather and I missed my connection. Both flights were on one Northstar ticket. Will you put me on another flight for free? | 100% | 100% | 100% | 100% | Not run |
| POL-02: I got a text offering me another flight. Does that mean I'm booked? | 0% | 0% | 0% | 100% | Not run |
| POL-03: When does Northstar pay for a hotel if I'm stuck overnight? | 100% | 100% | 100% | 100% | Not run |
| POL-04: I'm stuck overnight because of bad weather. Will Northstar pay for my hotel? | 100% | 100% | 100% | 100% | Not run |
| POL-05: The airline says a crew scheduling problem made me miss my connection. I'm stuck overnight away from home. Can I get a hotel? | 100% | 0% | 0% | 100% | Not run |
| POL-06: The new flight gets me to my destination three hours late. Can I get a refund if I turn it down? | 100% | 50% | 50% | 100% | Not run |
| POL-07: I took the replacement flight, but I arrived five hours late. Can I still get a full refund? | 100% | 100% | 100% | 100% | Not run |
| POL-08: The gate agent said weather, but the final investigation says it was a mechanical problem. Which explanation counts? | 100% | 50% | 50% | 100% | Not run |
| POL-09: My flights were booked on two separate tickets. Do I still get a free connection rebooking if the first flight is late? | 100% | 50% | 100% | 100% | Not run |
| POL-10: I'm stranded overnight at the airport in the city where I live. Will Northstar cover a room? | 100% | 50% | 50% | 100% | Not run |
| POL-11: Can I book a hotel myself and send Northstar the receipt? | 100% | 100% | 100% | 100% | Not run |
| POL-12: The agent says all the partner hotels are full. Does that mean I'm not eligible for a hotel anymore? | 100% | 100% | 100% | 100% | Not run |
| POL-13: Nobody has confirmed why my flight was delayed. Can I count on Northstar paying for a hotel? | 100% | 0% | 50% | 50% | Not run |
| POL-14: I missed my connection. Does that automatically mean I get my money back? | 100% | 67% | 67% | 67% | Not run |
| POL-15: I had a crew scheduling delay last year and had to stay overnight away from home. Would Northstar have paid for a hotel? | 100% | 100% | 100% | 100% | Not run |

## Questions

Expand a question to inspect its answer and gaps.

<details><summary>POL-01: My first flight was delayed by bad weather and I missed my connection. Both flights were on one Northstar ticket. Will you put me on another flight for free?</summary>

My first flight was delayed by bad weather and I missed my connection. Both flights were on one Northstar ticket. Will you put me on another flight for free?

**Missing gold sections in context:** None


</details>

<details><summary>POL-02: I got a text offering me another flight. Does that mean I&#x27;m booked?</summary>

I got a text offering me another flight. Does that mean I'm booked?

**Missing gold sections in context:** None


</details>

<details><summary>POL-03: When does Northstar pay for a hotel if I&#x27;m stuck overnight?</summary>

When does Northstar pay for a hotel if I'm stuck overnight?

**Missing gold sections in context:** None


</details>

<details><summary>POL-04: I&#x27;m stuck overnight because of bad weather. Will Northstar pay for my hotel?</summary>

I'm stuck overnight because of bad weather. Will Northstar pay for my hotel?

**Missing gold sections in context:** None


</details>

<details><summary>POL-05: The airline says a crew scheduling problem made me miss my connection. I&#x27;m stuck overnight away from home. Can I get a hotel?</summary>

The airline says a crew scheduling problem made me miss my connection. I'm stuck overnight away from home. Can I get a hotel?

**Missing gold sections in context:** None


</details>

<details><summary>POL-06: The new flight gets me to my destination three hours late. Can I get a refund if I turn it down?</summary>

The new flight gets me to my destination three hours late. Can I get a refund if I turn it down?

**Missing gold sections in context:** None


</details>

<details><summary>POL-07: I took the replacement flight, but I arrived five hours late. Can I still get a full refund?</summary>

I took the replacement flight, but I arrived five hours late. Can I still get a full refund?

**Missing gold sections in context:** None


</details>

<details><summary>POL-08: The gate agent said weather, but the final investigation says it was a mechanical problem. Which explanation counts?</summary>

The gate agent said weather, but the final investigation says it was a mechanical problem. Which explanation counts?

**Missing gold sections in context:** None


</details>

<details><summary>POL-09: My flights were booked on two separate tickets. Do I still get a free connection rebooking if the first flight is late?</summary>

My flights were booked on two separate tickets. Do I still get a free connection rebooking if the first flight is late?

**Missing gold sections in context:** None


</details>

<details><summary>POL-10: I&#x27;m stranded overnight at the airport in the city where I live. Will Northstar cover a room?</summary>

I'm stranded overnight at the airport in the city where I live. Will Northstar cover a room?

**Missing gold sections in context:** None


</details>

<details><summary>POL-11: Can I book a hotel myself and send Northstar the receipt?</summary>

Can I book a hotel myself and send Northstar the receipt?

**Missing gold sections in context:** None


</details>

<details><summary>POL-12: The agent says all the partner hotels are full. Does that mean I&#x27;m not eligible for a hotel anymore?</summary>

The agent says all the partner hotels are full. Does that mean I'm not eligible for a hotel anymore?

**Missing gold sections in context:** None


</details>

<details><summary>POL-13: Nobody has confirmed why my flight was delayed. Can I count on Northstar paying for a hotel?</summary>

Nobody has confirmed why my flight was delayed. Can I count on Northstar paying for a hotel?

**Missing gold sections in context:** NS-CAUSE-2026#3.2


</details>

<details><summary>POL-14: I missed my connection. Does that automatically mean I get my money back?</summary>

I missed my connection. Does that automatically mean I get my money back?

**Missing gold sections in context:** NS-REF-2026#2.2


</details>

<details><summary>POL-15: I had a crew scheduling delay last year and had to stay overnight away from home. Would Northstar have paid for a hotel?</summary>

I had a crew scheduling delay last year and had to stay overnight away from home. Would Northstar have paid for a hotel?

**Missing gold sections in context:** None


</details>
