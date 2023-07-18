'''
Skye Weaver Worster

Misty's LED turns different colors depending on her pitch and roll.

I was going to include yaw, but it's not super accurate when Misty is being manhandled. This is because her absolute yaw depends on her orientation on startup, not when the program starts. Working with yaw velocity is also super unreliable when she's being manipulated in three dimensions.
'''

from mistyPy.Robot import Robot
from mistyPy.Events import Events

misty = Robot("131.229.41.135")  # robot object with your IP
t = 2  # tolerance (degrees)
IMU_debounce = 100  # debounce for IMU (milliseconds)


def _TouchSensor(data):  # end program when head touched
    misty.UnregisterAllEvents()  # unregister
    misty.ChangeLED(0, 0, 0)  # LED off
    misty.StopAudio()  # stop playing audio clips
    print("Program ended (cap touch)")


def _IMU(data):
    p = data["message"]["pitch"]  # get pitch
    r = data["message"]["roll"]  # get roll

    # pitch and roll measurements can be -360 to 360. To simplify things, we'll just use -180 to 180. This is to account for 359 equalling -1, for example.
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
            misty.ChangeLED(255, 70, 0)  # orange
        elif r < -t:  # left
            misty.ChangeLED(255, 50, 50)  # pink
        else:  # center
            misty.ChangeLED(255, 0, 0)  # red

    elif p < -t:  # backwards
        if r > t:  # right
            misty.ChangeLED(0, 255, 0)  # green
        elif r < -t:  # left
            misty.ChangeLED(0, 0, 255)  # blue
        else:  # center
            misty.ChangeLED(0, 255, 255)  # teal

    else:  # pitch neutral
        if r > t:  # right
            misty.ChangeLED(255, 150, 0)  # yellow
        elif r < -t:  # left
            misty.ChangeLED(200, 0, 255)  # purple
        else:  # center
            misty.ChangeLED(0, 0, 0)  # off


if __name__ == "__main__":

    # register for IMU
    misty.RegisterEvent("IMU", Events.IMU, debounce=IMU_debounce,
                        keep_alive=True, callback_function=_IMU)

    # register for cap touch sensor
    misty.RegisterEvent("TouchSensor", Events.TouchSensor,
                        keep_alive=True, callback_function=_TouchSensor)
