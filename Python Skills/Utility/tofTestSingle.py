'''
Skye Weaver Worster '25J

Used to test a single TOF sensor. This is useful to check for malfunctions or specific sensor issues.

To change which sensor is being tested, change the condition parameter in the registration command. The options are: Right, Left, Center, Back, DownFrontRight, DownFrontLeft, DownBackRight, DownBackLeft.

Example: condition=[EventFilters.TimeOfFlightPosition.DownwardFrontLeft]
'''

# import statements
from mistyPy.Robot import Robot
from mistyPy.Events import Events
from mistyPy.EventFilters import EventFilters

misty = Robot("131.229.41.135")  # Misty robot with your IP
debounce = 100  # TOF sensor debounce in milliseconds


def _Sensor(data):
    # print status of sensor. flush makes it print ASAP
    print(data["message"]["status"], end=" ", flush=True)


if __name__ == "__main__":
    try:
        misty.RegisterEvent("TimeOfFlight", Events.TimeOfFlight, condition=[
                            EventFilters.TimeOfFlightPosition.DownwardFrontLeft], debounce=debounce, keep_alive=True, callback_function=_Sensor)

    except Exception as e:
        print("Exception:", e)
