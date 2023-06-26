'''
Skye Weaver Worster

Misty drives until bumped (stop and change light depending on bumper touched)

WARNING: This code temporarily disables Misty's TOF sensor hazards, so she won't automatically stop at table edges and other drops. Be careful!
'''

from mistyPy.Robot import Robot
from mistyPy.Events import Events

misty = Robot("131.229.41.135")  # robot with your IP
volume = 10  # volume for audio
lin_vel = 60  # linear velocity
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
        misty.PlayAudio("A_meow1.mp3", volume=volume)

        # unregister and reset hazards
        misty.UnregisterAllEvents()
        misty.UpdateHazardSettings(revertToDefault=True)


if __name__ == "__main__":

    # ignore TOF sensors
    misty.UpdateHazardSettings(disableTimeOfFlights=True)

    # register for bump sensor
    misty.RegisterEvent("BumpSensor", Events.BumpSensor, condition=None,
                        keep_alive=True, callback_function=_BumpSensor)

    misty.Drive(lin_vel, ang_vel)  # drive until stopped
