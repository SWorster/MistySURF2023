'''
Skye Weaver Worster, with invaluable assistance from Julia Yu

plan for this program:
-set desired map
-get Misty to localize in map
-start tracking
-do object searching behavior (done)
-finish tracking and get new position)
-make plot
'''


from mistyPy.Robot import Robot
from mistyPy.Events import Events
import time
import matplotlib.pyplot as plt
import pandas as pd
from PIL import Image as im
import numpy as np
import math

misty = Robot("131.229.41.135")  # robot with your IP
map_name = "polish dancing cow"  # name of map to plot on top of
img_name = "polish_dancing_cow.png"  # name to save image as

obj1 = "book"  # object to the left
obj2 = "bottle"  # object to the right

d_meter = 1  # thru driving distance, in meters
d_time = 10  # thru driving time, in seconds
ang_vel = 15  # searching turn angular velocity

imu_debounce = 10  # imu callback debounce, in ms
OD_debounce = 1000  # object detection debounce in ms
min_confidence = .2  # minimum confidence required to send report

# TODO find values for these
center = 150  # measurement of center in Misty's view (units unknown)
tol = 100  # tolerance for object detection (units unknown)


# ! Do not change anything below this comment!
# values to map later
start_yaw = None  # initial yaw
yaw1 = None  # yaw of first object center
yaw2 = None  # yaw of second object center
middle = None  # actual yaw at middle (wherever Misty ended up)
start_x = None  # starting x position
start_y = None  # starting y position
final_x = None  # ending x position
final_y = None  # ending y position

# values that don't get mapped
yaw = None  # current yaw from IMU
avg = 0  # center of current target object
bumped = False  # whether Misty has been bumped
first_dist = None  # degrees of first turn (right)
second_dist = None  # degrees of second turn (left)
calc_middle = None  # calculated yaw of middle of two objects

# SLAM and tracking
current_x = None  # current x location from SelfState
current_y = None  # current y location from SelfState
is_tracking = False  # whether Misty is currently tracking
# ? haven't done anything with this. checking to see if everything else works first
slam_reset = False


'''
PHASE 1: LOCALIZATION
'''


def _SelfState(data):
    'get current location in grid (current map)'
    global current_x, current_y
    current_x, current_y = data["message"]["occupancyGridCell"].values()
    #print(data["message"])


def _SlamStatus(data):
    print(data["message"]["slamStatus"]["runMode"])
    print(data["message"]["slamStatus"]["statusList"])
    'get whether Misty is currently tracking'
    global is_tracking, slam_reset
    if data["message"]["slamStatus"]["runMode"] == "Tracking":
        is_tracking = True
        misty.ChangeLED(0, 255, 255)  # LED teal
    else:
        is_tracking = False
        misty.ChangeLED(255, 0, 0)  # LED red

    if "Ready" in data["message"]["slamStatus"]["statusList"]:
        slam_reset = True
    else:
        slam_reset = False


def localize():
    'get current location before running behavior'
    global start_x, start_y, is_tracking

    try:

        # get the desired map from Misty, or use current map
        # map list with keys/names
        map_list = misty.GetSlamMaps().json()["result"]
        key = None
        for m in map_list:
            if m["name"] == map_name:
                key = m["key"]
        if key != None:
            misty.SetCurrentSlamMap(key)  # set current map
            print("Using map", map_name)
        else:
            print("Map not found, using current map")
            
        

        # register for slam status event to get tracking data
        misty.RegisterEvent(event_name="SlamStatus", event_type=Events.SlamStatus,
                            keep_alive=True, callback_function=_SlamStatus)
        
        misty.ResetSlam()
        
        print("\nresetting slam")
        
        while not slam_reset and not bumped:
            pass
    
        misty.StartTracking()  # start tracking current location in map

        # register for self state events to get position
        misty.RegisterEvent(event_name="SelfState", event_type=Events.SelfState,
                            keep_alive=True, callback_function=_SelfState)

        # register for bump sensor
        misty.RegisterEvent("BumpSensor", Events.BumpSensor,
                            keep_alive=True, callback_function=_BumpSensor)
        
    
        print("\nlocalizing")

        while not is_tracking and not bumped:
            pass  # wait until location found

        if bumped:
            print("bumped")
            _BumpSensor(1)
        else:
            start_x = current_x  # record starting coordinates
            start_y = current_y
            print("location:", start_x, start_y)

            # unregister from events. tracking will stay on, we just won't get data.
            misty.UnregisterEvent("SlamStatus")
            misty.UnregisterEvent("SelfState")

            is_tracking = False  # reset tracking for later use

            print("\nsearching")
            searching()

    except Exception as e:
        panic("localize", e)


'''
PHASE 2: DRIVING
'''

# CALLBACKS


def _BumpSensor(data):
    # runs when program ends or Misty is bumped
    global bumped, yaw1, yaw2
    if not bumped:  # prevents running again on un-bump
        bumped = True  # stops while loops
        '''
        set to 0, stops driveForward error. no idea if this works.
        might also be able to stop it by putting driveForward in a "while not bumped" that ends by changing it to bumped. idk, just spit-balling.
        another error is that making these 0 completely messes with the graph output part. so I'll get back to this later.
        yaw1 = 0  
        yaw2 = 0
        '''
        misty.Stop()  # stop moving
        misty.StopObjectDetector()  # stop detecting objects
        misty.StopTracking()  # stop tracking
        misty.UnregisterAllEvents()  # unregister from everything
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


# BEHAVIOR

def searching():
    global yaw1, yaw2, avg, start_yaw

    try:

        # ignore TOF sensors
        misty.UpdateHazardSettings(disableTimeOfFlights=True)

        misty.StartObjectDetector(min_confidence, 0, 5)  # start detection

        # # register for bump sensor
        # misty.RegisterEvent("BumpSensor", Events.BumpSensor,
        #                     keep_alive=True, callback_function=_BumpSensor)

        # register for object detection
        misty.RegisterEvent("ObjectDetection", Events.ObjectDetection,
                            debounce=OD_debounce, keep_alive=True, callback_function=_ObjectDetection)

        # register for IMU
        misty.RegisterEvent("IMU", Events.IMU, debounce=imu_debounce,
                            keep_alive=True, callback_function=_yaw)

        time.sleep(1)  # give time to register events

        start_yaw = yaw  # record initial yaw
        misty.ChangeLED(0, 0, 255)  # LED blue

        misty.Drive(0, -ang_vel)  # turn right

        # stops if avg is in range, or bumped
        while not (center-tol < avg < center+tol) and not bumped:
            pass

        if bumped:  # if bumped
            print("Bumped!")
            _BumpSensor(1)

        else:  # if target seen
            misty.ChangeLED(255, 200, 0)  # LED yellow
            yaw1 = yaw  # record and print yaw1
            print(yaw1)
            avg = 0  # reset avg
            misty.ChangeLED(255, 200, 0)  # LED yellow

            # stops if avg is in range, or bumped
            while not (center-tol < avg < center+tol) and not bumped:
                pass

            if bumped:  # Misty was bumped
                print("Bumped!")
                _BumpSensor(1)

            else:  # if target seen
                misty.Stop()  # stop moving
                yaw2 = yaw  # record and print yaw2
                print(yaw2)
                misty.ChangeLED(255, 0, 255)  # LED purple
                driveForward()  # call drive forward function
    except Exception as e:
        panic("moveRight", e)


def driveForward():
    # use IMU to get close to right heading, then use driveHeading for precision

    global calc_middle, first_dist, second_dist, middle

    # calculate total turn distance (degrees)
    if start_yaw < yaw2:  # start_yaw -- 0/360 -- yaw2
        first_dist = 360 - (yaw2-start_yaw)
    else:  # 0 -- start_yaw -- yaw2 -- 360
        first_dist = yaw2-start_yaw

    try:
        # stop OD and unregister unnecessary events
        misty.StopObjectDetector()
        misty.UnregisterEvent("ObjectDetection")

        # if start_y and y2 in "normal" range
        # 360 > start_y > y2 > 0
        if yaw1 > yaw2:
            calc_middle = (yaw1+yaw2)/2

        #  start_y  -- 0/360 -- y2
        else:
            # average, then flip across circle, then convert to range 0-360
            calc_middle = (180 - (yaw1+yaw2)/2) % 360

        misty.Drive(0, ang_vel)  # turn left

        if yaw > calc_middle:  # if 0-360 gap between current and next heading
            # yaw is decreasing left, either to 0 or to middle
            while ((yaw < yaw2) or (yaw > calc_middle)) and not bumped:
                pass
        else:  # 0 < yaw < calc_middle < 360
            print("else")
            # turn until calc_middle reached, or bumped
            while (yaw < calc_middle) and not bumped:
                pass

        misty.Stop()  # stop moving

        middle = yaw  # record actual yaw of turn

        # calculate total turn distance (degrees)
        if yaw > yaw2:
            second_dist = yaw-yaw2
        else:  # if straddling 0-360 gap, yaw2 > yaw
            second_dist = yaw2-yaw

        if bumped:  # Misty was bumped
            print("Bumped!")
            _BumpSensor(1)

        else:
            time.sleep(.5)  # time to stop moving

            misty.DriveHeading(calc_middle, d_meter, d_time*1000,
                               False)  # drive towards heading
            misty.ChangeLED(0, 255, 0)  # LED green

            time.sleep(d_time+.5)  # wait until drive done

            misty.Stop()  # stop moving
            misty.StopObjectDetector()  # stop detecting objects
            misty.UnregisterAllEvents()  # unregister everything
            misty.UpdateHazardSettings(revertToDefault=True)  # reset TOFs

            relocalize()  # go to relocalize function

    except Exception as e:
        panic("driveForward", e)


'''
PHASE 3: OUTPUT
'''


def relocalize():
    global is_tracking, final_x, final_y
    try:
        # register for slam status event to get tracking data
        misty.RegisterEvent(event_name="SlamStatus", event_type=Events.SlamStatus,
                            keep_alive=True, callback_function=_SlamStatus)

        # register for self state events to get position
        misty.RegisterEvent(event_name="SelfState", event_type=Events.SelfState,
                            keep_alive=True, callback_function=_SelfState)

        while (current_x == None) or (current_y == None):
            pass  # wait until location found

        final_x = current_x  # record final coordinates
        final_y = current_y

        # unregister from events. tracking will stay on, we just won't get data.
        misty.UnregisterEvent("SlamStatus")
        misty.UnregisterEvent("SelfState")

        output()
    except Exception as e:
        panic("relocalize", e)


def output():
    try:
        # get current map data
        arr = np.array(misty.GetMap().json()["result"]["grid"])
        for row in range(arr.shape[0]):
            for col in range(arr.shape[1]):
                if arr[row][col] == 1:  # open = 1
                    arr[row][col] = 255
                elif arr[row][col] == 2:  # occupied = 2
                    arr[row][col] = 0
                elif arr[row][col] == 3:  # obscured = 3
                    arr[row][col] = 200
                else:  # unknown = 0
                    arr[row][col] = 100
        arr = arr.astype(np.uint8)
        data = im.fromarray(arr)
        # originally when created is upside down in comparison to studio's image, so need to rotate it
        data = data.rotate(180)
        data.save(img_name, format="PNG")

        img = plt.imread(img_name)
        fig, ax = plt.subplots()
        ax.imshow(img, extent=[0, data.size[0], 0, data.size[1]], cmap='gray')
        ax.set_xlim(0, data.size[0])
        ax.set_ylim(0, data.size[1])

        '''
        CALCULATING DRIVING PATH
        '''

        'metersPerCell is the area in m^2 covered by each cell. cell length is therefore sqrt(mPC). converting from cell to meters is c_d * scale, converting from meters to cell is m_d / scale'
        mpc = misty.GetMap().json()["result"]["metersPerCell"]
        print(mpc)
        scale = math.sqrt(mpc)
        print(scale)

        d_cell = d_meter/scale  # distance driven in cells, from meters

        # ? Is map oriented with initial yaw = 0? for now i'm assuming that Misty's 0 yaw is along the x axis. I can adjust this later if needed.

        # x = r cos theta, y = r sin theta

        # calculate and plot driving path
        x2 = start_x + d_cell * math.cos(middle)
        y2 = start_y + d_cell * math.sin(middle)
        plt.plot([start_x, x2], [start_y, y2], 'r.-', label="movement")

        # calculate and plot first object angle
        x2 = start_x + d_cell * math.cos(yaw1)
        y2 = start_y + d_cell * math.sin(yaw1)
        plt.plot([start_x, x2], [start_y, y2], 'g.-', label=obj1)

        # calculate and plot second object angle
        x2 = start_x + d_cell * math.cos(yaw2)
        y2 = start_y + d_cell * math.sin(yaw2)
        plt.plot([start_x, x2], [start_y, y2], 'b.-', label=obj2)

        # plot actual position
        plt.plot([start_x, final_x], [start_y, final_y], 'b.-', label=obj2)

        plt.legend(loc="lower left")

        plt.show()
    except Exception as e:
        panic("output", e)


'''
PHASE 4: PANIC BUTTON
'''

def panic(location, e):
    print(f"ERROR IN {location}: {e}")
    # ends program not-so-gracefully when an error is detected
    misty.Stop()  # stop moving
    misty.StopObjectDetector()  # stop detecting objects
    misty.StopTracking()  # stop tracking
    misty.UnregisterAllEvents()  # unregister from everything
    misty.ChangeLED(0, 0, 0)  # LED off
    misty.UpdateHazardSettings(revertToDefault=True)  # reset TOFs
    plt.close()  # close plot
    print("end of program, hopefully")


if __name__ == "__main__":
    localize()
