"""
tools.py
--------
These are the 4 "action" functions. Each one CHANGES the mock data
in mock_data.py, the same way clicking "confirm" on a food delivery
app changes an order's status in a database.

Tisha's agent will call these functions when it decides on a recovery
action. Your job is just to make sure each one works correctly by
itself - you don't need any scoring/decision logic here.
"""

import mock_data as data


def execute_reroute(shipment_id, new_route_id):
    """
    Move a shipment onto a different route (e.g. a faster but pricier
    route, or a slower but cheaper one).
    Returns the updated shipment record, or an error message.
    """
    # 1. find the shipment
    shipment = None
    for s in data.shipments:
        if s["shipment_id"] == shipment_id:
            shipment = s
            break
    if shipment is None:
        return {"success": False, "error": f"No shipment found with id {shipment_id}"}

    # 2. find the new route
    new_route = None
    for r in data.routes:
        if r["route_id"] == new_route_id:
            new_route = r
            break
    if new_route is None:
        return {"success": False, "error": f"No route found with id {new_route_id}"}

    # 3. apply the change
    shipment["route_id"] = new_route["route_id"]
    shipment["eta_days"] = new_route["lead_time_days"]
    shipment["status"] = "in_transit"

    return {"success": True, "updated_shipment": shipment}


def execute_vendor_switch(item, warehouse, new_vendor_id, qty):
    """
    Cancel/replace the source of an item with a different vendor.
    Creates a brand new shipment coming from the new vendor.
    """
    # 1. find the vendor for this item
    vendor_list = data.vendors.get(item, [])
    new_vendor = None
    for v in vendor_list:
        if v["vendor_id"] == new_vendor_id:
            new_vendor = v
            break
    if new_vendor is None:
        return {"success": False, "error": f"No vendor {new_vendor_id} found for {item}"}

    # 2. build a brand-new shipment from that vendor
    new_shipment_id = f"SHIP-{len(data.shipments) + 1:03d}"
    new_shipment = {
        "shipment_id": new_shipment_id,
        "item": item,
        "from": new_vendor_id,
        "to": warehouse,
        "qty": qty,
        "route_id": None,
        "status": "in_transit",
        "eta_days": new_vendor["lead_time_days"],
    }
    data.shipments.append(new_shipment)

    return {"success": True, "new_shipment": new_shipment}


def execute_warehouse_transfer(item, from_warehouse, to_warehouse, qty):
    """
    Move stock of an item from one warehouse to another
    (e.g. borrowing stock from a warehouse that has plenty).
    """
    from_stock = data.inventory.get(from_warehouse, {}).get(item, 0)
    if from_stock < qty:
        return {
            "success": False,
            "error": f"{from_warehouse} only has {from_stock} of {item}, cannot transfer {qty}",
        }

    # subtract from source
    data.inventory[from_warehouse][item] -= qty
    # add to destination (create the entry if it doesn't exist yet)
    data.inventory.setdefault(to_warehouse, {})
    data.inventory[to_warehouse][item] = data.inventory[to_warehouse].get(item, 0) + qty

    return {
        "success": True,
        "from_warehouse_new_qty": data.inventory[from_warehouse][item],
        "to_warehouse_new_qty": data.inventory[to_warehouse][item],
    }


def verify_state():
    """
    Take a snapshot of the current inventory and shipments so the
    agent (or a human) can check what the world looks like right now.
    """
    return {
        "inventory": data.inventory,
        "shipments": data.shipments,
    }