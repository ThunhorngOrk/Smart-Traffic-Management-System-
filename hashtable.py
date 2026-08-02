# ============================================================
#  HASH TABLE — Vehicle Database
# ============================================================
#  DATA STRUCTURE DEMONSTRATION (DSA)
#  The vehicle registry is a Python DICT. A dict is implemented
#  internally as a HASH TABLE: given a plate number (the key) we
#  can fetch the vehicle record in O(1) average time.
#
#  Location stores a GRAPH NODE (1-10) so the vehicle's position
#  matches the road-network graph in graph.py.
#
#  The same data is used by the web app (app.py -> /api/traffic)
#  and matches the combined terminal program (fullsystem.py).
# ============================================================

vehicles = {
    "2A-1234": {"type": "Car",       "location": 5, "speed": 40},
    "2B-5678": {"type": "Bus",       "location": 2, "speed": 30},
    "2C-9999": {"type": "Truck",     "location": 6, "speed": 25},
    "2D-1111": {"type": "Motorbike", "location": 8, "speed": 35},
    "2E-2222": {"type": "Car",       "location": 1, "speed": 45},
}


def lookup_vehicle(plate):
    """O(1) average-time hash table lookup. Returns the vehicle record
    (dict with 'type', 'location', 'speed') or None if the plate has
    never been seen before. Plate numbers are matched case-insensitively."""
    return vehicles.get(plate.upper())


def register_vehicle(plate, vehicle_type, location, speed):
    """Adds/updates an entry in the hash table (simulates a camera
    detecting a new vehicle for the first time)."""
    vehicles[plate.upper()] = {
        "type": vehicle_type,
        "location": location,
        "speed": speed,
    }


if __name__ == "__main__":

    print("===== HASH TABLE (VEHICLE DATABASE) =====")

    vehicle_id = input("Enter Vehicle ID (e.g. 2A-1234): ")

    record = lookup_vehicle(vehicle_id)

    if record:

        print("\nVehicle Information")
        print("-------------------")
        print("Vehicle ID :", vehicle_id.upper())
        print("Type       :", record["type"])
        print("Location   : Node", record["location"])
        print("Speed      :", record["speed"], "km/h")

    else:
        print("Vehicle Not Found")
