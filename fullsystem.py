from collections import deque

# =====================================================
# SMART TRAFFIC MANAGEMENT SYSTEM
# =====================================================

# -----------------------------------------------------
# GRAPH
# Road Network (BFS Shortest Path)
# -----------------------------------------------------

road_network = {
    "A": ["B"],
    "B": ["A", "C"],
    "C": ["B", "D"],
    "D": ["C", "E"],
    "E": ["D", "F"],
    "F": ["E", "G"],
    "G": ["F", "H"],
    "H": ["G", "I"],
    "I": ["H", "J"],
    "J": ["I"]
}


def shortest_path(graph, start, end):

    queue = deque([[start]])
    visited = set()

    while queue:

        path = queue.popleft()
        node = path[-1]

        if node == end:
            return path

        if node not in visited:

            visited.add(node)

            for neighbor in graph[node]:
                new_path = list(path)
                new_path.append(neighbor)
                queue.append(new_path)

    return None


# -----------------------------------------------------
# HASH TABLE
# Vehicle Database
# -----------------------------------------------------

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


# -----------------------------------------------------
# TREE
# Traffic Light Decision Tree
# -----------------------------------------------------

def traffic_light(volume, queue_length, emergency):

    if emergency:
        return "Green Light: 60 Seconds"

    if volume.lower() == "high":

        if queue_length.lower() == "long":
            return "Green Light: 50 Seconds"

        else:
            return "Green Light: 35 Seconds"

    return "Green Light: 25 Seconds"


# =====================================================
# MAIN PROGRAM
# =====================================================

print("===== SMART TRAFFIC MANAGEMENT SYSTEM =====")

# ---------------- GRAPH ----------------

print("\nROAD NETWORK")
for stop in road_network:
    print(stop, "->", road_network[stop])

start = input("\nStart Stop (A-J): ").upper()
end = input("Destination Stop (A-J): ").upper()

route = shortest_path(road_network, start, end)

if route:
    print("Shortest Route:", " -> ".join(route))
else:
    print("Route Not Found")

# ---------------- HASH TABLE ----------------

plate = input("\nEnter Vehicle ID: ")

if plate in vehicles:

    print("\nVehicle Information")
    print("Type :", vehicles[plate]["Type"])
    print("Location :", vehicles[plate]["Location"])
    print("Speed :", vehicles[plate]["Speed"], "km/h")

else:
    print("Vehicle Not Found")

# ---------------- TREE ----------------

traffic = input("\nTraffic Volume (High/Low): ")
queue_length = input("Queue Length (Long/Short): ")
emergency = input("Emergency Vehicle (Yes/No): ")

decision = traffic_light(
    traffic,
    queue_length,
    emergency.lower() == "yes"
)

print("\nTraffic Decision")
print(decision)

print("\nSimulation Completed Successfully.")