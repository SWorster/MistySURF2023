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


def _FaceRecognition(data):  # callback for facial recognition data
    global count, num_pictures, image_list  # reference global variables

    print("Taking picture!")  # print each time callback executes

    try:  # handles malformed/irrelevant data

        dt = datetime.now()  # get current date and time
        # convert to string in specific format
        # dd.mm.yy_hh.mm.ss_Face
        imageName = dt.strftime("%d.%m.%Y_%H.%M.%S_Face")

        # take picture, return metadata
        image = misty.TakePicture(True, imageName, 320, 240, True, True)

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
    misty.MoveHead(5, 0, 0)  # lower head slightly to center face in frame
    misty.SetDisplaySettings(True)  # clear display
    misty.UnregisterAllEvents()  # unregister all existing events
    time.sleep(1)  # give Misty time to process unregister command

    # start facial recognition
    misty.RegisterEvent("FaceRecognition", Events.FaceRecognition, keep_alive=True,
                        debounce=FR_debounce, callback_function=_FaceRecognition)

    misty.StartFaceDetection()  # start face detection
