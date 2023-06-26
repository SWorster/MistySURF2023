'''
Skye Weaver Worster

Misty moves when her head is being touched.
'''

from mistyPy.Robot import Robot
from mistyPy.Events import Events

misty = Robot("131.229.41.135")  # robot object with your IP
purr = 10  # purr volume
meow = 5  # meow volume

# ! Do not change this, it could break things!
touched = False  # whether Misty is being touched


def _TouchSensor(data):
    if data["message"]["isContacted"]:  # if touched
        misty.ChangeLED(0, 255, 0)  # yellow
        misty.PlayAudio("A_purr1.mp3", volume=10)
        misty.Drive(10, 0)  # drive forward slowly
    else:  # if not touched
        misty.PlayAudio("A_meow3.mp3", volume=5)
        misty.ChangeLED(0, 0, 255)
        misty.Stop()  # stop driving


if __name__ == "__main__":

    # ignore TOF sensors
    misty.UpdateHazardSettings(disableTimeOfFlights=True)

    # register for touch sensor
    misty.RegisterEvent("TouchSensor", Events.TouchSensor, condition=None,
                        keep_alive=True, callback_function=_TouchSensor)
