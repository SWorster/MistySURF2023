'''
Skye Weaver Worster

WORK IN PROGRESS

Start Misty at pose0; If we show Misty object A, she moves left; For object B, she moves right.
'''

from mistyPy.Robot import Robot
from mistyPy.Events import Events
import os
import time


def _TimeOfFlight(data):
    name = data["message"]["sensorPosition"]
    d = data["message"]["distanceInMeters"]
    if data["message"]["status"] == 0:
        if name in ["Right", "Left", "Center", "Back"] and d < .2:
            print(name, d)
        elif d > .06:
            # pass due to bottom TOF sensor malfunction
            # print(name, d)
            pass


def tof():
    '''
    The boring half of the visual capabilities.
    '''
    misty.RegisterEvent("TimeOfFlight", Events.TimeOfFlight,
                        condition=None, keep_alive=True, callback_function=_TimeOfFlight)



def end():
    misty.UnregisterAllEvents()
    os.system('python3 /Users/skyeworster/Desktop/reset.py')
    print("program ended")


if __name__ == "__main__":
    misty = Robot("131.229.41.135")

    # clean slate. should print "reset"
    # os.system('python3 /Users/skyeworster/Desktop/reset.py')
    # time.sleep(2)

    # ignore TOF sensors
    misty.UpdateHazardSettings(disableTimeOfFlights=True)
