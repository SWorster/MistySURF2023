'''
Skye Weaver Worster

WORK IN PROGRESS OBVIOUSLY

Pablo's Instructions: 1) turn in place until seeing object A; 2) keep turning until seeing object B), then return half the rotation (from A to B) and then advance until passing "through" the two objects. The idea is that, if we place two objects a couple feet apart, Misty should be able to pass "through" them.
'''


from mistyPy.Robot import Robot
from mistyPy.Events import Events
import time

misty = Robot("131.229.41.135")  # robot with your IP
volume = 3  # volume for audio

ang_vel = 10  # angular velocity for searching turn

imu_debounce = 10  # imu callback debounce, in ms

center = 160  # measurement of center in Misty's view (units unknown)
tol = 20  # tolerance for object detection (units unknown)
OD_debounce = 1000  # object detection debounce in ms
min_confidence = .2  # minimum confidence required to send report
obj1 = "bottle"  # object to the left
obj2 = "backpack"  # object to the right

d_dist = 2  # driving distance, in meters
d_time = 10  # time to drive forward, in seconds

# ! Do not change these!
yaw1 = None  # yaw of first object center
yaw2 = None  # yaw of second object center
yaw = None  # current yaw
avg = 0  # center of target object
bumped = False  # whether Misty has been bumped


def _BumpSensor(data):
    global yaw1, yaw2, bumped
    bumped = True  # stops while loops
    yaw1 = 0  # set to 0, stops driveForward error
    yaw2 = 0
    misty.Stop()  # stop moving
    misty.StopObjectDetector()  # stop detecting objects
    misty.UnregisterAllEvents()  # unregister all
    misty.ChangeLED(0, 0, 0)  # LED off
    misty.StopAudio()  # stop audio
    misty.UpdateHazardSettings(revertToDefault=True)  # reset TOFs
    print("end of program")


def _yaw(data):
    global yaw
    yaw = data["message"]["yaw"]  # get yaw


def _ObjectDetection(data):
    global obj1, obj2, avg

    object = data["message"]["description"]  # get object name
    print(object)  # print what Misty sees

    if yaw1 == None and object == obj1:  # haven't seen obj1 yet
        left = data["message"]["imageLocationLeft"]
        right = data["message"]["imageLocationRight"]
        avg = (right+left)/2

    elif yaw1 != None and object == obj2:
        left = data["message"]["imageLocationLeft"]
        right = data["message"]["imageLocationRight"]
        avg = (right+left)/2


def moveLeft():  # moves head to the left
    global ang_vel, center, tol, avg

    misty.Drive(0, ang_vel)  # turn left

    # stops if avg is in range, or bumped
    while not (center-tol < avg < center+tol) and not bumped:
        pass

    if not bumped:  # if target seen
        misty.Stop()  # stop moving
        yaw1 = yaw  # record and print yaw1
        print(yaw1)
        moveRight()  # call move right function
    else:  # Misty was bumped
        print("bumped")
        _BumpSensor(1)


def moveRight():  # moves head to the left
    global ang_vel, center, tol, avg

    misty.Drive(0, -ang_vel)  # turn left

    # stops if avg is in range, or bumped
    while not (center-tol < avg < center+tol) and not bumped:
        pass

    if not bumped:  # if target seen
        misty.Stop()
        yaw2 = yaw  # record and print yaw2
        print(yaw2)
        driveForward()  # call drive forward function
    else:  # Misty was bumped
        print("bumped")
        _BumpSensor(1)


def driveForward():
    try:
        global yaw1, yaw2, d_dist, d_time

        # stop OD and unregister unnecessary events
        misty.StopObjectDetector()
        misty.UnregisterEvent("ObjectDetection")
        misty.UnregisterEvent("IMU")

        # convert yaw values to range 0-360
        yaw1 = yaw1 % 360
        yaw2 = yaw2 % 360

        # if y1 and y2 in "normal" range
        if yaw2 > yaw1:
            middle = (yaw1+yaw2)/2

        # if y2 smaller than y1 (straddling 0-360 line)
        elif yaw1 > yaw2:
            # average anyway, then flip across circle, then convert to range 0-360
            middle = (180 - (yaw1+yaw2)/2) % 360

        else:
            middle = yaw1  # if something goes wrong, drive towards obj1

        misty.DriveHeading(middle, d_dist, d_time*1000)

        time.sleep(d_time)  # wait until drive done
        _BumpSensor(1)
    except Exception as e:
        print("driveForward Error:", e)


if __name__ == "__main__":

    # ignore TOF sensors
    misty.UpdateHazardSettings(disableTimeOfFlights=True)

    misty.StartObjectDetector(min_confidence, 0, 5)  # start detection

    # register for bump sensor
    misty.RegisterEvent("BumpSensor", Events.BumpSensor,
                        keep_alive=True, callback_function=_BumpSensor)

    # register for object detection
    misty.RegisterEvent("ObjectDetection", Events.ObjectDetection,
                        debounce=OD_debounce, keep_alive=True, callback_function=_ObjectDetection)

    # register for IMU
    misty.RegisterEvent("IMU", Events.IMU, debounce=imu_debounce,
                        keep_alive=True, callback_function=_yaw)

    moveLeft()  # go to moveLeft function
