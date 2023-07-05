'''
Skye Weaver Worster

WORK IN PROGRESS

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


def _BumpSensor(data):
    misty.PlayAudio("A_VineBoom.mp3", volume=volume)  # play audio clip
    misty.Stop()  # stop moving
    print("Stopped: Bump Sensor")  # print to console
    misty.UnregisterAllEvents()  # unregister from all events (ends program)
    misty.UpdateHazardSettings(revertToDefault=True)  # reset hazards
    misty.ChangeLED(0, 0, 0)  # LED off


def _FaceRecognition(data):  # callback for face recognition
    try:  # handles irrelevant/malformed data
        name = data["message"]["label"]  # name of person Misty sees
        if (name != "unknown person" and name != None):  # if person is known/valid
            print(f"A face was recognized. Hello there, {name}!")
            misty.StopFaceRecognition()  # ends facial recognition
            print("Unregistering from all events.")
            misty.UnregisterAllEvents()  # unregisters from events
            print("Program complete!")
    except Exception as e:
        print(e)



if __name__ == "__main__":

    # unregister from all events to clear existing facial recognition
    print("Unregistering")
    misty.UnregisterAllEvents()
    
    # register for bump sensor
    misty.RegisterEvent("BumpSensor", Events.BumpSensor, condition=None,
                        keep_alive=True, callback_function=_BumpSensor)


    # Store the list of known faces and print it
    faceJSON = misty.GetKnownFaces().json()  # get list of known faces as JSON
    face_array = faceJSON["result"]  # convert to array
    print("Learned faces:", face_array)  # print to console


    # register for face recognition events
    misty.RegisterEvent("FaceRecognition", Events.FaceRecognition,
                        keep_alive=True, callback_function=_FaceRecognition)