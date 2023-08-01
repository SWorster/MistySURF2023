'''
Skye Weaver Worster '25J

WORK IN PROGRESS (obviously)
'''

from mistyPy.Robot import Robot
from mistyPy.Events import Events

misty = Robot("131.229.41.135")  # robot object with your IP


def _AR(data):  # AR callback
    print(data)  # print data


def _BumpSensor(data):  # BumpSensor callback
    misty.StopArTagDetector()  # stop detection
    misty.UnregisterAllEvents()  # unregister
    print("DONE")  # print to console


if __name__ == "__main__":
    try:
        # 5X5_1000 dictionary, 30 mm
        print(misty.StartArTagDetector(7, 30).json())

        # register for AR detection events
        print(misty.RegisterEvent("ArTagDetection", Events.ArTagDetection,
                                  debounce=100, keep_alive=True, callback_function=_AR))

    except Exception as e:
        print("ERROR:", e)  # error handling

    # register to BumpSensor for easy program ending
    misty.RegisterEvent("BumpSensor", Events.BumpSensor,
                        keep_alive=True, callback_function=_BumpSensor)
