"""
Skye Weaver Worster '25J

Misty moves when her head is being touched. She halts after contact ends.

This code does not differentiate between different touch locations. For example, if Misty is touched in two places and one of them is released, Misty will stop moving. Because the touch locations on her head are hard to find with your hand, this may result in Misty stopping if you move your hand too much.

WARNING: this code disables Misty's TOF sensors, so she won't automatically stop at table edges and other drops. They are only re-enabled if the program is terminated via the bump sensors. Be careful!
"""

from mistyPy.Robot import Robot
from mistyPy.Events import Events

misty = Robot("131.229.41.135")  # robot object with your IP
speed = 10  # movement speed

touch_clip = "purr1.mp3"  # audio to play when touched
touch_v = 20  # touch_clip volume
release_clip = "meow3.mp3"  # audio to play when released
release_v = 10  # release_clip volume


def _BumpSensor(data):
    misty.Stop()  # stop moving
    misty.UnregisterAllEvents()  # unregister all
    misty.ChangeLED(0, 0, 0)  # LED off
    misty.StopAudio()  # stop audio
    misty.UpdateHazardSettings(revertToDefault=True)  # reset TOFs
    print("end of program")


def _TouchSensor(data):
    if data["message"]["isContacted"]:  # if touched
        misty.ChangeLED(0, 255, 0)  # green
        misty.PlayAudio(touch_clip, touch_v)
        misty.Drive(speed, 0)  # drive forward slowly
    else:  # if not touched
        misty.PlayAudio(release_clip, release_v)
        misty.ChangeLED(0, 0, 255)  # blue
        misty.Stop()  # stop driving


# ignore TOF sensors
misty.UpdateHazardSettings(disableTimeOfFlights=True)

# register for touch sensor
misty.RegisterEvent("TouchSensor", Events.TouchSensor,
                    keep_alive=True, callback_function=_TouchSensor)

# register for bump sensor
misty.RegisterEvent("BumpSensor", Events.BumpSensor,
                    keep_alive=True, callback_function=_BumpSensor)
