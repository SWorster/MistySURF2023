'''
Skye Weaver Worster

WORK IN PROGRESS

This code assumes that you've cloned the github repo to your computer. Replace the path variable with the path to your clone's "Misty Photos" directory.

plan:
get all audio and image files from github folders
upload all to misty if she doesn't have them already
???
profit
'''

from mistyPy.Robot import Robot
from PIL import Image
import os
import base64
import json
import base64
from io import BytesIO


your_path = "/Users/skyeworster"  # ! replace "skyeworster" with your path
misty = Robot("131.229.41.135")  # Misty robot with your IP


# get github images
img_path = f"{your_path}/MistySURF2023/Other Resources/For Fun/MistyMedia/Misty Photos"
gh_images = os.listdir(img_path)  # list of images in github repo
gh_images.sort(key=str.lower)
print("on github:", gh_images)


# get list of images on Misty
misty_images = misty.GetImageList().json()["result"]
short_img = []
for x in misty_images:
    if x["systemAsset"] == False:
        short_img.append(x["name"])
print("on misty:", short_img)

for x in gh_images:
    if x not in short_img:
        print(f"{x} not on Misty")
        try:
            with open(f"{img_path}/{x}", "rb") as img:
                data = base64.b64encode(img.read())
            
            utf = data.decode('utf-8')
            misty.SaveImage(x, data=utf)

        except Exception as e:
            print(f"Could not save {x}: {e}")





# get github audio
sound_path = f"{your_path}/MistySURF2023/Other Resources/For Fun/MistyMedia/Misty Sounds"
gh_sounds = os.listdir(sound_path)  # list of sounds in github repo
gh_sounds.sort(key=str.lower)
print("on github:", gh_sounds)


# get list of audio on Misty
misty_sounds = misty.GetAudioList().json()["result"]
short_sounds = []
for x in misty_sounds:
    if x["systemAsset"] == False:
        short_sounds.append(x["name"])
print("on misty:", short_sounds)

for x in gh_sounds:
    if x not in short_sounds:
        print(f"{x} not on Misty")
        try:
            with open(f"{sound_path}/{x}", "rb") as au:
                data = base64.b64encode(au.read())
            
            utf = data.decode('utf-8')
            misty.SaveAudio(x,utf)

        except Exception as e:
            print(f"Could not save {x}: {e}")




# * doing audio later. might have to put everything in one folder for simplicity


# # get github audio
# img_path = f"{your_path}/MistySURF2023/Other Resources/For Fun/MistyMedia/Misty Photos"
# images = os.listdir(img_path) # list of images in github repo
# print(images)


# audio_list = misty.GetAudioList().json()["result"]
