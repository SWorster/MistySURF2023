'''
Start Misty at pose0; If touched, she advances, if touched again, she stops.
'''

from mistyPy.Robot import Robot
from mistyPy.Events import Events


def _TouchSensor(data):
    if data["message"]["isContacted"]:
        misty.ChangeLED(0, 255, 0)
        misty.PlayAudio("A_purr1.mp3", volume=10)
        misty.Drive(10, 0)
    else:
        misty.PlayAudio("A_meow3.mp3", volume=5)
        misty.ChangeLED(0, 0, 255)
        misty.Stop()


if __name__ == "__main__":
    global touched
    touched = False

    misty = Robot("131.229.41.135")

    # ignore TOF sensors
    misty.UpdateHazardSettings(disableTimeOfFlights=True)

    misty.RegisterEvent("TouchSensor", Events.TouchSensor, condition=None,
                        keep_alive=True, callback_function=_TouchSensor)
