"""
test_tools.py
-------------
Run this file to prove each tool works correctly on its own.
It just calls each function once and prints BEFORE and AFTER,
so you can eyeball that the data actually changed the way it should.

HOW TO RUN:
    python test_tools.py
(from inside this same folder)
"""

import mock_data as data
from tools import (
    execute_reroute,
    execute_vendor_switch,
    execute_warehouse_transfer,
    verify_state,
)


def line():
    print("-" * 60)


print("STARTING STATE")
line()
print(verify_state())

print("\n\nTEST 1: execute_reroute")
line()
print("Moving SHIP-001 onto route R1B (faster, pricier route)")
result = execute_reroute("SHIP-001", "R1B")
print("Result:", result)

print("\n\nTEST 2: execute_vendor_switch")
line()
print("Switching item_B supply (for WH2) to VendorY2, qty=15")
result = execute_vendor_switch("item_B", "WH2", "VendorY2", 15)
print("Result:", result)

print("\n\nTEST 3: execute_warehouse_transfer")
line()
print("Transferring 50 units of item_C from WH3 to WH1")
result = execute_warehouse_transfer("item_C", "WH3", "WH1", 50)
print("Result:", result)

print("\n\nTEST 4: verify_state (final check)")
line()
print(verify_state())

print("\n\nIf you see updated numbers above (not errors), all 4 tools work.")
