/* ============================================================
   TRAFFIC LIGHT CONTROL — Hash Table + Decision Tree (UI)
   ------------------------------------------------------------
   Wires the "Traffic Light Control" form to the PYTHON backend:

       Plate      ->  Hash Table lookup (hashtable.py)
       Location   ->  Graph (graph.py)
       Volume/Queue/Emergency -> Decision Tree (tree.py)
       Output     ->  Signal + green-light duration + tree path

   The server runs at  POST /api/traffic  (app.py).

   If the Python server is not running, a small client-side copy of
   the hash table + decision tree is used so the page still works
   (the same fallback pattern as dijkstra.js).
   ============================================================ */

// ----- Client-side copy of the hash table (offline fallback only) -----
const VEHICLES = {
  "2A-1234": { type: "Car", location: 5, speed: 40 },
  "2B-5678": { type: "Bus", location: 2, speed: 30 },
  "2C-9999": { type: "Truck", location: 6, speed: 25 },
  "2D-1111": { type: "Motorbike", location: 8, speed: 35 },
  "2E-2222": { type: "Car", location: 1, speed: 45 },
};

// ----- Client-side copy of the decision tree (offline fallback only) -----
function decideTrafficLight(volume, queue, emergency) {
  const path = ["Traffic Volume? -> " + cap(volume)];

  let base;
  if (volume === "high") {
    path.push("Queue Length? -> " + cap(queue));
    base = queue === "long" ? 60 : 45;
  } else {
    path.push("Queue Length? -> " + cap(queue));
    base = queue === "long" ? 30 : 15;
  }

  path.push("Emergency Vehicle? -> " + (emergency ? "Yes" : "No"));
  if (emergency) {
    return {
      signal: "Priority Green (Extend Time)",
      duration: base + 20,
      path: path,
    };
  }
  return { signal: "Normal Timing", duration: base, path: path };
}

function cap(text) {
  return text.charAt(0).toUpperCase() + text.slice(1);
}

// ----- DOM references -----
const trafficForm = document.getElementById("traffic-form");
const tplateInput = document.getElementById("tplate-input");
const tlocInput = document.getElementById("tloc-input");
const tlocPreview = document.getElementById("tloc-preview");
const tvolumeInput = document.getElementById("tvolume-input");
const tqueueInput = document.getElementById("tqueue-input");
const temergencyInput = document.getElementById("temergency-input");
const trafficBtn = document.getElementById("traffic-btn");
const trafficResult = document.getElementById("traffic-result");

// ----- Live location preview under the location field -----
tlocInput.addEventListener("input", () =>
  showNodePreview(tlocInput, tlocPreview),
);

// ----- Submit handler -----
trafficForm.addEventListener("submit", (event) => {
  event.preventDefault();

  // 1. Validate plate number.
  const plate = tplateInput.value.trim();
  if (!plate) {
    renderTrafficError("Please enter your vehicle plate number.");
    return;
  }

  // 2. Validate the vehicle's current location.
  const loc = parseNode(tlocInput.value);
  if (loc === null) {
    renderTrafficError("Please enter a valid location node from 1 to 10.");
    return;
  }

  const volume = tvolumeInput.value; // "high" | "low"
  const queue = tqueueInput.value; // "long" | "short"
  const emergency = temergencyInput.value === "yes";

  trafficBtn.disabled = true;
  trafficBtn.textContent = "Analyzing...";

  fetch("/api/traffic", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({
      plate: plate,
      location: loc,
      volume: volume,
      queue: queue,
      emergency: emergency,
    }),
  })
    .then((res) => res.json())
    .then((data) => {
      resetTrafficButton();
      if (!data.ok) {
        renderTrafficError(data.error);
        return;
      }
      handleTrafficData(data);
    })
    .catch(() => {
      // Fallback: the Python server is not running. Run the same decision
      // tree + hash table in the browser (main implementation is Python).
      const key = plate.toUpperCase();
      let info = VEHICLES[key];
      let registered = false;
      if (!info) {
        info = { type: "Car", location: loc, speed: 0 };
        VEHICLES[key] = info;
        registered = true;
      }
      const decision = decideTrafficLight(volume, queue, emergency);
      resetTrafficButton();

      handleTrafficData({
        ok: true,
        plate: key,
        vehicle_type: info.type,
        location: info.location,
        location_name: NODE_NAMES[info.location],
        speed: info.speed,
        registered: registered,
        volume: volume,
        queue: queue,
        emergency: emergency,
        signal: decision.signal,
        duration: decision.duration,
        path: decision.path,
      });
    });
});

function resetTrafficButton() {
  trafficBtn.disabled = false;
  trafficBtn.textContent = "Run Traffic Light Decision";
}

/* Render the decision + highlight the vehicle's node on the graph. */
function handleTrafficData(data) {
  renderTrafficResult(data);
  renderGraph(graphContainer, {
    startNode: data.location,
    onNodeClick: (nodeId) => {
      activeNodeInput.value = nodeId;
      activeNodeInput.dispatchEvent(new Event("input"));
      activeNodeInput.focus();
    },
  });
  trafficResult.scrollIntoView({ behavior: "smooth", block: "nearest" });
}

/* ------------------------------------------------------------
   Render the traffic-light decision panel.
   ------------------------------------------------------------ */
function renderTrafficResult(data) {
  const treePath = (data.path || [])
    .map(
      (step) =>
        '<div class="tree-step">' +
        '<span class="tree-arrow">&rarr;</span>' +
        "<span>" +
        escapeHtml(step) +
        "</span></div>",
    )
    .join("");

  const registeredBadge = data.registered
    ? '<span class="registered-badge">Newly registered</span>'
    : "";

  trafficResult.innerHTML =
    '<div class="route-meta">' +
    '<div class="meta-item"><span class="meta-label">Vehicle Plate</span>' +
    '<span class="meta-value">' +
    escapeHtml(data.plate) +
    "</span></div>" +
    '<div class="meta-item"><span class="meta-label">Vehicle Type</span>' +
    '<span class="meta-value">' +
    escapeHtml(data.vehicle_type) +
    "</span>" +
    registeredBadge +
    "</div>" +
    '<div class="meta-item"><span class="meta-label">Location</span>' +
    '<span class="meta-value">Node ' +
    data.location +
    " - " +
    escapeHtml(data.location_name) +
    "</span></div>" +
    '<div class="meta-item"><span class="meta-label">Speed</span>' +
    '<span class="meta-value">' +
    data.speed +
    " km/h</span></div>" +
    "</div>" +
    '<div class="shortest-route"><h3>Decision Tree Path</h3>' +
    '<div class="tree-path">' +
    treePath +
    "</div></div>" +
    '<div class="traffic-decision">' +
    '<div class="signal-badge">' +
    escapeHtml(data.signal) +
    "</div>" +
    '<div class="duration-big">Green Light Duration: <strong>' +
    data.duration +
    " seconds</strong></div>" +
    "</div>";
}

/* Print an error message in the traffic result area. */
function renderTrafficError(message) {
  trafficResult.innerHTML =
    '<div class="error-msg">&#9888;&#65039; ' + escapeHtml(message) + "</div>";
}
