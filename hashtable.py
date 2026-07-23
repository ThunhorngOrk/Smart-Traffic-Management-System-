# -----------------------------
# HASH TABLE (Vehicle Database)
# -----------------------------

vehicles = {

    "V001": {
        "Type": "Car",
        "Location": "E",
        "Speed": 45
    },

    "V002": {
        "Type": "Motorbike",
        "Location": "F",
        "Speed": 35
    },

    "V003": {
        "Type": "Bus",
        "Location": "H",
        "Speed": 30
    },

    "AMB001": {
        "Type": "Ambulance",
        "Location": "D",
        "Speed": 70
    }
}

# -----------------------------
# Search Vehicle
# -----------------------------

vehicle_id = input("Enter Vehicle ID: ")

if vehicle_id in vehicles:

    print("\nVehicle Information")
    print("-------------------")
    print("Vehicle ID :", vehicle_id)
    print("Type       :", vehicles[vehicle_id]["Type"])
    print("Location   :", vehicles[vehicle_id]["Location"])
    print("Speed      :", vehicles[vehicle_id]["Speed"], "km/h")

else:
    print("Vehicle Not Found")