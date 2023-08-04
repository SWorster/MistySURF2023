'''
Skye Weaver Worster '25J

Misty turns right until she sees object 1, then object 2. She turns left until she's pointing between the objects, then moves forward through them.
'''

from mistyPy.Robot import Robot
from mistyPy.Events import Events
import time

misty = Robot("131.229.41.135")  # robot with your IP
obj1 = "chair"  # object to the left
obj2 = "person"  # object to the right

ang_vel = 15  # searching turn angular velocity
d_dist = 1  # thru driving distance, in meters
d_time = 10  # thru driving time, in seconds

imu_debounce = 10  # imu callback debounce, in ms

OD_debounce = 1000  # object detection debounce in ms
min_confidence = .2  # minimum confidence required to send report
center = 160  # measurement of center in Misty's view (units unknown)
tol = 100  # tolerance for object detection (units unknown)

# ! Do not change these!
start_yaw = None  # initial yaw
yaw1 = None  # yaw of first object center
yaw2 = None  # yaw of second object center
middle = None  # yaw of middle of two objects
yaw = None  # current yaw from IMU
avg = 0  # center of current target object
bumped = False  # whether Misty has been bumped


def _BumpSensor(data):  # runs when program ends or Misty is bumped
    global bumped, yaw1, yaw2
    if not bumped:  # prevents running again on un-bump
        misty.UnregisterAllEvents()
        bumped = True  # stops while loops
        misty.Stop()  # stop moving
        misty.StopObjectDetector()  # stop detecting objects
        misty.ChangeLED(0, 0, 0)  # LED off
        misty.UpdateHazardSettings(revertToDefault=True)  # reset TOFs
        print("end of program")


def _yaw(data):
    global yaw
    yaw = data["message"]["yaw"] % 360  # get yaw, convert to range 0-360


def _ObjectDetection(data):
    global avg
    object = data["message"]["description"]  # get object name
    print(object)  # print what Misty sees
    left = data["message"]["imageLocationLeft"]
    right = data["message"]["imageLocationRight"]

    if yaw1 == None and object == obj1:  # haven't seen obj1 yet
        avg = (right+left)/2
    elif yaw1 != None and object == obj2:  # saw obj1, looking for obj2
        avg = (right+left)/2


def moveRight():  # turns right until object seen
    global yaw1, avg
    misty.Drive(0, -ang_vel)  # turn right

    while not (center-tol < avg < center+tol) and not bumped:
        pass  # stops if avg is in range, or bumped

    if bumped:
        _BumpSensor(1)
    else:  # if target seen
        misty.ChangeLED(255, 200, 0)  # LED yellow
        yaw1 = yaw  # record and print yaw1
        print(f"{obj1} seen at {yaw1}")
        avg = 0  # reset avg
        misty.ChangeLED(255, 200, 0)  # LED yellow

        while not (center-tol < avg < center+tol) and not bumped:
            pass  # stops if avg is in range, or bumped

        if bumped:  # Misty was bumped
            _BumpSensor(1)
        else:  # if target seen
            misty.Stop()  # stop moving
            yaw2 = yaw  # record yaw2
            print(f"{obj2} seen at {yaw2}")
            misty.ChangeLED(255, 0, 255)  # LED purple
            driveForward()  # call drive forward function


def driveForward():
    misty.StopObjectDetector()  # stop detection
    misty.UnregisterEvent("ObjectDetection")  # unregister detection

    middle = (yaw1+yaw2)/2  # get average of yaws
    if yaw1 < yaw2:  # if straddling 0-360 line, flip across circle
        middle = (180 - middle) % 360

    print(f"{obj1} heading: {yaw1}")
    print(f"{obj2} heading: {yaw2}")
    print(f"Middle heading: {middle}")
    misty.Drive(0, ang_vel)  # turn left

    if yaw > middle:  # if 0-360 line between current and next heading
        while ((yaw < yaw2) or (yaw > middle)) and not bumped:
            pass  # yaw is decreasing left, either to 0 or to middle
    else:  # 0 < yaw < middle < 360
        while (yaw < middle) and not bumped:
            pass  # turn until middle reached, or bumped

    misty.Stop()  # stop moving
    misty.ChangeLED(0, 255, 0)  # LED green

    if bumped:  # Misty was bumped
        _BumpSensor(1)
    else:
        time.sleep(.5)  # time to stop moving

        misty.DriveHeading(middle, d_dist, d_time*1000,
                           False)  # drive towards heading

        misty.ChangeLED(255, 255, 255)  # LED white
        time.sleep(d_time+.5)  # wait until drive done

        misty.Stop()  # just in case DriveHeading acts weird
        misty.UpdateHazardSettings(revertToDefault=True)  # reset TOFs
        misty.UnregisterAllEvents()


if __name__ == "__main__":
    misty.UpdateHazardSettings(disableTimeOfFlights=True)  # ignore TOF
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

    time.sleep(1)  # give time to register events

    print(yaw)
    start_yaw = yaw  # record initial yaw
    misty.ChangeLED(0, 0, 255)  # LED blue

    moveRight()  # go to moveRight function
