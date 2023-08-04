# Object Demos
##### Skye Weaver Worster '25J

## `objPosition.py`

This program has Misty detects objects in her field of view, then print their name and horizontal location to the console.

We register for the bump sensors, which allow us to easily and gracefully stop the program in the `_BumpSensor()` callback. We start object detection and register for the `ObjectDetection` event, which tells us whatever object Misty sees. We print that data, as well as the horizontal location of the object, to the console. This program repeats until a bump sensor is pressed.

## `objInteraction.py`

Misty turns to the right until she finds two specific objects, making note of their positions. She then drives between them.

In the main function, we start by ignoring the TOF hazard system and beginning object detection. We then register for the bump sensor, object detection, and IMU events. We give Misty a moment to process these requests, then record the current yaw as `start_yaw` and begin turning right.

Before we get into the movement, let's cover the callbacks. The `_BumpSensor()` callback gives us a graceful way to end the program. Because the movement functions have `while` loops and other logic running concurrently, we have to be able to break out of that easily. `_BumpSensor()` changes `bumped` to `True`, signalling that all other processes should stop. We'll see this in action later.

The `_yaw()` callback is used to process IMU data. We're only interested in the yaw measurements. The IMU can send values from -360 to 360. The orientation Misty faces at start of a program could be, for example, 0, -360, or 360. The sensor is accurate plus or minus about 5 degrees, so an actual heading of 0 could be -5 to 5, -360 to -355, or 355 to 360. To simplify this, we convert the yaw to a 0 to 360 degree range. This means an actual heading of 0 will only return 0-5 or 355-360.

The `_ObjectDetection()` callback handles data about whatever object Misty currently sees. If we haven't seen the first object yet, `yaw1` and `yaw2` will be `None`. When we see the first object, we return its average horizontal location to be handled later. We repeat this process for the second object. Note that this callback doesn't actually record the yaw values for these objects; it only asks whether those values are known and records their visual location.

Now let's talk about the movement. In `moveRight()`, Misty starts turning right while we wait for one of two conditions to be met. The first condition is whether `avg` is within a certain range `tol` of a `center` value. When Misty sees an object, its horizontal position is a value from 0 to 300 (approximately, see Skye after class if you want to hear her rant about it). If Misty sees the object way off in her peripheral view but records the yaw for that object as directly in front of her, she could drastically miscalculate the object's location.

The other condition is if Misty has been bumped. In this case, we want to exit the `while` loop and end the program. The bump sensor callback should do this already, but we can also run the callback a second time just to be sure. This is useful in cases where Misty is bumped and then immediately given a movement command, but it's good practice in all cases.

Once Misty has seen the first object, she records her current yaw, resets the `avg` value to 0, and repeats this process for the second object. When she sees that object, she stops and we enter the `driveForward()` function. This section of code didn't need to be its own function, but it can be difficult to read six indentations deep.

In `driveForward()`, we stop the object detection and unregister from that event. We then calculate the heading between the two objects. However, we have to account for the gap between 0 and 360. If Misty crosses this gap, the average of the object yaws will be 180 degrees across the circle from the intended heading. If this is the case, then `yaw1` will be less than `yaw2` and we can subtract the average from 180 to get the right heading.

We now need to turn Misty to face this heading. If Misty doesn't need to cross the 0-360 gap to get there, we simply turn her left until her current yaw is less than the `middle` value. Otherwise, we need her to turn until her yaw decreases to 0, then keep going until her yaw decreases to the `middle`.

Finally, we move Misty forward. We use the `DriveHeading()` command, which allows us to drive Misty on a very precise heading. Once her drive is over, we stop her and unregister from all events, ending the program.

## `graphingTest.py`

In this program, we can experiment with the graphing properties for the upcoming `odometryMapping.py` program without having to move Misty. We simply create our own values the positions objects and Misty.

Unlike most of our other programs, this one has no functions or callbacks. It also requires some additional setup. In the `path` variable, provide a path to wherever you want the graphs and background maps stored. Alternatively, tou can also change the variable `save` to `False` if you don't want the graphs saved, but the background image has to be saved somewhere for the program to work.

If you haven't installed the required packages already, do so now with the commands `pip install matplotlib` in your terminal. This should also install numpy and Pillow if needed.

First, we use `os.chdir()` to change to the specified directory.

We need to get the specified map from Misty. However, we only have the plaintext name of the map, not the alphanumeric key that we need to access it. We get the entire list of maps from Misty, which contains the name and key for each map. We can then find the key that matches our name and use that to set Misty's current map. Once Misty's current map is set to the one we've specified, we can finally get the actual data it contains.

The map data is a 2D array where each element is one of four values. We replace each of these with a different value between 0 and 255. We then convert this array to a numpy array of unsigned 8-bit integers, and then convert that to an image using the Image module from Pillow. Finally, we rotate it 90 degrees so that the axes match a traditional Cartesian plane orientation (Misty's mapping system places the origin at bottom right, with the x-axis vertical towards the top and the y-axis horizontal towards the left).

We now need to put this image as the background of our graph. We use matplotlib to create a `fig` figure containing one `ax` graph (or set of axes). We save the image as a PNG, then try opening it with matplotlib. Finally, we show it as the background of our `ax` graph. We specify that the `cmap` colormap is `gray`, so that values of 255 are white and 0 are black. We set the axis labels and title of the graph, and then move on to plotting Misty's movement.

We get the map from Misty again, but we're now only interested in the value `"metersPerCell"`, which is the length in meters that each grid cell covers. When we divide the driving distance in meters by this value, we get the driving distance in cells.

We've provided Misty's starting and ending positions in grid coordinate units, but her yaw values can't be graphed without creating some "end" position. We'll use the driving distance as a length, and graph the location Misty would end up in if she drove towards that yaw value.

First, however, we need to talk about the `offset` value. Despite my best efforts, there is no way to determine Misty's absolute yaw value relative to the occupancy grid (unless you count eyeballing it, which I don't). Misty's yaw is set to 0 when she starts up. 

TO BE CONTINUED...