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
min_confidence = .6  # confidence required to send event, form 0 to 1
OD_debounce = 1000  # object detection debounce, in ms
volume = 5  # audio volume


def _ObjectDetection(data):
    object = data["message"]["description"]
    print(object)  # print what Misty sees

    # if she sees a specific object, she reacts
    if object == "laptop":
        misty.PlayAudio("megalovania.m4a", volume)
        misty.ChangeLED(0, 255, 255)
        end()
    if object == "backpack":
        misty.PlayAudio("secrettunnel.mp3", volume)
        misty.ChangeLED(255, 0, 255)
        end()
    if object == "bottle":
        misty.PlayAudio("RickrollShort.mp3", volume)
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
