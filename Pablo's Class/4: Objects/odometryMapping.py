'''
Skye Weaver Worster '25J, with invaluable assistance from Julia Yu '24

Misty performs the objInteraction.py program while tracking her location with SLAM. We record her initial and final positions, and compare this to what we expected based on her IMU measurements and the instructions we gave her. The results of both methods are graphed on the occupancy grid.

Note: when Misty drives forward, she goes towards the calculated middle. This might differ slightly from where she actually ends up after the left turn due to processing/communication lag. I decided to use DriveHeading to have Misty return to the calculated heading as she drives forward, instead of going straight forward from the inaccurate middle. We're cutting so many corners anyway that this isn't a huge deal, but I wanted to record it. It's easy to change, if desired.

I'm assuming that the l-r center of Misty's vision is 150, because the left seems to be about 0 and the right about 300. I've set the window for detection super high, so anything within 50-250 should register. This gives Misty plenty of time to see objects, as long as the turn speed isn't set too high.

This program applies a manual offset to the yaw values. This is because the yaw is zeroed upon startup and does not correspond to the occupancy grid. This has to be eyeballed, because there is (as of writing this) no way to get yaw relative to occupancy grid.
'''


from mistyPy.Robot import Robot
from mistyPy.Events import Events
import time
import matplotlib.pyplot as plt
import pandas as pd
from PIL import Image as im
import numpy as np
import math
import os

misty = Robot("131.229.41.135")  # robot with your IP
path = "/Users/skyeworster/Desktop/pic"  # where to save finished graph
show = False  # whether to display graph upon completion

map_name = "polish dancing cow"  # name of map to plot on top of
img_name = "polish_dancing_cow.png"  # name to save image as
dpi = 800  # dpi to save image with

offset = 190  # manual offset for yaw values
obj1 = "book"  # object to the left
obj2 = "laptop"  # object to the right

d_meter = 1  # thru driving distance, in meters
d_time = 10  # thru driving time, in seconds
ang_vel = 15  # searching turn angular velocity. low speed to prevent head shake

imu_debounce = 10  # imu callback debounce, in ms
OD_debounce = 1000  # object detection debounce in ms
min_confidence = .2  # minimum confidence required to send report

# ? Investigate these values further
center = 150  # measurement of center in Misty's view (units unknown)
tol = 100  # tolerance for object detection (units unknown)

# ! Do not change anything below this comment!
# values to map later
start_yaw = None  # initial yaw
yaw1 = None  # yaw of first object center
yaw2 = None  # yaw of second object center
calc_middle = None  # calculated yaw of middle of two objects
start_x = None  # starting x position
start_y = None  # starting y position
final_x = None  # ending x position
final_y = None  # ending y position

# values that don't get mapped
yaw = None  # current yaw from IMU
avg = 0  # center of current target object
bumped = False  # whether Misty has been bumped

# SLAM and tracking
current_x = None  # current x location from SelfState
current_y = None  # current y location from SelfState
is_tracking = False  # whether Misty is currently tracking
slam_reset = False  # whether Misty's SLAM has finished resetting


'''
PHASE 1: LOCALIZATION
'''


def _SelfState(data):
    # get current location in grid (current map)
    global current_x, current_y
    if data["message"]["occupancyGridCell"]["x"] == 0:
        print(".", end="", flush=True)  # show we're waiting on this
    else:
        pass
    current_x, current_y = data["message"]["occupancyGridCell"].values()


def _SlamStatus(data):
    # get whether Misty is currently tracking and SLAM is ready
    global is_tracking, slam_reset
    print(data["message"]["slamStatus"]["runMode"], end="      ")
    print(data["message"]["slamStatus"]["statusList"])

    if data["message"]["slamStatus"]["runMode"] == "Tracking":
        is_tracking = True
    else:
        is_tracking = False

    if "Ready" in data["message"]["slamStatus"]["statusList"]:
        slam_reset = True
    else:
        slam_reset = False


def localize():
    # get current location before running behavior
    global start_x, start_y, is_tracking

    try:
        # get clean slate
        misty.StopObjectDetector()  # stop detecting objects
        misty.StopTracking()  # stop tracking
        misty.UnregisterAllEvents()  # unregister from everything
        misty.EnableSlamService()  # start SLAM
        time.sleep(.5)  # give time to execute commands
        print(misty.SlamServiceEnabled().json())  # verify that SLAM is enabled

        # register for bump sensor
        misty.RegisterEvent("BumpSensor", Events.BumpSensor,
                            keep_alive=True, callback_function=_BumpSensor)

        # get the desired map from Misty, or use current map
        map_list = misty.GetSlamMaps().json()["result"]
        key = None
        for m in map_list:  # find corresponding key
            if m["name"] == map_name:
                key = m["key"]
        if key != None:  # if key found
            misty.SetCurrentSlamMap(key)  # set current map
            print("Using map", map_name)
        else:  # key not found, just use current
            print("Map not found, using current map")

        # register for SLAM status event to get tracking data
        misty.RegisterEvent("SlamStatus", Events.SlamStatus,
                            keep_alive=True, callback_function=_SlamStatus)

        misty.ResetSlam()  # reset SLAM

        print("\nResetting SLAM")
        misty.ChangeLED(255, 100, 0)  # LED orange

        while not slam_reset and not bumped:
            pass  # wait for SLAM to reset

        print("\nLocalizing")
        misty.ChangeLED(0, 255, 255)  # LED cyan
        misty.StartTracking()  # start tracking current location in map

        # register for self state events to get position
        misty.RegisterEvent("SelfState", Events.SelfState,
                            keep_alive=True, callback_function=_SelfState)

        while not is_tracking and not bumped:
            pass  # wait until location found or bumped

        if bumped:
            _BumpSensor(1)
        else:  # while loop ended from tracking, not bump
            misty.ChangeLED(255, 200, 0)  # LED yellow
            print("Waiting on non-0 location values")

            while current_x == 0 and not bumped:  # Misty doesn't know location
                pass  # wait until we get location data that isn't 0

            if bumped:
                _BumpSensor(1)
            else:
                start_x = current_x  # record starting coordinates
                start_y = current_y
                print("Location:", start_x, start_y)

                # unregister from events. tracking will stay on, we just won't get data.
                misty.UnregisterEvent("SlamStatus")
                misty.UnregisterEvent("SelfState")

                print("\nSearching")
                searching()

    except Exception as e:
        panic("localize", e)


'''
PHASE 2: DRIVING
'''


def _BumpSensor(data):  # runs when program ends or Misty is bumped
    global bumped, yaw1, yaw2
    if not bumped:  # prevents running again on un-bump
        misty.UnregisterAllEvents()  # unregister from everything
        print("Bumped!")
        bumped = True  # stops while loops
        misty.Stop()  # stop moving
        misty.StopObjectDetector()  # stop detecting objects
        misty.StopTracking()  # stop tracking
        misty.ChangeLED(0, 0, 0)  # LED off
        misty.UpdateHazardSettings(revertToDefault=True)  # reset TOFs
        print("end of program")


def _IMU(data):
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


def searching():
    global yaw1, yaw2, avg, start_yaw

    try:
        misty.UpdateHazardSettings(disableTimeOfFlights=True)  # ignore TOF
        misty.StartObjectDetector(min_confidence, 0, 5)  # start detection

        # register for object detection
        misty.RegisterEvent("ObjectDetection", Events.ObjectDetection,
                            debounce=OD_debounce, keep_alive=True, callback_function=_ObjectDetection)

        # register for IMU
        misty.RegisterEvent("IMU", Events.IMU, debounce=imu_debounce,
                            keep_alive=True, callback_function=_IMU)

        time.sleep(1)  # give time to register events

        misty.ChangeLED(0, 0, 255)  # LED blue
        start_yaw = yaw  # record initial yaw

        misty.Drive(0, -ang_vel)  # turn right

        while not (center-tol < avg < center+tol) and not bumped:
            pass  # stops if avg is in range, or bumped

        if bumped:  # if bumped
            _BumpSensor(1)
        else:  # if target seen
            misty.ChangeLED(255, 200, 0)  # LED yellow
            yaw1 = yaw  # record yaw1
            print(f"{obj1} seen at {yaw1}")
            avg = 0  # reset avg

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

    except Exception as e:
        panic("moveRight", e)


def driveForward():
    global calc_middle
    try:
        misty.StopObjectDetector()  # stop detection
        misty.UnregisterEvent("ObjectDetection")  # unregister detection

        calc_middle = (yaw1+yaw2)/2  # get average of yaws
        if yaw1 < yaw2:  # if straddling 0-360 line, flip across circle
            calc_middle = (180 - calc_middle) % 360

        misty.Drive(0, ang_vel)  # turn left

        if yaw > calc_middle:  # if 0-360 line between current and next heading
            while ((yaw < yaw2) or (yaw > calc_middle)) and not bumped:
                pass  # yaw is decreasing left, either to 0 or to middle
        else:  # 0 < yaw < calc_middle < 360
            while (yaw < calc_middle) and not bumped:
                pass  # turn until calc_middle reached, or bumped

        misty.Stop()  # stop moving
        misty.ChangeLED(0, 255, 0)  # LED green

        if bumped:  # Misty was bumped
            _BumpSensor(1)

        else:
            time.sleep(.5)  # time to stop moving

            misty.DriveHeading(calc_middle, d_meter, d_time*1000,
                               False)  # drive towards heading

            misty.ChangeLED(255, 255, 255)  # LED white
            time.sleep(d_time+.5)  # wait until drive done

            misty.Stop()  # just in case DriveHeading acts weird
            misty.StopObjectDetector()  # stop detecting objects
            misty.UpdateHazardSettings(revertToDefault=True)  # reset TOFs

            relocalize()  # go to relocalize function

    except Exception as e:
        panic("driveForward", e)


'''
PHASE 3: OUTPUT
'''


def relocalize():
    global is_tracking, current_x, current_y, final_x, final_y
    try:
        # reset variables
        is_tracking = False
        current_x = None
        current_y = None

        # register for self state events to get position
        misty.RegisterEvent("SelfState", Events.SelfState,
                            keep_alive=True, callback_function=_SelfState)

        time.sleep(1)  # give time for reset

        while (current_x == None or current_y == None) and not bumped:
            pass  # wait until location found

        if bumped:
            _BumpSensor(1)
        else:
            final_x = current_x  # record final coordinates
            final_y = current_y

            misty.UnregisterAllEvents()  # unregister events
            misty.StopTracking()  # stop tracking
            output()

    except Exception as e:
        panic("relocalize", e)


def output():
    try:
        arr = np.array(misty.GetMap().json()["result"]["grid"])  # current map
        # convert to 0-255 values for grey scale
        for row in range(arr.shape[0]):
            for col in range(arr.shape[1]):
                if arr[row][col] == 1:  # open = 1
                    arr[row][col] = 255  # white
                elif arr[row][col] == 2:  # occupied = 2
                    arr[row][col] = 0  # black
                elif arr[row][col] == 3:  # obscured = 3
                    arr[row][col] = 200  # dark grey
                else:  # unknown = 0
                    arr[row][col] = 100  # light grey
        arr = arr.astype(np.uint8)  # convert to unsigned 8bit integer
        data = im.fromarray(arr)  # create image from array
        data = data.rotate(90)  # rotate to match axes

        fig, ax = plt.subplots()  # create figure

        try:
            data.save(img_name, format="PNG")  # try saving image
            img = plt.imread(img_name)  # open image in matplotlib
            ax.imshow(img, extent=[0, data.size[0], 0,
                                   data.size[1]], cmap='gray')  # display image as plot background
        except Exception as e:
            print("Could not save, read, or show image:", e)

        ax.set_xlabel("x axis")
        ax.set_ylabel("y axis")
        ax.set_title("Graphing Test")

        mpc = misty.GetMap().json()["result"]["metersPerCell"]
        d_cell = d_meter/mpc  # distance driven in cells, from meters

        def rad(deg):  # converts to radians, with offset
            return (offset+deg)*math.pi/180

        # calculate and plot start_yaw
        x0 = start_x + d_cell * math.cos(rad(start_yaw))
        y0 = start_y + d_cell * math.sin(rad(start_yaw))
        plt.plot([start_x, x0], [start_y, y0], 'k.-', label="start yaw")

        # calculate and plot driving path
        end_x = start_x + d_cell * math.cos(rad(calc_middle))
        end_y = start_y + d_cell * math.sin(rad(calc_middle))
        plt.plot([start_x, end_x], [start_y, end_y],
                 'r.-', label="odometry end")

        # calculate and plot first object angle
        x1 = start_x + d_cell * math.cos(rad(yaw1))
        y1 = start_y + d_cell * math.sin(rad(yaw1))
        plt.plot([start_x, x1], [start_y, y1],  'b.-', label=obj1)

        # calculate and plot second object angle
        x2 = start_x + d_cell * math.cos(rad(yaw2))
        y2 = start_y + d_cell * math.sin(rad(yaw2))
        plt.plot([start_x, x2], [start_y, y2],  'g.-', label=obj2)

        # plot actual position
        plt.plot([start_x, final_x], [start_y, final_y],
                 'y.-', label="SLAM end")

        plt.legend(loc="lower right", fontsize=5)  # create legend

        # movement data in string
        text_str = '\n'.join(((f"start SLAM: {start_x} {start_y}, yaw : {int(start_yaw)}"),
                              (f"end SLAM: {final_x} {final_y}"),
                              (f"{obj1}: yaw {int(yaw1)}, dot position {int(x1)} {int(y1)}"),
                              (f"{obj2}: yaw {int(yaw2)}, dot position {int(x2)} {int(y2)}"),
                              (f"end yaw: {int(calc_middle)}, dot position {int(end_x)} {int(end_y)}"),
                              (f"distance: {d_meter} meters = {d_cell} cells")))
        print(text_str)  # print movement data to console

        # create text box on graph with movement data
        props = dict(boxstyle='round', facecolor='wheat', alpha=0.5)
        ax.text(0.02, 0.02, text_str, transform=ax.transAxes, fontsize=5,
                verticalalignment='bottom', bbox=props)

        plt.savefig(time.strftime('%d%m%y_%H%M%S'), dpi=dpi)   # save image

        if show:
            print("displaying plot in window")
            plt.show()  # shows plot
        print("program complete")

    except Exception as e:
        panic("output", e)


'''
PHASE 4: PANIC BUTTON
'''


def panic(location, e):
    # ends program not-so-gracefully when an error is detected
    print(f".ERROR IN {location}: {e}")

    misty.Stop()  # stop moving
    misty.StopObjectDetector()  # stop detecting objects
    misty.StopTracking()  # stop tracking
    misty.UnregisterAllEvents()  # unregister from everything
    misty.ChangeLED(0, 0, 0)  # LED off
    misty.UpdateHazardSettings(revertToDefault=True)  # reset TOFs
    plt.close()  # close plot
    print("end of program, hopefully")


'''
MAIN
'''

if __name__ == "__main__":
    # change directory (saves graph and background image in same place)
    os.chdir(path)
    localize()
