'''
Skye Weaver Worster

WORK IN PROGRESS. HAVE NOT STARTED. THIS IS A COPY OF VISIONOBJECT CODE

Misty reacts to faces

Pablo's instructions:
Have Misty react to different Faces (a funny image/sound/light for each)
'''

from mistyPy.Robot import Robot
from mistyPy.Events import Events
import time

misty = Robot("131.229.41.135")  # robot object
min_confidence = .6  # confidence required to send event, form 0 to 1
OD_debounce = 1000  # object detection debounce, in ms
volume = 5  # audio volume


def _ObjectDetection(data):
    object = data["message"]["description"]
    print(object)  # print what Misty sees

    # if she sees a specific object, she reacts
    if object == "laptop":
        misty.PlayAudio("A_megalovania.m4a", volume)
        misty.ChangeLED(0, 255, 255)
        end()
    if object == "backpack":
        misty.PlayAudio("A_secrettunnel.mp3", volume)
        misty.ChangeLED(255, 0, 255)
        end()
    if object == "bottle":
        misty.PlayAudio("A_RickrollShort.mp3", volume)
        misty.ChangeLED(255, 0, 0)
        end()


def end():
    # stop and unregister
    misty.StopObjectDetector()
    misty.UnregisterAllEvents()
    print("done")
    time.sleep(5)  # limits playback to five seconds
    misty.StopAudio()
    misty.ChangeLED(0, 0, 0)


if __name__ == "__main__":
    misty.StartObjectDetector(min_confidence, 0, 5)  # start detection

    # register for object detection
    misty.RegisterEvent("ObjectDetection", Events.ObjectDetection,
                        debounce=OD_debounce, keep_alive=True, callback_function=_ObjectDetection)
