# Misty’s Physical Controller

#### *Created by Julia Yu*

## Wiring the Circuit

##### The code does not match either diagram, either wire the controller according to the diagram and change the code, or, wire the controller according to the code.

### [Arduino Uno Version](https://www.circuito.io/app?components=97,97,97,97,512,11021,611984,2631981)

![Arduino Uno Layout](imgs/uno_wiring.png)

### [Arduino Nano / Nano Every Version](https://www.circuito.io/app?components=97,97,97,97,514,11022,611984,2631981)

##### Note: the board in the picture is a Nano, but Nano Every has the same pin ordering, size, and better specs

![Arduino Nano Layout](imgs/nano_wiring.png)

# Uploading the Arduino code to the board
* Starting off, let's assume you’re using the IDE that is downloadable [here](https://www.arduino.cc/en/software). It’s a similar process with the Web Editor and the older Arduino uploader if you decide to go with those routes, so you can follow along regardless.

* Side note: If you are using the Nano Every, you'll need to install a driver for the IDE to recognize the board, link [here](https://docs.arduino.cc/software/ide-v1/tutorials/getting-started/cores/arduino-megaavr).

* First, have the board plugged into your computer through USB.

* Open the IDE and check that the board selected in the upper left is the board you’re using (it should automatically detect the COM port that it’s using, you’ll need that for a line in the Python controller file). *Refer to figure 1 for help.*
  * For troubleshooting, please refer to the [Arduino Support Page](https://support.arduino.cc/hc/en-us/articles/4412955149586-If-your-board-does-not-appear-on-a-port-in-Arduino-IDE).

* Click the checkmark to verify the sketch (or in other words, check there are no issues with the code), and then click the arrow that points to the right which is next to the checkmark. This uploads the code to the board, don’t disconnect it. *Refer to figure 2 for help.*

* After the program is uploaded, check that everything works by opening the serial monitor in the upper right corner where there is a magnifying glass. If it prints out a series of 3 numbers that change when you move the joystick and press the buttons, that means everything is wired correctly and it’s ready to go. *Refer to figure 3 for help.*

* Close the serial monitor, which you can do by either closing the IDE or clicking the little “x” that appears on the serial monitor tab at the bottom of the screen (you must do this before you run the python file since only 1 application can access the serial monitor at a time). *Refer to figure 3 for help.*

* If you are using the HC-05 Bluetooth module to enable wireless communication between the hardware and your computer, unplug the 2 wires that go to the Arduino Uno's Tx and Rx pins, since having those wired to the board while uploading will cause an error. If you are using an Arduino Nano, you don't need to do this. For more info as to why, read [this](https://docs.arduino.cc/tutorials/nano-every/uart).

* Please note, if the following text appears when you are uploading the sketch to an Arduino Nano Every, refer to [this link](https://support.arduino.cc/hc/en-us/articles/4405239282578-avrdude-jtagmkII-initialize-Cannot-locate-flash-and-boot-memories-in-description) for more information about what that means.

![Nano Every Warning](imgs/every_warning.png)

![Reference 1](imgs/ref1.png)

<p style="text-align: center;"> <em> Figure 1: Getting the computer to recognize the board </em> </p>

![Reference 2](imgs/ref2.png)

<p style="text-align: center;"> <em> Figure 2: Verifying and Uploading the Sketch (the pink and green boxes respectively) </em> </p>

![Reference 3](imgs/ref3.png)

<p style="text-align: center;"> <em> Figure 3: Opening and Closing the Serial Monitor (the orange and yellow boxes respectively) </em> </p>

# Connecting the Bluetooth Module to Your Computer

For Windows users, you will need to first connect to it via your Bluetooth settings. The password should be either 1234 or 0000 if it is at its defaults. Then, go to Control Panel and click *View devices and printers*. Scroll down to select the module and click the *Hardware* tab. Note down the *Standard Serial over Bluetooth* COM port, which will be used in the Python program.

For Mac and Linux users, you should also start by connecting to the module in your Bluetooth settings, password referenced above. Then open a Terminal window and type `ls /dev/tty.*` and press enter. You should see something like `/dev/tty.HC-05` listed. Use this in the Python program in place of the COM port used in Windows.

# Run the Python File
* If you don't have Python, [download at least 3.10](https://www.python.org/downloads/) and add it to your PATH. If you do have Python already, please update to 3.10 or later.

* Install the following python packages through pip. The second line should install the packages following it, but in case it doesn’t, the others are also listed. Check back in the Misty Walkthrough for more details on what versions specifically to install if this is the case.
  * `pip install pyserial`
  * `pip install Misty-SDK`
  * `pip install requests`
  * `pip install websocket-client`
  * `pip install yapf`

* Specifically: `requests` should be at least 2.25.1, `websocket-client` should be at most 0.57.0, and `yapf` should be at least 0.30.0.
* Please make sure that you are using Python 3.10 or later, as it has some syntax that was introduced during that version. If you really want to use something earlier, make sure you change the code in the callback functions `_TOFProcessor()` and `_BumpSensor()`

* When trying to run the controller file, you will need to change the IP address (line 8) to match it in the program to the one that your Misty uses. You also need to change the COM address (line 9) to match it to the one that the Arduino uses, or if intending to use the Bluetooth module, whatever port it is connected to on your computer.

* Run the file in Terminal / Command Prompt using `python <name-of-file.py>` while in the same directory and with the Arduino still plugged into your computer.

* If everything was done correctly, you have a functioning controller!

# Arduino Line-by-Line Code Walkthrough

#### Find the Arduino Documentation [Here](https://www.arduino.cc/reference/en/)

*Declarations and Variables*

``` cpp
#define VRX_PIN  A1
#define VRY_PIN  A0
#define SW_PIN   7
#define TREAD_BTN  6
#define ARM_BTN  5
#define HEAD_BTN 4
#define EXIT_BTN 3
```

The [#define statements](https://www.arduino.cc/reference/en/language/structure/further-syntax/define/) are somewhat like constants. These will assign a value to the given name of a variable, though these have their own drawbacks. These can be changed to be constants via something akin to `const int X = ...`.

Overall, these are used to tell the program what pins the buttons and joystick are hooked up to, and can be changed depending on the wiring of the actual circuit.

```cpp
int xValue = 0;
int yValue = 0;
int yellowState = 0;
int blueState = 0;
int greenState = 0;
int redState = 0;

int mode = 1;
const int timeDelay = 150;

int exitCounter = 0;

int treadState;
int lastYellowState = LOW;
int armState;
int lastBlueState = LOW;
int headState;
int lastGreenState = LOW;
int stopState;
int lastRedState = LOW;

unsigned long lastTreadTime = 0;
unsigned long lastArmTime = 0;
unsigned long lastHeadTime = 0;
unsigned long lastStopTime = 0;

unsigned long debounceDelay = 150;
```

These are global variables that are meant to keep track of certain values that would be important for us in this program. `xValue` and `yValue` are used for the joystick, while the different colored `__States` are used for the buttons. `Mode` is used for tracking which commands to send to Misty, and `timeDelay` is a constant that is user changeable in order to create a buffer between each line outputted in the Serial Monitor. `exitCounter` is used in order to provide a reset in the data sent over serial when using Bluetooth.

The following variables are adapted from the button debounce example code that can be found in the Arduino Examples folder. The purpose of these are to filter out any electrical interference that the buttons may create when not actually pressed and to create a threshold amount of time the button has to be pressed in order to recognize that the user has indicated a mode change.

*Setting Up*

```cpp
void setup() {
  #if defined(ARDUINO_AVR_NANO_EVERY) || defined(ARDUINO_AVR_NANO)
    Serial1.begin(9600);
    while (!Serial1);
  #elif defined(ARDUINO_AVR_UNO)
    Serial.begin(9600);
    while (!Serial);
  #else
    #error "Board Error"
  #endif

  pinMode(TREAD_BTN, INPUT);
  pinMode(ARM_BTN, INPUT);
  pinMode(HEAD_BTN, INPUT);
  pinMode(EXIT_BTN, INPUT);
}
```

The first thing that comes after constant declaration is the [setup loop](https://www.arduino.cc/reference/en/language/structure/sketch/setup/). It runs only once before the program moves on. Before the program starts to run, it checks the board that the code is being uploaded to. In doing so, it determines which code to use: if the board is of the Nano variant, it uses the other [UART channel](https://docs.arduino.cc/tutorials/nano-every/uart), if it is instead an Uno, it uses the only port that it has available. If it's neither, it will result in an error. Then it sets the `pinMode` for the buttons to be inputs, which is required in order for the program to know what the values coming in from those pins are.

*Forever Loop*

```cpp
void loop() {
  xValue = analogRead(VRX_PIN);
  yValue = analogRead(VRY_PIN);

  yellowState = digitalRead(TREAD_BTN);
  blueState = digitalRead(ARM_BTN);
  greenState = digitalRead(HEAD_BTN);
  redState = digitalRead(EXIT_BTN);

  if (yellowState != lastYellowState) lastTreadTime = millis();
  if (blueState != lastBlueState) lastArmTime = millis();
  if (greenState != lastGreenState) lastHeadTime = millis();
  if (redState != lastRedState) lastStopTime = millis();

  if ((millis() - lastTreadTime) > debounceDelay) {
    if (yellowState != treadState) {
      treadState = yellowState;
      if (treadState == HIGH) mode = 1;
    }
  }

  if ((millis() - lastArmTime) > debounceDelay) {
    if (blueState != armState) {
      armState = blueState;
      if (armState == HIGH) mode = 2;
    }
  }

  if ((millis() - lastHeadTime) > debounceDelay) {
    if (greenState != headState) {
      headState = greenState;
      if (headState == HIGH) mode = 3;
    }
  }

  if ((millis() - lastStopTime) > debounceDelay) {
    if (redState != stopState) {
      stopState = redState;
      if (stopState == HIGH) mode = 4;
    }
  }

  lastYellowState = yellowState;
  lastBlueState = blueState;
  lastGreenState = greenState;
  lastRedState = redState;

  if (exitCounter >= 4) {
    exitCounter = 0;
    mode = 1;
  }

  #if defined(ARDUINO_AVR_NANO_EVERY) || defined(ARDUINO_AVR_NANO)
    Serial1.print(xValue);
    Serial1.print(" ");
    Serial1.print(yValue);
    Serial1.print(" ");
    Serial1.println(mode);
  #elif defined(ARDUINO_AVR_UNO)
    Serial.print(xValue);
    Serial.print(" ");
    Serial.print(yValue);
    Serial.print(" ");
    Serial.println(mode);
  #else
    #error "Board Error"
  #endif

  delay(timeDelay);

  if (mode == 4) exitCounter++;
}
```

The loop runs the code in it over and over forever, and is where all the action happens. First it gets the values for the joystick’s positioning and assigns them to `xValue` and `yValue` through [`analogRead()`](https://www.arduino.cc/reference/en/language/functions/analog-io/analogread/). The program then does the same with the buttons, but instead uses [`digitalRead()`](https://www.arduino.cc/reference/en/language/functions/digital-io/digitalread/) which can only return either `HIGH` or `LOW` (2 values in opposition to `analogRead` being able to return numbers ranging from 0 to 1023).

The first 4 if statements are used to update the amount of time its been since the buttons have been pressed by checking if their values don't match what the previous button readings were. Then the next 4 are to check if the button has been pressed by checking the amount of time against a delay. If the value read in doesn't match the previous value, they swap, and then check if the buttons were pressed by comparing them to `HIGH`. This changes the mode accordingly. Then it saves the states from the current iteration to use in the next.

The next part of the code is for resetting the output to the serial monitor under Bluetooth. Once the exit command has been printed 4 times, the mode will reset back to 1 and the counter back to 0. The reason for this is because while not using the Bluetooth module, the program will end once the mode is 4 and the serial output will be restarted. With Bluetooth this is not the case and it will keep sending data regardless if there is a program to read the data or not.

`Serial.print()` and `Serial.println()` are the Serial Monitor print statements of Arduino. The purpose of having these here is to interface with the pySerial library in the Python program. It takes information from the Serial Monitor and allows us to use it for other purposes. Depending on the board being used, the output will either be to `Serial` or to `Serial1`, which is different depending on whether or not you are using a Nano with Bluetooth, a Nano on its own, or an Uno.

The delay will prevent the data from being sent too fast to the point of overloading Misty with commands via the Python program.

The final if statement is there to increment the exit counter in order for the reset to occur.

# Python Line-by-Line Code Walkthrough

*Python Imports and Misty, Constant, and Global Declaration*

```python
import serial
import time
from mistyPy.Robot import Robot
from mistyPy.Events import Events
```

These are the libraries that the code needs. See the above section on how to install them.

```python
MISTY_IP = "<insert Misty IP>"
ARDUINO_PORT = "<insert Arduino COM>"
```

These lines are constants which contain the IP address Misty uses and the COM / port that the Arduino (or the Bluetooth module) uses when connected to your computer.

```python
moveForwardToF = True
moveBackwardToF = True
contactFrontBumper = False
contactBackBumper = False
bumperTouched = [False, False, False, False]

NORTH = 341
SOUTH = 682
LEFT = 341
RIGHT = 682

tof_dist = .25  # distance to trigger avoidance behavior

# tread movement speeds
lin_v = 20  # linear velocity for forward/backward
ang_v = 20  # angular velocity for left/right
lin_turn = 20  # linear velocity while turning
ang_turn = 20  # angular velocity while turning

# arm movement variables
arm_up = -29  # max arm height
arm_down = 90  # min arm height
arm_v = 50  # arm movement speed
arm_unit = "degrees"  # unit type

# head movement variables
pitch_up = -40  # max pitch
pitch_down = 26  # min pitch
pitch_v = 100  # pitch movement speed
yaw_left = 81  # left yaw
yaw_right = -81  # right yaw
yaw_v = 85  # yaw movement speed
roll_left = -40  # roll left
roll_right = 40  # roll right
roll_v = 100  # roll movement speed
head_unit = "degrees"

misty = Robot(MISTY_IP) # create a Misty instance using its IP address (which varies from robot to robot)
```

From top to bottom, the first 2 global variables are used to allow Misty to move forwards or backwards, determined by data obtained from the time-of-flight sensors in the front and back. The next 3 globals, like the previous 2, determine whether or not Misty can move depending on whether or not the bumper sensors on the base are pressed.

The 4 constants named for the directions that the joystick can be held are used as thresholds for each movement option that exists. These can be changed if the user finds that the joystick returns different values. Everything before the last line are variables for holding numbers constantly used throughout the program repetitively.

The last thing is a Misty instance which uses the given IP address to establish a connection to the robot.

*Time-of-Flight Sensor Callback*

```python
def _TOFProcessor(data):
    global moveForwardToF, moveBackwardToF
    distance = data["message"]["distanceInMeters"]
    sensor = data["message"]["sensorId"]
    valid = data["message"]["status"]
    if distance < .25 and valid == 0:
        match sensor:
            case "toffc":
                moveForwardToF = False
                misty.Stop()
            case "tofr":
                moveBackwardToF = False
                misty.Stop()
    elif valid == 0 and distance > .25:
        match sensor:
            case "toffc":
                moveForwardToF = True
            case "tofr":
                moveBackwardToF = True
```

A time-of-flight sensor (or ToF) is used to calculate the distance an object lies from the sensor by sending out a laser and calculating the distance by using the time it takes to hit the object and the speed of light.

This function is used when the event set up in main is triggered. It works by checking to see if the front center sensor or rear sensor have been triggered (seeing something at a a distance of .25 meters) and it is a valid measurement. If it is, it stops Misty's movement and prevents it from moving any closer. Once Misty moves out of range, she can move in the original direction she was heading.

A caveat with this function is that Misty has to move out of the way, not the object she detected. This will be further explored later to see if we can adjust the code such that it doesn't need to be this way.

*Collision Sensor Callback*

```python
def _BumpSensor(data):
    try:
        global contactFrontBumper, contactBackBumper, bumperTouched
        touched = data["message"]["isContacted"]
        partTouched = data["message"]["sensorId"]
        if touched:
            misty.PlayAudio("A_VineBoom.mp3", 5)
            match partTouched:
                case "bfr": # front right
                    bumperTouched[1] = True
                    misty.ChangeLED(255, 0, 0)
                    misty.Stop()
                case "bfl": # front left
                    bumperTouched[0] = True
                    misty.ChangeLED(0, 255, 0)
                    misty.Stop()
                case "brl": # back left
                    bumperTouched[2] = True
                    misty.ChangeLED(0, 0, 255)
                    misty.Stop()
                case "brr": # back right
                    bumperTouched[3] = True
                    misty.ChangeLED(69, 69, 69)
                    misty.Stop()
        else:
            match partTouched:
                case "bfr":
                    bumperTouched[1] = False
                case "bfl":
                    bumperTouched[0] = False
                case "brl":
                    bumperTouched[2] = False
                case "brr":
                    bumperTouched[3] = False
        if bumperTouched[0] == False and bumperTouched[1] == False:
            contactFrontBumper = False
        else:
            contactFrontBumper = True
        if bumperTouched[2] == False and bumperTouched[3] == False:
            contactBackBumper = False
        else:
            contactBackBumper = True
    except Exception as e:
        print("EXCEPTION:", e)
```

There are 4 bumper sensors on the robot's base, which is what this function uses. When any of the 4 bumper sensors are pressed, the LED on Misty's chest changes color, she will make a noise, and her movement will stop. The color depends on the last sensor pressed, meaning that one can be pressed and then another which is recognized and the color shown will be of the most recent sensor. After the sensors are no longer in contact with anything, Misty will be able to move again.

*Treads Control*

```python
def treads(coords):
    split = coords.split()
    x = int(split[0])
    y = int(split[1])
    if y < NORTH and x > LEFT and x < RIGHT and (not contactFrontBumper) and moveForwardToF: # move forward (hold up on joystick)
        misty.Drive(linearVelocity = 20, angularVelocity = 0)
    elif y > SOUTH and x > LEFT and x < RIGHT and (not contactBackBumper) and moveBackwardToF: # move backward (hold down on joystick)
        misty.Drive(linearVelocity = -20, angularVelocity = 0)
    elif x < LEFT and y > NORTH and y < SOUTH: # turn left (hold left on joystick)
        misty.Drive(linearVelocity = 0, angularVelocity = 20)
    elif x > RIGHT and y > NORTH and y < SOUTH: # turn right (hold right on joystick)
        misty.Drive(linearVelocity = 0, angularVelocity = -20)
    elif x < LEFT and y < NORTH and (not contactFrontBumper) and moveForwardToF: # forward + left (hold upper left on joystick)
        misty.Drive(linearVelocity = 20, angularVelocity = 20)
    elif x > RIGHT and y < NORTH and (not contactFrontBumper) and moveForwardToF: # forward + right (hold upper right on joystick)
        misty.Drive(linearVelocity = 20, angularVelocity = -20)
    elif x < LEFT and y > SOUTH and (not contactBackBumper) and moveBackwardToF: # backward + left (hold lower left on joystick)
        misty.Drive(linearVelocity = -20, angularVelocity = 20)
    elif x > RIGHT and y > SOUTH and (not contactBackBumper) and moveBackwardToF: # backward + right (hold lower right on joystick)
        misty.Drive(linearVelocity = -20, angularVelocity = -20)
    else:
        misty.Stop()
```

This function is used when the button corresponding to `mode = 1` was pressed. It is also the initial movement option selected when first connecting and starting the controller up. The function has a single parameter which should be a string that was obtained from data in the Serial Monitor.

The first thing the function does is split the given string into an array of strings through `split()`, which defaults to separation via spaces. It then takes the first and second things in the array and changes them to be integers through `int()`. The reason it takes the first and second entries in the array is because of how the Arduino code is structured to print to the Serial Monitor. It first would print the X value, then the Y value, and finally the mode.

The following if-else chain is to correspond with the various situations that the joystick can be in at any given moment. The picture shown below is a good diagram that shows the coordinate system that the joystick uses.

[![Joystick Diagram](imgs/joystickMap.png "Click for source link")](https://lastminuteengineers.com/joystick-interfacing-arduino-processing/)

[`Misty.Drive()`](https://docs.mistyrobotics.com/misty-ii/web-api/api-reference/#drive) is evaluated using 2 parameters: `linearVelocity` and `angularVelocity`. Both handle the speed at which the treads go, from 0 to a maximum of 100. Linear handles speed straight ahead, while angular handles how much it turns (which is done by having one tread either be at a slower speed or not move at all). Holding up will drive Misty forward, while holding down will back her up. Left and right serve to turn Misty to the corresponding direction, and holding the joystick in any of the 4 remaining directions will evaluate to a combination of turning and moving forwards or backwards.

[`Misty.Stop()`](https://docs.mistyrobotics.com/misty-ii/web-api/api-reference/#stop) stops Misty's movement, which is what happens when the joystick is at resting position (otherwise known as the center).

*Arm(s) Control*

```python
def arms(data):
    split = data.split()
    x = int(split[0])
    y = int(split[1])
    if y < NORTH and x > LEFT and x < RIGHT: # left arm up (hold up on joystick)
        misty.MoveArm(arm = "left", position = -29, velocity = 50, units = "degrees")
    elif y > SOUTH and x > LEFT and x < RIGHT: # left arm down (hold down on joystick)
        misty.MoveArm(arm = "left", position = 90, velocity = 50, units = "degrees")
    elif x < LEFT and y > NORTH and y < SOUTH: # right arm down (hold left on joystick)
        misty.MoveArm(arm = "right", position = 90, velocity = 50, units = "degrees")
    elif x > RIGHT and y > NORTH and y < SOUTH: # right arm up (hold right on joystick)
        misty.MoveArm(arm = "right", position = -29, velocity = 50, units = "degrees")
    elif (x < LEFT and y < NORTH) or (x > RIGHT and y < NORTH): # both arms up (hold upper left or upper right on joystick)
        misty.MoveArm(arm = "both", position = -29, velocity = 50, units = "degrees")
    elif (x < LEFT and y > SOUTH) or (x > RIGHT and y > SOUTH): # both arms down (hold lower left or lower right on joystick)
        misty.MoveArm(arm = "both", position = 90, velocity = 50, units = "degrees")
    else:
        misty.Stop()
```

This function is very similar structure-wise to the above function for the treads as it uses all of the same controls on the joystick to do different things.

The first thing that is different is that it's only activated when a different button is pushed, being the one that corresponds to set `mode = 2`. It combines when the joystick is held at the upper left or right positions, as well as the lower left and right positions, in order to account for if the user would like to raise or lower both arms at once. Left and right will lower and raise the right arm respectively, while up and down will raise and lower the left arm. This function also has `misty.Stop()` in order to stop the arm movement when the user is no longer holding the joystick in a direction that is not it's resting position.

The way [`misty.MoveArm()`](https://docs.mistyrobotics.com/misty-ii/web-api/api-reference/#movearm) works is by having 2 parameters and 2 optional parameters. The 2 required are the arm that you would like to move, and the position that you would like the arm to move to. The other 2 parameters are the velocity at which the arm will move to the given position, and the units to use when moving Misty's arm(s).

*Head Control*

```python
def head(data):
    split = data.split()
    x = int(split[0])
    y = int(split[1])
    if y < NORTH and x > LEFT and x < RIGHT: # pitch up (hold up on joystick)
        misty.MoveHead(pitch = -40, velocity = 100, units = "degrees")
    elif y > SOUTH and x > LEFT and x < RIGHT: # pitch down (hold down on joystick)
        misty.MoveHead(pitch = 26, velocity = 100, units = "degrees")
    elif x < LEFT and y > NORTH and y < SOUTH: # yaw left (hold left on joystick)
        misty.MoveHead(yaw = 81, velocity = 85, units = "degrees")
    elif x > RIGHT and y > NORTH and y < SOUTH: # yaw right (hold right on joystick)
        misty.MoveHead(yaw = -81, velocity = 85, units = "degrees")
    elif x < LEFT and y < NORTH: # roll left (hold upper left on joystick)
        misty.MoveHead(roll = -40, velocity = 100, units = "degrees")
    elif x > RIGHT and y < NORTH: # roll right (hold upper right on joystick)
        misty.MoveHead(roll = 40, velocity = 100, units = "degrees")
    else:
        misty.Stop()
```

Like the other 2 functions above, this one is also very similar. There is however, 2 missing conditionals as they aren't needed in this case.

Misty's head is able to move in 3 dimensions (x, y, z) or (roll, pitch, yaw). See the handy diagram below to have gain a better understanding about what each mean.

<a href="https://www.linearmotiontips.com/motion-basics-how-to-define-roll-pitch-and-yaw-for-linear-systems/">
    <img src="imgs/Roll-Pitch-Yaw.jpg" alt="3D Diagram" width="60%" height="60%">
</a> 

If you still don't really understand, think of it this way: pitch will cause Misty to nod, roll will cause Misty to shake her head no, and yaw will cause Misty to look like a cat tilting their head to the side.

So, according to the code, pushing up or down on the joystick will cause Misty to move her head up and down, left and right will cause Misty to turn her head left and right, and holding the joystick to either the top left or top right will cause Misty to tilt her head.

The way that [`misty.MoveHead()`](https://docs.mistyrobotics.com/misty-ii/web-api/api-reference/#movehead) works is by having 3 required parameters, one for roll, pitch, and yaw. These will default to 0 if not specified. This method also uses velocity, which defaults to 10, duration of how long to move the head for (though the documentation specifies to only pass in a value for either velocity or duration and not both), and the units that the roll, pitch or yaw would be specified in.

*Mode Selection*

```python
def mode(data):
    split = data.split()
    command = int(split[2])
    if command == 1:
        treads(data)
    elif command == 2:
        arms(data)
    elif command == 3:
        head(data)
    elif command == 4:
        print("stop misty communication")
```

Like all the other functions created above, this one also uses data from the Serial Monitor. However, `mode()` is not reliant on where the joystick is positioned. It relies on whichever button has been recently pressed in order to change what the joystick will act as. Remembering the Arduino code, the way that data is printed to the Serial Monitor is by first having the x and y coordinates of the joystick, and then the integer corresponding to the mode, changeable only through button presses.

All in all, the process is the same, but only with 1 number and it won't fluctuate if you try and move it.

*Changing Misty's Settings*

```python
def init():
    misty.UpdateHazardSettings(disableTimeOfFlights = True)
    misty.MoveHead(0, 0, 0)
    misty.ChangeLED(255, 200, 0)
```

The purpose of having this function is to disable the hazard system's time-of-flight sensors and to reset the head to the neutral position. The reason we disable the TOF sensors is because (for the robot that we're testing this code on), the sensors on the bottom are being triggered and showing odd readings which indicate that Misty thinks she's about to fall off a cliff which stops her from moving correctly. We circumvent this by disabling them, which still allows for event TOF functions to work.

*Bringing it All Together*

```python
if __name__ == "__main__":
    init()
    ser = serial.Serial(ARDUINO_PORT, 9600, timeout = 1) # open connection to the COM port that the Arduino is connected to to get serial data from it
    time.sleep(1) # stop for a second

    'set up the event listeners for the bumpers and ToF respectively'
    misty.RegisterEvent(event_name = "stop", event_type = Events.BumpSensor, callback_function = _BumpSensor, keep_alive = True)
    misty.RegisterEvent(event_name = "tof", event_type = Events.TimeOfFlight, callback_function = _TOFProcessor, keep_alive = True, debounce = 150)

    while True:
        line = ser.readline() # get next line of the serial monitor (its in bytes)
        if line:
            string = line.decode() # convert the bytes to a string
            if " " in string:
                strip = string.strip() # strip the string of a newline character and return character
                mode(strip)
                if int(strip.split()[2]) == 4: # break out of infinite while if specific button pressed
                    misty.UnregisterAllEvents()
                    misty.StopAudio()
                    break
    ser.close() # close the serial connection
```

The first thing called is `init()`, which was discussed above. This is important since it resets the head position and disables the sensors on the bottom which hindered the movement the robot could take. This may not be needed on other Misty units, but on this one, it is.

Using [`serial.Serial()`](https://pythonhosted.org/pyserial/pyserial_api.html) we are able to open communications between the COM port on a computer and this Python script.

[`misty.RegisterEvent()`](https://docs.mistyrobotics.com/misty-ii/dotnet-sdk/dotnet-skill-architecture/#registering-amp-unregistering-events) creates a listener to check if a certain peripheral has been triggered. The 2 instances here create listeners for the bumpers and the TOF sensors. Other types of events can be found [here](https://docs.mistyrobotics.com/misty-ii/robot/sensor-data/). Afterwards, the LED on Misty's chest will change color.

[`ser.readline()`](https://pyserial.readthedocs.io/en/latest/shortintro.html?highlight=readline#readline) lets us get a single line of data from the Serial Monitor in a byte object. If this results in anything, it goes ahead and decodes it from being in bytes to being a string in Python we can manipulate. We then check to make sure that there is a space in the string, as it would not be a valid piece of data otherwise. If there is, the string will be stripped of the newline character that comes at the end of it, and the result will be passed into `mode()`.

After `mode()` evaluates, if the mode is equal to 4, that means that the user pressed the button corresponding to 4 and the code will break out of the infinite `while`  that was made and then will close the communication between the Serial Monitor and the Python script and terminate the program.
