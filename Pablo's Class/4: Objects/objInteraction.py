'''
Skye Weaver Worster '25J

Misty turns right until she sees object 1, then object 2. She turns left until she's pointing between the objects, then moves forward.

Pablo's Instructions: 1) turn in place until seeing object A; 2) keep turning until seeing object B), then return half the rotation (from A to B) and then advance until passing "through" the two objects. The idea is that, if we place two objects a couple feet apart, Misty should be able to pass "through" them.
'''


from mistyPy.Robot import Robot
from mistyPy.Events import Events
import time

misty = Robot("131.229.41.135")  # robot with your IP
obj1 = "book"  # object to the left
obj2 = "bottle"  # object to the right

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


def _BumpSensor(data):
    # runs when program ends or Misty is bumped
    global bumped, yaw1, yaw2
    if not bumped:  # prevents running again on un-bump
        bumped = True  # stops while loops
        yaw1 = 0  # set to 0, stops driveForward error
        yaw2 = 0
        misty.Stop()  # stop moving
        misty.StopObjectDetector()  # stop detecting objects
        misty.UnregisterAllEvents()
        misty.ChangeLED(0, 0, 0)  # LED off
        misty.UpdateHazardSettings(revertToDefault=True)  # reset TOFs
        print("end of program")


def _yaw(data):
    global yaw
    yaw = data["message"]["yaw"] % 360  # get yaw, convert to range 0-360

    # * Note on yaw: Yaw is set to 0 upon Misty startup. IMU can send values from -360 to 360. So the orientation she faces at start could be 0, -360, or 360. The sensor is accurate plus or minus about 2 degrees, so an actual heading of 0 could be -2 to 2, -360 to -358, or 358 to 360. To simplify this, I've converted the yaw to the 0 to 360 degree range. This means an actual heading of 0 will only return 0-2 or 358-360.


def _ObjectDetection(data):
    global avg

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


def moveRight1():  # turns right until object seen
    global yaw1, avg

    misty.Drive(0, -ang_vel)  # turn right

    # stops if avg is in range, or bumped
    while not (center-tol < avg < center+tol) and not bumped:
        pass

    if not bumped:  # if target seen
        misty.ChangeLED(255, 200, 0)  # LED yellow
        print("          saw object 1")
        yaw1 = yaw  # record and print yaw1
        print(yaw1)
        avg = 0  # reset avg
        misty.ChangeLED(255, 200, 0)  # LED yellow
        moveRight2()  # call next function

    else:  # Misty was bumped
        print("Bumped!")
        _BumpSensor(1)


def moveRight2():  # keep turning right
    global yaw2

    # stops if avg is in range, or bumped
    while not (center-tol < avg < center+tol) and not bumped:
        pass

    if not bumped:  # if target seen
        print("           saw object 2")
        misty.Stop()  # stop moving
        yaw2 = yaw  # record and print yaw2
        print(yaw2)
        misty.ChangeLED(255, 0, 255)  # LED purple
        driveForward()  # call drive forward function

    else:  # Misty was bumped
        print("Bumped!")
        _BumpSensor(1)


def driveForward():
    # use IMU to get close to right heading, then use driveHeading for precision

    # calculate total turn distance (degrees)
    if start_yaw < yaw2:  # start_yaw -- 0/360 -- yaw2
        total = 360 - (yaw2-start_yaw)
    else:  # 0 -- start_yaw -- yaw2 -- 360
        total = yaw2-start_yaw

    print(f"Initial heading: {start_yaw}")
    print(f"Max turn heading: {yaw2}")
    print(f"Total turn distance: {total}")

    try:
        global middle

        # stop OD and unregister unnecessary events
        misty.StopObjectDetector()
        misty.UnregisterEvent("ObjectDetection")

        # if y1 and y2 in "normal" range
        # 360 > y1 > y2 > 0
        if yaw1 > yaw2:
            middle = (yaw1+yaw2)/2

        #  y1  -- 0/360 -- y2
        else:
            # average, then flip across circle, then convert to range 0-360
            middle = (180 - (yaw1+yaw2)/2) % 360

        print(f"{obj1} heading: {yaw1}")
        print(f"{obj2} heading: {yaw2}")
        print(f"Middle heading: {middle}")

        misty.Drive(0, ang_vel)  # turn left

        if yaw > middle:  # if 0-360 gap between current and next heading
            # yaw is decreasing left, either to 0 or to middle
            while ((yaw < yaw2) or (yaw > middle)) and not bumped:
                pass
        else:  # 0 < yaw < middle < 360
            print("else")
            while (yaw < middle) and not bumped:  # turn until middle reached, or bumped
                pass

        misty.Stop()  # stop moving

        # calculate total turn distance (degrees)
        if yaw > yaw2:
            total2 = yaw-yaw2
        else:  # if straddling 0-360 gap, yaw2 > yaw
            total2 = yaw2-yaw

        print(f"Current heading: {yaw}")
        print(f"Second turn distance: {total2}")

        if not bumped:
            time.sleep(1)  # time to stop moving

            print(f"Driving {d_dist} meters in {d_time*1000} seconds")

            # drive towards heading
            print(misty.DriveHeading(middle, d_dist, d_time*1000, False).json())
            misty.ChangeLED(0, 255, 0)  # LED green

            time.sleep(d_time+.5)  # wait until drive done
            _BumpSensor(1)

        else:  # Misty was bumped
            print("Bumped!")
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

    time.sleep(1)  # give time to register events

    print(yaw)
    start_yaw = yaw  # record initial yaw
    misty.ChangeLED(0, 0, 255)  # LED blue

    moveRight1()  # go to moveRight function
