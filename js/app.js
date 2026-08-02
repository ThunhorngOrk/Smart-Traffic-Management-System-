/* ============================================================
   APP — UI CONTROLLER
   ------------------------------------------------------------
   Wires the HTML form to the PYTHON backend (app.py + dijkstra.py):

       User Input  ->  Plate Number
                    ->  Current Node
                    ->  Destination Node
       Graph (graph.py) -> Dijkstra (dijkstra.py) -> Shortest Path
       Display    ->  Recommended Route + Distance + Alternatives

   The graph data in graph.js and the SVG renderer in graph-viz.js
   are used ONLY for drawing the map on this page. The shortest
   path calculation itself runs in Python and is fetched from the
   POST /api/route endpoint.
   ============================================================ */

// ----- DOM references -----
const plateInput = document.getElementById("plate-input");
const fromInput = document.getElementById("from-input");
const toInput = document.getElementById("to-input");
const fromPreview = document.getElementById("from-preview");
const toPreview = document.getElementById("to-preview");
const form = document.getElementById("route-form");
const resultBox = document.getElementById("result-box");
const graphContainer = document.getElementById("graph-container");
const findBtn = document.getElementById("find-btn");

// Track which input a node click on the map should fill.
let activeNodeInput = fromInput;

// ----- Draw the initial (unhighlighted) graph -----
renderGraph(graphContainer, {
  onNodeClick: (nodeId) => {
    activeNodeInput.value = nodeId;
    activeNodeInput.dispatchEvent(new Event("input"));
    activeNodeInput.focus();
  }
});

// ----- Live location preview under each node input -----
function showNodePreview(input, preview) {
  const id = parseNode(input.value);
  if (id !== null) {
    preview.textContent = "Node " + id + " - " + NODE_NAMES[id];
  } else {
    preview.textContent = "";
  }
}

fromInput.addEventListener("input", () => showNodePreview(fromInput, fromPreview));
toInput.addEventListener("input", () => showNodePreview(toInput, toPreview));

fromInput.addEventListener("focus", () => { activeNodeInput = fromInput; });
toInput.addEventListener("focus", () => { activeNodeInput = toInput; });

/* ------------------------------------------------------------
   Validation helpers (client-side pre-check for instant feedback;
   the Python server validates again before running Dijkstra).
   ------------------------------------------------------------ */

/* Parse "2" or "10" into a node id, or return null if invalid. */
function parseNode(raw) {
  const trimmed = (raw || "").trim();
  if (!/^\d{1,2}$/.test(trimmed)) return null;
  const id = Number(trimmed);
  if (id < 1 || id > 10) return null;
  return id;
}

/* Print an error message in the result area. */
function showError(message) {
  resultBox.innerHTML =
    '<div class="error-msg">&#9888;&#65039; ' + escapeHtml(message) + "</div>";
}

/* Escape user-supplied text before injecting into HTML. */
function escapeHtml(text) {
  return String(text)
    .replace(/&/g, "&amp;")
    .replace(/</g, "&lt;")
    .replace(/>/g, "&gt;")
    .replace(/"/g, "&quot;")
    .replace(/'/g, "&#39;");
}

/* ------------------------------------------------------------
   Form submit handler -> calls the Python Dijkstra API.
   ------------------------------------------------------------ */
form.addEventListener("submit", (event) => {
  event.preventDefault();

  // 1. Validate plate number.
  const plate = plateInput.value.trim();
  if (!plate) {
    showError("Please enter your vehicle plate number.");
    return;
  }

  // 2. Validate starting node.
  const start = parseNode(fromInput.value);
  if (start === null) {
    showError("Please enter a valid node from 1 to 10.");
    return;
  }

  // 3. Validate destination node.
  const dest = parseNode(toInput.value);
  if (dest === null) {
    showError("Please enter a valid node from 1 to 10.");
    return;
  }

  // 4. Same start / destination check.
  if (start === dest) {
    showError("You are already at your destination.");
    return;
  }

  // 5. Ask the Python server to run Dijkstra's algorithm.
  findBtn.disabled = true;
  findBtn.textContent = "Calculating...";

  fetch("/api/route", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ plate: plate, start: start, dest: dest })
  })
    .then((res) => res.json())
    .then((data) => {
      resetButton();

      if (!data.ok) {
        showError(data.error);
        return;
      }

      handleRouteData(data);
    })
    .catch(() => {
      // Fallback: the Python server is not running (e.g. index.html was
      // opened directly). Run the same Dijkstra algorithm in the browser
      // so the page still works. The main implementation is in Python.
      const local = dijkstra(GRAPH, start, dest);

      if (!local) {
        resetButton();
        showError("No route could be found between those nodes.");
        return;
      }

      const candidates = findAlternativeRoutes(GRAPH, start, dest, 10);
      const alternatives = candidates
        .filter(
          (r) =>
            Math.abs(r.distance - local.distance) > 0.0001 ||
            r.path.join(",") !== local.path.join(",")
        )
        .slice(0, 3);

      resetButton();

      handleRouteData({
        ok: true,
        plate: plate,
        start: start,
        dest: dest,
        start_name: NODE_NAMES[start],
        dest_name: NODE_NAMES[dest],
        path: local.path,
        distance: local.distance,
        alternatives: alternatives
      });
    });
});

/* Render results + highlight the graph for any route data object. */
function handleRouteData(data) {
  renderResult(data);
  renderGraph(graphContainer, {
    startNode: data.start,
    destNode: data.dest,
    routePath: data.path,
    altPaths: data.alternatives.map((r) => r.path),
    onNodeClick: (nodeId) => {
      activeNodeInput.value = nodeId;
      activeNodeInput.dispatchEvent(new Event("input"));
      activeNodeInput.focus();
    }
  });

  // Scroll results into view on small screens.
  resultBox.scrollIntoView({ behavior: "smooth", block: "nearest" });
}

function resetButton() {
  findBtn.disabled = false;
  findBtn.textContent = "Find Shortest Route";
}

/* ------------------------------------------------------------
   Render the route result panel from the API response.
   ------------------------------------------------------------ */
function renderResult(data) {
  const path = data.path;
  const total = data.distance;
  const alternatives = data.alternatives || [];

  // Arrow string like "2 → 5 → 9 → 10".
  const pathString = path
    .map((id) => "<span>" + id + "</span>")
    .join('<span class="arrow">&rarr;</span>');

  // Node-by-node vertical list.
  const steps = path
    .map(
      (id) =>
        '<div class="step-node">' +
        '<span class="step-num">Node ' + id + "</span>" +
        '<span class="step-name">' + escapeHtml(NODE_NAMES[id]) + "</span>" +
        "</div>"
    )
    .join('<div class="step-desc">&#8595;</div>');

  // Alternative routes HTML.
  let altHtml = "";
  if (alternatives.length > 0) {
    altHtml =
      '<div class="alternatives"><h3>Alternative Routes</h3>' +
      alternatives
        .map(
          (r, i) =>
            '<div class="alt-row">' +
            '<span class="alt-path">Route ' + (i + 1) + ": " +
            r.path.join(" &rarr; ") + "</span>" +
            '<span class="alt-dist">' + r.distance.toFixed(1) + " km</span>" +
            "</div>"
        )
        .join("") +
      "</div>";
  }

  resultBox.innerHTML =
    '<div class="route-meta">' +
    '<div class="meta-item"><span class="meta-label">Vehicle Plate</span>' +
    '<span class="meta-value">' + escapeHtml(data.plate) + "</span></div>" +
    '<div class="meta-item"><span class="meta-label">From</span>' +
    '<span class="meta-value">Node ' + data.start + " - " +
    escapeHtml(data.start_name) + "</span></div>" +
    '<div class="meta-item"><span class="meta-label">To</span>' +
    '<span class="meta-value">Node ' + data.dest + " - " +
    escapeHtml(data.dest_name) + "</span></div>" +
    "</div>" +

    '<div class="success-banner">&#9989; ' +
    escapeHtml(data.message || "Recommended route found.") + "</div>" +

    '<div class="shortest-route">' +
    "<h3>Shortest Route (Dijkstra's Algorithm)</h3>" +
    '<div class="path-string">' + pathString + "</div>" +
    '<div class="total-distance">Total Distance: <strong>' +
    total.toFixed(1) + " km</strong></div>" +
    "</div>" +

    '<div class="shortest-route"><h3>Route Details</h3>' +
    '<div class="node-steps">' + steps + "</div></div>" +

    altHtml;
}
