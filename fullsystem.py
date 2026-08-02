"""
========================================================================
 PHNOM PENH SMART TRAFFIC MANAGEMENT SYSTEM
 Graph + Hash Table + Decision Tree (Terminal / DSA Project)
========================================================================

This program demonstrates FOUR core Data Structures & Algorithms concepts,
matching the "Smart Traffic Management System" workflow diagram:

    1. GRAPH        -> road network, represented as an ADJACENCY LIST
    2. DIJKSTRA'S ALGORITHM -> manual shortest-path search on the graph
    3. HASH TABLE    -> instant vehicle lookup by plate number (a Python
                        dict IS a hash table: plate -> vehicle info)
    4. DECISION TREE -> nested if/else logic that decides traffic-light
                        timing from traffic volume, queue length, and
                        whether an emergency vehicle is present

Project structure (all in one file for simplicity, but clearly separated
with section headers):

    SECTION 1: Graph Data              -> NODES, EDGES, build_graph()
    SECTION 2: Dijkstra's Algorithm    -> find_shortest_path()
    SECTION 3: Alternative Route       -> find_alternative_path()
    SECTION 4: Hash Table              -> VEHICLE_DB, lookup/register
    SECTION 5: Decision Tree           -> decide_traffic_light()
    SECTION 6: Camera / Workflow       -> run_traffic_light_control()
    SECTION 7: Display / UI Helpers    -> node_label(), print_route()
    SECTION 8: Input Validation        -> get_valid_node(), etc.
    SECTION 9: Main Program Loop       -> main()
========================================================================
"""

import heapq  # priority queue, used to always expand the closest node first

# ========================================================================
# SECTION 1: GRAPH DATA
# ========================================================================

# The 10 intersections/areas from the Phnom Penh road-network diagram.
NODES = {
    1: "Monivong Intersection",
    2: "Sihanouk Intersection",
    3: "Kampuchea Krom Market",
    4: "Olympic Intersection",
    5: "Orussey Market",
    6: "Royal University Area",
    7: "Railway Station",
    8: "Central Market Intersection",
    9: "Wat Phnom Area",
    10: "Riverside Intersection",
}

# Each road (edge) is bidirectional and has a distance in kilometers.
EDGES = [
    (1, 2, 2.0),
    (2, 3, 5.1),
    (1, 4, 1.9),
    (1, 5, 2.6),
    (2, 5, 1.8),
    (2, 6, 4.3),
    (3, 6, 4.0),
    (4, 5, 2.2),
    (4, 7, 2.8),
    (4, 8, 2.3),
    (5, 6, 2.9),
    (5, 8, 1.4),
    (5, 9, 1.7),
    (6, 10, 1.8),
    (6, 9, 2.7),
    (7, 8, 1.6),
    (8, 9, 1.6),
    (9, 10, 1.5),
]


def build_graph():
    """
    Builds the road network as an ADJACENCY LIST.

    Example shape:
        graph = {
            1: [{"node": 2, "distance": 2.0}, {"node": 4, "distance": 1.9}, ...],
            2: [{"node": 1, "distance": 2.0}, ...],
            ...
        }

    Since roads are bidirectional, every edge (a, b, dist) is added
    in BOTH directions: a -> b and b -> a.
    """
    graph = {node_id: [] for node_id in NODES}
    for a, b, dist in EDGES:
        graph[a].append({"node": b, "distance": dist})
        graph[b].append({"node": a, "distance": dist})
    return graph


GRAPH = build_graph()


# ========================================================================
# SECTION 2: DIJKSTRA'S ALGORITHM (implemented manually)
# ========================================================================

def find_shortest_path(start_node, destination_node, blocked_edges=None):
    """
    Manual implementation of Dijkstra's Shortest Path Algorithm.

    How it works:
      1. Keep a "distance" table: the best known distance from start_node
         to every other node. Start it at infinity for everything except
         the start node itself (distance 0).
      2. Use a min-priority-queue (heap) so we always process the node
         that currently has the smallest known distance next.
      3. For the current node, look at each neighbor via the adjacency
         list. If going through the current node gives a SHORTER path
         to that neighbor than what we already recorded, update it
         ("relaxing" the edge) and remember which node we came from.
      4. Repeat until every reachable node has been finalized.
      5. Walk backwards from the destination using the "previous node"
         table to rebuild the actual path.

    blocked_edges: optional set of frozenset({a, b}) pairs to temporarily
                   ignore. Used by find_alternative_path() to force the
                   algorithm to look for a different route.

    Returns:
        {"path": [2, 5, 6, 10], "distance": 6.5}   on success
        {"path": [], "distance": float("inf")}     if no route exists
    """
    blocked_edges = blocked_edges or set()

    # Step 1: distance table, initialized to infinity for every node.
    distances = {node_id: float("inf") for node_id in NODES}
    distances[start_node] = 0

    # Table to remember the previous node on the shortest path so far,
    # so we can rebuild the full path once we reach the destination.
    previous = {node_id: None for node_id in NODES}

    # Min-heap of (distance_so_far, node_id). Start with the start node.
    priority_queue = [(0, start_node)]
    visited = set()

    while priority_queue:
        current_distance, current_node = heapq.heappop(priority_queue)

        if current_node in visited:
            continue
        visited.add(current_node)

        # Early exit once we've finalized the destination.
        if current_node == destination_node:
            break

        # Step 3: check every road leaving the current intersection.
        for edge in GRAPH[current_node]:
            neighbor = edge["node"]
            road_distance = edge["distance"]

            if frozenset({current_node, neighbor}) in blocked_edges:
                continue  # this road is excluded (used for alternatives)
            if neighbor in visited:
                continue

            new_distance = current_distance + road_distance

            # Relax the edge if we found a shorter path to "neighbor".
            if new_distance < distances[neighbor]:
                distances[neighbor] = new_distance
                previous[neighbor] = current_node
                heapq.heappush(priority_queue, (new_distance, neighbor))

    # Step 5: no path found.
    if distances[destination_node] == float("inf"):
        return {"path": [], "distance": float("inf")}

    # Step 5: rebuild the path by walking backwards from destination.
    path = []
    node = destination_node
    while node is not None:
        path.append(node)
        node = previous[node]
    path.reverse()

    return {"path": path, "distance": round(distances[destination_node], 2)}


# ========================================================================
# SECTION 3: ALTERNATIVE ROUTE
# ========================================================================

def find_alternative_path(start_node, destination_node, best_path):
    """
    Finds a reasonable ALTERNATIVE route (not just the absolute best one).

    Approach: temporarily block every edge used in the best/recommended
    path, then re-run Dijkstra's algorithm on the remaining roads. This
    forces the algorithm to find a genuinely different way through the
    graph, rather than repeating the same recommended route.
    """
    if len(best_path) < 2:
        return None

    blocked = set()
    for i in range(len(best_path) - 1):
        blocked.add(frozenset({best_path[i], best_path[i + 1]}))

    result = find_shortest_path(start_node, destination_node, blocked_edges=blocked)
    if not result["path"] or result["path"] == best_path:
        return None
    return result


# ========================================================================
# SECTION 4: HASH TABLE (Vehicle Information)
# ========================================================================
#
# A HASH TABLE stores key -> value pairs and gives (on average) O(1)
# lookup time. In Python, a dict already IS a hash table under the hood
# (the plate number string is hashed to find its "bucket" instantly),
# so we use one directly instead of re-implementing hashing by hand.
#
#   key   = plate number (string)
#   value = {"type": ..., "location": ..., "speed": ...}

VEHICLE_DB = {
    "2A-1234": {"type": "Car",       "location": 5, "speed": 40},
    "2B-5678": {"type": "Bus",       "location": 2, "speed": 30},
    "2C-9999": {"type": "Truck",     "location": 6, "speed": 25},
    "2D-1111": {"type": "Motorbike", "location": 8, "speed": 35},
    "2E-2222": {"type": "Car",       "location": 1, "speed": 45},
}


def lookup_vehicle(plate):
    """
    O(1) average-time hash table lookup: given a plate number, instantly
    retrieve the vehicle's type, current intersection (node), and speed.
    Returns None if the plate has never been seen before.
    """
    return VEHICLE_DB.get(plate.upper())


def register_vehicle(plate, vehicle_type, location, speed):
    """Adds/updates an entry in the hash table (simulates a camera seeing
    a new vehicle for the first time)."""
    VEHICLE_DB[plate.upper()] = {
        "type": vehicle_type,
        "location": location,
        "speed": speed,
    }


# ========================================================================
# SECTION 5: DECISION TREE (Traffic Light Analysis)
# ========================================================================
#
# A DECISION TREE asks a sequence of yes/no or multi-way questions and
# branches to a final decision. Here it's implemented directly as nested
# if/else statements, mirroring the tree in the diagram:
#
#   Traffic Volume? --High/Low--> Queue Length? --Long/Short--> base timing
#                                                     |
#                                        Emergency Vehicle? --Yes/No-->
#                                          Priority Green / Normal Timing

def decide_traffic_light(traffic_volume, queue_length, emergency_vehicle):
    """
    Walks the decision tree and returns:
        {"duration": 60, "signal": "Normal Timing", "path": [...]}

    traffic_volume:     "high" or "low"
    queue_length:        "long" or "short"
    emergency_vehicle:   True or False
    """
    decision_path = [f"Traffic Volume? -> {traffic_volume.title()}"]

    # Branch 1: Traffic Volume
    if traffic_volume == "high":
        decision_path.append("Queue Length? -> " + queue_length.title())
        # Branch 2: Queue Length (under High volume)
        if queue_length == "long":
            base_duration = 60
        else:  # short
            base_duration = 45
    else:  # low
        decision_path.append("Queue Length? -> " + queue_length.title())
        # Branch 2: Queue Length (under Low volume)
        if queue_length == "long":
            base_duration = 30
        else:  # short
            base_duration = 15

    # Branch 3: Emergency Vehicle override (applies after base timing)
    decision_path.append(f"Emergency Vehicle? -> {'Yes' if emergency_vehicle else 'No'}")
    if emergency_vehicle:
        signal = "Priority Green (Extend Time)"
        duration = base_duration + 20  # extend green light for emergency vehicles
    else:
        signal = "Normal Timing"
        duration = base_duration

    return {"duration": duration, "signal": signal, "path": decision_path}


# ========================================================================
# SECTION 6: CAMERA / TRAFFIC LIGHT WORKFLOW
# ========================================================================
#
# Ties everything together, following the diagram's flow:
#   Camera detects plate -> Hash Table lookup -> Graph (map location)
#   -> Decision Tree -> Traffic Light Decision

def run_traffic_light_control():
    """Simulates the full camera -> hash table -> graph -> decision tree
    -> traffic light pipeline for one detected vehicle."""
    print("\n[1] Camera / Sensor detects a vehicle at an intersection.")
    plate = input("    Enter detected Plate Number (e.g. 2A-1234): ").strip()
    if not plate:
        print("Please enter your vehicle plate number.")
        return

    print("\n[2] Plate Number captured:", plate.upper())

    print("\n[3] Searching Hash Table for vehicle info...")
    info = lookup_vehicle(plate)
    if info is None:
        print("    Plate not found in Hash Table. Let's register it now.")
        vehicle_type = input("    Vehicle type (Car/Bus/Truck/Motorbike): ").strip() or "Car"
        location = get_valid_node("    Current location (node number 1-10): ")
        speed_raw = input("    Speed in km/h: ").strip()
        speed = int(speed_raw) if speed_raw.isdigit() else 0
        register_vehicle(plate, vehicle_type, location, speed)
        info = lookup_vehicle(plate)
    print(f"    Found -> Type: {info['type']}, "
          f"Location: {node_label(info['location'])}, Speed: {info['speed']} km/h")

    print("\n[4] Mapping location on the Graph (Road Network)...")
    print(f"    Vehicle is at {node_label(info['location'])}.")

    print("\n[5] Decision Tree - Traffic Analysis")
    volume = ""
    while volume not in ("high", "low"):
        volume = input("    Traffic volume at this intersection? (high/low): ").strip().lower()

    queue = ""
    while queue not in ("long", "short"):
        queue = input("    Queue length? (long/short): ").strip().lower()

    emergency_raw = input("    Is this an emergency vehicle? (y/n): ").strip().lower()
    emergency = emergency_raw == "y"

    result = decide_traffic_light(volume, queue, emergency)

    print("\n    Decision Tree path:")
    for step in result["path"]:
        print(f"      -> {step}")

    print("\n[6] TRAFFIC LIGHT DECISION")
    print("-" * 72)
    print(f"Vehicle: {plate.upper()} ({info['type']})")
    print(f"Intersection: {node_label(info['location'])}")
    print(f"Signal: {result['signal']}")
    print(f"Green Light Duration: {result['duration']} seconds")
    print("-" * 72)


# ========================================================================
# SECTION 7: DISPLAY / UI HELPERS
# ========================================================================

def node_label(node_id):
    """Formats a node as 'Node 2 - Sihanouk Intersection'."""
    return f"Node {node_id} - {NODES[node_id]}"


def print_route(path):
    """Prints a route as 'Node 2 -> Node 5 -> Node 6 -> Node 10' with arrows."""
    lines = []
    for i, node_id in enumerate(path):
        lines.append(f"   Node {node_id} ({NODES[node_id]})")
        if i != len(path) - 1:
            lines.append("      |")
            lines.append("      v")
    print("\n".join(lines))


def print_header():
    print("=" * 72)
    print("        PHNOM PENH SMART TRAFFIC ROUTE SYSTEM")
    print("        Graph-Based Shortest Path Navigation (Dijkstra's Algorithm)")
    print("=" * 72)


def print_node_list():
    print("\nAvailable Nodes:")
    for node_id, name in NODES.items():
        print(f"  {node_id:>2}. {name}")


# ========================================================================
# SECTION 8: INPUT VALIDATION
# ========================================================================

def get_plate_number():
    while True:
        plate = input("\nEnter Vehicle Plate Number (e.g. 2A-1234): ").strip()
        if not plate:
            print("Please enter your vehicle plate number.")
            continue
        return plate


def get_valid_node(prompt_text):
    while True:
        raw = input(prompt_text).strip()
        if not raw.isdigit() or int(raw) not in NODES:
            print("Please enter a valid node from 1 to 10.")
            continue
        return int(raw)


# ========================================================================
# SECTION 9: MAIN PROGRAM LOOP
# ========================================================================

def run_route_search():
    """Handles one full 'Find Shortest Route' request, end to end."""
    plate = get_plate_number()

    print_node_list()
    start_node = get_valid_node("\nEnter Current Location (node number): ")
    destination_node = get_valid_node("Enter Destination (node number): ")

    if start_node == destination_node:
        print("\nYou are already at your destination.")
        return

    result = find_shortest_path(start_node, destination_node)

    print("\n" + "-" * 72)
    print(f"Vehicle Plate: {plate}")
    print(f"\nFrom:\n  {node_label(start_node)}")
    print(f"\nTo:\n  {node_label(destination_node)}")

    if not result["path"]:
        print("\nNo available route was found between these two nodes.")
        print("-" * 72)
        return

    print("\nRecommended Route:\n")
    print_route(result["path"])
    route_str = " -> ".join(str(n) for n in result["path"])
    print(f"\nShortest Route (node sequence): {route_str}")
    print(f"Total Distance: {result['distance']} km")
    print("\nMessage: Recommended route found.")

    # Alternative route (if one exists that differs from the best route).
    alt = find_alternative_path(start_node, destination_node, result["path"])
    if alt:
        alt_str = " -> ".join(str(n) for n in alt["path"])
        print("\nAlternative Route:\n")
        print_route(alt["path"])
        print(f"\nAlternative Route (node sequence): {alt_str}")
        print(f"Alternative Distance: {alt['distance']} km")
    else:
        print("\nNo distinct alternative route is available for this trip.")

    print("-" * 72)


def print_menu():
    print("\nMAIN MENU")
    print("  1. Find Shortest Route (Graph + Dijkstra)")
    print("  2. Traffic Light Control (Camera + Hash Table + Decision Tree)")
    print("  3. Exit")


def main():
    print_header()
    while True:
        print_menu()
        choice = input("Choose an option (1-3): ").strip()

        if choice == "1":
            run_route_search()
        elif choice == "2":
            run_traffic_light_control()
        elif choice == "3":
            print("\nThank you for using the Smart Traffic Management System. Drive safe!")
            break
        else:
            print("Please choose 1, 2, or 3.")


if __name__ == "__main__":
    main()
