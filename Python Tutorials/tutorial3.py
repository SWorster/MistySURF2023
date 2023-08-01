'''
Skye Weaver Worster '25J
Misty Tutorial #3
'''

# import statements
from mistyPy.Robot import Robot
from mistyPy.Events import Events


misty = Robot("131.229.41.135")  # Robot object with your IP
you = "YourName"  # string with your name.


def _FaceTraining(data):  # callback for face training
    try:  # handles irrelevant/malformed data
        # if process is complete, unregister from FT event and start recognition
        if data["message"]["isProcessComplete"]:  # when face training ends
            print("Face training complete!")
            misty.UnregisterEvent("FaceTraining")  # unregister from FT event
            misty.StartFaceRecognition()  # begin facial recognition
    except Exception as e:
        print(e)


def _FaceRecognition(data):  # callback for all face recognition events
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

    # register for face recognition events
    misty.RegisterEvent("FaceRecognition", Events.FaceRecognition,
                        keep_alive=True, callback_function=_FaceRecognition)

    # Store the list of known faces and print it
    faceJSON = misty.GetKnownFaces().json()  # get list of known faces as JSON
    face_array = faceJSON["result"]  # convert to array
    print("Learned faces:", face_array)  # print to console

    if you in face_array:  # if your name is in the array
        print("You were found on the list! Starting face recognition.")
        misty.StartFaceRecognition()  # starts facial recognition

    else:  # if your name is not in the array
        print("You're not on the list. Starting face training.")

        # register for face training events
        misty.RegisterEvent("FaceTraining", Events.FaceTraining,
                            keep_alive=True, callback_function=_FaceTraining)

        misty.StartFaceTraining(you)  # start face training
