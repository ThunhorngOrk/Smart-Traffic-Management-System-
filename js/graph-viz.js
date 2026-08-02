/* ============================================================
   GRAPH VISUALIZATION (SVG)
   ------------------------------------------------------------
   Draws the road network as an SVG diagram:
     - circular nodes with node numbers + names
     - roads as lines with distance labels
   When a route is found it re-draws the map with:
     - start node  highlighted green
     - destination node highlighted red
     - recommended route drawn thick & green with direction arrows
     - alternative routes drawn dashed & orange
   ============================================================ */

const SVG_NS = "http://www.w3.org/2000/svg";
const NODE_RADIUS = 24;
const VIEW_W = 800;
const VIEW_H = 420;

/* Helper: create an SVG element with attributes. */
function svgEl(tag, attrs) {
  const el = document.createElementNS(SVG_NS, tag);
  if (attrs) {
    for (const key in attrs) {
      el.setAttribute(key, attrs[key]);
    }
  }
  return el;
}

/* Wrap a node name into short lines for the map label. */
function wrapName(name, maxChars) {
  const words = name.split(" ");
  const lines = [];
  let line = "";

  words.forEach((word) => {
    const candidate = line ? line + " " + word : word;
    if (candidate.length > maxChars && line) {
      lines.push(line);
      line = word;
    } else {
      line = candidate;
    }
  });

  if (line) lines.push(line);
  return lines.slice(0, 2);
}

/* Shorten a line so an arrow head ends at the node boundary. */
function shorten(x1, y1, x2, y2) {
  const dx = x2 - x1;
  const dy = y2 - y1;
  const len = Math.hypot(dx, dy) || 1;
  const ux = dx / len;
  const uy = dy / len;
  return {
    x1: x1 + ux * NODE_RADIUS,
    y1: y1 + uy * NODE_RADIUS,
    x2: x2 - ux * NODE_RADIUS,
    y2: y2 - uy * NODE_RADIUS
  };
}

/* Text with a white halo so labels stay readable over lines. */
function labelText(x, y, text, size, weight) {
  const t = svgEl("text", {
    x: x,
    y: y,
    "font-size": size || 11,
    "font-weight": weight || 700,
    "text-anchor": "middle",
    fill: "#2563eb",
    stroke: "#ffffff",
    "stroke-width": 4,
    "paint-order": "stroke"
  });
  t.textContent = text;
  return t;
}

/* ------------------------------------------------------------
   MAIN RENDER FUNCTION
   ------------------------------------------------------------
   container  : DOM element that receives the SVG
   options    : {
                  startNode : id of highlighted start (or null)
                  destNode  : id of highlighted destination (or null)
                  routePath : [nodeId, ...] recommended route (or null)
                  altPaths  : [[nodeId, ...], ...] alternative routes (or null)
                  onNodeClick : callback(nodeId)
                }
   ------------------------------------------------------------ */
function renderGraph(container, options) {
  options = options || {};
  container.innerHTML = "";

  const svg = svgEl("svg", {
    viewBox: "0 0 " + VIEW_W + " " + VIEW_H,
    role: "img",
    "aria-label": "Phnom Penh road network graph"
  });

  // Lookup tables from node id -> coordinates.
  const pos = {};
  NODES.forEach((n) => { pos[n.id] = { x: n.x, y: n.y }; });

  // ----- SVG defs: arrow markers for routes -----
  const defs = svgEl("defs");
  defs.appendChild(arrowMarker("arrow-green", "#16a34a"));
  defs.appendChild(arrowMarker("arrow-orange", "#f59e0b"));
  svg.appendChild(defs);

  // Which edges are used by recommended / alternative routes?
  const routeEdgeSet = new Set();
  if (options.routePath) {
    for (let i = 0; i < options.routePath.length - 1; i++) {
      routeEdgeSet.add(
        options.routePath[i] + "-" + options.routePath[i + 1]
      );
    }
  }

  const altEdgeSet = new Set();
  if (options.altPaths) {
    options.altPaths.forEach((path) => {
      for (let i = 0; i < path.length - 1; i++) {
        altEdgeSet.add(path[i] + "-" + path[i + 1]);
      }
    });
  }

  // ----- BASE EDGES (light blue, drawn underneath) -----
  EDGES.forEach((edge) => {
    const keyA = edge.from + "-" + edge.to;
    const keyB = edge.to + "-" + edge.from;

    const isRoute = routeEdgeSet.has(keyA) || routeEdgeSet.has(keyB);
    const isAlt = altEdgeSet.has(keyA) || altEdgeSet.has(keyB);

    // Only draw as a plain base edge if it is not highlighted.
    if (!isRoute && !isAlt) {
      svg.appendChild(
        svgEl("line", {
          x1: pos[edge.from].x,
          y1: pos[edge.from].y,
          x2: pos[edge.to].x,
          y2: pos[edge.to].y,
          stroke: "#b9d3ee",
          "stroke-width": 3,
          "stroke-linecap": "round"
        })
      );
    }
  });

  // ----- ALTERNATIVE ROUTE EDGES (dashed orange) -----
  if (options.altPaths) {
    options.altPaths.forEach((path) => {
      for (let i = 0; i < path.length - 1; i++) {
        const a = pos[path[i]];
        const b = pos[path[i + 1]];
        const keyA = path[i] + "-" + path[i + 1];
        const keyB = path[i + 1] + "-" + path[i];
        // Skip edges that are part of the recommended route.
        if (routeEdgeSet.has(keyA) || routeEdgeSet.has(keyB)) continue;

        const pts = shorten(a.x, a.y, b.x, b.y);
        svg.appendChild(
          svgEl("line", {
            x1: pts.x1, y1: pts.y1, x2: pts.x2, y2: pts.y2,
            stroke: "#f59e0b",
            "stroke-width": 3.5,
            "stroke-dasharray": "7 5",
            "marker-end": "url(#arrow-orange)",
            "stroke-linecap": "round"
          })
        );
      }
    });
  }

  // ----- RECOMMENDED ROUTE EDGES (thick green + arrows) -----
  if (options.routePath) {
    for (let i = 0; i < options.routePath.length - 1; i++) {
      const a = pos[options.routePath[i]];
      const b = pos[options.routePath[i + 1]];
      const pts = shorten(a.x, a.y, b.x, b.y);
      svg.appendChild(
        svgEl("line", {
          x1: pts.x1, y1: pts.y1, x2: pts.x2, y2: pts.y2,
          stroke: "#16a34a",
          "stroke-width": 5,
          "marker-end": "url(#arrow-green)",
          "stroke-linecap": "round"
        })
      );
    }
  }

  // ----- DISTANCE LABELS on every road -----
  EDGES.forEach((edge) => {
    const a = pos[edge.from];
    const b = pos[edge.to];
    const mx = (a.x + b.x) / 2;
    const my = (a.y + b.y) / 2;

    // Place the label beside the line (prefer above it).
    const dx = b.x - a.x;
    const dy = b.y - a.y;
    const len = Math.hypot(dx, dy) || 1;
    let ox = -dy / len;
    let oy = dx / len;
    if (oy > 0) { ox = -ox; oy = -oy; }   // flip so offset points up

    svg.appendChild(
      labelText(mx + ox * 13, my + oy * 13, edge.distance.toFixed(1), 11, 700)
    );
  });

  // ----- NODES (drawn last so they sit on top) -----
  NODES.forEach((node) => {
    const isStart = node.id === options.startNode;
    const isDest = node.id === options.destNode;
    const isOnRoute =
      options.routePath && options.routePath.indexOf(node.id) !== -1;

    let fill = "#ffffff";
    let stroke = "#3b82f6";
    let strokeWidth = 3;

    if (isStart) { fill = "#dcfce7"; stroke = "#16a34a"; strokeWidth = 4.5; }
    else if (isDest) { fill = "#fee2e2"; stroke = "#dc2626"; strokeWidth = 4.5; }
    else if (isOnRoute) { fill = "#dcfce7"; stroke = "#16a34a"; strokeWidth = 3.5; }

    const group = svgEl("g", {
      class: "node",
      transform: "translate(" + node.x + "," + node.y + ")",
      cursor: options.onNodeClick ? "pointer" : "default"
    });

    // Tooltip with the full name.
    const title = svgEl("title");
    title.textContent = "Node " + node.id + " - " + node.name;
    group.appendChild(title);

    group.appendChild(
      svgEl("circle", {
        r: NODE_RADIUS,
        fill: fill,
        stroke: stroke,
        "stroke-width": strokeWidth
      })
    );

    const num = svgEl("text", {
      "text-anchor": "middle",
      y: 5,
      "font-size": 15,
      "font-weight": 800,
      fill: "#1e293b"
    });
    num.textContent = node.id;
    group.appendChild(num);

    // Name label(s) underneath the circle.
    const lines = wrapName(node.name, 14);
    lines.forEach((lineText, index) => {
      const name = svgEl("text", {
        "text-anchor": "middle",
        y: NODE_RADIUS + 14 + index * 10,
        "font-size": 9.5,
        "font-weight": 600,
        fill: "#334155",
        stroke: "#ffffff",
        "stroke-width": 3,
        "paint-order": "stroke"
      });
      name.textContent = lineText;
      group.appendChild(name);
    });

    if (options.onNodeClick) {
      group.addEventListener("click", () => options.onNodeClick(node.id));
    }

    svg.appendChild(group);
  });

  container.appendChild(svg);
}

/* Build an arrow-head marker definition for a given color. */
function arrowMarker(id, color) {
  const marker = svgEl("marker", {
    id: id,
    viewBox: "0 0 10 10",
    refX: 8,
    refY: 5,
    markerWidth: 7,
    markerHeight: 7,
    orient: "auto-start-reverse"
  });
  const path = svgEl("path", { d: "M 0 0 L 10 5 L 0 10 z", fill: color });
  marker.appendChild(path);
  return marker;
}
