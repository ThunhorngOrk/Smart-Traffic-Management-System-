# ============================================================
#  APP — Phnom Penh Smart Traffic Route System (Web Server)
# ============================================================
#  A small Python web server built ONLY on the standard library
#  (no external packages / no pip install needed).
#
#  It does two things:
#    1. Serves the web interface (index.html, css, js).
#    2. Exposes a JSON API endpoint  POST /api/route  that runs
#       Dijkstra's algorithm (dijkstra.py) on the road-network
#       graph (graph.py) and returns the shortest route.
#
#  Run it with:  python app.py
#  Then open:    http://127.0.0.1:8000
# ============================================================

import json
import os
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer

from dijkstra import dijkstra, find_alternative_routes
from graph import GRAPH, NODES

# Folder that contains this script (where index.html lives).
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
PORT = int(os.environ.get("PORT", "8000"))

# Map file extensions to the HTTP content type sent to the browser.
CONTENT_TYPES = {
    ".html": "text/html; charset=utf-8",
    ".css": "text/css; charset=utf-8",
    ".js": "application/javascript; charset=utf-8",
    ".json": "application/json; charset=utf-8",
    ".png": "image/png",
    ".svg": "image/svg+xml",
    ".ico": "image/x-icon",
}


# ------------------------------------------------------------
#  Helpers
# ------------------------------------------------------------
def parse_node(value):
    """Turn user input into a valid node id, or None if invalid."""
    if isinstance(value, bool):
        return None
    if isinstance(value, int):
        text = str(value)
    elif isinstance(value, str):
        text = value.strip()
    else:
        return None

    if text.isdigit():
        node_id = int(text)
        if node_id in GRAPH:
            return node_id
    return None


def compute_route(plate, start_raw, dest_raw):
    """Validate the input, run Dijkstra, and build the API response."""
    # 1. Plate number must not be empty.
    if not plate:
        return {"ok": False, "error": "Please enter your vehicle plate number."}

    # 2. Starting node must exist.
    start = parse_node(start_raw)
    if start is None:
        return {"ok": False, "error": "Please enter a valid node from 1 to 10."}

    # 3. Destination node must exist.
    dest = parse_node(dest_raw)
    if dest is None:
        return {"ok": False, "error": "Please enter a valid node from 1 to 10."}

    # 4. Same start and destination.
    if start == dest:
        return {"ok": False, "error": "You are already at your destination."}

    # 5. Run Dijkstra's algorithm.
    result = dijkstra(GRAPH, start, dest)
    if result is None:
        return {"ok": False, "error": "No route could be found between those nodes."}

    # 6. Find a few alternative routes (shortest ones, excluding the
    #    recommended route returned by Dijkstra).
    candidates = find_alternative_routes(GRAPH, start, dest, limit=10)
    alternatives = [
        {
            "path": route["path"],
            "distance": round(route["distance"], 3),
        }
        for route in candidates
        if abs(route["distance"] - result["distance"]) > 1e-9
        or route["path"] != result["path"]
    ][:3]

    return {
        "ok": True,
        "message": "Recommended route found.",
        "plate": plate,
        "start": start,
        "dest": dest,
        "start_name": NODES[start],
        "dest_name": NODES[dest],
        "path": result["path"],
        "distance": round(result["distance"], 3),
        "alternatives": alternatives,
    }


# ------------------------------------------------------------
#  HTTP handler
# ------------------------------------------------------------
class RouteHandler(BaseHTTPRequestHandler):
    # Suppress the default "127.0.0.1 - - [...]" logging noise.
    def log_message(self, format, *args):
        pass

    # ----- GET: serve the web interface -----
    def do_GET(self):
        path = self.path.split("?")[0]

        if path in ("/", "/index.html"):
            self.serve_file("index.html", CONTENT_TYPES[".html"])
            return

        rel = path.lstrip("/")
        if not rel:
            self.serve_file("index.html", CONTENT_TYPES[".html"])
            return

        if ".." in rel:
            self.send_error(403, "Forbidden")
            return

        ext = os.path.splitext(rel)[1].lower()
        self.serve_file(rel, CONTENT_TYPES.get(ext, "application/octet-stream"))

    # ----- POST: /api/route runs Dijkstra -----
    def do_POST(self):
        if self.path.split("?")[0] != "/api/route":
            self.send_json({"ok": False, "error": "Unknown endpoint."}, status=404)
            return

        length = int(self.headers.get("Content-Length", 0) or 0)
        raw = self.rfile.read(length) if length else b""

        try:
            data = json.loads(raw.decode("utf-8") or "{}")
        except (ValueError, UnicodeDecodeError):
            data = {}

        plate = (data.get("plate") or "").strip()
        response = compute_route(plate, data.get("start"), data.get("dest"))
        self.send_json(response)

    # ----- small file-serving helper -----
    def serve_file(self, rel, content_type):
        path = os.path.join(BASE_DIR, rel)
        try:
            with open(path, "rb") as f:
                body = f.read()
        except OSError:
            self.send_error(404, "Not Found")
            return

        self.send_response(200)
        self.send_header("Content-Type", content_type)
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        self.wfile.write(body)

    # ----- JSON response helper -----
    def send_json(self, obj, status=200):
        body = json.dumps(obj).encode("utf-8")
        self.send_response(status)
        self.send_header("Content-Type", "application/json; charset=utf-8")
        self.send_header("Content-Length", str(len(body)))
        self.send_header("Cache-Control", "no-store")
        self.end_headers()
        self.wfile.write(body)


# ------------------------------------------------------------
#  Entry point
# ------------------------------------------------------------
def main():
    # Try the configured port first; if it is busy, use the next
    # free port so the server never fails to start.
    port = PORT
    server = None
    for attempt in range(10):
        try:
            server = ThreadingHTTPServer(("127.0.0.1", port), RouteHandler)
            break
        except OSError:
            port += 1

    if server is None:
        print("Could not start the server. All ports are busy.")
        return

    url = "http://127.0.0.1:{}".format(port)

    print("=============================================")
    print("  Phnom Penh Smart Traffic Route System")
    print("  Graph + Dijkstra's Algorithm (Python)")
    print("=============================================")
    print("  Serving at:  {}".format(url))
    print("  Press Ctrl+C to stop.")
    print("---------------------------------------------")

    # Open the page in the default web browser automatically.
    try:
        import webbrowser

        webbrowser.open(url)
    except Exception:
        pass

    try:
        server.serve_forever()
    except KeyboardInterrupt:
        print("\nServer stopped.")
    finally:
        server.server_close()


if __name__ == "__main__":
    main()
