# import statements
from mistyPy.Robot import Robot
import time

if __name__ == "__main__":
    misty = Robot("131.229.41.135")  # Robot object with your IP
    
    image_list = misty.GetImageList().json()["result"]
    for image in image_list:
        if image["systemAsset"] == False and image["name"][0] != "A":
            misty.DisplayImage(image["name"])
            time.sleep(.1)
            s = misty.DeleteImage(image["name"])
            print("Deleted :", image["name"])
    
    image_list = misty.GetImageList().json()["result"]
    print("\nRemaining images (excluding system assets):")
    for image in image_list:
        if image["systemAsset"] == False:
            print(image["name"], end="    ")

    misty.SetDisplaySettings(True)