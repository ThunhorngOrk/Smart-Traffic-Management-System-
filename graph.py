#  GRAPH DATA — Phnom Penh Road Network
#  DATA STRUCTURE DEMONSTRATION (DSA)
#  Each road intersection is a NODE (vertex) of the graph.
#  Each road connecting two intersections is an EDGE with a
#  distance measured in kilometres.
#
#  The network is stored as an ADJACENCY LIST so that for every
#  node we instantly know which neighbouring nodes it connects
#  to and the cost (distance) of travelling along that road.
#
#  Example format (as requested in the project brief):
#
#      graph = {
#         1: [{"node": 2, "distance": 2.0},
#             {"node": 4, "distance": 1.9},
#             {"node": 5, "distance": 2.6}],
#         ...
#      }
#
#  All roads are treated as BIDIRECTIONAL, so every edge is
#  inserted into the adjacency list of BOTH endpoints.
# ============================================================

# ------------------------------------------------------------
#  NODES (intersections / areas)
#  Each key is a node number, each value is the display name.
# ------------------------------------------------------------
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

# ------------------------------------------------------------
#  EDGES (roads)
#  Each tuple is: (from_node, to_node, distance_in_km)
# ------------------------------------------------------------
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


def build_adjacency_list():
    """Build the adjacency-list graph from NODES and EDGES.

    Because the roads are bidirectional, each edge is added to
    the adjacency list of BOTH endpoints.
    """
    # Start with an empty list of neighbours for every node.
    graph = {}
    for node_id in NODES:
        graph[node_id] = []

    # Insert every road in both directions.
    for from_id, to_id, distance in EDGES:
        graph[from_id].append({"node": to_id, "distance": distance})
        graph[to_id].append({"node": from_id, "distance": distance})

    return graph


# Ready-to-use graph object shared by dijkstra.py and app.py.
GRAPH = build_adjacency_list()
