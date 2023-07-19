'''
Skye Weaver Worster

just testing graphing without movement
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
map_name = "polish dancing cow"  # name of map to plot on top of
img_name = "polish_dancing_cow.png"  # name to save image as
dpi = 800  # dpi to save image with

obj1 = "book"  # object to the left
obj2 = "laptop"  # object to the right

d_meter = 1  # thru driving distance, in meters
obj_scale = 1  # show objects as further than they actually are, for clarity

# ! Do not change anything below this comment!
# values to map later
yaw1 = 306  # yaw of first object center
yaw2 = 235  # yaw of second object center
calc_middle = 271  # calculated yaw of middle of two objects
start_x = 150  # starting x position from SLAM
start_y = 150  # starting y position from SLAM
final_x = 176  # ending x position from SLAM
final_y = 155  # ending y position from SLAM
start_yaw = 0

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

arr = np.array(misty.GetMap().json()["result"]["grid"])  # current map
# convert to 0-255 values for grey scale
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
arr = arr.astype(np.uint8)  # convert to unsigned 8bit integer
data = im.fromarray(arr)  # create image from array
data = data.rotate(90)  # rotate to match Misty Studio orientation

fig, ax = plt.subplots()  # create figure

try:
    data.save(img_name, format="PNG")
    img = plt.imread(img_name)  # open image in matplotlib
    ax.imshow(img, extent=[0, data.size[0], 0,
                           data.size[1]], cmap='gray')  # display image as plot background
except Exception as e:
    print(e)

# ax.invert_yaxis()  # moves origin to bottom right
ax.set_xlabel("x axis")
ax.set_ylabel("y axis")

# commented this out so that axes will resize to fit all points
# ax.set_xlim(data.size[0], 0)  # set axes to match graph
# ax.set_ylim(0, data.size[1])

# TODO: force graph to be square (if needed)

# metersPerCell is the area in m^2 covered by each cell. cell length is therefore sqrt(mPC). converting from cell to meters is c_d * scale, converting from meters to cell is m_d / scale
mpc = misty.GetMap().json()["result"]["metersPerCell"]
scale = math.sqrt(mpc)
print("mpc:", mpc, "scale:", scale)

# ! CHANGE THIS BACK TO d_cell = d_meter/scale, i think?????? ASK PABLO
d_cell = d_meter/mpc  # distance driven in cells, from meters

# ? Is map oriented with initial yaw = 0? i'm not changing anything until i know for sure

# calculate and plot start_yaw
x0 = start_x + d_cell * math.cos(start_yaw)
y0 = start_y + d_cell * math.sin(start_yaw)
plt.plot([start_x, x0], [start_y, y0], 'k.-', label="start yaw")

# calculate and plot driving path
end_x = start_x + d_cell * math.cos(calc_middle)
end_y = start_y + d_cell * math.sin(calc_middle)
plt.plot([start_x, end_x], [start_y, end_y], 'r.-', label="odometry")

# calculate and plot first object angle
x1 = start_x + d_cell * math.cos(yaw1) * obj_scale
y1 = start_y + d_cell * math.sin(yaw1) * obj_scale
plt.plot([start_x, x1], [start_y, y1],  'g.-', label=obj1)

# calculate and plot second object angle
x2 = start_x + d_cell * math.cos(yaw2) * obj_scale
y2 = start_y + d_cell * math.sin(yaw2) * obj_scale
plt.plot([start_x, x2], [start_y, y2],  'b.-', label=obj2)

# plot actual position
plt.plot([start_x, final_x], [start_y, final_y],
         'y.-', label="real end (SLAM)")

text_str = '\n'.join((
    (f"start SLAM: {start_x} {start_y}, yaw : {start_yaw}"),
    (f"end SLAM: {final_x} {final_y}"),
    (f"end odometry: {end_x} {end_y}"),
    (f"distance: {d_meter} meters = {d_cell} cells"),
    (f"{obj1}: yaw {yaw1}, dot position {x1} {y1}"),
    (f"{obj2}: yaw {yaw2}, dot position {x2} {y2}"),
    (f"middle yaw: {calc_middle}")))

print(text_str)

props = dict(boxstyle='round', facecolor='wheat', alpha=0.5)
ax.text(0.02, 0.02, text_str, transform=ax.transAxes, fontsize=5,
        verticalalignment='bottom', bbox=props)  # text box properties

plt.legend(loc="lower right", fontsize=5)

os.chdir("/Users/skyeworster/Desktop/pic")  # ! remove later
plt.savefig(time.strftime('%d%m%y_%H%M%S'), dpi=dpi)

# plt.show()  # show plot
print("program complete")
