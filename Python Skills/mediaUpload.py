'''
Skye Weaver Worster

WORK IN PROGRESS

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

# list of images in github repo
path = "/Users/skyeworster/MistySURF2023/Other Resources/For Fun/MistyMedia/Misty Photos"
images = os.listdir(path)
    
print(images)

misty = Robot("131.229.41.135")  # Misty robot with your IP

# get list of images on Misty
misty_images = misty.GetImageList().json()["result"]

for x in images:
    if x not in misty_images:
        try:
            # img = Image.open(f"{path}/{x}")
            
            with open(f"{path}/{x}", "rb") as img:
                encoded_string = base64.b64encode(img.read())
            misty.SaveImage(x, encoded_string)
            img.close()
        except Exception as e:
            print(f"Could not save {x}: {e}")


# audio_list = misty.GetAudioList().json()["result"]
