'''
Skye Weaver Worster

Misty's LED turns different colors depending on her pitch, roll, and yaw.
'''

from mistyPy.Robot import Robot
from mistyPy.Events import Events

misty = Robot("131.229.41.135") # robot object with your IP

def _BumpSensor(data):
    # if bumper hit, change LED to white
    if data["message"]["isContacted"]:
        misty.ChangeLED(255, 255, 255)


def _IMU(data):

    m = data["message"]
    t = 2  # tolerance

    red = 0
    green = 0
    blue = 0

    pv = m["pitch"]
    if pv > t:
        red = 50
    elif pv > 360-t:
        red = 255

    rv = m["roll"]
    if rv > t:
        green = 50
    elif rv < -t:
        green = 255

    yv = m["yawVelocity"]
    if yv > t:
        blue = 50
    elif yv < -t:
        blue = 255

    misty.ChangeLED(red, green, blue)


if __name__ == "__main__":

    misty.RegisterEvent("IMU", Events.IMU, condition=None,
                        debounce=10, keep_alive=True, callback_function=_IMU)

    misty.RegisterEvent("BumpSensor", Events.BumpSensor, condition=None,
                        keep_alive=True, callback_function=_BumpSensor)
