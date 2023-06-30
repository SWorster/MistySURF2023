# Imports
import serial
from mistyPy.Robot import Robot
from mistyPy.Events import Events

misty = Robot("<Replace w/ Misty's IP address>") # create a Misty instance using its IP address (which varies from robot to robot)

'The 4 constants below are thresholds for the joystick position to move in different directions'
NORTH = 341 # North and South are in Y
SOUTH = 682
LEFT = 341 # Left and Right are in X
RIGHT = 682

startMovement = False # this will prevent Misty from moving until she has a pose

def _SlamData(data):
    global startMovement
    status = data["message"]["slamStatus"]["statusList"]
    if "HasPose" in status: # make the LED green if she has a pose
        misty.ChangeLED(0, 255, 0)
        startMovement = True
    elif ("HasPose" not in status) or ("LostPose" in status): # make the LED red if she lost her pose or mapping isn't ready yet
        misty.ChangeLED(255, 0, 0)
        misty.PlayAudio("A_VineBoom.mp3", 5)

def treads(coords): # Controls the treads for overall mobility
    split = coords.split() # data format: [x, y, mode]
    x = int(split[0])
    y = int(split[1])
    if startMovement:
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
    elif command == 2:
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
    ser = serial.Serial('<Replace w/ COM port of the Arduino>', 9600, timeout = 1) # open connection to the COM port that the arduino is connected to to get serial data from it
    # create an event listener for Misty's slam status; callbeck is used whenever there is an update to the status
    misty.RegisterEvent(event_name = "stats", event_type = Events.SlamStatus, callback_function = _SlamData, keep_alive = True)
    misty.StartMapping() # starts the mapping process
    while True:
        line = ser.readline() # get next line of the serial monitor (its in bytes)
        if line:
            string = line.decode() # convert the bytes to a string
            if " " in string:
                strip = string.strip() # strip the string of a newline character and return character
                mode(strip)
                if int(strip.split()[2]) == 4: # break out of infinite while if specific button pressed
                    misty.UnregisterAllEvents()
                    break
    misty.StopMapping() # ends the mapping process; needed because it can cause errors if not ended gracefully
    ser.close() # close the serial connection
