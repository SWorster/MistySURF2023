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
from github import Github

misty = Robot("131.229.41.135")  # Misty robot with your IP

image_list = misty.GetImageList().json()["result"]  # get list of images


g = Github("USERNAME", "PASSWORD")
repo = g.get_user().get_repo("MistySURF2023")
print(repo.get_dir_contents(""))


image_folder = f"https://github.com/SWorster/MistySURF2023/blob/dbafbb5b1140949509c74493b7497c059c4b7504/Other%20Resources/For%20Fun/MistyMedia/Misty%20Photos"









# audio_list = misty.GetAudioList().json()["result"]

# cat_folder = "https://github.com/SWorster/MistySURF2023/tree/dbafbb5b1140949509c74493b7497c059c4b7504/Other%20Resources/For%20Fun/MistyMedia/Misty%20Sounds/cat"

# address = f"https://github.com/SWorster/MistySURF2023/raw/main/file.jpg"

