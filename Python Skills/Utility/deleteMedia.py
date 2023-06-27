'''
Skye Weaver Worster

This code deletes all images and sounds that aren't system assets or ones we've specified we want to keep. If you want to keep some files, rename them with the first letter "A" (example: "A_importantImage.jpg"). This isn't a standard convention or anything; I just made it up on the spot and it works. ¯\_(ツ)_/¯
'''

from mistyPy.Robot import Robot

misty = Robot("131.229.41.135")  # Robot object with your IP

image_list = misty.GetImageList().json()["result"]  # get list of images

for image in image_list:  # for each image

    # if image isn't a system asset or one of the ones we want to keep
    if image["systemAsset"] == False and image["name"][0] != "A":
        s = misty.DeleteImage(image["name"])  # delete image
        print("Deleted:", image["name"])  # confirm deletion

image_list = misty.GetImageList().json()["result"]  # get list of images again
print("\nRemaining images (excluding system assets):")
for image in image_list:  # go through list
    if image["systemAsset"] == False:  # if not system asset
        print(image["name"])  # print remaining images


clip_list = misty.GetAudioList().json()["result"]  # get list of clips

for clip in clip_list:  # for each clip

    # if clip isn't a system asset or one of the ones we want to keep
    if clip["systemAsset"] == False and clip["name"][0] != "A":
        s = misty.DeleteImage(clip["name"])  # delete clip
        print("Deleted:", clip["name"])  # confirm deletion

clip_list = misty.GetImageList().json()["result"]  # get list of clips again
print("\nRemaining clips (excluding system assets):")
for clip in clip_list:  # go through list
    if clip["systemAsset"] == False:  # if not system asset
        print(clip["name"])  # print remaining clips
