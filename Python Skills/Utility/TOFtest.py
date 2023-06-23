'''
Useful test of Misty's TOF sensors.

Gets data from all TOF sensors, printing to console if within default tolerances.

There are a few lines in main that are commented out. These provide different testing conditions.
'''

from mistyPy.Robot import Robot
from mistyPy.Events import Events
from mistyPy.EventFilters import EventFilters


def _Center(data):
    if data["message"]["distanceInMeters"] <= .215 and data["message"]["status"] == 0:
        print("CENTER: ", data["message"]["distanceInMeters"])


def _Right(data):
    if data["message"]["distanceInMeters"] <= .215 and data["message"]["status"] == 0:
        print("RIGHT: ", data["message"]["distanceInMeters"])


def _Left(data):
    if data["message"]["distanceInMeters"] <= .215 and data["message"]["status"] == 0:
        print("LEFT: ", data["message"]["distanceInMeters"])


def _Back(data):
    if data["message"]["distanceInMeters"] <= .215 and data["message"]["status"] == 0:
        print("BACK: ", data["message"]["distanceInMeters"])


def _DRight(data):
    if data["message"]["distanceInMeters"] >= .06 and data["message"]["status"] == 0:
        print("DOWNRIGHT: ", data["message"]["distanceInMeters"])


def _DLeft(data):
    if data["message"]["distanceInMeters"] >= .06 and data["message"]["status"] == 0:
        print("DOWNLEFT: ", data["message"]["distanceInMeters"])


def _BL(data):
    if data["message"]["distanceInMeters"] >= .06 and data["message"]["status"] == 0:
        print("BACKLEFT: ", data["message"]["distanceInMeters"])


def _BR(data):
    if data["message"]["distanceInMeters"] >= .06 and data["message"]["status"] == 0:
        print("BACKRIGHT: ", data["message"]["distanceInMeters"])


# def _Stop(data):
#     if first:
#         if data["message"]["leftVelocity"] != 0:
#             first= True
#     else:
#         if data["message"]["leftVelocity"] == 0:
#             misty.UnregisterAllEvents()


if __name__ == "__main__":
    # global first
    # first = True
    misty = Robot("131.229.41.135")

    misty.UpdateHazardSettings(revertToDefault=True)

    '''
    # Uncomment this block to set your own thresholds
    # Have to update above callbacks on your own, though
    '''

    # t = [
    #     {"sensorName": "TOF_DownFrontRight", "threshold": 0.2},
    #     {"sensorName": "TOF_DownFrontLeft", "threshold": 0.2}
    #     # {"sensorName": "TOF_DownBackRight", "threshold": 0.06},
    #     # {"sensorName": "TOF_DownBackLeft", "threshold": 0.06},
    #     # {"sensorName": "TOF_Right", "threshold": 0.215},
    #     # {"sensorName": "TOF_Left", "threshold": 0.215},
    #     # {"sensorName": "TOF_Center", "threshold": 0.215},
    #     # {"sensorName": "TOF_Back", "threshold": 0.215}
    # ]

    # print(misty.UpdateHazardSettings(timeOfFlightThresholds=t).json())

    # Uncomment this line to completely disable TOF sensor hazard checks
    # misty.UpdateHazardSettings(disableTimeOfFlights=True)

    try:
        misty.RegisterEvent("CenterTimeOfFlight", Events.TimeOfFlight, condition=[
                            EventFilters.TimeOfFlightPosition.FrontCenter], keep_alive=True, callback_function=_Center, debounce=5)

        misty.RegisterEvent("RightTimeOfFlight", Events.TimeOfFlight, condition=[
                            EventFilters.TimeOfFlightPosition.FrontRight], keep_alive=True, callback_function=_Right, debounce=5)

        misty.RegisterEvent("LeftTimeOfFlight", Events.TimeOfFlight, condition=[
                            EventFilters.TimeOfFlightPosition.FrontLeft], keep_alive=True, callback_function=_Left, debounce=5)

        misty.RegisterEvent("DownRightTimeOfFlight", Events.TimeOfFlight, condition=[
                            EventFilters.TimeOfFlightPosition.DownwardFrontRight], keep_alive=True, callback_function=_DRight, debounce=5)

        misty.RegisterEvent("DownLeftTimeOfFlight", Events.TimeOfFlight, condition=[
                            EventFilters.TimeOfFlightPosition.DownwardFrontLeft], keep_alive=True, callback_function=_DLeft, debounce=5)

        misty.RegisterEvent("BackLeftTimeOfFlight", Events.TimeOfFlight, condition=[
                            EventFilters.TimeOfFlightPosition.DownwardBackLeft], keep_alive=True, callback_function=_BL, debounce=5)

        misty.RegisterEvent("BackRightTimeOfFlight", Events.TimeOfFlight, condition=[
                            EventFilters.TimeOfFlightPosition.DownwardBackRight], keep_alive=True, callback_function=_BR, debounce=5)

        misty.RegisterEvent("BackTimeOfFlight", Events.TimeOfFlight, condition=[
                            EventFilters.TimeOfFlightPosition.Back], keep_alive=True, callback_function=_Back, debounce=5)
        
        # misty.RegisterEvent("Stop", Events.DriveEncoders, keep_alive=True, debounce=5, callback_function=_Stop)

    except:
        print("whoops")

    # Uncomment to have Misty drive
    # print(misty.Drive(20, 0))
