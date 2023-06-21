'''
Start Misty at pose0; Have her advance until bumped (stop and change light depending on bumper touched)
'''

from mistyPy.Robot import Robot
from mistyPy.Events import Events


def _BumpSensor(data):
    if data["message"]["isContacted"]:
        misty.Stop()
        name = data["message"]["sensorId"]
        if name == "bfr":
            misty.ChangeLED(255, 0, 0)
        if name == "bfl":
            misty.ChangeLED(0, 255, 0)
        if name == "brr":
            misty.ChangeLED(0, 0, 255)
        if name == "brl":
            misty.ChangeLED(255, 160, 0)
        misty.PlayAudio("A_meow1.mp3", volume=5)
        misty.UnregisterAllEvents()
        misty.UpdateHazardSettings(revertToDefault=True)


if __name__ == "__main__":
    misty = Robot("131.229.41.135")

    # ignore TOF sensors
    misty.UpdateHazardSettings(disableTimeOfFlights=True)

    misty.RegisterEvent("BumpSensor", Events.BumpSensor, condition=None,
                        keep_alive=True, callback_function=_BumpSensor)

    misty.Drive(60, 0)
