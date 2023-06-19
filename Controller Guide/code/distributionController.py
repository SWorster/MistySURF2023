import serial
import time
from mistyPy.Robot import Robot
from mistyPy.Events import Events

misty = Robot("<insert Misty IP>")

def _TOFProcessor(data):
    global canMoveForward, canMoveBackward
    distance = data["message"]["distanceInMeters"]
    sensor = data["message"]["sensorId"]
    valid = data["message"]["status"]
    if distance < .25 and valid == 0:
        if sensor == "toffc":
            canMoveForward = False
            misty.Stop()
        elif sensor == "tofr":
            canMoveBackward = False
            misty.Stop()
    elif valid == 0 and distance > .25:
        if sensor == "toffc":
            canMoveForward = True
        elif sensor == "tofr":
            canMoveBackward = True

def _BumpSensor(data):
    try:
        global lastPlace, contactFront, contactBack
        touched = data["message"]["isContacted"]
        partTouched = data["message"]["sensorId"]
        
        if partTouched != lastPlace:
            lastPlace = ""

        if lastPlace == "":
            lastPlace = partTouched
            if partTouched == "bfr" and touched:
                misty.ChangeLED(255, 0, 0)
                contactFront = True
                misty.Stop()
            elif partTouched == "bfl" and touched:
                misty.ChangeLED(0, 255, 0)
                contactFront = True
                misty.Stop()
            elif partTouched == "brl" and touched:
                misty.ChangeLED(0, 0, 255)
                contactBack = True
                misty.Stop()
            elif partTouched == "brr" and touched:
                misty.ChangeLED(69, 69, 69)
                contactBack = True
                misty.Stop()
        else:
            if lastPlace == "bfr":
                if touched == False and partTouched == "bfr":
                    lastPlace = ""
                    contactFront = False
            if lastPlace == "bfl":
                if touched == False and partTouched == "bfl":
                    lastPlace = ""
                    contactFront = False
            if lastPlace == "brl":
                if touched == False and partTouched == "brl":
                    lastPlace = ""
                    contactBack = False
            if lastPlace == "brr":
                if touched == False and partTouched == "brr":
                    lastPlace = ""
                    contactBack = False
    except Exception as e:
        print("EXCEPTION:", e)

def treads(coords):
    global canMoveForward, canMoveBackward, contactFront, contactBack
    split = coords.split()
    x = int(split[0])
    y = int(split[1])
    if y < 341 and x > 341 and x < 682 and not contactFront and canMoveForward:
        misty.Drive(linearVelocity = 20, angularVelocity = 0)
    elif y > 682 and x > 341 and x < 682 and not contactBack and canMoveBackward:
        misty.Drive(linearVelocity = -20, angularVelocity = 0)
    elif x < 341 and y > 341 and y < 682:
        misty.Drive(linearVelocity = 0, angularVelocity = 50)
    elif x > 682 and y > 341 and y < 682:
        misty.Drive(linearVelocity = 0, angularVelocity = -50)
    elif x < 341 and y < 341 and not contactFront and canMoveForward:
        misty.Drive(linearVelocity = 20, angularVelocity = 20)
    elif x > 682 and y < 341 and not contactFront and canMoveForward:
        misty.Drive(linearVelocity = 20, angularVelocity = -20)
    elif x < 341 and y > 682 and not contactBack and canMoveBackward:
        misty.Drive(linearVelocity = -20, angularVelocity = 20)
    elif x > 682 and y > 682 and not contactBack and canMoveBackward:
        misty.Drive(linearVelocity = -20, angularVelocity = -20)
    else:
        misty.Stop()

def arms(data):
    split = data.split()
    x = int(split[0])
    y = int(split[1])
    if y < 341 and x > 341 and x < 682:
        misty.MoveArm(arm = "left", position = -29, velocity = 50, units = "degrees")
    elif y > 682 and x > 341 and x < 682:
        misty.MoveArm(arm = "left", position = 90, velocity = 50, units = "degrees")
    elif x < 341 and y > 341 and y < 682:
        misty.MoveArm(arm = "right", position = 90, velocity = 50, units = "degrees")
    elif x > 682 and y > 341 and y < 682:
        misty.MoveArm(arm = "right", position = -29, velocity = 50, units = "degrees")
    elif (x < 341 and y < 341) or (x > 682 and y < 341):
        misty.MoveArm(arm = "both", position = -29, velocity = 50, units = "degrees")
    elif (x < 341 and y > 682) or (x > 682 and y > 682):
        misty.MoveArm(arm = "both", position = 90, velocity = 50, units = "degrees")
    else:
        misty.Stop()

def head(data):
    split = data.split()
    x = int(split[0])
    y = int(split[1])
    if y < 341 and x > 341 and x < 682:
        misty.MoveHead(pitch = -40, velocity = 100, units = "degrees")
    elif y > 682 and x > 341 and x < 682:
        misty.MoveHead(pitch = 26, velocity = 100, units = "degrees")
    elif x < 341 and y > 341 and y < 682:
        misty.MoveHead(yaw = 81, velocity = 85, units = "degrees")
    elif x > 682 and y > 341 and y < 682:
        misty.MoveHead(yaw = -81, velocity = 85, units = "degrees")
    elif x < 341 and y < 341:
        misty.MoveHead(roll = -40, velocity = 100, units = "degrees")
    elif x > 682 and y < 341:
        misty.MoveHead(roll = 40, velocity = 100, units = "degrees")
    else:
        misty.Stop()

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

def init():
    misty.UpdateHazardSettings(disableTimeOfFlights = True)
    misty.MoveHead(0, 0, 0)

if __name__ == "__main__":
    global lastPlace, canMoveForward, canMoveBackward, contactFront, contactBack
    lastPlace = ""
    canMoveForward = True
    canMoveBackward = True
    contactFront = False
    contactBack = False

    init()
    ser = serial.Serial("<insert Arduino COM>", 9600, timeout = 1)
    time.sleep(1)

    misty.RegisterEvent(event_name = "stop", event_type = Events.BumpSensor, callback_function = _BumpSensor, keep_alive = True)
    misty.RegisterEvent(event_name = "tof", event_type = Events.TimeOfFlight, callback_function = _TOFProcessor, keep_alive = True, debounce = 100)
    misty.ChangeLED(255, 200, 0)

    while True:
        line = ser.readline()
        if line:
            string = line.decode()
            if " " in string:
                strip = string.strip()
                mode(strip)
                if int(strip.split()[2]) == 4:
                    misty.UnregisterAllEvents()
                    misty.StopAudio()
                    break
    ser.close()
