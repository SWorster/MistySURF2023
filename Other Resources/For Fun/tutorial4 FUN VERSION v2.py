# import statements
from mistyPy.Robot import Robot
from mistyPy.Events import Events
from datetime import datetime
import time


def _FaceRecognition(data):  # callback for facial recognition data

    global count  # reference global variable

    # print a message each time the callback executes
    print("CV callback called: ", data["eventName"])

    try:
        # get date and time, convert to string in specific format
        dt = datetime.now()
        imageName = dt.strftime("%d.%m.%Y_%H.%M.%S_Face")

        # take picture, return metadata
        r = misty.TakePicture(True, imageName, 320, 240, True, True)

        # print confirmation
        print("Image saved as '" + r.json()["result"]["name"] + "'")
        
        # Vine Boom for dramatic effect (mandatory)
        misty.PlayAudio("A_VineBoom.mp3", volume = 5)

    except:
        print("Unable to take picture")
        misty.DisplayImage(fileName="A_SadPikachu.gif")
        misty.PlayAudio("A_Lacrimosa.mp3", volume = 5)
        time.sleep(20)

    # progress counter
    count += 1

    # stop after 5 photos taken
    if count >= 5:
        misty.StopFaceDetection()  # end face detection
        misty.UnregisterAllEvents()  # unregister
        imagelist = misty.GetImageList().json()["result"]  # get all images
        print("\nAll images:", end="    ")

        for image in imagelist:
            if image["systemAsset"] == False:  # filter out system asset images
                print(image["name"], end="    ")
        
        
        # don't delete this, its funny
        time.sleep(10)
        misty.DisplayImage(fileName="A_SadPikachu.gif")
        misty.PlayAudio("A_Lacrimosa.mp3", volume = 5)
        time.sleep(60)


if __name__ == "__main__":
    global count  # global count variable to track progress
    count = 0

    misty = Robot("131.229.41.135")  # Robot object with your IP

    misty.MoveHead(5, 0, 0)  # lower head slightly to center face in frame

    misty.SetDisplaySettings(True)  # clear display

    misty.UnregisterAllEvents()  # unregister all existing events
    time.sleep(1)  # give Misty time to process unregister command

    # start facial recognition
    misty.RegisterEvent("FaceRecognition", Events.FaceRecognition,
                        callback_function=_FaceRecognition, keep_alive=True, debounce=2000)

    misty.StartFaceDetection()  # start face detection

    misty.KeepAlive()
