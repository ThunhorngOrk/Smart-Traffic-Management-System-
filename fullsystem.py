# ============================================================
#  PHNOM PENH SMART TRAFFIC ROUTE SYSTEM — COMBINED CONSOLE
# ============================================================
#  DATA STRUCTURES DEMONSTRATION (DSA)
#
#  This single program brings together all three data
#  structures used in the project:
#
#    1. GRAPH      -> Road Network (graph.py + dijkstra.py)
#    2. HASH TABLE -> Vehicle Data (hashtable.py)
#    3. TREE       -> Traffic Light Decision (tree.py)
#
#  Run it with:  python fullsystem.py
# ============================================================

from graph import NODES, EDGES, GRAPH
from dijkstra import dijkstra
from hashtable import vehicles, lookup_vehicle
from tree import traffic_light


def show_header():
    print()
    print("=============================================")
    print("  PHNOM PENH SMART TRAFFIC ROUTE SYSTEM")
    print("  Graph + Hash Table + Tree (DSA Project)")
    print("=============================================")


# ------------------------------------------------------------
#  1. GRAPH  ->  ROAD NETWORK
# ------------------------------------------------------------
def demo_graph():
    print()
    print("----- 1. GRAPH : ROAD NETWORK -----")

    print("\nRoads (EDGES):")
    for from_id, to_id, distance in EDGES:
        print("  Node {:<2} <-> Node {:<2}  {} km".format(
            from_id, to_id, distance))

    start = input("\nStart Node (1-10): ")
    dest = input("Destination Node (1-10): ")

    if not (start.isdigit() and dest.isdigit()):
        print("Invalid input. Numbers only.")
        return
    start, dest = int(start), int(dest)

    if start not in GRAPH or dest not in GRAPH:
        print("Invalid node. Choose from 1 to 10.")
        return
    if start == dest:
        print("Start and destination are the same node.")
        return

    result = dijkstra(GRAPH, start, dest)

    if result is None:
        print("No route could be found.")
        return

    path = result["path"]
    print("\nShortest Route (Dijkstra):")
    for i, node_id in enumerate(path):
        marker = " -> " if i < len(path) - 1 else ""
        print("  Node {} ({}){}".format(node_id, NODES[node_id], marker),
              end=" ")
    print()
    print("Total Distance: {:.1f} km".format(result["distance"]))


# ------------------------------------------------------------
#  2. HASH TABLE  ->  VEHICLE DATA
# ------------------------------------------------------------
def demo_hashtable():
    print()
    print("----- 2. HASH TABLE : VEHICLE DATA -----")

    plate = input("\nEnter Vehicle Plate / ID: ").upper().strip()

    record = lookup_vehicle(plate)

    if record is None:
        print("Vehicle Not Found.")
        return

    print("\nVehicle Information")
    print("-------------------")
    print("Vehicle ID :", plate)
    print("Type       :", record["Type"])
    print("Location   : Node {} - {}".format(
        record["Location"], NODES[record["Location"]]))
    print("Speed      :", record["Speed"], "km/h")


# ------------------------------------------------------------
#  3. TREE  ->  TRAFFIC LIGHT DECISION
# ------------------------------------------------------------
def demo_tree():
    print()
    print("----- 3. TREE : TRAFFIC LIGHT DECISION -----")

    volume = input("\nTraffic Volume (High/Low): ")
    queue = input("Queue Length (Long/Short): ")
    emergency = input("Emergency Vehicle (Yes/No): ")

    decision = traffic_light(volume, queue, emergency.lower() == "yes")

    print("\nTraffic Decision")
    print("----------------")
    print(decision)


# ------------------------------------------------------------
#  MAIN MENU
# ------------------------------------------------------------
def main():

    show_header()

    while True:
        print()
        print("  MAIN MENU")
        print("  1. Graph      -> Road Network")
        print("  2. Hash Table -> Vehicle Data")
        print("  3. Tree       -> Traffic Light Decision")
        print("  4. Exit")

        choice = input("Choose an option: ").strip()

        if choice == "1":
            demo_graph()
        elif choice == "2":
            demo_hashtable()
        elif choice == "3":
            demo_tree()
        elif choice == "4":
            print("\nGoodbye!")
            break
        else:
            print("Invalid choice. Try again.")


if __name__ == "__main__":
    main()
