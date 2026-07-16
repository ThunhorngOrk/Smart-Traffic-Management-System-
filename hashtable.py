# -----------------------------
# HASH TABLE (Vehicle Database)
# -----------------------------

vehicles = {

    "2AB-1234": {
        "Type": "Car",
        "Location": "Stop 3",
        "Speed": 45
    },

    "1C-5678": {
        "Type": "Motorbike",
        "Location": "Stop 6",
        "Speed": 35
    },

    "3D-9999": {
        "Type": "Bus",
        "Location": "Stop 8",
        "Speed": 30
    },

    "AMB-001": {
        "Type": "Ambulance",
        "Location": "Stop 4",
        "Speed": 70
    }

}

plate = input("Enter Plate Number : ")

if plate in vehicles:

    print("\nVehicle Found\n")

    print("Plate :", plate)
    print("Type :", vehicles[plate]["Type"])
    print("Location :", vehicles[plate]["Location"])
    print("Speed :", vehicles[plate]["Speed"], "km/h")

else:

    print("Vehicle Not Found")