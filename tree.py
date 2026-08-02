# ============================================================
#  TREE — Traffic Light Decision Making
# ============================================================
#  DATA STRUCTURE DEMONSTRATION (DSA)
#  The traffic-light rule is a DECISION TREE:
#
#            [Traffic Volume?]
#            /              \
#          high              low
#         /    \           /    \
#   [Queue?]   [Queue?]  [Queue?] [Queue?]
#   long short long short long short long short
#     60s  45s   30s  15s
#
#   Then an EMERGENCY VEHICLE check is applied LAST:
#     - Emergency vehicle present -> extend green time by 20 seconds
#       and mark the signal as "Priority Green (Extend Time)".
#     - Otherwise -> "Normal Timing".
#
#  This mirrors the decision tree in the combined program
#  (fullsystem.py) and is also used by the web app (app.py).
# ============================================================

def decide_traffic_light(traffic_volume, queue_length, emergency_vehicle):
    """
    Walks the decision tree and returns:
        {"duration": 60, "signal": "Normal Timing", "path": [...]}

    traffic_volume:     "high" or "low"
    queue_length:       "long" or "short"
    emergency_vehicle:  True or False
    """
    traffic_volume = traffic_volume.lower()
    queue_length = queue_length.lower()

    decision_path = [f"Traffic Volume? -> {traffic_volume.title()}"]

    # Branch 1: Traffic Volume
    if traffic_volume == "high":
        decision_path.append("Queue Length? -> " + queue_length.title())
        # Branch 2: Queue Length (under High volume)
        if queue_length == "long":
            base_duration = 60
        else:  # short
            base_duration = 45
    else:  # low
        decision_path.append("Queue Length? -> " + queue_length.title())
        # Branch 2: Queue Length (under Low volume)
        if queue_length == "long":
            base_duration = 30
        else:  # short
            base_duration = 15

    # Branch 3: Emergency Vehicle override (applies after base timing)
    decision_path.append(
        f"Emergency Vehicle? -> {'Yes' if emergency_vehicle else 'No'}"
    )
    if emergency_vehicle:
        signal = "Priority Green (Extend Time)"
        duration = base_duration + 20  # extend green light for emergency vehicles
    else:
        signal = "Normal Timing"
        duration = base_duration

    return {"duration": duration, "signal": signal, "path": decision_path}


def traffic_light(volume, queue_length, emergency):
    """Simpler string wrapper kept for backwards compatibility."""
    result = decide_traffic_light(volume, queue_length, emergency)
    return "{} : {} Seconds".format(result["signal"], result["duration"])


if __name__ == "__main__":

    print("===== TREE (TRAFFIC LIGHT DECISION) =====")

    traffic = input("Traffic Volume (High/Low): ")
    queue_length = input("Queue Length (Long/Short): ")
    emergency = input("Emergency Vehicle (Yes/No): ")

    result = traffic_light(
        traffic,
        queue_length,
        emergency.lower() == "yes"
    )

    print("\nTraffic Decision")
    print(result)
