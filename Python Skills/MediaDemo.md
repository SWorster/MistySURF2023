# Media Upload Demo

##### Skye Weaver Worster '25J

`mediaSync.py` compares the images and sound clips in the GitHub repository to those in Misty. If a file is missing from Misty, we upload it. If Misty has an extra file, it is deleted. This does not affect the built-in sounds and images that Misty comes with.

`mediaUpload.py` will upload GitHub files to Misty, but will not delete extraneous files. For simplicity, we will only cover `mediaSync.py` here.

## Cloning the GitHub Repo

This program assumes that you've cloned the GitHub repo to your computer. This may work differently for each IDE. The following instructions are for VSCode.

You should have git installed on your computer. It's probably on there already, but [here's some instructions, just in case](https://git-scm.com/book/en/v2/Getting-Started-Installing-Git).

In VSCode, click Accounts on your Activity Bar (if you've personalized your VSCode, the location and appearance of Accounts may be different). There should be an option to sign in to GitHub.

Now click Source Control (which is probably on your Activity Bar). There should be an option to clone a repository. Choose where to store this repository on your computer (we recommend a high level, like Users). Provide the following URL for the repository: [https://github.com/SWorster/MistySURF2023](https://github.com/SWorster/MistySURF2023). 

There are many potential issues with this process depending on your personal setup. A quick Google search should be sufficient to get you fully set up.

## The Actual Code

Provide the path to your local repository in `your_path` before running the code.

First, we get the list of images from the repo. We declare `img_path` as the string path to the `Misty Photos` directory. We use the `os` module to get a list of the files in that directory, which we then sort alphabetically (ignoring case).

We now get the list of images on Misty with the `GetImageList` command. However, this contains system assets that we want to ignore. We iterate through the images, adding them to a separate list if they aren't system assets.

Now we compare the two lists. First, we'll find the images that are on GitHub but not on Misty. We open the image in question from the cloned repo and encode the raw bytes as base64. We decode the base64 to a utf8 string, which Misty can process and save.

If an image is on Misty but not on the GitHub, we simply delete it.

Now we need to deal with sounds. Fortunately, most of this is the same. All we need to change are the specific commands we use to save and delete files from Misty (so that we don't save audio files as images).