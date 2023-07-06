from mistyPy.Robot import Robot
import numpy as np
from PIL import Image as im
import cv2

misty = Robot("<Replace w/ Misty's IP address>")
x_path_coords = []
y_path_coords = []

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
    if event == cv2.EVENT_LBUTTONDOWN or event == cv2.EVENT_RBUTTONDOWN:
        print(280 - y, " ", 280 - x)
        x_path_coords.append(280 - y)
        y_path_coords.append(280 - x)
        font = cv2.FONT_HERSHEY_SIMPLEX
        cv2.putText(img, str(280 - y) + "," + str(280 - x), (x, y), font, .4, (255, 0, 0), 2)
        cv2.imshow("image", img)

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
    9: Print the options again
    10: Create a path with a given map
    11: Exit
    """
    print(huh)

if __name__ == "__main__":
    print("Welcome to the programized map controller.\nYou have the following options:")
    print_instructions()
    choice = "0"
    while choice != "10":
        choice = input("Pick from the above: ")
        match choice:
            case "1":
                print_all_maps()
            case "2":
                rename_map()
            case "3":
                set_current_map()
            case "4":
                print(misty.GetCurrentSlamMap().json()["result"])
            case "5":
                delete_map()
            case "6":
                delete_all_maps()
            case "7":
                output_grid()
            case "8":
                map_visual()
            case "9":
                print_instructions()
            case "10":
                x_path_coords.clear()
                y_path_coords.clear()
                map_to_path = input("Enter the name of the map you want to get the coords of (with the extension): ")
                try:
                    img = cv2.imread(map_to_path, 1)
                    cv2.imshow('image', img)
                except:
                    print("Exception occured, check the file name")
                else:
                    print("Use the cursor to indicate the places you want Misty to go.\nOnce done, press any key to exit.")
                    cv2.setMouseCallback('image', click_event)
                    cv2.waitKey(0)
                    cv2.destroyAllWindows()
                if len(x_path_coords) > 0:
                    print(x_path_coords)
                    print(y_path_coords)
            case "11":
                print("Goodbye mapping nerd")
            case other:
                print("Invalid choice. Please try again.")
        if choice != "10":
            print_instructions()
