'''
Skye Weaver Worster '25J, with invaluable assistance from Julia Yu '24

Graphs user-provided values, without moving the robot. Useful for debugging or testing graph options.

Note: this program applies a manual offset to the yaw values. This is because the yaw is zeroed upon startup and does not correspond to the occupancy grid. This has to be eyeballed, because (as of writing this) there is no way to get yaw relative to occupancy grid.
'''

from mistyPy.Robot import Robot
import time
import matplotlib.pyplot as plt
from PIL import Image as im
import numpy as np
import math
import os

misty = Robot("131.229.41.135")  # robot with your IP
path = "/Users/skyeworster/Desktop/pics"  # where to save finished graph
save = True  # whether to save the graph
show = False  # whether to display graph upon completion

map_name = "polish dancing cow"  # name of map to plot on top of
img_name = "polish_dancing_cow.png"  # name to save image as
dpi = 800  # dpi to save image with
loc = "lower right"  # legend location
fontsize = 5  # legend font size

offset = 190  # manual offset for yaw values
obj1 = "book"  # object to the left
obj2 = "laptop"  # object to the right
d_meter = 1  # thru driving distance, in meters

# color values for space type
open = 255  # white open space
occupied = 0  # black occupied space
obscured = 200  # covered/obscured areas light gray
unknown = 100  # unknown areas dark gray

# values that get mapped
yaw1 = 281  # yaw of first object center
yaw2 = 231  # yaw of second object center
calc_middle = 256  # calculated yaw of middle of two objects
start_x = 172  # starting x position from SLAM
start_y = 135  # starting y position from SLAM
final_x = 174  # ending x position from SLAM
final_y = 157  # ending y position from SLAM
start_yaw = 352  # starting yaw

os.chdir(path)  # change directory (saves graph and background image in same place)

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
            arr[row][col] = open  # white
        elif arr[row][col] == 2:  # occupied = 2
            arr[row][col] = occupied  # black
        elif arr[row][col] == 3:  # obscured = 3
            arr[row][col] = obscured  # dark grey
        else:  # unknown = 0
            arr[row][col] = unknown  # light grey
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
plt.plot([start_x, end_x], [start_y, end_y], 'r.-', label="odometry end")

# calculate and plot first object angle
x1 = start_x + d_cell * math.cos(rad(yaw1))
y1 = start_y + d_cell * math.sin(rad(yaw1))
plt.plot([start_x, x1], [start_y, y1], 'b.-', label=obj1)

# calculate and plot second object angle
x2 = start_x + d_cell * math.cos(rad(yaw2))
y2 = start_y + d_cell * math.sin(rad(yaw2))
plt.plot([start_x, x2], [start_y, y2], 'g.-', label=obj2)

# plot actual position
plt.plot([start_x, final_x], [start_y, final_y], 'y.-', label="SLAM end")

plt.legend(loc=loc, fontsize=fontsize)  # create legend

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
ax.text(0.02, 0.02, text_str, transform=ax.transAxes,
        fontsize=5, verticalalignment='bottom', bbox=props)

if save:
    plt.savefig(time.strftime('%d%m%y_%H%M%S'), dpi=dpi)  # save image

if show:
    print("displaying plot in window")
    plt.show()  # shows plot

print("program complete")
