'''
Skye Weaver Worster '25J

When Misty sees certain objects, she reacts by changing her LED and playing a song clip. I decided against moving left and right, because that limits Misty to being on the floor (and playing meme songs is more fun).
'''

from mistyPy.Robot import Robot
from mistyPy.Events import Events

misty = Robot("131.229.41.135")  # robot object
OD_debounce = 1000  # object detection debounce, in ms

min_confidence = .6  # confidence required to send event, from 0 to 1
model_ID = 0  # which TensorFlow model to use, from 0-3
max_tracker_history = 5  # how long to hold previous obj history

obj1 = "laptop"  # object 1
sound1 = "megalovania.m4a"  # sound to play for object 1
vol1 = 10  # volume for sound 1
c1 = [0, 255, 255]  # teal

obj2 = "backpack"  # object 2
sound2 = "kittycatShort.m4a"
vol2 = 10
c2 = [255, 0, 255]  # purple

obj3 = "bottle"
sound3 = "RickrollShort.mp3"
vol3 = 10
c3 = [255, 0, 0]  # red

obj4 = "person"
sound4 = "soothingMusic.mp3"
vol4 = 10  # warning: loud
c4 = [255, 255, 255]  # white


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

    if object == obj1:  # if she sees a specific object, she reacts
        misty.PlayAudio(sound1, vol1)  # play clip
        misty.ChangeLED(c1[0], c1[1], c1[2])  # change LED
        misty.UnregisterEvent("ObjectDetection")  # stop detection
    elif object == obj2:
        misty.PlayAudio(sound2, vol2)
        misty.ChangeLED(c2[0], c2[1], c2[2])
        misty.UnregisterEvent("ObjectDetection")
    elif object == obj3:
        misty.PlayAudio(sound3, vol3)
        misty.ChangeLED(c3[0], c3[1], c3[2])
        misty.UnregisterEvent("ObjectDetection")
    elif object == obj4:
        misty.PlayAudio(sound4, vol4)
        misty.ChangeLED(c4[0], c4[1], c4[2])
        misty.UnregisterEvent("ObjectDetection")


def _AudioPlayComplete(data):  # when audio stops
    print("Program Ended: Object Detected")  # print to console
    misty.StopObjectDetector()  # stop facial recognition
    misty.UnregisterAllEvents()  # unregister from all events
    misty.UpdateHazardSettings(revertToDefault=True)  # reset hazards
    misty.ChangeLED(0, 0, 0)  # LED off


def end():  # stop and unregister
    misty.StopObjectDetector()
    misty.UnregisterAllEvents()
    print("done")
    misty.ChangeLED(0, 0, 0)


if __name__ == "__main__":
    print("detecting objects")

    # start detection
    misty.StartObjectDetector(min_confidence, model_ID, max_tracker_history)

    # register for object detection
    misty.RegisterEvent("ObjectDetection", Events.ObjectDetection,
                        debounce=OD_debounce, keep_alive=True, callback_function=_ObjectDetection)

    # register for audio completion
    misty.RegisterEvent("AudioPlayComplete", Events.AudioPlayComplete,
                        keep_alive=True, callback_function=_AudioPlayComplete)

    # register for bump sensor
    misty.RegisterEvent("BumpSensor", Events.BumpSensor,
                        keep_alive=True, callback_function=_BumpSensor)
