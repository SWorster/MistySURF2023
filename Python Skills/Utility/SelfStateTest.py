'''
Skye Weaver Worster

Gets current SelfState data
'''


from mistyPy.Robot import Robot
from mistyPy.Events import Events

misty = Robot("131.229.41.135")  # robot with your IP


def _BumpSensor(data):
    misty.UnregisterAllEvents()


def _SelfState(data):
    try:
        m = data["message"]

        l = m["location"]
        print("location bde: ", l["bearing"], l["distance"], l["elevation"])

        p = l["pose"]
        print("pose bde: ", p["bearing"], p["distance"], p["elevation"])
        print("pose pry: ", p["pitch"], p["roll"], p["yaw"])
        print("pose xyz: ", p["x"], p["y"], p["z"])

        h = p["homogeneousCoordinates"]
        print("homo bde: ", h["bearing"], h["distance"], h["elevation"])
        print("homo pry: ", h["pitch"], h["roll"], h["yaw"])
        print("homo xyz: ", h["x"], h["y"], h["z"])
    except Exception as e:
        print(e)

    misty.UnregisterAllEvents()


if __name__ == "__main__":

    # register for bump sensor
    misty.RegisterEvent("BumpSensor", Events.BumpSensor,
                        keep_alive=True, callback_function=_BumpSensor)

    # register for object detection
    misty.RegisterEvent("SelfState", Events.SelfState,
                        debounce=1000, keep_alive=True, callback_function=_SelfState)
