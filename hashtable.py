# ============================================================
#  HASH TABLE — Vehicle Database
# ============================================================
#  DATA STRUCTURE DEMONSTRATION (DSA)
#  The vehicle registry is a Python DICT. A dict is implemented
#  internally as a HASH TABLE: given a plate number (the key) we
#  can fetch the vehicle record in O(1) average time.
#
#  Location now stores a GRAPH NODE (1-10) so the vehicle's
#  position matches the road-network graph in graph.py.
# ============================================================

vehicles = {

    "2AB-1234": {
        "Type": "Car",
        "Location": 5,
        "Speed": 45
    },

    "V002": {
        "Type": "Motorbike",
        "Location": 6,
        "Speed": 35
    },

    "V003": {
        "Type": "Bus",
        "Location": 8,
        "Speed": 30
    },

    "AMB001": {
        "Type": "Ambulance",
        "Location": 4,
        "Speed": 70
    }
}


def lookup_vehicle(plate):
    """Return the vehicle record for a plate number, or None."""
    return vehicles.get(plate)


if __name__ == "__main__":

    print("===== HASH TABLE (VEHICLE DATABASE) =====")

    vehicle_id = input("Enter Vehicle ID: ")

    record = lookup_vehicle(vehicle_id)

    if record:

        print("\nVehicle Information")
        print("-------------------")
        print("Vehicle ID :", vehicle_id)
        print("Type       :", record["Type"])
        print("Location   : Node", record["Location"])
        print("Speed      :", record["Speed"], "km/h")

    else:
        print("Vehicle Not Found")