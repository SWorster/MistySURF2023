'''
Skye Weaver Worster, with invaluable assistance from Julia Yu

This is where I'm testing out getting/displaying the map in pyplot, in preparation for odometryMapping.py. I've taken out the driving and object detection parts of the program. When I start on turtle graphics, I'll manually give it some data to work with. This will make testing much less stressful.
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

obj1 = "book"  # object to the left
obj2 = "bottle"  # object to the right

d_meter = 1  # thru driving distance, in meters
d_time = 10  # thru driving time, in seconds
ang_vel = 15  # searching turn angular velocity

imu_debounce = 10  # imu callback debounce, in ms
OD_debounce = 1000  # object detection debounce in ms
min_confidence = .2  # minimum confidence required to send report

# TODO find values for these
center = 160  # measurement of center in Misty's view (units unknown)
tol = 100  # tolerance for object detection (units unknown)


# ! Do not change these!
start_yaw = None  # initial yaw
yaw1 = None  # yaw of first object center
yaw2 = None  # yaw of second object center
middle = None  # calculated yaw of middle of two objects
actual_middle = None  # actual yaw at middle (wherever Misty ended up)

yaw = None  # current yaw from IMU
avg = 0  # center of current target object
bumped = False  # whether Misty has been bumped
first_dist = None  # degrees of first turn (right)
second_dist = None  # degrees of second turn (left)


# list of maps, with key and name values
map_list = misty.GetSlamMaps().json()["result"]
key = None
for m in map_list:
    if m["name"] == map_name:
        key = m["key"]
if key != None:
    misty.SetCurrentSlamMap(key)  # set current map
else:
    print("Map not found, using current map")

# get current map data
arr = np.array(misty.GetMap().json()["result"]["grid"])
size = arr.shape[0]
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
data.save(map_name, format="PNG")

img = plt.imread(map_name)
fig, ax = plt.subplots()
ax.imshow(img, extent=[0, size, 0, size], cmap='gray')


# metersPerCell is the area in m^2 covered by each cell.
# cell length is therefore sqrt(mPC).
# converting from cell to meters is c_d / scale
# converting from meters to cell is m_d * scale
scale = math.sqrt(misty.GetMap().json()["result"]["metersPerCell"])

start_yaw = 180  # initial yaw
yaw1 = 100  # yaw of first object center
yaw2 = 40  # yaw of second object center
actual_middle = (yaw1+yaw2)/2  # actual yaw at middle (wherever Misty ended up)
d_meter = 1  # thru driving distance, in meters


# TODO get starting position in terms of map orientation
# seems like position is values from 0-1 that scale how many pixels are in a meter. not something i can deal with yet
x1 = 100  # starting x
y1 = 100  # starting y

d_cell = scale * d_meter  # distance in cell, from meters

# ? Is map oriented with initial yaw = 0? for now i'm assuming that Misty's 0 yaw is along the x axis. I can adjust this later if needed.

# calculate and plot driving path
x2 = x1 + d_cell * math.cos(actual_middle)
y2 = y1 + d_cell * math.sin(actual_middle)
plt.plot([x1, x2], [y1, y2], 'ro-')

# calculate and plot first object angle
x2 = x1 + d_cell * math.cos(yaw1)
y2 = y1 + d_cell * math.sin(yaw1)
plt.plot([x1, x2], [y1, y2], 'yo-')

# calculate and plot second object angle
x2 = x1 + d_cell * math.cos(yaw2)
y2 = y1 + d_cell * math.sin(yaw2)
plt.plot([x1, x2], [y1, y2], 'bo-')

plt.legend("Movement", f"{obj1}", f"{obj2}")
plt.show()
