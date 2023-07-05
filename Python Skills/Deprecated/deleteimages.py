'''
Skye Weaver Worster

This code deletes all images that aren't system assets or ones we've specified we want to keep. If you want to keep some images, rename them with the first letter "A" (example: "A_importantImage.jpg"). This isn't a standard convention or anything; I just made it up on the spot and it works. ¯\_(ツ)_/¯
'''

# import statements
from mistyPy.Robot import Robot
import time

misty = Robot("131.229.41.135")  # Robot object with your IP

image_list = misty.GetImageList().json()["result"]  # get list of images

for image in image_list:  # for each image

    # if image isn't a system asset or one of the ones we want to keep
    if image["systemAsset"] == False and image["name"][0] != "A":
        misty.DisplayImage(image["name"])  # display the image briefly
        time.sleep(.1)  # let image remain on display briefly
        s = misty.DeleteImage(image["name"])  # delete image
        print("Deleted:", image["name"])  # confirm deletion

image_list = misty.GetImageList().json()["result"]  # get list of images again
print("\nRemaining images (excluding system assets):")
for image in image_list:  # go through list
    if image["systemAsset"] == False:  # if not system asset
        print(image["name"], end="    ")  # print remaining images

misty.SetDisplaySettings(True)  # reset display
