'''
Skye Weaver Worster '25J

Gets current SelfState data. Compares data from "location", "pose", and "homogeneousCoordinates". If different, prints differences. If identical (which they usually are), only prints one.

This must be used in conjunction with Misty Studio's mapping interface. Here's how:

1. In the Mapping tab, load the current map. Click Start Tracking.
2. Wait for pose indicator to turn from red to white (Misty has localized).
3. Run this program.
'''

from mistyPy.Robot import Robot
from mistyPy.Events import Events
import time

misty = Robot("131.229.41.135")  # robot with your IP
ss_debounce = 1000  # debounce in milliseconds
first_time = True


def _SelfState(data):
    if first_time:
        print("waiting on valid message: ", end="", flush=True)
        first_time = False

    try:
        # * behold: the JSON Matryoshka Doll!
        m = data["message"]  # message field in data
        l = m["location"]  # location field in message
        p = l["pose"]  # pose field in location
        h = p["homogeneousCoordinates"]  # homo field in pose

        # list of fields to print
        names = ["bearing", "distance", "elevation",
                 "pitch", "roll", "yaw", "x", "y", "z"]

        # list of fields in location
        short_names = ["bearing", "distance", "elevation"]

        print("\n")  # give room for formatting

        for x in range(0, 9):  # for each field
            y = names[x]  # field name
            spaces = " "*(10-len(y))  # spaces to print even columns

            if y in short_names:  # compare all three
                if l[y] == p[y] == h[y]:  # if all equal
                    if p[y] < 0:  # adjust spaces for negative sign
                        spaces = " "*(9-len(y))
                    print(f"{y}: {spaces}{p[y]}")
                else:  # if not equal, assume all different
                    print(
                        f"{y}: {spaces}{l[y]} (loc), {p[y]} (pose), {h[y]} (homo)")

            else:  # compare pose and homo
                if p[y] == h[y]:  # if equal
                    if p[y] < 0:  # adjust spaces for negative sign
                        spaces = " "*(9-len(y))
                    print(f"{y}: {spaces}{p[y]}")
                else:  # if not equal, print both
                    print(f"{y}: {spaces}{p[y]} (pose) and {h[y]} (homo)")

        misty.UnregisterAllEvents()  # unregister (ends program)

    except Exception as e:
        # NoneType exception is thrown when invalid message sent
        if str(e) == "'NoneType' object is not subscriptable":
            print(".", end="", flush=True)  # print waiting sign
        else:
            print(e)


if __name__ == "__main__":
    print("enabling slam")
    misty.EnableSlamService()
    enabled = False
    while not enabled:
        enabled = misty.SlamServiceEnabled().json()["result"]
        time.sleep(.5)

    print("slam enabled\nregistering for self state")

    # register for self state
    misty.RegisterEvent("SelfState", Events.SelfState,
                        debounce=ss_debounce, keep_alive=True, callback_function=_SelfState)
