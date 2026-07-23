# -----------------------------
# TREE (Traffic Light Decision)
# -----------------------------

def traffic_light(volume, queue_length, emergency):

    if emergency:
        return "Green Light : 60 Seconds"

    if volume.lower() == "high":

        if queue_length.lower() == "long":
            return "Green Light : 50 Seconds"

        else:
            return "Green Light : 35 Seconds"

    else:
        return "Green Light : 25 Seconds"


# -----------------------------
# User Input
# -----------------------------

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