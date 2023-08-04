'''
Skye Weaver Worster '25J

This just prints the middle position of the object.
'''

from mistyPy.Robot import Robot
from mistyPy.Events import Events

misty = Robot("131.229.41.135")  # robot with your IP
volume = 3  # volume for audio
lin_vel = 10  # linear velocity
ang_vel = 0  # angular velocity
OD_debounce = 1000  # object detection debounce in ms
min_confidence = .6  # minimum confidence required to send report


def _BumpSensor(data):
    misty.Stop()  # stop moving
    misty.StopObjectDetector()  # stop detecting objects
    misty.UnregisterAllEvents()  # unregister all
    misty.ChangeLED(0, 0, 0)  # LED off
    misty.StopAudio()  # stop audio
    print("end of program")


def _ObjectDetection(data):
    object = data["message"]["description"]
    left = data["message"]["imageLocationLeft"]
    right = data["message"]["imageLocationRight"]
    print(object, (right+left)/2)  # print what Misty sees


# register for bump sensor
misty.RegisterEvent("BumpSensor", Events.BumpSensor,
                    keep_alive=True, callback_function=_BumpSensor)

misty.StartObjectDetector(min_confidence, 0, 5)  # start detection

# register for object detection
misty.RegisterEvent("ObjectDetection", Events.ObjectDetection,
                    debounce=OD_debounce, keep_alive=True, callback_function=_ObjectDetection)
