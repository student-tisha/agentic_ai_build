"""
mock_data.py
------------
This file holds all the FAKE (mock) data that pretends to be a real
supply chain. Nothing here is "smart" - it's just data sitting in
Python dictionaries and lists, the way a spreadsheet holds data in
rows and columns.

Tisha's agent logic will read and change this data.
Sankur's UI will display this data.
"""

# ---------------------------------------------------------------------
# 1. INVENTORY: how much of each item sits in each warehouse right now
# ---------------------------------------------------------------------
inventory = {
    "WH1": {"item_A": 120, "item_B": 40, "item_C": 15},
    "WH2": {"item_A": 30,  "item_B": 90, "item_C": 60},
    "WH3": {"item_A": 5,   "item_B": 10, "item_C": 200},
}

# ---------------------------------------------------------------------
# 2. SHIPMENTS: items currently on the move between locations
# ---------------------------------------------------------------------
shipments = [
    {
        "shipment_id": "SHIP-001",
        "item": "item_A",
        "from": "VendorX",
        "to": "WH1",
        "qty": 50,
        "route_id": "R1",
        "status": "in_transit",   # in_transit | delayed | delivered | cancelled
        "eta_days": 3,
    },
    {
        "shipment_id": "SHIP-002",
        "item": "item_B",
        "from": "VendorY",
        "to": "WH2",
        "qty": 20,
        "route_id": "R2",
        "status": "in_transit",
        "eta_days": 5,
    },
]

# ---------------------------------------------------------------------
# 3. VENDORS: who can supply each item, and at what cost/speed/carbon
# ---------------------------------------------------------------------
vendors = {
    "item_A": [
        {"vendor_id": "VendorX",  "price_per_unit": 10.0, "lead_time_days": 3, "carbon_kg_per_unit": 2.0},
        {"vendor_id": "VendorX2", "price_per_unit": 11.5, "lead_time_days": 2, "carbon_kg_per_unit": 1.5},
        {"vendor_id": "VendorX3", "price_per_unit": 9.0,  "lead_time_days": 6, "carbon_kg_per_unit": 3.2},
    ],
    "item_B": [
        {"vendor_id": "VendorY",  "price_per_unit": 7.0,  "lead_time_days": 5, "carbon_kg_per_unit": 1.0},
        {"vendor_id": "VendorY2", "price_per_unit": 8.2,  "lead_time_days": 3, "carbon_kg_per_unit": 0.8},
    ],
    "item_C": [
        {"vendor_id": "VendorZ",  "price_per_unit": 4.5,  "lead_time_days": 4, "carbon_kg_per_unit": 0.5},
        {"vendor_id": "VendorZ2", "price_per_unit": 4.0,  "lead_time_days": 7, "carbon_kg_per_unit": 1.2},
    ],
}

# ---------------------------------------------------------------------
# 4. ROUTES: alternative shipping routes between locations
# ---------------------------------------------------------------------
routes = [
    {"route_id": "R1", "from": "VendorX", "to": "WH1", "price": 100.0, "lead_time_days": 3, "carbon_kg": 40.0},
    {"route_id": "R1B", "from": "VendorX", "to": "WH1", "price": 140.0, "lead_time_days": 1, "carbon_kg": 70.0},
    {"route_id": "R2", "from": "VendorY", "to": "WH2", "price": 80.0, "lead_time_days": 5, "carbon_kg": 25.0},
    {"route_id": "R2B", "from": "VendorY", "to": "WH2", "price": 120.0, "lead_time_days": 2, "carbon_kg": 55.0},
    {"route_id": "R3", "from": "WH2", "to": "WH1", "price": 30.0, "lead_time_days": 1, "carbon_kg": 10.0},
    {"route_id": "R4", "from": "WH3", "to": "WH1", "price": 45.0, "lead_time_days": 2, "carbon_kg": 15.0},
]
