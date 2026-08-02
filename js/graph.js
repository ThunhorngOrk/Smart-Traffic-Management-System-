/* ============================================================
   GRAPH DATA — Phnom Penh Road Network
   ------------------------------------------------------------
   DATA STRUCTURE DEMONSTRATION (DSA)
   ------------------------------------------------------------
   Each road intersection is a NODE (vertex) of the graph.
   Each road connecting two intersections is an EDGE with a
   distance measured in kilometres.

   The network is stored as an ADJACENCY LIST so that for every
   node we instantly know which neighbouring nodes it connects
   to and the cost (distance) of travelling along that road.

   Example format (as requested):

       graph = {
         1: [{ node: 2, distance: 2.0 },
             { node: 4, distance: 1.9 },
             { node: 5, distance: 2.6 }],
         ...
       }

   All roads are treated as BIDIRECTIONAL, so each edge is
   inserted into the adjacency list of BOTH endpoints.
   ============================================================ */

/* ------------------------------------------------------------
   NODES
   Each entry: { id, name, x, y }
   (x, y) are pixel coordinates used only for the on-page map
   drawing. They are NOT part of the algorithm.
   ------------------------------------------------------------ */
const NODES = [
  { id: 1, name: "Monivong Intersection",         x: 330, y: 330 },
  { id: 2, name: "Sihanouk Intersection",         x: 460, y: 250 },
  { id: 3, name: "Kampuchea Krom Market",         x: 590, y: 330 },
  { id: 4, name: "Olympic Intersection",          x: 200, y: 250 },
  { id: 5, name: "Orussey Market",                x: 340, y: 250 },
  { id: 6, name: "Royal University Area",         x: 560, y: 150 },
  { id: 7, name: "Railway Station",               x: 110, y: 170 },
  { id: 8, name: "Central Market Intersection",   x: 215, y: 115 },
  { id: 9, name: "Wat Phnom Area",                x: 270, y:  55 },
  { id: 10, name: "Riverside Intersection",       x: 440, y:  70 }
];

/* ------------------------------------------------------------
   EDGES (roads)
   Each entry: { from, to, distance } in kilometres.
   ------------------------------------------------------------ */
const EDGES = [
  { from: 1,  to: 2,  distance: 2.0 },
  { from: 2,  to: 3,  distance: 5.1 },
  { from: 1,  to: 4,  distance: 1.9 },
  { from: 1,  to: 5,  distance: 2.6 },
  { from: 2,  to: 5,  distance: 1.8 },
  { from: 2,  to: 6,  distance: 4.3 },
  { from: 3,  to: 6,  distance: 4.0 },
  { from: 4,  to: 5,  distance: 2.2 },
  { from: 4,  to: 7,  distance: 2.8 },
  { from: 4,  to: 8,  distance: 2.3 },
  { from: 5,  to: 6,  distance: 2.9 },
  { from: 5,  to: 8,  distance: 1.4 },
  { from: 5,  to: 9,  distance: 1.7 },
  { from: 6,  to: 10, distance: 1.8 },
  { from: 6,  to: 9,  distance: 2.7 },
  { from: 7,  to: 8,  distance: 1.6 },
  { from: 8,  to: 9,  distance: 1.6 },
  { from: 9,  to: 10, distance: 1.5 }
];

/* ------------------------------------------------------------
   Build the ADJACENCY LIST graph from the edges above.
   Because roads are bidirectional, each edge is added twice.
   ------------------------------------------------------------ */
const GRAPH = {};

NODES.forEach((node) => {
  GRAPH[node.id] = [];
});

EDGES.forEach((edge) => {
  // direction: from -> to
  GRAPH[edge.from].push({ node: edge.to, distance: edge.distance });
  // direction: to -> from (bidirectional road)
  GRAPH[edge.to].push({ node: edge.from, distance: edge.distance });
});

/* ------------------------------------------------------------
   Quick lookup: node id -> display name
   ------------------------------------------------------------ */
const NODE_NAMES = {};
NODES.forEach((node) => {
  NODE_NAMES[node.id] = node.name;
});
