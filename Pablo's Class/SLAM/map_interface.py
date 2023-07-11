from mistyPy.Robot import Robot
from mistyPy.Events import Events
import numpy as np
from PIL import Image as im
import cv2
import serial

misty = Robot("<Misty IP address goes here>")

'The 4 constants below are thresholds for the joystick position to move in different directions'
NORTH = 341 # North and South are in Y
SOUTH = 682
LEFT = 341 # Left and Right are in X
RIGHT = 682

x_path_coords = []
y_path_coords = []

tracking = False

def treads(coords): # Controls the treads for overall mobility
    split = coords.split() # data format: [x, y, mode]
    x = int(split[0])
    y = int(split[1])
    if y < NORTH and x > LEFT and x < RIGHT: # move forward (hold up on joystick)
        misty.Drive(linearVelocity = 20, angularVelocity = 0)
    elif y > SOUTH and x > LEFT and x < RIGHT: # move backward (hold down on joystick)
        misty.Drive(linearVelocity = -20, angularVelocity = 0)
    elif x < LEFT and y > NORTH and y < SOUTH: # turn left (hold left on joystick)
        misty.Drive(linearVelocity = 0, angularVelocity = 20)
    elif x > RIGHT and y > NORTH and y < SOUTH: # turn right (hold right on joystick)
        misty.Drive(linearVelocity = 0, angularVelocity = -20)
    elif x < LEFT and y < NORTH: # forward + left (hold upper left on joystick)
        misty.Drive(linearVelocity = 20, angularVelocity = 20)
    elif x > RIGHT and y < NORTH: # forward + right (hold upper right on joystick)
        misty.Drive(linearVelocity = 20, angularVelocity = -20)
    elif x < LEFT and y > SOUTH: # backward + left (hold lower left on joystick)
        misty.Drive(linearVelocity = -20, angularVelocity = 20)
    elif x > RIGHT and y > SOUTH: # backward + right (hold lower right on joystick)
        misty.Drive(linearVelocity = -20, angularVelocity = -20)
    else:
        misty.Stop() # stop Misty from moving (default position on joystick)

def _SlamStats(data):
    global tracking
    print(data["message"])
    if data["message"]["slamStatus"]["runMode"] == "Tracking":
        tracking = True
        misty.ChangeLED(0, 255, 255)
    else:
        tracking = False
        misty.ChangeLED(255, 0, 0)

def print_all_maps(): # print all maps from Misty's memory
    for map in misty.GetSlamMaps().json()["result"]:
        print(map)

def rename_map(): # rename a map in Misty's memory
    new_name = input("Enter the new name of the map: ")
    print_all_maps()
    map_to_rename = input("Enter the key of the map you want to rename (hint: just copy paste): ")
    misty.RenameSlamMap(map_to_rename, new_name)

def set_current_map(): # sets the current map for Misty's use
    print_all_maps()
    map_to_set = input("Enter the key of the map you want to set as the current map (hint: copy paste exists): ")
    misty.SetCurrentSlamMap(map_to_set) # SetCurrentSlamMap works with only map key

def delete_map(): # delete a map from Misty's memory
    print_all_maps()
    map_to_destroy = input("Enter the key of the map you want to delete (hint: please just copy paste): ")
    misty.DeleteSlamMap(map_to_destroy)

def delete_all_maps(): # delete all maps in Misty's memory
    for map in misty.GetSlamMaps().json()["result"]:
        misty.DeleteSlamMap(map["key"])

def output_grid(): # output the occupancy grid of the current map to a specified file
    file_name = input("Enter what you want to call the file that stores the map data (with .txt at the end): ")
    map_data = open(file_name, "w")
    liststr = map(str, misty.GetMap().json()["result"]["grid"])
    map_data.writelines(liststr)
    map_data.close()

def map_visual(): # creates an image of the current map in your working directory
    pic_name = input("Enter what you want the map to be called (include the file extension): ")
    arr = np.array(misty.GetMap().json()["result"]["grid"])
    for row in range(arr.shape[0]):
        for col in range(arr.shape[1]):
            if arr[row][col] == 1: # open = 1
                arr[row][col] = 255
            elif arr[row][col] == 2: # occupied = 2
                arr[row][col] = 0
            elif arr[row][col] == 3: # obscured = 3
                arr[row][col] = 200
            else: # unknown = 0
                arr[row][col] = 100
    arr = arr.astype(np.uint8)
    data = im.fromarray(arr)
    data = data.rotate(180) # originally when created is upside down in comparison to studio's image, so need to rotate it
    data.save(pic_name, format = "PNG")

def click_event(event, x, y, flags, params):
    global x_path_coords, y_path_coords
    height = img.shape[0]
    width = img.shape[1]
    if event == cv2.EVENT_LBUTTONDOWN or event == cv2.EVENT_RBUTTONDOWN:
        print(height - y, " ", width - x)
        x_path_coords.append(height - y) # note: the appended coords should in theory be correct since the maps tend to be squares
        y_path_coords.append(width - x) # so that means the height/width can possibly be interchangable?
        font = cv2.FONT_HERSHEY_SIMPLEX
        cv2.putText(img, str(height - y) + "," + str(width - x), (x, y), font, .4, (255, 0, 0), 2)
        cv2.imshow("image", img)

def follow_path():
    if len(x_path_coords) > 0:
        misty.RegisterEvent(event_name = "stats", event_type = Events.SlamStatus, callback_function = _SlamStats, keep_alive = True)
        misty.StartTracking()
        ser = serial.Serial('<Arduino COM here>', 9600, timeout = 1) # open connection to the COM port that the arduino is connected to to get serial data from it
        print("go")
    else:
        print("Please create a path first!")
        return
    
    # create the string with the coordinates in the format FollowPath wants
    path = ""
    for index_coord in range(len(x_path_coords)):
        path = path + str(x_path_coords[index_coord]) + ":" + str(y_path_coords[index_coord]) + ","
    path = path[:-1]

    while not tracking: # catch to hold it here while not localized
        line = ser.readline() # get next line of the serial monitor (its in bytes)
        if line:
            string = line.decode() # convert the bytes to a string
            if " " in string:
                strip = string.strip() # strip the string of a newline character and return character
                treads(strip)
                if int(strip.split()[2]) == 4: # break out of infinite while if specific button pressed
                    break
    ser.close() # close the serial connection

    # misty.FollowPath(path, .2)
    misty.StopTracking()
    misty.UnregisterAllEvents()
    
def print_instructions(): # prints the option menu
    huh = """
    1: Print Misty's current maps
    2: Rename one of Misty's maps
    3: Set the current map Misty will use
    4: Get the current map Misty is using
    5: Delete a map
    6: Delete all maps
    7: Get the occupancy grid of the current map
    8: Create an image of the current map
    9: Create a path with a given map
    10: Follow a given path
    11: Exit
    """
    print(huh)

def init():
    misty.UpdateHazardSettings(disableTimeOfFlights = True)
    misty.MoveHead(0, 0, 0)
    misty.ChangeLED(0, 0, 0)

if __name__ == "__main__":
    init()
    print("Welcome to the programized map controller.\nYou have the following options:")
    print_instructions()
    choice = "0"

    while choice != "11":
        choice = input("Pick from the above: ")
        match choice:
            case "1": # printing all maps
                print_all_maps()
            case "2": # rename a map
                rename_map()
            case "3": # set the current map
                set_current_map()
            case "4": # print the current map
                print(misty.GetCurrentSlamMap().json()["result"])
            case "5": # delete a map
                delete_map()
            case "6": # delete all maps
                delete_all_maps()
            case "7": # output the occupancy grid of the current map to a file
                output_grid()
            case "8": # create a picture of the current map
                map_visual()
            case "9": # using an indicated map file, create a path for misty to follow
                x_path_coords.clear()
                y_path_coords.clear()
                map_to_path = input("Enter the name of the map you want to get the coords of (with the extension): ")
                try:
                    img = cv2.imread(map_to_path, 1)
                    cv2.imshow('image', img)
                except:
                    print("Exception occured, check the file name and directory")
                else:
                    print("Use the cursor to indicate the places you want Misty to go.\nOnce done, press any key to exit.")
                    cv2.setMouseCallback('image', click_event)
                    cv2.waitKey(0)
                    cv2.destroyAllWindows()
                if len(x_path_coords) > 0:
                    print(x_path_coords)
                    print(y_path_coords)
            case "10": # follow the created map
                follow_path()
            case "11": # exit
                print("Goodbye mapping nerd")
            case other: # error
                print("Invalid choice. Please try again.")
        if choice != "11": # print the instructions after every run
            print_instructions()
