"""
Skye Weaver Worster '25J

Misty drives until bumped (stop and change light depending on bumper touched). She does not resume moving after contact.

WARNING: this code disables Misty's TOF sensors, so she won't automatically stop at table edges and other drops. They are only re-enabled if the program is terminated via the bump sensors. Be careful!
"""

from mistyPy.Robot import Robot
from mistyPy.Events import Events
import time

misty = Robot("131.229.41.135")  # robot with your IP
volume = 10  # volume for audio
lin_vel = 10  # linear velocity
ang_vel = 0  # angular velocity


def _BumpSensor(data):
    if data["message"]["isContacted"]:  # if Misty hits something
        misty.Stop()  # stop moving (should happen automatically)
        name = data["message"]["sensorId"]  # get name
        if name == "bfr":  # front right
            misty.ChangeLED(255, 0, 0)  # red
        if name == "bfl":  # front left
            misty.ChangeLED(0, 255, 0)  # green
        if name == "brr":  # back right
            misty.ChangeLED(0, 0, 255)  # blue
        if name == "brl":  # back left
            misty.ChangeLED(255, 160, 0)  # yellow
        misty.PlayAudio("meow1.mp3", volume)

        misty.UnregisterAllEvents()  # unregister and reset hazards
        misty.UpdateHazardSettings(revertToDefault=True)
        time.sleep(3)  # wait before turning off LED
        misty.ChangeLED(0, 0, 0)


# ignore TOF sensors
misty.UpdateHazardSettings(disableTimeOfFlights=True)

# register for bump sensor
misty.RegisterEvent(
    "BumpSensor", Events.BumpSensor, keep_alive=True, callback_function=_BumpSensor
)

misty.Drive(lin_vel, ang_vel)  # drive until stopped
