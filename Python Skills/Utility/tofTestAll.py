'''
Skye Weaver Worster

Useful test of Misty's TOF sensors. Gets data from all TOF sensors, printing to console if within default tolerances.

The mode constant below changes the mode of operation for the built-in hazard settings. These settings tell Misty to stop if the range sensors detect an obstacle or the edge sensors detect a drop. 0 uses the default hazard settings (.215 for range sensors, .06 for edge sensors). 1 uses the thresholds you specify in the global range and edge constants. 2 completely disables TOF hazards, so Misty won't stop based on any TOF data (she'll still stop if her bump sensors hit something).
'''

# import statements
from mistyPy.Robot import Robot
from mistyPy.Events import Events
from mistyPy.EventFilters import EventFilters

misty = Robot("131.229.41.135")
range = .215  # threshold for range sensors
edge = .06  # threshold for edge sensors
debounce = 5  # TOF debounce in milliseconds

mode = 0  # * mode of operation
# 0: uses default hazard settings
# 1: uses range and edge thresholds as hazard settings
# 2: disables TOF hazard settings


def _Center(data):  # center TOF
    # if close to obstacle and distance is valid, print
    if data["message"]["distanceInMeters"] <= range and data["message"]["status"] == 0:
        print("CENTER: ", data["message"]["distanceInMeters"])


def _Right(data):
    if data["message"]["distanceInMeters"] <= range and data["message"]["status"] == 0:
        print("RIGHT: ", data["message"]["distanceInMeters"])


def _Left(data):
    if data["message"]["distanceInMeters"] <= range and data["message"]["status"] == 0:
        print("LEFT: ", data["message"]["distanceInMeters"])


def _Back(data):
    if data["message"]["distanceInMeters"] <= range and data["message"]["status"] == 0:
        print("BACK: ", data["message"]["distanceInMeters"])


def _DRight(data):
    # if drop-off detected and distance is valid, print
    if data["message"]["distanceInMeters"] >= edge and data["message"]["status"] == 0:
        print("DOWNRIGHT: ", data["message"]["distanceInMeters"])


def _DLeft(data):
    if data["message"]["distanceInMeters"] >= edge and data["message"]["status"] == 0:
        print("DOWNLEFT: ", data["message"]["distanceInMeters"])


def _BL(data):
    if data["message"]["distanceInMeters"] >= edge and data["message"]["status"] == 0:
        print("BACKLEFT: ", data["message"]["distanceInMeters"])


def _BR(data):
    if data["message"]["distanceInMeters"] >= edge and data["message"]["status"] == 0:
        print("BACKRIGHT: ", data["message"]["distanceInMeters"])


if __name__ == "__main__":
    misty.UpdateHazardSettings(revertToDefault=True)  # revert hazards

    if mode == 1:  # new thresholds for hazard settings
        t = [
            {"sensorName": "TOF_DownFrontRight", "threshold": edge},
            {"sensorName": "TOF_DownFrontLeft", "threshold": edge},
            {"sensorName": "TOF_DownBackRight", "threshold": edge},
            {"sensorName": "TOF_DownBackLeft", "threshold": edge},
            {"sensorName": "TOF_Right", "threshold": range},
            {"sensorName": "TOF_Left", "threshold": range},
            {"sensorName": "TOF_Center", "threshold": range},
            {"sensorName": "TOF_Back", "threshold": range}
        ]

        # updates hazards with new thresholds, prints result
        print(misty.UpdateHazardSettings(timeOfFlightThresholds=t).json())
    elif mode == 2:  # disable TOF sensor hazard checks
        misty.UpdateHazardSettings(disableTimeOfFlights=True)

    try:
        misty.RegisterEvent("CenterTimeOfFlight", Events.TimeOfFlight, condition=[
                            EventFilters.TimeOfFlightPosition.FrontCenter], debounce=debounce, keep_alive=True, callback_function=_Center)

        misty.RegisterEvent("RightTimeOfFlight", Events.TimeOfFlight, condition=[
                            EventFilters.TimeOfFlightPosition.FrontRight], debounce=debounce, keep_alive=True, callback_function=_Right)

        misty.RegisterEvent("LeftTimeOfFlight", Events.TimeOfFlight, condition=[
                            EventFilters.TimeOfFlightPosition.FrontLeft], debounce=debounce, keep_alive=True, callback_function=_Left)

        misty.RegisterEvent("DownRightTimeOfFlight", Events.TimeOfFlight, condition=[
                            EventFilters.TimeOfFlightPosition.DownwardFrontRight], debounce=debounce, keep_alive=True, callback_function=_DRight)

        misty.RegisterEvent("DownLeftTimeOfFlight", Events.TimeOfFlight, condition=[
                            EventFilters.TimeOfFlightPosition.DownwardFrontLeft], debounce=debounce, keep_alive=True, callback_function=_DLeft)

        misty.RegisterEvent("BackLeftTimeOfFlight", Events.TimeOfFlight, condition=[
                            EventFilters.TimeOfFlightPosition.DownwardBackLeft], debounce=debounce, keep_alive=True, callback_function=_BL)

        misty.RegisterEvent("BackRightTimeOfFlight", Events.TimeOfFlight, condition=[
                            EventFilters.TimeOfFlightPosition.DownwardBackRight], debounce=debounce, keep_alive=True, callback_function=_BR)

        misty.RegisterEvent("BackTimeOfFlight", Events.TimeOfFlight, condition=[
                            EventFilters.TimeOfFlightPosition.Back], debounce=debounce, keep_alive=True, callback_function=_Back)
    except Exception as e:
        print("Exception:", e)
