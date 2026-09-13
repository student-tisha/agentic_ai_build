import json
import os
from groq import Groq

import mock_data as data
import tools

client = Groq(api_key=os.environ.get("GROQ_API_KEY"))
MODEL = "openai/gpt-oss-120b"

BLOCKED_OPTIONS = [
    {"type": "reroute", "id": "R1B"},
    {"type": "vendor_switch", "id": "VendorX2"},
]


def score_option(price, lead_time_days, carbon,
                  cost_weight=1.0, time_weight=50.0, carbon_weight=5.0):
    return (price * cost_weight) + (lead_time_days * time_weight) + (carbon * carbon_weight)


def get_shipment(shipment_id):
    for s in data.shipments:
        if s["shipment_id"] == shipment_id:
            return s
    return None


def detect_disruption(shipment):
    if shipment["status"] == "delayed":
        return {"disrupted": True, "reason": "shipment_delayed"}
    return {"disrupted": False, "reason": None}


def build_candidate_options(shipment):
    options = []

    for r in data.routes:
        if r["from"] == shipment["from"] and r["to"] == shipment["to"] and r["route_id"] != shipment["route_id"]:
            options.append({
                "type": "reroute", "id": r["route_id"],
                "price": r["price"], "lead_time_days": r["lead_time_days"], "carbon": r["carbon_kg"],
            })

    for v in data.vendors.get(shipment["item"], []):
        if v["vendor_id"] != shipment["from"]:
            options.append({
                "type": "vendor_switch", "id": v["vendor_id"],
                "price": v["price_per_unit"] * shipment["qty"],
                "lead_time_days": v["lead_time_days"],
                "carbon": v["carbon_kg_per_unit"] * shipment["qty"],
            })

    for wh, items in data.inventory.items():
        stock = items.get(shipment["item"], 0)
        if wh != shipment["to"] and stock >= shipment["qty"]:
            route = next((r for r in data.routes if r["from"] == wh and r["to"] == shipment["to"]), None)
            if route:
                options.append({
                    "type": "warehouse_transfer", "id": wh,
                    "price": route["price"], "lead_time_days": route["lead_time_days"], "carbon": route["carbon_kg"],
                })

    return options


def decide(disruption, candidate_options, failed_options):
    candidate_options = [
        opt for opt in candidate_options
        if not any(opt["type"] == f["type"] and opt["id"] == f["id"] for f in failed_options)
    ]
    if not candidate_options:
        return {"action_type": "escalate", "target_id": None, "reasoning": "No viable options remain."}

    scored = [{**o, "score": score_option(o["price"], o["lead_time_days"], o["carbon"])} for o in candidate_options]
    scored.sort(key=lambda x: x["score"])
    best = scored[0]

    system = (
        "You are a supply chain recovery assistant. Given a disruption and the "
        "best-scored recovery option, write a short 1-2 sentence justification. "
        "Respond ONLY as JSON: {\"reasoning\": str}"
    )
    user = json.dumps({"disruption": disruption, "chosen_option": best})
    try:
        response = client.chat.completions.create(
            model=MODEL,
            messages=[{"role": "system", "content": system}, {"role": "user", "content": user}],
            temperature=0.2,
            response_format={"type": "json_object"},
        )
        reasoning = json.loads(response.choices[0].message.content).get("reasoning", "")
    except Exception:
        reasoning = "Selected based on lowest combined price/time/carbon score."

    return {"action_type": best["type"], "target_id": best["id"], "reasoning": reasoning}


def act(shipment, action_type, target_id):
    if action_type == "reroute":
        return tools.execute_reroute(shipment["shipment_id"], target_id)
    if action_type == "vendor_switch":
        return tools.execute_vendor_switch(shipment["item"], shipment["to"], target_id, shipment["qty"])
    if action_type == "warehouse_transfer":
        return tools.execute_warehouse_transfer(shipment["item"], target_id, shipment["to"], shipment["qty"])
    return {"success": False, "error": "unknown_action"}


def evaluate(act_result, blocked_check):
    if blocked_check:
        return {"verified": False, "reason": "blocked_for_demo"}
    if not act_result.get("success"):
        return {"verified": False, "reason": act_result.get("error")}
    return {"verified": True}


def resolve_disruption(shipment_id, max_attempts=4):
    trace = []
    shipment = get_shipment(shipment_id)
    disruption = detect_disruption(shipment)
    trace.append({"step": "observe+detect", "data": disruption})

    if not disruption["disrupted"]:
        return {"resolved": True, "final_outcome": "no_action_needed", "trace": trace}

    candidate_options = build_candidate_options(shipment)
    failed_options = []

    for attempt in range(1, max_attempts + 1):
        decision = decide(disruption, candidate_options, failed_options)
        trace.append({"step": f"decide (attempt {attempt})", "data": decision})

        if decision["action_type"] == "escalate":
            return {"resolved": False, "final_outcome": "escalate", "trace": trace}

        is_demo_blocked = any(
            b["type"] == decision["action_type"] and b["id"] == decision["target_id"] for b in BLOCKED_OPTIONS
        )
        if is_demo_blocked:
            act_result = {"success": False, "error": "unavailable_for_demo"}
        else:
            act_result = act(shipment, decision["action_type"], decision["target_id"])
        trace.append({"step": f"act (attempt {attempt})", "data": act_result})

        eval_result = evaluate(act_result, is_demo_blocked)
        trace.append({"step": f"evaluate (attempt {attempt})", "data": eval_result})

        if eval_result["verified"]:
            return {"resolved": True, "final_outcome": decision, "attempts": attempt, "trace": trace}

        failed_options.append({"type": decision["action_type"], "id": decision["target_id"]})
        trace.append({"step": f"adapt (attempt {attempt})", "data": failed_options[-1]})

    return {"resolved": False, "final_outcome": "escalate", "trace": trace}

def reset_demo():
    data.shipments.clear()
    data.shipments.extend([
        {
            "shipment_id": "SHIP-001", "item": "item_A", "from": "VendorX", "to": "WH1",
            "qty": 50, "route_id": "R1", "status": "in_transit", "eta_days": 3,
        },
        {
            "shipment_id": "SHIP-002", "item": "item_B", "from": "VendorY", "to": "WH2",
            "qty": 20, "route_id": "R2", "status": "in_transit", "eta_days": 5,
        },
    ])
    data.inventory["WH1"] = {"item_A": 120, "item_B": 40, "item_C": 15}
    data.inventory["WH2"] = {"item_A": 30, "item_B": 90, "item_C": 60}
    data.inventory["WH3"] = {"item_A": 5, "item_B": 10, "item_C": 200}

if __name__ == "__main__":
    data.shipments[0]["status"] = "delayed"
    result = resolve_disruption("SHIP-001")
    print(json.dumps(result, indent=2))