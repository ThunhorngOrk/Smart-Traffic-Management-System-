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
#   Then a VEHICLE SPEED branch adjusts the base timing:
#     - Slow   (< 30 km/h)  -> +5 s   (slow vehicles clear the box slowly)
#     - Normal (30-49 km/h) -> +0 s
#     - Fast   (>= 50 km/h) -> +10 s  (fast vehicles need a wider safety window)
#
#   Finally an EMERGENCY VEHICLE check is applied:
#     - Emergency vehicle present -> extend green time by 20 seconds
#       and mark the signal as "Priority Green (Extend Time)".
#     - Otherwise -> "Normal Timing".
#
#  This mirrors the decision tree in the combined program
#  (fullsystem.py) and is also used by the web app (app.py).
# ============================================================

def decide_traffic_light(traffic_volume, queue_length, vehicle_speed, emergency_vehicle):
    """
    Walks the decision tree and returns:
        {"duration": 70, "signal": "Normal Timing", "path": [...]}

    traffic_volume:     "high" or "low"
    queue_length:       "long" or "short"
    vehicle_speed:      detected speed in km/h (number)
    emergency_vehicle:  True or False

    Speed branch:
        Slow   (< 30 km/h)  -> +5 s   (slow vehicles clear the box slowly)
        Normal (30-49 km/h) -> +0 s
        Fast   (>= 50 km/h) -> +10 s  (fast vehicles need a wider safety window)
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

    # Branch 3: Vehicle Speed (adjusts the base timing)
    if vehicle_speed >= 50:
        speed_effect = "Fast"
        speed_adjustment = 10
    elif vehicle_speed >= 30:
        speed_effect = "Normal"
        speed_adjustment = 0
    else:
        speed_effect = "Slow"
        speed_adjustment = 5
    decision_path.append(
        f"Vehicle Speed? -> {vehicle_speed} km/h ({speed_effect})"
    )

    # Branch 4: Emergency Vehicle override (applies after base timing)
    decision_path.append(
        f"Emergency Vehicle? -> {'Yes' if emergency_vehicle else 'No'}"
    )
    if emergency_vehicle:
        signal = "Priority Green (Extend Time)"
        duration = base_duration + speed_adjustment + 20  # extend green light
    else:
        signal = "Normal Timing"
        duration = base_duration + speed_adjustment

    return {"duration": duration, "signal": signal, "path": decision_path}


def traffic_light(volume, queue_length, emergency, speed=0):
    """Simpler string wrapper kept for backwards compatibility."""
    result = decide_traffic_light(volume, queue_length, speed, emergency)
    return "{} : {} Seconds".format(result["signal"], result["duration"])


if __name__ == "__main__":

    print("===== TREE (TRAFFIC LIGHT DECISION) =====")

    traffic = input("Traffic Volume (High/Low): ")
    queue_length = input("Queue Length (Long/Short): ")
    speed_raw = input("Vehicle Speed (km/h): ")
    speed = int(speed_raw) if speed_raw.strip().isdigit() else 0
    emergency = input("Emergency Vehicle (Yes/No): ")

    result = traffic_light(
        traffic,
        queue_length,
        emergency.lower() == "yes",
        speed,
    )

    print("\nTraffic Decision")
    print(result)
