# Julia Yu '24

# Imports
import serial
import time
from mistyPy.Robot import Robot
from mistyPy.Events import Events

# Place the following information into the 2 constants below
MISTY_IP = "insert Misty IP"
ARDUINO_PORT = "insert Arduino COM"

# ToF variables track if Misty can move in the corresponding direction based on obstacles in her path
moveForwardToF = True
moveBackwardToF = True

# Bumper contact variables track if Misty hits something and shouldn't move in that direction
contactFrontBumper = False
contactBackBumper = False
# front left, front right, rear left, rear right
bumperTouched = [False, False, False, False]

# Thresholds for the joystick position to move in different directions
NORTH = 341  # North and South are in Y
SOUTH = 682
LEFT = 341  # Left and Right are in X
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

# create a Misty instance using its IP address
misty = Robot(MISTY_IP)


def _TOFProcessor(data):  # Processes ToF sensor data, prevents collisions
    # tracks if obstacle in front of or behind Misty
    global moveForwardToF, moveBackwardToF

    distance = data["message"]["distanceInMeters"]  # distance to object, float
    sensor = data["message"]["sensorId"]  # which sensor sent data, str
    valid = data["message"]["status"]  # if measurement is valid, bool

    if distance < tof_dist and valid == 0:  # if object close and measurement valid
        match sensor:  # case for each sensor
            case "toffc":  # if front center, stop moving forward
                moveForwardToF = False
                misty.Stop()
            case "tofr":  # if rear sensor, stop moving backward
                moveBackwardToF = False
                misty.Stop()

    # if object far away, allow movement in that direction
    elif valid == 0 and distance > tof_dist:
        match sensor:
            case "toffc":
                moveForwardToF = True
            case "tofr":
                moveBackwardToF = True


def _BumpSensor(data):  # When bumped, LED changes color and stops
    try:
        # tracks which of the 4 bumpers have been pressed and modifies if it's in contact with something
        global contactFrontBumper, contactBackBumper, bumperTouched
        touched = data["message"]["isContacted"]  # touched T or released F
        partTouched = data["message"]["sensorId"]  # string sensor source

        if touched:  # if bumper pressed
            misty.PlayAudio("A_VineBoom.mp3", 5)
            match partTouched:  # case for each bumper
                case "bfr":  # front right
                    bumperTouched[1] = True  # record which bumper touched
                    misty.ChangeLED(255, 0, 0)  # LED red
                    misty.Stop()  # stop moving
                case "bfl":  # front left
                    bumperTouched[0] = True
                    misty.ChangeLED(0, 255, 0)  # LED green
                    misty.Stop()
                case "brl":  # back left
                    bumperTouched[2] = True
                    misty.ChangeLED(0, 0, 255)  # LED blue
                    misty.Stop()
                case "brr":  # back right
                    bumperTouched[3] = True
                    misty.ChangeLED(69, 69, 69)  # LED white
                    misty.Stop()

        else:  # if bumper released
            match partTouched:  # case for each bumper
                case "bfr":
                    bumperTouched[1] = False  # change array value to false
                case "bfl":
                    bumperTouched[0] = False
                case "brl":
                    bumperTouched[2] = False
                case "brr":
                    bumperTouched[3] = False

        # if no front bumper touched, allow forward movement
        if bumperTouched[0] == False and bumperTouched[1] == False:
            contactFrontBumper = False
        else:  # if a front bumper touched
            contactFrontBumper = True  # prevent forward movement

        # same, for back bumpers
        if bumperTouched[2] == False and bumperTouched[3] == False:
            contactBackBumper = False
        else:
            contactBackBumper = True

    except Exception as e:  # catch and print error
        print("EXCEPTION:", e)


def treads(coords):  # Controls the treads for overall mobility
    split = coords.split()  # data format: [x, y, mode]
    x = int(split[0])
    y = int(split[1])

    # move forward (hold up on joystick)
    if y < NORTH and LEFT < x < RIGHT and (not contactFrontBumper) and moveForwardToF:
        misty.Drive(linearVelocity=lin_v, angularVelocity=0)

    # move backward (hold down on joystick)
    elif y > SOUTH and LEFT < x < RIGHT and (not contactBackBumper) and moveBackwardToF:
        misty.Drive(linearVelocity=-lin_v, angularVelocity=0)

    # turn left (hold left on joystick)
    elif x < LEFT and NORTH < y < SOUTH:
        misty.Drive(linearVelocity=0, angularVelocity=ang_v)

    # turn right (hold right on joystick)
    elif x > RIGHT and NORTH < y < SOUTH:
        misty.Drive(linearVelocity=0, angularVelocity=-ang_v)

    # forward + left (hold upper left on joystick)
    elif x < LEFT and y < NORTH and (not contactFrontBumper) and moveForwardToF:
        misty.Drive(linearVelocity=lin_turn, angularVelocity=ang_turn)

    # forward + right (hold upper right on joystick)
    elif x > RIGHT and y < NORTH and (not contactFrontBumper) and moveForwardToF:
        misty.Drive(linearVelocity=lin_turn, angularVelocity=-ang_turn)

    # backward + left (hold lower left on joystick)
    elif x < LEFT and y > SOUTH and (not contactBackBumper) and moveBackwardToF:
        misty.Drive(linearVelocity=-lin_turn, angularVelocity=ang_turn)

    # backward + right (hold lower right on joystick)
    elif x > RIGHT and y > SOUTH and (not contactBackBumper) and moveBackwardToF:
        misty.Drive(linearVelocity=-lin_turn, angularVelocity=-ang_turn)

    else:  # stop Misty from moving (default position on joystick)
        misty.Stop()


def arms(data):  # Controls the arm movement
    split = data.split()  # data format: [x, y, mode]
    x = int(split[0])
    y = int(split[1])

    if y < NORTH and LEFT < x < RIGHT:  # left arm up (hold up on joystick)
        misty.MoveArm(arm="left", position=arm_up,
                      velocity=arm_v, units=arm_unit)

    # left arm down (hold down on joystick)
    elif y > SOUTH and LEFT < x < RIGHT:
        misty.MoveArm(arm="left", position=arm_down,
                      velocity=arm_v, units=arm_unit)

    # right arm down (hold left on joystick)
    elif x < LEFT and NORTH < y < SOUTH:
        misty.MoveArm(arm="right", position=arm_down,
                      velocity=arm_v, units=arm_unit)

    # right arm up (hold right on joystick)
    elif x > RIGHT and NORTH < y < SOUTH:
        misty.MoveArm(arm="right", position=arm_up,
                      velocity=arm_v, units=arm_unit)

    # both arms up (hold upper left or upper right on joystick)
    elif (x < LEFT and y < NORTH) or (x > RIGHT and y < NORTH):
        misty.MoveArm(arm="both", position=arm_up,
                      velocity=arm_v, units=arm_unit)

    # both arms down (hold lower left or lower right on joystick)
    elif (x < LEFT and y > SOUTH) or (x > RIGHT and y > SOUTH):
        misty.MoveArm(arm="both", position=arm_down,
                      velocity=arm_v, units=arm_unit)

    else:
        misty.Stop()  # stop Misty's motion (default joystick position)


def head(data):  # Controls the head movement
    split = data.split()  # data format: [x, y, mode]
    x = int(split[0])
    y = int(split[1])

    if y < NORTH and LEFT < x < RIGHT:  # pitch up (hold up on joystick)
        misty.MoveHead(pitch=pitch_up, velocity=pitch_v, units=head_unit)

    elif y > SOUTH and LEFT < x < RIGHT:  # pitch down (hold down on joystick)
        misty.MoveHead(pitch=pitch_down, velocity=pitch_v, units=head_unit)

    elif x < LEFT and NORTH < y < SOUTH:  # yaw left (hold left on joystick)
        misty.MoveHead(yaw=yaw_left, velocity=yaw_v, units=head_unit)

    elif x > RIGHT and NORTH < y < SOUTH:  # yaw right (hold right on joystick)
        misty.MoveHead(yaw=yaw_right, velocity=yaw_v, units=head_unit)

    elif x < LEFT and y < NORTH:  # roll left (hold upper left on joystick)
        misty.MoveHead(roll=roll_left, velocity=roll_v, units=head_unit)

    elif x > RIGHT and y < NORTH:  # roll right (hold upper right on joystick)
        misty.MoveHead(roll=roll_right, velocity=roll_v, units=head_unit)

    else:
        misty.Stop()  # stop Misty's movement


def mode(data):  # Switches the mode being used depending on the button pressed
    split = data.split()  # data format: [x, y, mode]
    command = int(split[2])
    if command == 1:
        treads(data)
    elif command == 2:
        arms(data)
    elif command == 3:
        head(data)
    elif command == 4:
        print("stop misty communication")


def init():  # Resets Misty's head position and LED color. Disables the hazard ToFs
    misty.UpdateHazardSettings(disableTimeOfFlights=True)
    misty.MoveHead(0, 0, 0)
    misty.ChangeLED(255, 200, 0)


if __name__ == "__main__":
    init()
    # opens connection to the COM port for the Arduino to get serial data from it
    ser = serial.Serial(ARDUINO_PORT, 9600, timeout=1)
    time.sleep(1)  # stop for a second

    # set up the event listeners for the bumpers and ToF respectively
    misty.RegisterEvent(event_name="stop", event_type=Events.BumpSensor,
                        callback_function=_BumpSensor, keep_alive=True)
    misty.RegisterEvent(event_name="tof", event_type=Events.TimeOfFlight,
                        callback_function=_TOFProcessor, keep_alive=True, debounce=150)

    while True:  # ends when fourth button pressed
        line = ser.readline()  # get next line of the serial monitor (in bytes)
        if line:
            string = line.decode()  # convert the bytes to a string
            if " " in string:
                strip = string.strip()  # strip the string of newline/return characters
                mode(strip)
                # break out of infinite loop if specific button pressed
                if int(strip.split()[2]) == 4:
                    misty.UnregisterAllEvents()
                    misty.StopAudio()
                    break

    ser.close()  # close the serial connection
