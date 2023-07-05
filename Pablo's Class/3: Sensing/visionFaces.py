'''
Skye Weaver Worster

Misty plays a different audio clip for each face she sees

Pablo's instructions:
Have Misty react to different Faces (a funny image/sound/light for each)
'''

from mistyPy.Robot import Robot
from mistyPy.Events import Events

misty = Robot("131.229.41.135")  # robot object
FR_debounce = 1000  # facial recognition debounce, in ms
volume = 2  # audio volume

def _BumpSensor(data):
    print("Program Ended: Bump Sensor")  # print to console
    misty.PlayAudio("A_VineBoom.mp3", volume=volume)  # play audio clip
    end()

def _AudioPlayComplete(data):  # when audio stops
    print("Program Ended: Face Detected")  # print to console
    end()

def end():
    misty.StopFaceRecognition()  # stop facial recognition
    misty.UnregisterAllEvents()  # unregister from all events
    misty.UpdateHazardSettings(revertToDefault=True)  # reset hazards
    misty.ChangeLED(0, 0, 0)  # LED off

def _FaceRecognition(data):  # callback for face recognition
    try:  # handles irrelevant/malformed data
        name = data["message"]["label"]  # name of person Misty sees
        if (name != "unknown person" and name != None):  # if person is known/valid

            # stop and unregister face recognition
            misty.StopFaceRecognition()
            misty.UnregisterEvent("FaceRecognition")

            print(f"A face was recognized. Hello there, {name}!")

            # register for audio completion
            misty.RegisterEvent("AudioPlayComplete", Events.AudioPlayComplete,
                                keep_alive=True, callback_function=_AudioPlayComplete)

            # play different audio for each person
            if name == "Skye":
                misty.PlayAudio("A_megalovania.m4a", volume)
            elif name == "JuliaYu":
                misty.PlayAudio("A_RickrollShort.mp3", volume)
            elif name == "test":
                misty.PlayAudio("A_LacrimosaShort.m4a", volume)
            else:
                misty.PlayAudio("A_sorryDave.mp3", volume)

    except Exception as e:
        print("Facial Recognition error:", e)


if __name__ == "__main__":

    # unregister from all events to clear existing facial recognition
    misty.UnregisterAllEvents()

    # register for bump sensor
    misty.RegisterEvent("BumpSensor", Events.BumpSensor,
                        keep_alive=True, callback_function=_BumpSensor)

    # Store the list of known faces and print it
    faceJSON = misty.GetKnownFaces().json()  # get list of known faces as JSON
    face_array = faceJSON["result"]  # convert to array
    print("Learned faces:", face_array)  # print to console

    misty.StartFaceRecognition()  # start facial recognition

    # register for face recognition events
    misty.RegisterEvent("FaceRecognition", Events.FaceRecognition,
                        debounce=FR_debounce, keep_alive=True, callback_function=_FaceRecognition)
