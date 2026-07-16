# -----------------------------
# GRAPH (Road Network)
# -----------------------------

road_network = {
    "Stop 1": ["Stop 2"],
    "Stop 2": ["Stop 1", "Stop 3"],
    "Stop 3": ["Stop 2", "Stop 4"],
    "Stop 4": ["Stop 3", "Stop 5"],
    "Stop 5": ["Stop 4", "Stop 6"],
    "Stop 6": ["Stop 5", "Stop 7"],
    "Stop 7": ["Stop 6", "Stop 8"],
    "Stop 8": ["Stop 7", "Stop 9"],
    "Stop 9": ["Stop 8", "Stop 10"],
    "Stop 10": ["Stop 9"]
}

print("========== ROAD NETWORK ==========\n")

for stop in road_network:
    print(stop, "->", road_network[stop])