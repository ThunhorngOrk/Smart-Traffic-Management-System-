# -----------------------------
# TREE (Traffic Light Decision)
# -----------------------------

traffic = input("Traffic Volume (High/Low): ")
queue = input("Queue Length (Long/Short): ")
emergency = input("Emergency Vehicle (Yes/No): ")

print("\nDecision")

if emergency.lower() == "yes":

    print("Green Light : 60 Seconds")

else:

    if traffic.lower() == "high":

        if queue.lower() == "long":

            print("Green Light : 50 Seconds")

        else:

            print("Green Light : 35 Seconds")

    else:

        print("Green Light : 25 Seconds")