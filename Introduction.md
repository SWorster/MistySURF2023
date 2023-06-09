# Introduction to Misty

#### Julia Yu and Skye Worster

## Setup

### Handling

_**DO NOT**_ pick up Misty [by the arms](https://docs.mistyrobotics.com/misty-ii/robot/misty-ii/#unpacking-the-misty-ii). She can be picked up by the torso (which the arms are attached to) or the base.

_**DO NOT**_ place Misty on tables or raised surfaces. Misty should always be on the ground to avoid fall damage, even if she is under heavy supervision. It is surprisingly easy to accidentally activate her locomotive controls, and she is _**VERY**_ expensive and difficult to repair. The only exception is when using the provided foam block to lift her treads off the ground, as this prevents her from moving. This should only be done in a controlled environment under supervision.

[To power her on](https://docs.mistyrobotics.com/misty-ii/robot/misty-ii/#powering-up-amp-powering-down), use the switch on the rear underside of the base. She may take a long time to power up fully, especially if she needs to install updates. To restart Misty, power her off and wait ten seconds before switching her on.

### Charging

The version of Misty that we have [charges wirelessly](https://docs.mistyrobotics.com/misty-ii/robot/misty-ii/#wireless-charging). Place the charging station on the floor. Place Misty on the platform facing outward. Align the triangular symbols on the platform with the ones on the sides of Misty’s base. When charging, the chest LED will pulse orange and the fans will turn on. Misty can be on or off while charging, but will stop charging after four hours if she is off. When fully charged, the LED will be a solid orange.

### Internet

The simplest way to connect Misty to WiFi is through the [Misty Studio mobile app](https://docs.mistyrobotics.com/tools-&-apps/mobile/misty-app/#connecting-misty-to-bluetooth-and-wi-fi). Download the app on your mobile device, turn on Bluetooth, and turn on location services for the Misty app. In the app, connect to Misty. The app may take a few minutes to load and connect, so be patient. If it still doesn’t connect, try connecting [via USB](https://docs.mistyrobotics.com/misty-ii/robot/misty-ii/#connecting-to-wi-fi).

Once the mobile app is connected to Misty, the [IP address](https://docs.mistyrobotics.com/tools-&-apps/mobile/misty-app/#getting-information-about-misty) will be shown on the next screen along with the battery percentage. The app also lets the user [drive Misty](https://docs.mistyrobotics.com/tools-&-apps/mobile/misty-app/#driving-misty-with-the-misty-app).

After connecting to WiFi, Misty will start to get [updates automatically](https://docs.mistyrobotics.com/misty-ii/robot/system-updates/). If needed, there is also an Update Manager in Misty Studio to begin updating manually.

### Misty Studio on browser

The webpage version of Misty Studio is much more powerful than the app. In a browser page, type `http://MISTY-IP-ADDRESS-HERE/`. You must be on the same WiFi network as Misty.

This section focuses on Misty’s most basic capabilities. Further details on how to use Misty Studio are in the section below, but we recommend following along with the simple movement commands on the Wizard page.

### Locomotion

Before trying to move Misty, familiarize yourself with the Halt button on the top right of the Misty Studio browser page. This will cancel all of Misty’s movements and actions. We also recommend being prepared to physically grab the robot to prevent it from running headlong into danger.

Misty has eight movement options. These directions are aligned with the base/torso orientation, not with the head. When using the Misty Studio browser platform, it is easy to get confused by the camera showing Misty’s point of view. Practice with the movement controls without looking at this camera, or while the head is facing forward.

Misty’s speed is controlled by the slider. Always start at a slower speed!

- **Forward/backward**: Misty can drive forward and backward at the given speed. It may take a few seconds for her to accelerate to that speed. We recommend starting with slower speeds until the handler is accustomed to the acceleration.
- **Turning in place**: The left and right arrows turn Misty without changing her position. This is done by running the treads in opposition. Depending on the friction of the floor, this movement may place a fair bit of stress on the motors. It is not uncommon to experience a stuttering, jerky turning movement, especially at higher speeds. We recommend turning at low speeds and being patient.
- **Turning while moving**: the diagonal controls turn Misty while she is moving forward or backward. These turns are very gradual, but are smoother than turning in place. With some practice, three-point turns might be more time-efficient and elegant than turning in place.

### Body orientation

Misty’s [position and orientation](https://docs.mistyrobotics.com/misty-ii/robot/misty-ii/#coordinate-system-amp-movement-ranges) are set to 0 when she boots up. These change when she moves or when someone moves her manually.

Misty’s body has an Internal Measurement Unit (IMU) that records and updates her position and orientation. To view Misty’s orientation data, click Live Data in the top right corner of Misty Studio. Scroll down and check the boxes next to IMU Sensors.

- **Roll**: rotation around the forward (X) axis. Think leaning side-to-side.
- **Pitch**: rotation around the horizontal (Y) axis. Think up/down tilt.
- **Yaw**: rotation around the vertical (Z) axis. Think basic left/right turning.

The body records the velocities for roll, pitch, and yaw. The body also records X, Y, and Z axis acceleration. Note that when Misty is stationary, her Z acceleration is -9.8 m/s2 due to gravity.

### Head and arm orientation

Misty also records the position of its head and arms. In the Live Data tab, check the box next to Actuator Positions to view this data.

Misty’s head, like the base, records its roll, pitch, and yaw. These measurements are all 0 degrees when the head is in the neutral position. Head movements are limited in range.

- **Roll**: tilts the head side-to-side. Limited to 40 degrees in each direction.
- **Pitch**: raises and lowers the head. Limited to -40 degrees up and 26 degrees down.
- **Yaw**: turns the head left and right. Limited to 81 degrees in each direction.

Arm positions are also limited, from 90 degrees (straight down) to -26 degrees (raised). 0 degrees is straight forward.

Misty’s head and arms use separate measurement systems, so moving those will not affect the IMU readings.

All angles are measured in degrees, not radians. All movement programming should be done in degrees to maintain accuracy.

### Interface issues

Because of internet lag, Misty’s head and arm movement often stutters, and may not completely move to the specified position. We suspect that the slider interface may also be a factor. If Misty does not complete a movement, click on the slider again at the desired position.

## Misty Studio

### Wizard and Explore

Wizard is the starting page for the Studio, and it allows the user to adjust head position, arm position, the chest LED color, etc. It comes with built-in presets that change the various physical aspects of Misty. Explore goes into more depth for each capability, such as Expression, Locomotion, Vision, Hearing, and Mapping. In each category, there are options for changing what Misty does.

**Expression** lets the user change the chest LED, head movement, and arm movement. It also allows the user to choose a face display and play audio. The user can upload their own media to Misty. Note that the volume slider is at the top of the page, next to the Halt button. We recommend starting with a low volume.

**Location** shows Misty’s head camera, along with distance sensor reading in various directions. If the camera footage does not load, reload the page or try again with Google Chrome. To the right, there is a driving interface. The center button will halt the robot’s movement. There are also three boxes below for driving by time, turning, and driving by distance. Ensure that Misty has enough room to complete the given commands, and be prepared to manually halt her.

**Vision** has the ability to record video and take photos. Most importantly, it is also the interface for face detection, recognition, and training. Start with face training. Enter your name in the FaceID box, move your face in front of the camera, and click start training. Hold still until Misty is done. Then click Start Face Recognition to let Misty identify any faces she sees. Face Detection streams Misty’s face detection output to the browser console.

**Hearing** allows the user to record audio. It also has a program called Audio Localization, which we haven’t explored yet.

**Mapping** allows Misty to [map the layout](https://docs.mistyrobotics.com/misty-ii/misty-studio/mapping/) of a room. We haven’t experimented with this yet, and it seems that mapping has only been beta tested.

### Programming

There are multiple ways to program Misty, but we recommend using the Web API which utilizes HTML and JavaScript. Other methods include using C# in .NET applications or Python. Utilizing C# is the most supported, but is unavailable on non-Windows machines. Python, which is a highly accessible method like the Web API, is restrictive in that you can only have a single file running at a time and cannot use external libraries.

### Tutorials

_**DO NOT CLICK ON THESE!**_ There are 3 tutorials that are given in Misty Studio. When clicked on, they will immediately start to execute, so it’s not recommended that you use these.

### Settings
Various extra settings and info such as Studio Settings, WiFi, Update Management, and Diagnostics. Studio Settings is useful for resetting the robot’s various positions back to their defaults.

## Coding

Misty’s programs are called skills: a file or set of files that give Misty instructions to complete a task. Misty can store these skills internally and run them from her onboard processors, but she can also take commands from code running on your computer.

### External

We recommend using VS Code to create HTML/JavaScript programs. Many programming languages can access the Web API, but JavaScript is the most well-documented.

### Internal

Misty can also store and run code internally, but there are some limitations.

The best option is to use JavaScript and JSON in conjunction with the [Misty JavaScript](https://docs.mistyrobotics.com/tools-&-apps/plugins-&-extensions/misty-skills-extension/) extension for VS Code.

Misty can interpret Python skills, but can only handle one file at a time with no dependencies.

There is also a C# and .NET option, but this is only usable on Windows computers because it relies on Visual Studio extensions.
