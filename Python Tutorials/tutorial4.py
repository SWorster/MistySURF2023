'''
Skye Weaver Worster
Misty Tutorial #4
'''

# import statements
from mistyPy.Robot import Robot
from mistyPy.Events import Events
from datetime import datetime
import time

misty = Robot("131.229.41.135")  # Robot object with your IP
FR_debounce = 2000  # facial recognition debounce in milliseconds
count = 0  # tracks current number of pictures taken
num_pictures = 2  # number of pictures Misty will take
image_list = [None] * num_pictures  # empty array to store image names
width = 320  # image width
height = 420  # image height

# ! Width and height options: 4160 x 3120, 3840 x 2160, 3264 x 2448, 3200 x 2400, 2592 x 1944, 2048 x 1536, 1920 x 1080, 1600 x 1200, 1440 x 1080, 1280 x 960, 1024 x 768, 800 x 600, 640 x 480, 320 x 240. From https://docs.mistyrobotics.com/misty-ii/web-api/api-reference/#takepicture


def _FaceRecognition(data):  # callback for facial recognition data
    global count, image_list  # reference global variables

    print("Taking picture!")  # print each time callback executes

    try:  # handles malformed/irrelevant data

        dt = datetime.now()  # get current date and time
        # convert to string in specific format
        # dd.mm.yy_hh.mm.ss_Face
        imageName = dt.strftime("%d.%m.%Y_%H.%M.%S_Face")

        # take picture, return metadata
        image = misty.TakePicture(base64=True, fileName=imageName, width=width,
                                  height=height, displayOnScreen=True, overwriteExisting=True)

        # print confirmation
        print(f'Image saved as {image.json()["result"]["name"]}')

        # add image name to list
        image_list[count] = image.json()["result"]["name"]

    except Exception as e:
        print(f"Unable to take picture: {e}")

    count += 1  # count number of photos taken

    if count >= num_pictures:  # stop after num_pictures taken
        misty.StopFaceDetection()  # end face detection
        misty.UnregisterAllEvents()  # unregister

        print("\nImages taken:")
        for pic in image_list:  # prints names of images
            print(pic)


if __name__ == "__main__":
    # Preconditions
    misty.MoveHead(0, 0, 0)  # lower head slightly to center face in frame
    misty.SetDisplaySettings(True)  # clear display
    misty.UnregisterAllEvents()  # unregister all existing events
    time.sleep(1)  # give Misty time to process unregister command

    # start facial recognition
    misty.RegisterEvent("FaceRecognition", Events.FaceRecognition, keep_alive=True,
                        debounce=FR_debounce, callback_function=_FaceRecognition)

    misty.StartFaceDetection()  # start face detection
