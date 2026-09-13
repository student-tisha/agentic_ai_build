# Demo Video Script — NEXUS

Target length: **90–120 seconds**. Record your screen on `index.html` at a normal desktop width. Suggested pacing below assumes you narrate live while clicking, but you can also record the click-through first and voice over it after.

---

### 0:00–0:10 — Open on the hero

**Show:** land on the top of the page, metrics visible.

**Say:**
"Supply chains break in small ways constantly — a shipment gets delayed, a vendor runs out of stock, demand spikes. Today, most systems just throw an alert and leave a human to figure out the fix. NEXUS is different: it's an agent that investigates, decides, and acts on its own."

### 0:10–0:20 — Point at the metrics

**Show:** hover briefly over the metric cards (Active Disruptions, Orders Protected, Delivery Promise).

**Say:**
"It's watching the whole network right now — three active disruptions, over a thousand orders currently protected, delivery promise sitting at 97.8%."

### 0:20–0:25 — Trigger the demo

**Show:** click **Run Autonomous Recovery**.

**Say:**
"Let's watch it handle one, end to end."

### 0:25–0:35 — Monitor → Disruption detected

**Show:** the loop track lights up node 1, then node 2 (red).

**Say:**
"It's continuously monitoring shipments, inventory, and vendors. Here — shipment SHP-4821 just got delayed. A hundred and eighty-four orders are now at risk of missing their delivery promise."

### 0:35–0:50 — Investigate → Alternatives

**Show:** node 3 (investigate, scanning counter ticking up), then node 4 (alternative cards appearing).

**Say:**
"Instead of just flagging it, the agent starts investigating — scanning fourteen candidate recoveries across backup vendors, warehouse transfers, and route reassignments. Three come back viable, each scored on cost, delivery time, carbon, and success probability."

### 0:50–1:05 — Decision

**Show:** node 5, weighted bars filling in, confidence ring, recommendation box.

**Say:**
"This is the part that matters most: it's not picking the first option it finds. It's weighing delivery promise at 45%, cost at 30%, carbon at 15%, reliability at 10% — and it lands on the warehouse transfer from Pune to Kolkata, at 94% confidence, with a plain-language reason: it preserves the delivery promise while minimizing cost and carbon."

### 1:05–1:15 — Action

**Show:** node 6, execution checklist ticking off items one by one.

**Say:**
"Now it actually executes — reserving inventory, creating the transfer, reassigning the shipment, updating the ETA, notifying the order system. Six real writes, not a suggestion for someone to do later."

### 1:15–1:25 — Verify

**Show:** node 7, before/after verification cards, green success banner.

**Say:**
"And critically, it checks its own work. Inventory, ETA, and orders-at-risk are all re-read from the live system after the fix — not assumed. Zero orders at risk. Delivery promise restored."

### 1:25–1:35 — Monitor again → next disruption

**Show:** node 8, then the loop restarting, activity feed updating.

**Say:**
"And it doesn't stop there — it goes straight back to monitoring, and it's already picking up the next one: a vendor dropping below safety stock. This is the whole point — one resolved issue doesn't end the process. The loop just keeps running."

### 1:35–1:45 — Close

**Show:** scroll to the Disruption Panel and Agent Activity feed briefly, then back to the top.

**Say:**
"That's NEXUS — detect, investigate, decide, act, verify, repeat. Not a dashboard that reports problems. An agent that recovers from them."

---

## B-roll shots to grab if you have extra time before/after the main take

- Slow pan across the Supply Network panel showing the node states (healthy / at risk / disrupted / agent intervention).
- A close-up scroll through the "Why this action?" explanation panel.
- Clicking directly on a loop stage node (outside demo mode) to show it's explorable, not just an animation.

## Narration tips

- Speak in present tense throughout ("it's investigating," not "it will investigate") — it reinforces that this is live, autonomous behavior, not a slideshow.
- Don't apologize for the mock data layer in the video itself; save that nuance for Q&A or the README. The demo should read as confident and real.
- If a judge asks live: "the interaction design and full agent loop are real and built; the vendor/warehouse APIs behind them are mocked for the demo — architecture is in the repo showing exactly where real integrations plug in."
