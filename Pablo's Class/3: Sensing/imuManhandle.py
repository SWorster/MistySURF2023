'''
Skye Weaver Worster '25J

Misty's LED turns different colors depending on her pitch and roll.

I was going to include yaw, but it's not super accurate when Misty is being manhandled. This is because her absolute yaw depends on her orientation on startup, not when the program starts. Working with yaw velocity is also super unreliable when she's being manipulated in three dimensions.
'''

from mistyPy.Robot import Robot
from mistyPy.Events import Events

misty = Robot("131.229.41.135")  # robot object with your IP
t = 3  # tolerance (degrees)
IMU_debounce = 100  # debounce for IMU (milliseconds)

# colors for each position
fr = [255, 70, 0]  # forward right orange
fl = [255, 50, 50]  # forward left pink
fc = [255, 0, 0]  # forward center red
br = [0, 255, 0]  # back right green
bl = [0, 0, 255]  # back left blue
bc = [0, 255, 255]  # back center teal
nr = [255, 150, 0]  # neutral right yellow
nl = [200, 0, 255]  # neutral left purple
nc = [0, 0, 0]  # neutral center off


def _TouchSensor(data):  # end program when head touched
    misty.UnregisterAllEvents()  # unregister
    misty.ChangeLED(0, 0, 0)  # LED off
    print("Program ended (cap touch)")


def _IMU(data):
    p = data["message"]["pitch"]  # get pitch
    r = data["message"]["roll"]  # get roll

    # pitch and roll measurements can be -360 to 360.
    # To simplify things, we'll just use -180 to 180.
    # This is to account for 359 equalling -1, for example.
    if p > 180:
        p = p-360
    elif p < -180:
        p = p + 360

    if r > 180:
        r = r-360
    elif r < -180:
        r = r + 360

    if p > t:  # forwards
        if r > t:  # right
            misty.ChangeLED(fr[0], fr[1], fr[2])  # orange
        elif r < -t:  # left
            misty.ChangeLED(fl[0], fl[1], fl[2])  # pink
        else:  # center
            misty.ChangeLED(fc[0], fc[1], fc[2])  # red

    elif p < -t:  # backwards
        if r > t:  # right
            misty.ChangeLED(br[0], br[1], br[2])  # green
        elif r < -t:  # left
            misty.ChangeLED(bl[0], bl[1], bl[2])  # blue
        else:  # center
            misty.ChangeLED(bc[0], bc[1], bc[2])  # teal

    else:  # pitch neutral
        if r > t:  # right
            misty.ChangeLED(nr[0], nr[1], nr[2])  # yellow
        elif r < -t:  # left
            misty.ChangeLED(nl[0], nl[1], nl[2])  # purple
        else:  # center
            misty.ChangeLED(nc[0], nc[1], nc[2])  # off


print("program running")

# register for IMU
misty.RegisterEvent("IMU", Events.IMU, debounce=IMU_debounce,
                    keep_alive=True, callback_function=_IMU)

# register for cap touch sensor
misty.RegisterEvent("TouchSensor", Events.TouchSensor,
                    keep_alive=True, callback_function=_TouchSensor)
