#Python Programming

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
misty.PlayAudio("s_Joy4.wav", 5) // second param is volume out of 100
```

This may seem easier than JavaScript, but not for long.

### Tutorial #2: Driving Straight

The full program for the following tutorial can be found [here](https://drive.google.com/file/d/1vK-c7lPe18s5oFcK_KVzvXmUVF2ovBcd/view?usp=drive_link).

This program’s goal is to have Misty drive straight forward for a certain amount of time or until an obstacle is detected.

Begin with the following import statements:

```python
from mistyPy.Robot import Robot
from mistyPy.Events import Events
from mistyPy.EventFilters import EventFilters
```

We’ll start with the main function first, then go back and write our callbacks later. Create the `Robot` object, print a line to the console, and change the LED color.

```python
if __name__ == "__main__":
    misty = Robot("MISTY-IP-ADDRESS-HERE")
    print("Going on an adventure!")
    misty.ChangeLED(0, 0, 255)
```

Next, we’ll declare a global variable to keep track of Misty’s state.  We’re not using promise-based code here, so it’s a bit harder to keep track of what Misty has and hasn’t done. We can keep track of whether Misty is driving with `isDriving`.

```python
global isDriving
isDriving = False
```

Now we need to get data from the TOF sensor. In Python, this is called registering instead of subscribing. The parameters are similar, but vary according to the specific event type we’re using. Always check the [documentation](https://docs.mistyrobotics.com/misty-ii/robot/sensor-data/) before working with an event. For TOF, the parameters are as follows:

1. `event_name`: the human-readable name of the event we’re creating. Call this one `"CenterTimeOfFlight"`
2. `event_type`: the Event object associated with this event. Here, we use Events.TimeOfFlight
3. `Condition`: some events are transmitted together, so we need to filter out unwanted sensor readings. This uses the `EventFilters` class we imported earlier: `[EventFilters.TimeOfFlightPosition.FrontCenter]`. Note that this must be in brackets.
4. `debounce`: the frequency that Misty will send data, in milliseconds. This should usually be 0, but 5 is also acceptable when Misty is moving at lower speeds. There are some event types that will send data in certain conditions, and not constantly (for example, `LocationCommand` only sends data when Misty’s velocity changes). In those cases, do not specify a `debounce` value.
5. `keep_alive`: when `True`, this will keep the connection open until it is manually closed. When `False`, the connection will only send data once.
6. `callback_function`: this is the function that will run whenever the connection receives data. The data will be given to the callback function as a parameter. Our callback is `tof_callback`.

```python
try:
    front_center = misty.RegisterEvent("CenterTimeOfFlight", Events.TimeOfFlight, condition=[EventFilters.TimeOfFlightPosition.FrontCenter], debounce=5, keep_alive=True, callback_function=tof_callback)
```
 
Next, we’ll do the same for Misty’s movement sensors. Because `LocationCommand` in Python doesn’t send data when Misty stops moving, we’ll use the `DriveEncoders` event instead. We can go with the default 0 ms for debounce, but 5 is also fine.

```python
movement = misty.RegisterEvent("DriveEncoders", Events.DriveEncoders, callback_function=move_callback, keep_alive=True)
```

Once we’ve registered to these events, they’ll immediately start collecting data and running their callback functions. While they do this in the background, we need to get Misty to start driving with the `DriveTime` command:

```python
misty.DriveTime(linearVelocity=10, angularVelocity=0, timeMs=5000)
```

Python needs to be told not to continue onwards in the main function until the registrations are ended. This is done with the `KeepAlive` command:

```python
misty.KeepAlive()
```

This is the end of our `try` block. We need to provide an exception handler, which will print errors to the console if they appear.

```python
except Exception as ex:
print(ex)
```

Let’s go back and write our callbacks. First is the TOF callback, which takes the data from the sensor as a parameter. Start by referencing the global variable; we specify that it’s `global` here because otherwise Python would create a local variable with the same name.

```python
def tof_callback(data):
    global isDriving
```

We use another `try` block to handle data that doesn’t match the format we’re looking for (like registration messages and errors). We can access the TOF sensor’s distance measurement by indexing the `data` object.

```python
try:
    distance = data["message"]["distanceInMeters"]
except:
    pass
```

Now we need to program the behavior we want from Misty. At this point, the `isDriving` variable becomes very useful. We don’t want Misty to react to obstacles unless she’s moving. When we code the movement callback later, we’ll have it change `isDriving` to `True` once Misty starts moving. We can use this to have Misty react when an obstacle is within 0.2 meters and Misty is moving.

There are several things that we want Misty to do in this case. First, we print a message to the console and change Misty’s LED to red. We then play an audio file at a low volume. Most importantly, we send a `DriveTime` command to stop Misty’s movement. Now that she’s finished moving, we change `isDriving` to `False`. We then print a message to the console saying why she stopped. Finally, we unregister from all events; this kills the processes that have been giving us TOF and movement data.

```python
if (distance < 0.2 and isDriving):
    print("Misty is", distance, "meters from an obstacle")
    misty.ChangeLED(255, 0, 0)
    misty.PlayAudio("s_joy2.wav", 10)
    misty.DriveTime(linearVelocity=0, angularVelocity=0, timeMs=2000)
    isDriving = False
    print("Stopped: Obstacle")
    misty.UnregisterAllEvents()
```

Let’s start on the movement callback. It begins just like the TOF callback:

```python
def move_callback(data):
    global isDriving
```

In a `try` block, store the left and right tread velocities. If they are greater than some arbitrary amount, Misty is moving and `isDriving` is flipped to `True`. It might seem reasonable to instead compare these velocities to 0, but remember that these measurements come from sensors that may be slightly inaccurate. If you want to have your robot drive at a slower speed, you can lower this value as needed.

```python
try:
    lvel = data["message"]["leftVelocity"]
    rvel = data["message"]["rightVelocity"]
    if (lvel + rvel > 1):
        isDriving = True
```

Now we need to detect whether Misty is stopped. Because the sensors on her treads are a bit inaccurate, we give a little bit of leeway in our comparison. Importantly, we need to specify that `isDriving` is `True`; otherwise, we might accidentally run this section of code before Misty starts moving.

If Misty is stopped, then we want to change her LED to green, play an audio file, print a message to the console, and unregister from all events.

```python
if (lvel+rvel < 0.001 and isDriving):
    misty.ChangeLED(0, 255, 0)
    misty.PlayAudio("s_Joy4.wav", 10)
    print("Stopped: time limit reached")
    misty.UnregisterAllEvents()
```

Finally, finish the `try-except` block so that we ignore all irrelevant messages:

```python
except:
    pass
```

### Tutorial #3: Computer Vision and Facial Recognition

The full program for the following tutorial can be found [here](https://drive.google.com/file/d/1MHQYbb9OacBYdUdc2oxDWjZL1TeWxMNo/view?usp=drive_link).

This program uses Misty’s facial recognition capabilities. Misty will check whether she knows a given name. If she knows the name and sees that person, she will greet the person. If she does not know the name, Misty will use facial recognition to learn the person’s face.

Begin with the following import statements:

```python
from mistyPy.Robot import Robot
from mistyPy.Events import Events
```

We’ll start with the main function first, then go back and write our callbacks later. Create the `Robot` object with your IP, then declare two global variables. `you` is the name of the person Misty will look for. This name can’t have any spaces or special characters. `onList` is how we’ll check whether Misty already knows the person she’s been told to look for.

```python
misty = Robot("MISTY-IP-ADDRESS-HERE")
global you
you = "YourName"
global onList
onList = False
```

Next, we’ll unregister from all existing events, just in case something was already running.

```python
print("unregistering")
misty.UnregisterAllEvents()
```
    
Now we register for face recognition events. This should feel familiar after the last tutorial. We’ll make the callback `_FaceRecognition` later. We want this event to stay alive, so we’ll need to put `misty.KeepAlive()` at the end of the main function; however, we can't put this here because it would prevent further progress.

```python
misty.RegisterEvent("FaceRecognition", Events.FaceRecognition, callback_function=_FaceRecognition, keep_alive=True)
```

Let’s get the list of faces Misty already knows. When we get a response form Misty, we need to translate it into a JSON format so that we can parse it. The list of faces is in the `“result”` field of the JSON file.

```python
faceJSON = misty.GetKnownFaces().json()
faceArr = faceJSON["result"]
print("Learned faces:", faceArr)
```

If your name is in this list, flip `onList` to `True`.

```python
if you in faceArr:
    onList = True
```

If you’re on the list, we don’t need to do any face training because Misty already knows what you look like. We just need to start facial recognition.

```python
if onList:
    print("You were found on the list!")
    print("starting face recognition")
    misty.StartFaceRecognition()
```

If you’re not on the list, Misty needs to learn your face. We register for `FaceTraining` events first. When the `StartFaceTraining` command runs, this will appear as a `FaceTraining` event, running the callback function `_FaceTraining`.

```python
else:
    print("You're not on the list...")
    print("starting face training")
    misty.RegisterEvent("FaceTraining", Events.FaceTraining, callback_function=_FaceTraining, keep_alive=True)
    misty.StartFaceTraining(you)
```

Finally, we tell Misty to keep the `FaceRecognition` event alive. The `KeepAlive()` method prevents any further progress in the code until all events are unregistered, so we couldn’t put this right after the registration commands.

```python
misty.KeepAlive()
```

Now let’s work on our callbacks. In `_FaceTraining`, use a `try-except` block to ignore irrelevant messages. When the training process is complete, Misty will send a message where the `isProcessComplete` field is set to `True`. When we see this message, we can unregister from `FaceTraining` events and begin facial recognition.

```python
def _FaceTraining(data):
    try:
        if data["message"]["isProcessComplete"]:
            print("face training complete")
            misty.UnregisterEvent("FaceTraining")
            misty.StartFaceRecognition()
    except:
        pass
```

The `_FaceRecognition` callback is triggered any time a face recognition event occurs (when Misty finds your name on the list, or after face training). When we receive `FaceRecognition` data, we can check to see who was recognized by accessing the `"label"` field. After checking to make sure that the name isn’t invalid, we print a greeting and unregister from all events.

```python
def _FaceRecognition(data):
    try:
        name = data["message"]["label"]
        if (name != "unknown person" and name != None):
            print("A face was recognized. Hello there, " + name + "!");
            misty.StopFaceRecognition()
            print("unregistering from all events")
            misty.UnregisterAllEvents()
            print("program complete")
    except:
        pass
```

### Tutorial #4: Taking Pictures

The full program for the following tutorial can be found [here](https://drive.google.com/file/d/11I-0llvC1FiVu72jzqbA92aIDZmOKnU1/view?usp=drive_link).

This program lets Misty take a photo when she detects a face. Because Python handles asynchronicity differenly, this tutorial has been heavily altered from the original JavaScript.

Begin with the following import statements:

```python
from mistyPy.Robot import Robot
from mistyPy.Events import Events
from datetime import datetime
import time
```

In our main function, delare the global variable `count` and set it to 0. This will allow us to take a set number of pictures.

```python
if __name__ == "__main__":
    global count
    count = 0
```

Create a Robot object with your IP. Straighten the head so that Misty's camera is facing directly forward; this helps to center the subject's face in the frame.

```python
misty = Robot("MISTY-IP-ADDRESS-HERE")
misty.MoveHead(5, 0, 0)
```

Next, we'll clear Misty's display with `SetDisplaySettings`. Its first parameter is `revertToDefault`, which sets Misty's display as the standard blinking eyes when `True`. We'll also unregister from all existing events, and give Misty a second to process all these commands.

```python
misty.SetDisplaySettings(True)
misty.UnregisterAllEvents()
time.sleep(1)
```

Now we register for `FaceRecognition` events. Our strategy here is quite different from what we've done previously. We'll stay subscribed to `FaceRecognition` and keep `FaceDetection` active the entire time. Whenever Misty detects a face with `FaceDetection`, it's sent to us as a `FaceRecognition` event. We keep `FaceRecognition` with a `debounce` of 2000 ms so that Misty will take photos every two seconds if she sees someone in that timeframe.

```python
misty.RegisterEvent("FaceRecognition", Events.FaceRecognition, callback_function=_FaceRecognition, keep_alive=True, debounce=2000)
misty.StartFaceDetection()
misty.KeepAlive()
```

Let's tackle the callback function `_FaceRecognition` that gets called whenever we detect a face. Reference the global variable `count` so that we can use it later, and print the event data so we know when we've started a new callback.

```python
def _FaceRecognition(data):
    global count
    print("CV callback called: ", data["eventName"])
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

We confirm that we've taken and saved the picture properly by storing the response it gives us, converting it to a JSON with `.json()`, and indexing the `"name"` field.

```python
r = misty.TakePicture(True, imageName, 320, 240, True, True)
print("Image saved as '" + r.json()["result"]["name"] + "'")
```

If this throws an error at any point, print a message to the console.

```python
except:
    print("Unable to take picture")
```

Increment `count` now that we've taken another photo. If we've taken all the photos we wanted, we stop `FaceDetection` and unregister from `FaceRecognition`. We also get the list pictures Misty has stored with `GetImageList`, convert it to a JSON with `.json()`, and access the `"result"` field. We then loop through all Misty's images. If the image is't a `"systemAsset"`, such as Misty's various built-in expressions, we print the image name.

```python
count += 1
else:
    misty.StopFaceDetection()
    misty.UnregisterAllEvents()
    imagelist = misty.GetImageList().json()["result"]
    print("\nAll images:", end="    ")
    for image in imagelist:
        if image["systemAsset"] == False:
            print(image["name"], end="    ")
```
