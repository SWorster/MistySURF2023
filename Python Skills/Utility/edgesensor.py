'''
Useful test of Misty's TOF sensors.

Gets data from all TOF sensors, printing to console if within default tolerances.

There are a few lines in main that are commented out. These provide different testing conditions.
'''

from mistyPy.Robot import Robot
from mistyPy.Events import Events
from mistyPy.EventFilters import EventFilters


def _DRight(data):
    print(data["message"]["status"], end=" ", flush=True)


if __name__ == "__main__":
    misty = Robot("131.229.41.135")

    try:
        misty.RegisterEvent("DownRightTimeOfFlight", Events.TimeOfFlight, condition=[
                            EventFilters.TimeOfFlightPosition.DownwardFrontLeft], keep_alive=True, callback_function=_DRight, debounce=100)

    except:
        print("whoops")
