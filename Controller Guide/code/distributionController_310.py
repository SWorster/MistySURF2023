# Imports
import serial
import time
from mistyPy.Robot import Robot
from mistyPy.Events import Events

misty = Robot("<insert Misty IP>") # create a Misty instance using its IP address (which varies from robot to robot)

'Variables for use throughout the program'
moveForwardToF = True # ToF variables to track if Misty can move in the corresponding direction based on obstacles in her path
moveBackwardToF = True
contactFrontBumper = False # Bumper contact variables to track if Misty is in contact something and shouldn't move in that direction
contactBackBumper = False
bumperTouched = [False, False, False, False] # front left, front right, rear left, rear right

'The 4 constants below are thresholds for the joystick position to move in different directions'
NORTH = 341 # North and South are in Y
SOUTH = 682
LEFT = 341 # Left and Right are in X
RIGHT = 682

def _TOFProcessor(data): # Processes the ToF sensor's data, will prevent collisions
    global moveForwardToF, moveBackwardToF # these global variables will change if there is something detected in front of, or behind, Misty
    distance = data["message"]["distanceInMeters"] # float that contains the distance from detected objects in meters
    sensor = data["message"]["sensorId"] # string specifying the ToF that the data corresponds to
    valid = data["message"]["status"] # int specifying if the data taken is valid or not (0 means valid, anything else means a validity error)
    if distance < .25 and valid == 0:
        # if the distance is less than .25 meters and the measurement is valid
        match sensor:
            case "toffc": # if the data came from the front center ToF, moveForwardToF is changed to false to prevent forwards movement, and stops using Stop()
                moveForwardToF = False
                misty.Stop()
            case "tofr": # if the data came from the rear ToF, moveBackwardToF is changed to false to prevent backwards movement, and stops using Stop()
                moveBackwardToF = False
                misty.Stop()
    elif valid == 0 and distance > .25:
        # if the distance is over .25 meters and is a valid reading, change moveForwardToF or moveBackwardToF according to the sensor the data originated from
        match sensor:
            case "toffc":
                moveForwardToF = True
            case "tofr":
                moveBackwardToF = True

def _BumpSensor(data): # When bumped, robot LED changes color and stops
    try:
        global contactFrontBumper, contactBackBumper, bumperTouched # tracks which of the 4 bumpers have been pressed and modifies if it's in contact with something
        touched = data["message"]["isContacted"] # boolean. True if touched, False if released
        partTouched = data["message"]["sensorId"] # string sensor source
        if touched: # if a bumper was pressed, change the according value in the array to True, the color of the LED, and stop the robot from moving
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
        else: # when the bumper is released, change the corresponding array value to False
            match partTouched:
                case "bfr":
                    bumperTouched[1] = False
                case "bfl":
                    bumperTouched[0] = False
                case "brl":
                    bumperTouched[2] = False
                case "brr":
                    bumperTouched[3] = False
        # if either of the 2 bumpers in the front/back are true, then it's still in contact with something, preventing movement in the corresponding direction
        if bumperTouched[0] == False and bumperTouched[1] == False:
            contactFrontBumper = False
        else:
            contactFrontBumper = True
        if bumperTouched[2] == False and bumperTouched[3] == False:
            contactBackBumper = False
        else:
            contactBackBumper = True
    except Exception as e: # catch and print the error
        print("EXCEPTION:", e)

def treads(coords): # Controls the treads for overall mobility
    split = coords.split() # data format: [x, y, mode]
    x = int(split[0])
    y = int(split[1])
    if y < NORTH and x > LEFT and x < RIGHT and (not contactFrontBumper) and moveForwardToF: # move forward (hold up on joystick)
        misty.Drive(linearVelocity = 20, angularVelocity = 0)
    elif y > SOUTH and x > LEFT and x < RIGHT and (not contactBackBumper) and moveBackwardToF: # move backward (hold down on joystick)
        misty.Drive(linearVelocity = -20, angularVelocity = 0)
    elif x < LEFT and y > NORTH and y < SOUTH: # turn left (hold left on joystick)
        misty.Drive(linearVelocity = 0, angularVelocity = 50)
    elif x > RIGHT and y > NORTH and y < SOUTH: # turn right (hold right on joystick)
        misty.Drive(linearVelocity = 0, angularVelocity = -50)
    elif x < LEFT and y < NORTH and (not contactFrontBumper) and moveForwardToF: # forward + left (hold upper left on joystick)
        misty.Drive(linearVelocity = 20, angularVelocity = 20)
    elif x > RIGHT and y < NORTH and (not contactFrontBumper) and moveForwardToF: # forward + right (hold upper right on joystick)
        misty.Drive(linearVelocity = 20, angularVelocity = -20)
    elif x < LEFT and y > SOUTH and (not contactBackBumper) and moveBackwardToF: # backward + left (hold lower left on joystick)
        misty.Drive(linearVelocity = -20, angularVelocity = 20)
    elif x > RIGHT and y > SOUTH and (not contactBackBumper) and moveBackwardToF: # backward + right (hold lower right on joystick)
        misty.Drive(linearVelocity = -20, angularVelocity = -20)
    else:
        misty.Stop() # stop Misty from moving (default position on joystick)

def arms(data): # Controls the arm movement
    split = data.split() # data format: [x, y, mode]
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
        misty.Stop() # stop Misty's motion (default joystick position)
    
def head(data): # Controls the head movement
    split = data.split() # data format: [x, y, mode]
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
        misty.Stop() # stop Misty's movement

def mode(data): # Switches the mode being used depending on the button pressed
    split = data.split() # data format: [x, y, mode]
    command = int(split[2])
    if command == 1:
        treads(data)
    elif command == 2:
        arms(data)
    elif command == 3:
        head(data)
    elif command == 4:
        print("stop misty communication")

def init(): # Resets Misty's head position and LED color. Disables the hazard ToFs
    misty.UpdateHazardSettings(disableTimeOfFlights = True)
    misty.MoveHead(0, 0, 0)
    misty.ChangeLED(255, 200, 0)
    # misty.PlayAudio("A_Circus.mp3", 5)

if __name__ == "__main__":
    init()
    ser = serial.Serial('<insert Arduino COM>', 9600, timeout = 1) # open connection to the COM port that the arduino is connected to to get serial data from it
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
