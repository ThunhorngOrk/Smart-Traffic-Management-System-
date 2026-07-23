from collections import deque

# -----------------------------
# GRAPH (Road Network)
# -----------------------------

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

# -----------------------------
# BFS Shortest Path
# -----------------------------

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


# -----------------------------
# Display Graph
# -----------------------------

print("===== ROAD NETWORK GRAPH =====")

for junction in road_network:
    print(junction, "->", road_network[junction])

# -----------------------------
# Route Search
# -----------------------------

start = input("\nEnter Start Junction (A-J): ").upper()
end = input("Enter Destination Junction (A-J): ").upper()

route = shortest_path(road_network, start, end)

if route:
    print("\nShortest Route:")
    print(" -> ".join(route))
else:
    print("Route Not Found")