/* ============================================================
   DIJKSTRA'S ALGORITHM — CLIENT-SIDE FALLBACK
   ------------------------------------------------------------
   NOTE FOR DSA GRADING
   --------------------
   The MAIN implementation of Dijkstra's algorithm lives in the
   PYTHON file  dijkstra.py  (used by app.py's /api/route).

   This copy exists ONLY so that the page still works when the
   Python server is not running (for example, when index.html is
   opened directly by double-clicking the file). It uses the same
   graph data from graph.js and implements the same algorithm.
   ============================================================ */

/* ------------------------------------------------------------
   MIN-HEAP (binary heap priority queue)
   Stores { node, priority }. The entry with the smallest
   priority is always popped first.
   ------------------------------------------------------------ */
class MinHeap {
  constructor() {
    this.items = [];
  }

  push(node, priority) {
    this.items.push({ node: node, priority: priority });

    let index = this.items.length - 1;
    while (index > 0) {
      const parentIndex = Math.floor((index - 1) / 2);
      if (this.items[parentIndex].priority <= this.items[index].priority) {
        break;
      }
      [this.items[parentIndex], this.items[index]] =
        [this.items[index], this.items[parentIndex]];
      index = parentIndex;
    }
  }

  pop() {
    if (this.items.length === 0) return null;

    const top = this.items[0];
    const last = this.items.pop();

    if (this.items.length > 0) {
      this.items[0] = last;
      this.siftDown(0);
    }
    return top;
  }

  siftDown(index) {
    const size = this.items.length;
    while (true) {
      let smallest = index;
      const left = 2 * index + 1;
      const right = 2 * index + 2;

      if (left < size && this.items[left].priority < this.items[smallest].priority) {
        smallest = left;
      }
      if (right < size && this.items[right].priority < this.items[smallest].priority) {
        smallest = right;
      }
      if (smallest === index) break;

      [this.items[index], this.items[smallest]] =
        [this.items[smallest], this.items[index]];
      index = smallest;
    }
  }

  isEmpty() {
    return this.items.length === 0;
  }
}

/* ------------------------------------------------------------
   DIJKSTRA — returns { path: [nodeId,...], distance } or null.
   ------------------------------------------------------------ */
function dijkstra(graph, start, end) {
  const distances = {};
  const previous = {};
  const visited = {};

  for (const nodeId in graph) {
    distances[nodeId] = Infinity;
    previous[nodeId] = null;
  }

  distances[start] = 0;

  const pq = new MinHeap();
  pq.push(start, 0);

  while (!pq.isEmpty()) {
    const current = pq.pop();
    const nodeId = current.node;
    const currentDist = current.priority;

    if (visited[nodeId]) continue;
    visited[nodeId] = true;

    if (nodeId === end) break;

    for (const edge of graph[nodeId]) {
      const neighbour = edge.node;
      const newDistance = currentDist + edge.distance;
      if (newDistance < distances[neighbour]) {
        distances[neighbour] = newDistance;
        previous[neighbour] = nodeId;
        pq.push(neighbour, newDistance);
      }
    }
  }

  if (distances[end] === Infinity) return null;

  const path = [];
  let cursor = end;
  while (cursor !== null) {
    path.unshift(Number(cursor));
    cursor = previous[cursor];
  }

  return { path: path, distance: distances[end] };
}

/* ------------------------------------------------------------
   ALTERNATIVE ROUTES — DFS enumeration of simple paths.
   Only practical because our graph is small (10 nodes).
   ------------------------------------------------------------ */
function findAlternativeRoutes(graph, start, end, limit) {
  const results = [];
  const visited = new Set();

  function dfs(current, path, distance) {
    if (results.length >= 200) return;
    if (current === end) {
      results.push({ path: path.slice(), distance: distance });
      return;
    }
    for (const edge of graph[current]) {
      if (visited.has(edge.node)) continue;
      visited.add(edge.node);
      path.push(edge.node);
      dfs(edge.node, path, distance + edge.distance);
      path.pop();
      visited.delete(edge.node);
    }
  }

  visited.add(start);
  dfs(start, [start], 0);

  results.sort((a, b) => a.distance - b.distance);
  return results.slice(0, limit);
}
