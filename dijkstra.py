# ============================================================
#  DIJKSTRA'S ALGORITHM
# ============================================================
#  DSA DEMONSTRATION
#  -----------------------------------
#  Dijkstra's algorithm finds the SHORTEST path from one starting
#  node to every other node in a weighted graph where all edge
#  weights are non-negative (our road distances are always >= 0).
#
#  Core idea:
#    1. Give the starting node a tentative distance of 0 and every
#       other node a tentative distance of infinity.
#    2. Repeatedly pick the UNVISITED node with the SMALLEST
#       tentative distance (this is where a Min-Heap speeds things
#       up - it is a manual implementation, no library is used).
#    3. For that node, inspect every neighbour. If travelling
#       through the current node gives the neighbour a SHORTER
#       distance than what we recorded before, update the
#       neighbour's distance and remember which node we came from
#       (the "previous" pointer). This step is called RELAXATION.
#    4. Mark the current node as visited - its best distance is now
#       final, because all remaining unvisited nodes are farther away.
#    5. Repeat until every node is visited or the destination is
#       reached.
#
#  Finally we reconstruct the path by following the "previous"
#  pointers backwards from the destination to the start.
# ============================================================


# ------------------------------------------------------------
#  MIN-HEAP (binary heap used as a priority queue)
#  ------------------------------------------------------------
#  Stores (priority, value) pairs. The pair with the smallest
#  priority is always popped first. We implement it by hand so
#  the whole algorithm is built manually for the DSA project.
# ------------------------------------------------------------
class MinHeap:
    def __init__(self):
        self.items = []  # the heap stored in a list/array

    def push(self, priority, value):
        """Insert a new item and bubble it up to the correct place."""
        self.items.append((priority, value))

        index = len(self.items) - 1
        # Bubble up while the parent has a larger priority.
        while index > 0:
            parent = (index - 1) // 2
            if self.items[parent][0] <= self.items[index][0]:
                break
            # Swap child with parent.
            self.items[parent], self.items[index] = (
                self.items[index],
                self.items[parent],
            )
            index = parent

    def pop(self):
        """Remove and return the item with the smallest priority."""
        if not self.items:
            return None

        top = self.items[0]
        last = self.items.pop()

        # If the heap still has items, move the last one to the top
        # and sift it down until the heap order is restored.
        if self.items:
            self.items[0] = last
            self._sift_down(0)

        return top

    def _sift_down(self, index):
        """Restore heap order by moving an item down the tree."""
        size = len(self.items)

        while True:
            smallest = index
            left = 2 * index + 1
            right = 2 * index + 2

            if left < size and self.items[left][0] < self.items[smallest][0]:
                smallest = left
            if right < size and self.items[right][0] < self.items[smallest][0]:
                smallest = right

            if smallest == index:
                break

            self.items[index], self.items[smallest] = (
                self.items[smallest],
                self.items[index],
            )
            index = smallest

    def is_empty(self):
        return len(self.items) == 0


# ------------------------------------------------------------
#  DIJKSTRA — main shortest-path function
#  ------------------------------------------------------------
#  graph : adjacency-list dict built in graph.py
#  start : starting node id
#  end   : destination node id
#
#  Returns:
#      {"path": [node_id, ...], "distance": km}
#  or None if the destination cannot be reached.
# ------------------------------------------------------------
def dijkstra(graph, start, end):
    # 1. INITIALISE distances and previous pointers.
    #    distances = best known distance to every node.
    #    previous  = which node we came from (used to rebuild path).
    distances = {}
    previous = {}
    visited = {}

    for node_id in graph:
        distances[node_id] = float("inf")
        previous[node_id] = None

    distances[start] = 0  # distance from start to itself is 0

    priority_queue = MinHeap()
    priority_queue.push(0, start)

    # 2. MAIN LOOP — process nodes in order of increasing distance.
    while not priority_queue.is_empty():
        current_dist, node_id = priority_queue.pop()

        # Skip nodes we already finalised with a shorter distance.
        if visited.get(node_id):
            continue
        visited[node_id] = True

        # We can stop as soon as the destination is finalised,
        # because its distance can no longer get smaller.
        if node_id == end:
            break

        # 3. RELAXATION — inspect every neighbour of the current node.
        for edge in graph[node_id]:
            neighbour = edge["node"]
            new_distance = current_dist + edge["distance"]

            # A better route found -> update distance and previous.
            if new_distance < distances[neighbour]:
                distances[neighbour] = new_distance
                previous[neighbour] = node_id
                priority_queue.push(new_distance, neighbour)

    # 4. REBUILD PATH — walk backwards from the destination.
    if distances[end] == float("inf"):
        return None  # destination was never reached

    path = []
    cursor = end
    while cursor is not None:
        path.insert(0, cursor)
        cursor = previous[cursor]

    return {"path": path, "distance": distances[end]}


# ------------------------------------------------------------
#  ALTERNATIVE ROUTES (simple-path enumeration)
#  ------------------------------------------------------------
#  To display "alternative routes" we enumerate every simple path
#  (a path that never visits the same node twice) from start to end
#  using a depth-first search, then sort them by distance.
#
#  This is only practical because our graph is small (10 nodes).
#  The first (shortest) result should match Dijkstra's answer and
#  doubles as a verification of the Dijkstra implementation above.
# ------------------------------------------------------------
def find_alternative_routes(graph, start, end, limit=3):
    results = []
    visited = set()

    def dfs(current, path, distance):
        # Safety cap so the search always finishes quickly.
        if len(results) >= 200:
            return

        if current == end:
            results.append({"path": list(path), "distance": distance})
            return

        for edge in graph[current]:
            if edge["node"] in visited:
                continue  # avoid cycles

            visited.add(edge["node"])
            path.append(edge["node"])
            dfs(edge["node"], path, distance + edge["distance"])
            path.pop()  # backtrack
            visited.remove(edge["node"])

    visited.add(start)
    dfs(start, [start], 0)

    # Shortest first.
    results.sort(key=lambda route: route["distance"])
    return results[:limit]
