from mistyPy.Robot import Robot

misty = Robot("<Replace w/ Misty's IP address>")

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

def print_instructions(): # prints the option menu
    huh = """
    1: Print Misty's current maps
    2: Rename one of Misty's maps
    3: Set the current map Misty will use
    4: Get the current map Misty is using
    5: Delete a map
    6: Delete all maps
    7: Get the occupancy grid of the current map
    8: Print the options again
    9: Exit
    """
    print(huh)

if __name__ == "__main__":
    print("Welcome to the programized map controller.\nYou have the following options:")
    print_instructions()
    choice = "0"
    # if using Python 3.9, you will need to adjust the match case below to be an if-else chain
    # if using Python 3.10, you can run this program as is
    while choice != "9":
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
                print_instructions()
            case "9":
                print("Goodbye mapping nerd")
            case other:
                print("Invalid choice. Please try again.")
