'''
Skye Weaver Worster '25J

Misty plays a different audio clip for each face she sees.

This is hard-coded for specific names. I could also do it based on the person's index in the list of faces, If you want it more generalized.

Pablo's instructions:
Have Misty react to different Faces (a funny image/sound/light for each)
'''

from mistyPy.Robot import Robot
from mistyPy.Events import Events

misty = Robot("131.229.41.135")  # robot object
FR_debounce = 1000  # facial recognition debounce, in ms

bump = "VineBoom.mp3"  # plays when bumped
volume = 10  # audio volume

name1 = "Skye"  # person 1
sound1 = "megalovania.m4a"  # audio for p1
vol1 = 10  # volume for p1

name2 = "JuliaYu"  # person 2
sound2 = "RickrollShort.mp3"
vol2 = 10

name3 = "test"  # person 3
sound3 = "LacrimosaShort.m4a"
vol3 = 10

sound0 = "sorryDave.mp3"  # unknown person
vol0 = 10


def _BumpSensor(data):
    print("Program Ended: Bump Sensor")  # print to console
    misty.PlayAudio(bump, volume)  # play audio clip
    misty.StopFaceRecognition()  # stop facial recognition
    misty.UnregisterAllEvents()  # unregister from all events
    misty.UpdateHazardSettings(revertToDefault=True)  # reset hazards
    misty.ChangeLED(0, 0, 0)  # LED off


def _AudioPlayComplete(data):  # when audio stops
    print("Program Ended: Face Detected")  # print to console
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
            if name == name1:
                misty.PlayAudio(sound1, vol1)
            elif name == name2:
                misty.PlayAudio(sound2, vol2)
            elif name == "test":
                misty.PlayAudio(sound3, vol3)
            else:
                misty.PlayAudio(sound0, vol0)

    except Exception as e:
        print("Facial Recognition error:", e)


if __name__ == "__main__":
    print("running")
    misty.UnregisterAllEvents()  # stop preexisting events
    misty.StopFaceRecognition()  # stop preexisting facial rec

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
