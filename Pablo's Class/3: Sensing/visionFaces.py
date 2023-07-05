'''
Skye Weaver Worster

WORK IN PROGRESS

Misty reacts to faces

Pablo's instructions:
Have Misty react to different Faces (a funny image/sound/light for each)
'''

from mistyPy.Robot import Robot
from mistyPy.Events import Events

misty = Robot("131.229.41.135")  # robot object
FR_debounce = 1000  # facial recognition debounce, in ms
volume = 2  # audio volume


def _BumpSensor(data):
    misty.PlayAudio("A_VineBoom.mp3", volume=volume)  # play audio clip
    print("Stopped: Bump Sensor")  # print to console
    misty.StopFaceRecognition() # stop facial recognition
    misty.UnregisterAllEvents()  # unregister from all events (ends program)
    misty.UpdateHazardSettings(revertToDefault=True)  # reset hazards
    misty.ChangeLED(0, 0, 0)  # LED off


def _FaceRecognition(data):  # callback for face recognition
    try:  # handles irrelevant/malformed data
        name = data["message"]["label"]  # name of person Misty sees
        if (name != "unknown person" and name != None):  # if person is known/valid
            print(f"A face was recognized. Hello there, {name}!")
    except Exception as e:
        print("Facial Recognition error:", e)


if __name__ == "__main__":

    # unregister from all events to clear existing facial recognition
    misty.UnregisterAllEvents()

    # register for bump sensor
    misty.RegisterEvent("BumpSensor", Events.BumpSensor, condition=None,
                        keep_alive=True, callback_function=_BumpSensor)

    # Store the list of known faces and print it
    faceJSON = misty.GetKnownFaces().json()  # get list of known faces as JSON
    face_array = faceJSON["result"]  # convert to array
    print("Learned faces:", face_array)  # print to console
    
    misty.StartFaceRecognition() # start facial recognition

    # register for face recognition events
    misty.RegisterEvent("FaceRecognition", Events.FaceRecognition,
                        debounce=FR_debounce, keep_alive=True, callback_function=_FaceRecognition)
