# NEXUS — Autonomous Retail Supply Chain Recovery Agent

**Problem Statement 6 · Hackathon submission**

A dashboard tells you a shipment is late. NEXUS notices, investigates alternatives, weighs cost against delivery time and carbon, fixes it, and checks its own work — on a loop that never stops.

---

## What's in this folder

| File | What it is |
|---|---|
| `index.html` | The full interactive dashboard — open it directly in any browser, no build step, no dependencies to install. |
| `PROBLEM_SOLUTION_BRIEF.md` | The problem statement, why it needs an agent rather than a dashboard, and the solution walkthrough. |
| `ARCHITECTURE.md` | System architecture with a Mermaid diagram and component-by-component breakdown. |
| `architecture-diagram.svg` | Standalone rendered version of the architecture diagram (opens in any browser/image viewer). |
| `DEMO_VIDEO_SCRIPT.md` | A shot-by-shot narration script for recording the demo video. |

## Running it

**Simplest — just open the file:**

1. Unzip this folder.
2. Double-click `index.html`, or open it in Chrome/Edge/Firefox.
3. Click **Run Autonomous Recovery** at the top of the page.

This covers everything except the optional Live AI Groq feature, which some browsers block when a page is opened directly from disk (`file://`) rather than served over `http://`.

**For a real localhost (and to make the Live AI feature work reliably):**

```powershell
cd agentic-ai
npm start
```
Then open **http://localhost:3000** in your browser.

There's nothing to install — `npm start` runs a small zero-dependency static server (`server.js`, using only Node's built-in `http` module). If you'd rather not use Node at all, Python works too:

```bash
cd agentic-ai
python3 -m http.server 8000
# then open http://localhost:8000
```


## What to look at first

1. **Run Autonomous Recovery** (top of the page) — plays the full 10-step loop automatically in under a minute: monitor → disruption → investigate → alternatives → decision → action → verify → monitor again → next disruption.
2. **Autonomous Recovery Loop** section — click any of the 8 stage nodes to jump straight to it and inspect the detail panel underneath.
3. **Disruption Panel** — the three disruptions the agent is currently tracking, each with its own severity, blast radius, and agent status.
4. **Agent Activity feed** — a live-updating log that fills in as the demo runs.
5. **Why this action?** — the plain-language explanation and confidence score behind the agent's decision, not a black box.

## Optional: live AI reasoning

The **Decision** stage of the loop has a "Connect" field where you can paste a [Groq](https://console.groq.com/keys) API key to have the agent's explanation ("why this action?") generated live by `llama-3.3-70b-versatile`, instead of showing the static demo copy.

This is deliberately **not hardcoded into the file**:
- The key lives only in a JS variable for the current page load — it's never written to disk, never saved to `localStorage`, and it isn't committed anywhere in this repo.
- It's sent directly from your browser to `api.groq.com` and nowhere else.
- Leave the field blank and the dashboard works exactly the same, just with the pre-written demo explanation.

**If you're pushing this to a public repo for judging: never paste a real key into the HTML source itself.** Get a fresh key from the Groq console right before the demo, type it into the field live, and treat any key that's ever touched a chat log, a commit, or a screen-share as compromised — rotate it afterward.

## What's real vs. simulated in this build

This is a **frontend-first hackathon build**. The interaction design, the 8-stage loop, the decision-weighting visualization, the demo sequencing, and every screen are fully built and interactive. The vendor/warehouse/routing/inventory systems behind them are a mock data layer shaped to match what a real backend would emit — see `ARCHITECTURE.md` for exactly how a real backend would slot in without changing the frontend.

## Tech

Plain HTML, CSS, and vanilla JavaScript — one file, zero dependencies, zero build step. Chosen deliberately for a hackathon: it opens instantly on any judge's laptop, survives a spotty venue Wi-Fi, and there's nothing to `npm install` five minutes before a demo slot.

## Team notes

- Color system, type system, and component list are documented inline in `index.html` — see the CSS custom properties at the top of the `<style>` block.
- If you extend this: the mock data objects (`STAGES`, `DISRUPTIONS`, `ALTS`, `NETWORK`, `DEMO_STEPS`) are all in one place near the top of the `<script>` block, so adding a new disruption scenario doesn't require touching any rendering code.


## Quick Start (Recommended)

```bash
pip install -r requirements.txt
pip install flask flask-cors
export GROQ_API_KEY="your_key_here"   # get one free at console.groq.com
python run_all.py
```

This automatically starts both the backend and frontend, and opens the demo in your browser at `http://localhost:8000/index.html`.