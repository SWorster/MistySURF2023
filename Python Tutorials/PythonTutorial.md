# Python Programming

Content is from [here](https://github.com/MistyCommunity/Python-SDK) with supplements from [here](https://github.com/MistyCommunity/Wrapper-Python), though a bit outdated.

First, ensure Python is [updated](https://www.pythoncentral.io/how-to-update-python/) to at least 3.8. Then type the following commands into the Terminal to install the required dependencies:

```bash
pip install requests
pip install websocket-client
pip install yapf
pip install Misty-SDK
```

`requests` should be at least 2.25.1, `websocket-client` should be _at most_ 0.57.0, and `yapf` should be at least 0.30.0.

Pip may throw an error about dependency conflicts. To resolve this issue:

```bash
pip uninstall other-dependency
```
### Tutorial #1: Changing LED

The full program for the following tutorial can be found [here](https://drive.google.com/file/d/1D1nF5usx70wRW4txIvkdAtJAdfyw1iJ6/view?usp=drive_link).

In your Python file, begin with the following import statement:

```python
from mistyPy.Robot import Robot
```

Create a Robot object with your Misty’s IP address:

```python
misty = Robot("MISTY-IP-ADDRESS-HERE")
```

You can now use the available [API commands](https://docs.google.com/spreadsheets/u/0/d/1727c4QWk_gk5HifvtBzIwqhPoPjMOLw44PZuSmjHApA/edit) as if they were methods for the misty object.

```python
misty.ChangeLED(0,0,255)
```

### Tutorial #2: Driving Straight

The full program for the following tutorial can be found [here](https://drive.google.com/file/d/1vK-c7lPe18s5oFcK_KVzvXmUVF2ovBcd/view?usp=drive_link).

This program’s goal is to have Misty drive straight forward for a certain amount of time or until an obstacle is detected.

Begin with the following import statements:

```python
from mistyPy.Robot import Robot
from mistyPy.Events import Events
from mistyPy.EventFilters import EventFilters
```

Let's start by declaring all the global variables we'll need.

- `misty`: our robot object
- `driving_time`: the time Misty will drive for, in seconds
- `driving_speed`: linear velocity, from -100 to 100
- `driving_angle`: angular velocity, from -100 to 100
- `volume`: volume of Misty's audio responses
- `is_driving`: tracks whether Misty is currently moving (boolean)
- `threshold`: how close Misty will get to an obstacle, in meters
- `min_speed`: the minimum speed at which Misty is still considered to be driving
- `TOF_debounce`: Time of Flight event debounce, in milliseconds
- `DE_debounce`: DriveEncoders event debounce, in milliseconds

```python
misty = Robot("MISTY-IP-ADDRESS-HERE")
driving_time = 5
driving_speed = 10
driving_angle = 0
volume = 2
is_driving = False
threshold = 0.2
min_speed = 0.1
TOF_debounce = 5
DE_debounce = 500
```

We’ll start with the main function first, then go back and write our callbacks later. Print a line to the console and change the LED color, so that we know Misty's receiving our commands.

It's good practice to unregister from all events. If we run this code after another program, Misty might still be registered to old events.

The author's Misty has a malfuncitoning Time-of-Flight sensor, which convinces Misty that she's constantly about to run off a ledge. This makes Misty stop moving in the direction of that non-existent edge. We can disable this behavior with the `UpdateHazardSettings` command. If your robot has similar issues, investigate the Live Data panel on Misty Studio to diagnose the problem.

```python
if __name__ == "__main__":
    print("Going on an adventure!")
    misty.ChangeLED(0, 0, 255)
    misty.UnregisterAllEvents()
    misty.UpdateHazardSettings(disableTimeOfFlights=True)
```

Now we need to get data from the TOF sensor. In Python, this is called registering instead of subscribing. The parameters are similar, but vary according to the specific event type we’re using. Always check the [documentation](https://docs.mistyrobotics.com/misty-ii/robot/sensor-data/) before working with an event. For TOF, the parameters are as follows:

1. `event_name`: the human-readable name of the event we’re creating. Call this one `"CenterTimeOfFlight"`
2. `event_type`: the Event object associated with this event. Here, we use `Events.TimeOfFlight`
3. `Condition`: some events are transmitted together, so we need to filter out unwanted sensor readings. This uses the `EventFilters` class we imported earlier: `[EventFilters.TimeOfFlightPosition.FrontCenter]`. Note that this must be in brackets.
4. `debounce`: the frequency that Misty will send data, in milliseconds. This should usually be 0, but 5 is also acceptable when Misty is moving at lower speeds. There are some event types that will send data in certain conditions, and not constantly (for example, `BumpSensor` only sends data when Misty’s bump sensors are touched). In those cases, do not specify a `debounce` value. We already specified this value as the global variable `TOF_debounce`
5. `keep_alive`: when `True`, this will keep the connection open until it is manually closed. When `False`, the connection will only send data once.
6. `callback_function`: this is the function that will run whenever the connection receives data. The data will be given to the callback function as a parameter. Our callback is `tof_callback`.

```python
misty.RegisterEvent("CenterTimeOfFlight", Events.TimeOfFlight, condition=[EventFilters.TimeOfFlightPosition.FrontCenter], debounce=TOF_debounce, keep_alive=True, callback_function=_TimeOfFlight)
```
 
Next, we’ll do the same for Misty’s movement sensors. Because `LocationCommand` in Python doesn’t send data when Misty stops moving, we’ll use the `DriveEncoders` event instead. We can go with the default 0 ms for debounce, but 5 is also fine. This is stored in the global varialbe `DE_debounce`.

```python
misty.RegisterEvent("DriveEncoders", Events.DriveEncoders, keep_alive=True, debounce=DE_debounce, callback_function=_DriveEncoders)
```

Once we’ve registered to these events, they’ll immediately start collecting data and running their callback functions. While they do this in the background, we need to get Misty to start driving with the `DriveTime` command. Speed, angle, and time are global constants we defined earlier.

```python
misty.DriveTime(linearVelocity=driving_speed, angularVelocity=driving_angle, timeMs=driving_time*1000)
```

Let’s go back and write our callbacks. First is the TOF callback, which takes the data from the sensor as a parameter. Start by referencing the global variables we'll use; we specify that they're `global` here because otherwise Python would create local variables with the same names.

```python
def _TimeOfFlight(data):
    global threshold, is_driving, volume
```

We use another `try` block to handle data that doesn’t match the format we’re looking for (like registration messages and errors). We can access the TOF sensor’s distance measurement by indexing the `data` object. We can also tell whether the distace measurement is valid with the boolean passed in the `"status"` field.

```python
try:
    distance = data["message"]["distanceInMeters"]
    status = data["message"]["status"]
except Exception as e:
    print(e)
```

Now we need to program the behavior we want from Misty. At this point, the `isDriving` variable becomes very useful. We don’t want Misty to react to obstacles unless she’s moving. When we code the movement callback later, we’ll have it change `isDriving` to `True` once Misty starts moving. We can use this to have Misty react when an obstacle is within the threshold we set, the distance measurement is valid, and Misty is moving.

There are several things that we want Misty to do in this case. First, we print a message to the console and change Misty’s LED to red. We then play an audio file at a set volume. Most importantly, we send a `Stop` command to stop Misty’s movement. Now that she’s finished moving, we change `isDriving` to `False`. We then print a message to the console saying why she stopped. Finally, we unregister from all events; this kills the processes that have been giving us TOF and movement data. We can also revert the hazard settings to their defaults, if we changed that earlier.

```python
if (distance < threshold and status == 0 and is_driving):
    print(f"Misty is {distance} meters from an obstacle")
    misty.ChangeLED(255, 0, 0)
    misty.PlayAudio("s_Joy2.wav", volume=volume)
    misty.Stop()
    is_driving = False
    print("Stopped: Obstacle")
    misty.UnregisterAllEvents()
    misty.UpdateHazardSettings(revertToDefault=True)
```

Let’s start on the movement callback. It begins just like the TOF callback, but uses different global variables:

```python
def _DriveEncoders(data):
    global min_speed, is_driving, volume
```

In a `try` block, store the left and right tread velocities. If they are greater than the `min_speed` we set earlier, Misty is moving and `isDriving` is flipped to `True`. It might seem reasonable to instead compare these velocities to 0, but remember that these measurements come from sensors that may be slightly inaccurate.

```python
try:
    left_vel = data["message"]["leftVelocity"]
    right_vel = data["message"]["rightVelocity"]
    if (left_vel+right_vel > min_speed):
        is_driving = True
```

Now we need to detect whether Misty is stopped. Because the sensors on her treads are a bit inaccurate, we give a little bit of leeway by comparing to `min_speed` instead of 0. Importantly, we need to specify that `isDriving` is `True`; otherwise, we might accidentally run this section of code before Misty starts moving.

If Misty is stopped, then we want to change her LED to green, play an audio file, print a message to the console, and unregister from all events. If we changed the hazard settings earlier, this is where we should reset them.

```python
if (left_vel+right_vel < min_speed and is_driving):
    misty.ChangeLED(0, 255, 0)
    misty.PlayAudio("s_Joy4.wav", volume=volume)
    print("Stopped: time limit reached")
    misty.UnregisterAllEvents()
    misty.UpdateHazardSettings(revertToDefault=True)
```

Finally, finish the `try-except` block so that we ignore all irrelevant messages:

```python
except Exception as e:
    print(e)
```

### Tutorial #3: Computer Vision and Facial Recognition

The full program for the following tutorial can be found [here](https://github.com/SWorster/MistySURF2023/blob/985587e67e9b00be827aed27f984d61d829eb3b6/Python%20Tutorials/tutorial3.py).

This program uses Misty’s facial recognition capabilities. Misty will check whether she knows a given name. If she knows the name and sees that person, she will greet the person. If she does not know the name, Misty will use facial recognition to learn the person’s face.

Begin with the following import statements:

```python
from mistyPy.Robot import Robot
from mistyPy.Events import Events
```

We then declare our two global variables. One is the `Robot` object with your robot's IP. `you` is the name of the person Misty will look for. This name can’t have any spaces or special characters.

```python
misty = Robot("131.229.41.135")
you = "YourName"
```

We’ll start with the main function first, then go back and write our callbacks later.

Start by unregistering from all existing events, just in case something was already running.

```python
print("Unregistering")
misty.UnregisterAllEvents()
```
    
Now we register for face recognition events. This should feel familiar after the last tutorial. We’ll make the callback `_FaceRecognition` later.

```python
misty.RegisterEvent("FaceRecognition", Events.FaceRecognition, keep_alive=True, callback_function=_FaceRecognition)
```

Let’s get the list of faces Misty already knows. When we get a response form Misty, we need to translate it into a JSON format so that we can parse it. The list of faces is in the `“result”` field of the JSON file.

```python
faceJSON = misty.GetKnownFaces().json()
face_array = faceJSON["result"]
print("Learned faces:", face_array)
```

If you’re on the list, we don’t need to do any face training because Misty already knows what you look like. We just need to start facial recognition.

```python
if you in face_array:
    print("You were found on the list! Starting face recognition.")
    misty.StartFaceRecognition()
```

If you’re not on the list, Misty needs to learn your face. We register for `FaceTraining` events first. When the `StartFaceTraining` command runs, this will appear as a `FaceTraining` event, running the callback function `_FaceTraining`.

```python
else:
    print("You're not on the list. Starting face training.")
    misty.RegisterEvent("FaceTraining", Events.FaceTraining, keep_alive=True, callback_function=_FaceTraining)
    misty.StartFaceTraining(you)
```

Now let’s work on our callbacks. In `_FaceTraining`, use a `try-except` block to ignore irrelevant messages. When the training process is complete, Misty will send a message with the `isProcessComplete` field set to `True`. When we see this message, we can unregister from `FaceTraining` events and begin facial recognition.

```python
def _FaceTraining(data):
    try:
        if data["message"]["isProcessComplete"]:
            print("Face training complete!")
            misty.UnregisterEvent("FaceTraining")
            misty.StartFaceRecognition()
    except Exception as e:
        print(e)
```

The `_FaceRecognition` callback is triggered any time a face recognition event occurs (when Misty finds your name on the list, or after face training). When we receive `FaceRecognition` data, we can check to see who was recognized by accessing the `"label"` field. After checking to make sure that the name isn’t invalid, we print a greeting and unregister from all events.

```python
def _FaceRecognition(data):
    try:
        name = data["message"]["label"]
        if (name != "unknown person" and name != None):
            print(f"A face was recognized. Hello there, {name}!")
            misty.StopFaceRecognition()
            print("Unregistering from all events.")
            misty.UnregisterAllEvents()
            print("Program complete!")
    except Exception as e:
        print(e)
```

### Tutorial #4: Taking Pictures

The full program for the following tutorial can be found [here](https://github.com/SWorster/MistySURF2023/blob/main/Python%20Tutorials/tutorial4.py).

This program lets Misty take a photo when she detects a face. Because Python handles asynchronicity differenly, this tutorial has been heavily altered from the original JavaScript.

Begin with the following import statements:

```python
from mistyPy.Robot import Robot
from mistyPy.Events import Events
from datetime import datetime
import time
```

Let's start with our globals. We need to track the current number of pictures taken, declare the total number of pictures to take, and create an array to store the names of the images we take. We'll also provide the width and height of the images we want to take. [These options](https://docs.mistyrobotics.com/misty-ii/web-api/api-reference/#takepicture) are: 4160 x 3120, 3840 x 2160, 3264 x 2448, 3200 x 2400, 2592 x 1944, 2048 x 1536, 1920 x 1080, 1600 x 1200, 1440 x 1080, 1280 x 960, 1024 x 768, 800 x 600, 640 x 480, 320 x 240.

```python
misty = Robot("131.229.41.135")
FR_debounce = 2000
count = 0
num_pictures = 2
image_list = [None] * num_pictures
width = 320  # image width
height = 420  # image height
```

In our main function, move Misty's head back to a neutral position. Next, we'll clear Misty's display with `SetDisplaySettings`. Its first parameter is `revertToDefault`, which sets Misty's display as the standard blinking eyes when `True`. We'll also unregister from all existing events, and give Misty a second to process all these commands.

```python
if __name__ == "__main__":
    misty.MoveHead(0, 0, 0)
    misty.SetDisplaySettings(True)
    misty.UnregisterAllEvents()
    time.sleep(1)
```

Now we register for `FaceRecognition` events. Our strategy here is quite different from what we've done previously. We'll stay subscribed to `FaceRecognition` and keep `FaceDetection` active the entire time. Whenever Misty detects a face with `FaceDetection`, it's sent to us as a `FaceRecognition` event. We keep `FaceRecognition` with a `debounce` of 2000 ms so that Misty will take photos every two seconds if she sees someone in that timeframe.

```python
misty.RegisterEvent("FaceRecognition", Events.FaceRecognition, keep_alive=True, debounce=FR_debounce, callback_function=_FaceRecognition)
misty.StartFaceDetection()
```

Let's tackle the callback function `_FaceRecognition` that gets called whenever we detect a face. Reference our global variables so that we can use them later, and print a line to the console.

```python
def _FaceRecognition(data):
    global count, num_pictures, image_list
    print("Taking picture!")
```

In a `try` block, we'll attempt to take and display a picture. Start by using the `datetime.now()` method to get the current date and time. Cast this into a string with the method `strftime()`. This uses some very specific format parameters, which can be found [here](https://man7.org/linux/man-pages/man3/strftime.3.html).

```python
try:
    dt = datetime.now()
    imageName = dt.strftime("%d.%m.%Y_%H.%M.%S_Face")
```

Next, we take the picture. `TakePicture` uses the following [parameters](https://docs.mistyrobotics.com/misty-ii/web-api/api-reference/#takepicture):

1. `Base64`: when `True`, sends the image as a Byte64 string. If this is `False`, no data will be sent with the response.
2. `FileName`: the name we want to save the file as. The photo will get saved as `imageName.jpg`
3. `Width`: the resolution can only be chosen from the provided list (see above)
4. `Height`
5. `DisplayOnScreen`: displays the image on Misty's screen when `True`
6. `OverwriteExisting`: if another file already has the same name, replace it with the new photo if `True`.

We confirm that we've taken and saved the picture properly by storing the response it gives us, converting it to a JSON with `.json()`, and indexing the `"name"` field. We print this name and store it in the array of images.

```python
image = misty.TakePicture(True, imageName, 320, 240, True, True)
print(f'Image saved as {image.json()["result"]["name"]}')
image_list[count] = image.json()["result"]["name"]
```

If this throws an error at any point, print a message to the console.

```python
except Exception as e:
    print(f"Unable to take picture: {e}")
```

Increment `count` now that we've taken another photo. If we've taken all the photos we wanted, we stop `FaceDetection` and unregister from `FaceRecognition`. Finally, we print the list of pictures Misty has taken.

```python
count += 1
if count >= num_pictures:
    misty.StopFaceDetection()
    misty.UnregisterAllEvents()
    print("\nImages taken:")
    for pic in image_list:
        print(pic)
```
