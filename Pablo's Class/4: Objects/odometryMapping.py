'''
Skye Weaver Worster

Pablo's Instructions: Have the sequence of motions from the "Obj Interaction" Activity printed out and a graphical representation of the path visualized (forward 30cm; left 45 degrees; forward 55cm; right 15 degrees; etc). basically, run previous activity and record movement/position data, then display on top of provided map


Ignoring how this requires the previous program - I remember you don't want me to use mapping. The only other ways to record her movement are:
- DriveEncoders. Requires calculus (rate of movement, duration since last update).
- IMU. Unreliable measurements and intensive data-gathering. Doesn't record absolute position, so calculus required.
- logging exact movement instructions. Completely inaccurate, as intended and actual movement vary drastically.

This would be damn near impossible with any of these methods. Using mapping would at least make a solution plausible. A possible procedure would be:

- get map of known area
- find position in map
- move (either programmatic or from controller)
- at set interval, get current pose
- save pose to file with timestamp
- on movement completion, stop getting data
- load map of area
- for each timestamped entry, plot position

Alternatively, there is a built-in tracking functionality. It seems designed to work with some path-following and drive-to-location commands. Setting a path will return a list of waypoints Misty will hit. I'll need to confer with Julia to get more info about how this might work.
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
middle = None  # calculated yaw of middle of two objects
actual_middle = None # actual yaw at middle (wherever Misty ended up)
yaw = None  # current yaw from IMU
avg = 0  # center of current target object
bumped = False  # whether Misty has been bumped
first_dist = None # degrees of first turn (right)
second_dist = None # degrees of second turn (left)

'''
SECOND PHASE (MAPPING)
'''

def output():
    global start_yaw, yaw1, yaw2, middle, actual_middle, d_dist, d_time, first_dist, second_dist
    print(f"Initial heading: {start_yaw}")
    print(f"Max turn heading: {yaw2}")
    print(f"Total turn distance: {first_dist}")
    print(f"{obj1} heading: {yaw1}")
    print(f"{obj2} heading: {yaw2}")
    print(f"Calculated middle heading: {middle}")
    print(f"Actual middle heading: {actual_middle}")
    print(f"Second turn distance: {second_dist}")
    print(f"Driving distance: {d_dist}")
    
    print("\nInstructions:")
    print(f"Turn right {first_dist} degrees")
    print(f"Turn left {second_dist} degrees")
    print(f"Drive forward {d_dist} meters")



'''
FIRST PHASE (DRIVING)
'''

def _BumpSensor(data):
    # runs when program ends or Misty is bumped
    global bumped, yaw1, yaw2
    if not bumped:  # prevents running again on un-bump
        bumped = True  # stops while loops
        # yaw1 = 0  # set to 0, stops driveForward error
        # yaw2 = 0
        misty.Stop()  # stop moving
        misty.StopObjectDetector()  # stop detecting objects
        misty.UnregisterAllEvents()
        misty.ChangeLED(0, 0, 0)  # LED off
        misty.UpdateHazardSettings(revertToDefault=True)  # reset TOFs
        print("end of program")
        output()


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

    global middle, first_dist, second_dist, actual_middle
    
    # calculate total turn distance (degrees)
    if start_yaw < yaw2:  # start_yaw -- 0/360 -- yaw2
        first_dist = 360 - (yaw2-start_yaw)
    else:  # 0 -- start_yaw -- yaw2 -- 360
        first_dist = yaw2-start_yaw

    try:

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
        
        actual_middle = yaw # record actual yaw of turn

        # calculate total turn distance (degrees)
        if yaw > yaw2:
            second_dist = yaw-yaw2
        else:  # if straddling 0-360 gap, yaw2 > yaw
            second_dist = yaw2-yaw


        if not bumped:
            time.sleep(1)  # time to stop moving

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
