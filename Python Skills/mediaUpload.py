'''
Skye Weaver Worster '25J

This code assumes that you've cloned the GitHub repo to your computer. Replace the path variable with the path to your clone's "Misty Photos" directory.

For a version that also deletes extraneous images and audio, see mediaSync.py.
'''

from mistyPy.Robot import Robot
import os
import base64


your_path = "/Users/skyeworster"  # ! replace "skyeworster" with your path
misty = Robot("131.229.41.135")  # Misty robot with your IP


# get GitHub images
img_path = f"{your_path}/MistySURF2023/Other Resources/Misty Photos"
gh_images = os.listdir(img_path)  # list of images in GitHub repo
gh_images.sort(key=str.lower)  # sort alphabetically (not case-sensitive)


# get list of images on Misty
misty_images = misty.GetImageList().json()["result"]  # all images
short_img = []  # list of image names, excluding system assets
for x in misty_images:
    if x["systemAsset"] == False:  # if not a system asset
        short_img.append(x["name"])  # add name to short list

for x in gh_images:  # look at all GitHub images
    if x not in short_img:  # if image in GitHub but not Misty
        print(f"{x} is not on Misty... ", end="")  # print to console
        try:
            with open(f"{img_path}/{x}", "rb") as img:  # open image for reading
                data = base64.b64encode(img.read())  # read, encode as base64

            utf = data.decode('utf-8')  # decode base64 to string
            misty.SaveImage(x, data=utf)  # save to Misty
            print(f"Saved {x} to Misty!")

        except Exception as e:  # error handling
            print(f"Could not save {x}: {e}")


# get GitHub audio
sound_path = f"{your_path}/MistySURF2023/Other Resources/Misty Sounds"
gh_sounds = os.listdir(sound_path)  # list of sounds in GitHub repo
gh_sounds.sort(key=str.lower)  # sort alphabetically (not case-sensitive)


# get list of audio on Misty
misty_sounds = misty.GetAudioList().json()["result"]  # all clips
short_sounds = []  # list of clip names, excluding system assets
for x in misty_sounds:
    if x["systemAsset"] == False:  # if not a system asset
        short_sounds.append(x["name"])  # add name to short list


for x in gh_sounds:  # look at all GitHub clips
    if x not in short_sounds:  # if clip in GitHub but not Misty
        print(f"{x} is not on Misty... ", end="")  # print to console
        try:
            with open(f"{sound_path}/{x}", "rb") as au:  # open clip for reading
                data = base64.b64encode(au.read())  # read, encode as base64

            utf = data.decode('utf-8')  # decode base64 to string
            misty.SaveAudio(x, utf)  # save to Misty
            print(f"Saved {x} to Misty!")

        except Exception as e:  # error handling
            print(f"Could not save {x}: {e}")
