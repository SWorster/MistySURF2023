import serial
import time
from mistyPy.Robot import Robot

misty = Robot("<insert Misty IP>")

def treads(coords):
    split = coords.split()
    x = int(split[0])
    y = int(split[1])
    if y < 341 and x > 341 and x < 682:
        misty.Drive(linearVelocity = 10, angularVelocity = 0)
    elif y > 682 and x > 341 and x < 682:
        misty.Drive(linearVelocity = -10, angularVelocity = 0)
    elif x < 341 and y > 341 and y < 682:
        misty.Drive(linearVelocity = 0, angularVelocity = 10)
    elif x > 682 and y > 341 and y < 682:
        misty.Drive(linearVelocity = 0, angularVelocity = -10)
    elif x < 341 and y < 341:
        misty.Drive(linearVelocity = 10, angularVelocity = 10)
    elif x > 682 and y < 341:
        misty.Drive(linearVelocity = 10, angularVelocity = -10)
    elif x < 341 and y > 682:
        misty.Drive(linearVelocity = -10, angularVelocity = 10)
    elif x > 682 and y > 682:
        misty.Drive(linearVelocity = -10, angularVelocity = -10)
    else:
        misty.Halt()

def arms(data):
    split = data.split()
    x = int(split[0])
    y = int(split[1])
    if y < 341 and x > 341 and x < 682:
        misty.MoveArm(arm = "left", position = -29, velocity = 20, units = "degrees")
    elif y > 682 and x > 341 and x < 682:
        misty.MoveArm(arm = "left", position = 90, velocity = 20, units = "degrees")
    elif x < 341 and y > 341 and y < 682:
        misty.MoveArm(arm = "right", position = 90, velocity = 20, units = "degrees")
    elif x > 682 and y > 341 and y < 682:
        misty.MoveArm(arm = "right", position = -29, velocity = 20, units = "degrees")
    elif (x < 341 and y < 341) or (x > 682 and y < 341):
        misty.MoveArm(arm = "both", position = -29, velocity = 20, units = "degrees")
    elif (x < 341 and y > 682) or (x > 682 and y > 682):
        misty.MoveArm(arm = "both", position = 90, velocity = 20, units = "degrees")
    else:
        misty.Halt()

def head(data):
    split = data.split()
    x = int(split[0])
    y = int(split[1])
    if y < 341 and x > 341 and x < 682:
        misty.MoveHead(pitch = -40, velocity = 70, units = "degrees")
    elif y > 682 and x > 341 and x < 682:
        misty.MoveHead(pitch = 26, velocity = 70, units = "degrees")
    elif x < 341 and y > 341 and y < 682:
        misty.MoveHead(yaw = 81, velocity = 70, units = "degrees")
    elif x > 682 and y > 341 and y < 682:
        misty.MoveHead(yaw = -81, velocity = 70, units = "degrees")
    elif x < 341 and y < 341:
        misty.MoveHead(roll = -40, velocity = 70, units = "degrees")
    elif x > 682 and y < 341:
        misty.MoveHead(roll = 40, velocity = 70, units = "degrees")
    else:
        misty.Halt()

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


if __name__ == "__main__":
    ser = serial.Serial("<insert Arduino COM>", 9600, timeout = 1)
    time.sleep(1)
    while True:
        line = ser.readline()
        if line:
            string = line.decode()
            if " " in string:
                strip = string.strip()
                mode(strip)
                if int(strip.split()[2]) == 4:
                    break
    ser.close()