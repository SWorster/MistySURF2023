'''
Skye Weaver Worster

WORK IN PROGRESS

Start Misty at pose0; Have her advance until ToF averages to below a threshold value (in a sliding window of time); then, stop and change light
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




if __name__ == "__main__":
    misty = Robot("131.229.41.135")

    # ignore TOF sensors
    misty.UpdateHazardSettings(disableTimeOfFlights=True)
    
    # misty.Drive(10,0)
