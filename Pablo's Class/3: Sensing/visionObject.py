'''
Skye Weaver Worster

When Misty sees certain objects, she reacts by changing her LED and playing a song clip. I decided against moving left and right, because that limits Misty to being on the floor (and playing meme songs is more fun).

Pablo's instructions:
Start Misty at pose0; If we show Misty object A, she moves left; For object B, she moves right.
'''

from mistyPy.Robot import Robot
from mistyPy.Events import Events
import time

misty = Robot("131.229.41.135")  # robot object
min_confidence = .6  # confidence required to send event, from 0 to 1
OD_debounce = 1000  # object detection debounce, in ms
volume = 5  # audio volume

def _BumpSensor(data):
    misty.StopObjectDetector()  # stop detecting objects
    misty.UnregisterAllEvents()  # unregister all
    misty.ChangeLED(0, 0, 0)  # LED off
    misty.StopAudio()  # stop audio
    misty.UpdateHazardSettings(revertToDefault=True)  # reset TOFs
    print("end of program")

def _ObjectDetection(data):
    object = data["message"]["description"]
    print(object)  # print what Misty sees

    # if she sees a specific object, she reacts
    if object == "laptop":
        misty.PlayAudio("megalovania.m4a", volume)
        misty.ChangeLED(0, 255, 255)
        misty.UnregisterEvent("ObjectDetection")
    elif object == "backpack":
        misty.PlayAudio("kittycatShort.m4a", volume)
        misty.ChangeLED(255, 0, 255)
        misty.UnregisterEvent("ObjectDetection")
    elif object == "bottle":
        misty.PlayAudio("RickrollShort.mp3", volume)
        misty.ChangeLED(255, 0, 0)
        misty.UnregisterEvent("ObjectDetection")


def _AudioPlayComplete(data):  # when audio stops
    print("Program Ended: Object Detected")  # print to console
    misty.StopObjectDetector()  # stop facial recognition
    misty.UnregisterAllEvents()  # unregister from all events
    misty.UpdateHazardSettings(revertToDefault=True)  # reset hazards
    misty.ChangeLED(0, 0, 0)  # LED off


def end():
    # stop and unregister
    misty.StopObjectDetector()
    misty.UnregisterAllEvents()
    print("done")
    misty.ChangeLED(0, 0, 0)


if __name__ == "__main__":
    misty.StartObjectDetector(min_confidence, 0, 5)  # start detection

    # register for object detection
    misty.RegisterEvent("ObjectDetection", Events.ObjectDetection,
                        debounce=OD_debounce, keep_alive=True, callback_function=_ObjectDetection)

    # register for audio completion
    misty.RegisterEvent("AudioPlayComplete", Events.AudioPlayComplete,
                        keep_alive=True, callback_function=_AudioPlayComplete)
    
    # register for bump sensor
    misty.RegisterEvent("BumpSensor", Events.BumpSensor,
                        keep_alive=True, callback_function=_BumpSensor)
