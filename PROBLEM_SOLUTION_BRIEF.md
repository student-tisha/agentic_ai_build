# NEXUS — Autonomous Retail Supply Chain Recovery Agent
### Problem & Solution Brief · Problem Statement 6

---

## 1. The Problem

Supply chains break in small ways, constantly:

- A shipment gets delayed in transit
- A vendor runs out of stock
- Demand spikes faster than replenishment can react
- A warehouse hits capacity
- A route becomes slow, blocked, or uneconomical

Today, when this happens, the system does one thing: it shows an alert.

> "Vendor X shipment delayed."

Then a human has to open the alert, pull up inventory, call around to vendors, check warehouse stock, compare a few options in their head or a spreadsheet, and manually re-route the order — usually under time pressure, with incomplete information, after the delay has already started eating into the delivery promise.

**Dashboards report. They don't recover.**

## 2. Who feels this

Retail and logistics operations teams who are on the hook for keeping delivery promises intact even when the plan breaks mid-execution — the people who get paged when a shipment is late, not the people who built the dashboard that told them so.

## 3. Why this is an agentic problem, not a reporting problem

A dashboard can tell you a vendor is delayed. It cannot:

- Compare alternative vendors, warehouses, and routes against each other
- Weigh cost vs. delivery time vs. carbon impact instead of picking the first option it finds
- Actually execute the fix — reroute the shipment, place a backup order, transfer stock
- Notice if that fix introduces a *new* problem, and go again

That's a closed decision loop: **observe → decide → act → verify → repeat.** It needs an agent that keeps running, not a report that gets read once.

## 4. The solution — NEXUS

Think of NEXUS as an operations manager who never sleeps and watches the entire network in real time. It runs one loop, continuously:

| Stage | What happens |
|---|---|
| **Monitor** | Continuously watches inventory levels, shipment status, vendor availability, demand signals, warehouse capacity, and routes. |
| **Detect** | Notices when something breaks the plan — a delay, a stock-out, a demand spike — the moment it happens, not at the next scheduled report. |
| **Investigate** | Looks at other vendors, other routes, other warehouse allocations that could still hit the delivery promise. |
| **Weigh options** | Scores every viable alternative on a cost / delivery-time / carbon calculator, instead of grabbing the first workable fix. |
| **Decide** | Picks the option with the best overall trade-off and states its confidence and its reasoning in plain language. |
| **Act** | Actually executes the fix — reroutes the shipment, places the backup order, transfers stock between warehouses. |
| **Verify** | Re-reads live inventory, ETA, and at-risk order counts to confirm the fix held — not just that an API call succeeded. |
| **Monitor again** | Returns to watching the network. The loop is already running for the next disruption. |

## 5. What makes this different from "an alert with extra steps"

1. **It compares, not just finds.** Every disruption produces multiple candidate recoveries, scored on the same weighted criteria (delivery promise, cost, carbon, reliability) before one is chosen.
2. **It explains itself.** Every decision comes with a plain-language reason and a confidence score, not a black-box output.
3. **It acts, then checks its own work.** Verification is a separate step from execution — the loop doesn't call a fix "done" until the live system state confirms it.
4. **It never stops.** One resolved disruption doesn't end the process. The same loop is already watching for the next one.

## 6. Demo scenario used in this build

- **Trigger:** Shipment `SHP-4821` (Mumbai → Kolkata) delayed, expected arrival today 14:30 pushed to tomorrow 22:15 — 184 orders at risk.
- **Alternatives evaluated:** Backup vendor (Mumbai), warehouse transfer (Pune → Kolkata), route reassignment — 14 candidates scanned in total.
- **Decision:** Warehouse transfer, Pune → Kolkata, selected on a weighted mix of delivery promise (45%), cost (30%), carbon (15%), and reliability (10%), at 94% confidence.
- **Action:** Six linked writes — reserve inventory, create transfer request, reassign shipment, update ETA, notify order system, update transport plan.
- **Verification:** Inventory 420 → 236 units, ETA tomorrow 22:15 → today 18:40, orders at risk 184 → 0.
- **Next loop:** Vendor `V-019` drops below safety stock on SKU `SKU-8842` — the agent starts again immediately.

## 7. Scope of this build

This is a **frontend-first hackathon build**: the UI, interaction design, and mock data layer are real and interactive; the underlying vendor/warehouse/routing integrations are simulated for the demo rather than wired to live systems. The architecture (see `ARCHITECTURE.md`) is designed so those mocked services are drop-in replaceable with real APIs without changing the agent loop or the frontend contract.
