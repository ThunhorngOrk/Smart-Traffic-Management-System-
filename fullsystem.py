from collections import deque

# -----------------------------
# GRAPH
# -----------------------------

road_network = {
    "Stop 1": ["Stop 2"],
    "Stop 2": ["Stop 1", "Stop 3"],
    "Stop 3": ["Stop 2", "Stop 4"],
    "Stop 4": ["Stop 3", "Stop 5"],
    "Stop 5": ["Stop 4", "Stop 6"],
    "Stop 6": ["Stop 5", "Stop 7"],
    "Stop 7": ["Stop 6", "Stop 8"],
    "Stop 8": ["Stop 7", "Stop 9"],
    "Stop 9": ["Stop 8", "Stop 10"],
    "Stop 10": ["Stop 9"]
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

            for neighbour in graph[node]:
                new_path = list(path)
                new_path.append(neighbour)
                queue.append(new_path)

    return None


# -----------------------------
# HASH TABLE
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


# -----------------------------
# TREE
# -----------------------------

def traffic_light(volume, queue, emergency):

    if emergency:

        return "Green Light : 60 Seconds"

    if volume.lower() == "high":

        if queue.lower() == "long":

            return "Green Light : 50 Seconds"

        else:

            return "Green Light : 35 Seconds"

    return "Green Light : 25 Seconds"


# -----------------------------
# MAIN PROGRAM
# -----------------------------

print("===== SMART TRAFFIC MANAGEMENT SYSTEM =====")

print("\nRoad Network")
for stop in road_network:
    print(stop, "->", road_network[stop])

plate = input("\nEnter Plate Number : ")

if plate in vehicles:

    print("\nVehicle Information")
    print(vehicles[plate])

else:

    print("Vehicle Not Found")

start = input("\nStart Stop : ")
end = input("Destination Stop : ")

route = shortest_path(road_network, start, end)

if route:
    print("Shortest Route :", " -> ".join(route))
else:
    print("Route Not Found")

traffic = input("\nTraffic Volume (High/Low): ")
queue = input("Queue Length (Long/Short): ")
emergency = input("Emergency Vehicle (Yes/No): ")

result = traffic_light(
    traffic,
    queue,
    emergency.lower() == "yes"
)

print("\nTraffic Decision")
print(result)

print("\nSimulation Completed Successfully.")