# ============================================================
#  TREE — Traffic Light Decision Making
# ============================================================
#  DATA STRUCTURE DEMONSTRATION (DSA)
#  The traffic-light rule is a DECISION TREE:
#
#            [Emergency vehicle?]
#            /              \
#          yes               no
#          |                  [Volume high?]
#          |                 /            \
#          |              yes              no
#          |             /    \              \
#          |      [Queue long?]             25s
#          |       /        \
#          |     50s         35s
#         60s
# ============================================================

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