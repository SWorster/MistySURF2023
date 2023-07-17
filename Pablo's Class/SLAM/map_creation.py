# Imports
from datetime import datetime, timedelta
import serial
from mistyPy.Robot import Robot
from mistyPy.Events import Events

'Place the following information into the 2 constants below'
MISTY_IP = "<Misty's IP>"
ARDUINO_PORT = "Arduino COM"

'The 4 constants below are thresholds for the joystick position to move in different directions'
NORTH = 341 # North and South are in Y
SOUTH = 682
LEFT = 341 # Left and Right are in X
RIGHT = 682

'Globals for callback reference'
startMovement = False # this will prevent Misty from moving until she has a pose
startedMapping = False # keeps track of if Misty has started to map
lostStartTime = datetime.now() # gets the current time
hasPose = False # tracks if Misty has a pose and knows where she is

misty = Robot(MISTY_IP) # create a Misty instance using its IP address (which varies from robot to robot)

def _SlamData(data): # callback for whenever the slam statuses change
    global startMovement, startedMapping, lostStartTime, hasPose
    status = data["message"]["slamStatus"]["statusList"] # gets and stores the list of current statuses of the slam system
    print(data["message"]["created"], status)
    if "HasPose" in status: # make the LED green if she has a pose
        misty.ChangeLED(0, 255, 0)
        startMovement = True # let Misty start to move because she has a pose
        startedMapping = True # flags that Misty has started to map
        hasPose = True # flags that she has a pose
    elif ("HasPose" not in status) and (not startedMapping): # make the LED red if she lost her pose or mapping isn't ready yet
        misty.ChangeLED(255, 0, 0)
    elif startedMapping == True and "LostPose" in status: # if Misty started mapping (meaning she got a pose) and then she loses the pose
        lostStartTime = datetime.now() # records the current time that the robot lost pose
        hasPose = False
        misty.ChangeLED(255, 0, 0)
        misty.PlayAudio("VineBoom.mp3", 5)

def treads(coords): # Controls the treads for overall mobility
    split = coords.split() # data format: [x, y, mode]
    x = int(split[0])
    y = int(split[1])
    if startMovement: # only lets Misty move once she gets a pose
        if y < NORTH and x > LEFT and x < RIGHT: # move forward (hold up on joystick)
            misty.Drive(linearVelocity = 20, angularVelocity = 0)
        elif y > SOUTH and x > LEFT and x < RIGHT: # move backward (hold down on joystick)
            misty.Drive(linearVelocity = -20, angularVelocity = 0)
        elif x < LEFT and y > NORTH and y < SOUTH: # turn left (hold left on joystick)
            misty.Drive(linearVelocity = 0, angularVelocity = 20)
        elif x > RIGHT and y > NORTH and y < SOUTH: # turn right (hold right on joystick)
            misty.Drive(linearVelocity = 0, angularVelocity = -20)
        elif x < LEFT and y < NORTH: # forward + left (hold upper left on joystick)
            misty.Drive(linearVelocity = 20, angularVelocity = 20)
        elif x > RIGHT and y < NORTH: # forward + right (hold upper right on joystick)
            misty.Drive(linearVelocity = 20, angularVelocity = -20)
        elif x < LEFT and y > SOUTH: # backward + left (hold lower left on joystick)
            misty.Drive(linearVelocity = -20, angularVelocity = 20)
        elif x > RIGHT and y > SOUTH: # backward + right (hold lower right on joystick)
            misty.Drive(linearVelocity = -20, angularVelocity = -20)
        else:
            misty.Stop() # stop Misty from moving (default position on joystick)

def mode(data): # Switches the mode being used depending on the button pressed
    split = data.split() # data format: [x, y, mode]
    command = int(split[2])
    if command == 1:
        treads(data)
    elif command == 2: # passes over 2 and 3 (they'd do nothing if pressed)
        pass
    elif command == 3:
        pass
    elif command == 4:
        print("stop misty communication")

def init(): # Resets Misty's head position and LED color. Disables the hazard ToFs
    misty.UpdateHazardSettings(disableTimeOfFlights = True)
    misty.MoveHead(0, 0, 0)
    misty.ChangeLED(255, 200, 0)

if __name__ == "__main__":
    init()
    ser = serial.Serial(ARDUINO_PORT, 9600, timeout = 1) # open connection to the COM port that the arduino is connected to to get serial data from it
    misty.RegisterEvent(event_name = "stats", event_type = Events.SlamStatus, callback_function = _SlamData, keep_alive = True) # create an event listener for Misty's slam status
    misty.StartMapping() # starts the mapping process
    while True:
        line = ser.readline() # get next line of the serial monitor (its in bytes)
        if line:
            string = line.decode() # convert the bytes to a string
            if " " in string:
                strip = string.strip() # strip the string of a newline character and return character
                mode(strip)
                'if the button pressed is the exit button, or about 30 seconds have elapsed since Misty lost pose and has not reestablished, stop the program'
                if int(strip.split()[2]) == 4 or ((lostStartTime + timedelta(seconds = 30)).timestamp() <= datetime.now().timestamp() and startedMapping and not hasPose):
                    misty.UnregisterAllEvents()
                    misty.ChangeLED(0, 0, 0)
                    break
    misty.StopMapping() # ends the mapping process; needed because it can cause errors if not ended gracefully
    ser.close() # close the serial connection
