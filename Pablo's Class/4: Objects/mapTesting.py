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

misty = Robot("131.229.41.135")  # robot with your IP
map_name = "pain.png"  # name of map to plot on top of


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
actual_middle = None  # actual yaw at middle (wherever Misty ended up)
yaw = None  # current yaw from IMU
avg = 0  # center of current target object
bumped = False  # whether Misty has been bumped
first_dist = None  # degrees of first turn (right)
second_dist = None  # degrees of second turn (left)


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

# ! figure out how to get image from Julia

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

plt.show()


