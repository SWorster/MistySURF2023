from mistyPy.Robot import Robot

misty = Robot("131.229.41.135")

def print_all_maps():
    # print all maps from Misty's memory
    for map in misty.GetSlamMaps().json()["result"]:
        print(map)

def rename_map():
    new_name = input("Enter the new name of the map: ")
    print_all_maps()
    map_to_rename = input("Enter the key of the map you want to rename (hint: just copy paste): ")
    misty.RenameSlamMap(map_to_rename, new_name)

def set_current_map():
    # SetCurrentSlamMap works with only map key
    print_all_maps()
    map_to_set = input("Enter the key of the map you want to set as the current map (hint: copy paste exists): ")
    misty.SetCurrentSlamMap(map_to_set)

def delete_map():
    # delete a map from Misty's memory
    print_all_maps()
    map_to_destroy = input("Enter the key of the map you want to delete (hint: please just copy paste): ")
    misty.DeleteSlamMap(map_to_destroy)

def delete_all_maps():
    for map in misty.GetSlamMaps().json()["result"]:
        misty.DeleteSlamMap(map["key"])

def output_grid():
    file_name = input("Enter what you want to call the file that stores the map data (with .txt at the end): ")
    map_data = open(file_name, "w")
    liststr = map(str, misty.GetMap().json()["result"]["grid"])
    map_data.writelines(liststr)
    map_data.close()

def print_instructions():
    huh = """
    1: Print Misty's current maps
    2: Rename one of Misty's maps
    3: Set the current map Misty will use
    4: Delete a map
    5: Delete all maps
    6: Get the occupancy grid of the current map
    7: Print the options again
    8: Exit
    """
    print(huh)

if __name__ == "__main__":
    print("Welcome to the programized map controller.\nYou have the following options:")
    print_instructions()
    choice = "0"
    while choice != "8":
        choice = input("Pick from the above: ")
        match choice:
            case "1":
                print_all_maps()
            case "2":
                rename_map()
            case "3":
                set_current_map()
            case "4":
                delete_map()
            case "5":
                delete_all_maps()
            case "6":
                output_grid()
            case "7":
                print_instructions()
            case "8":
                print("Goodbye mapping nerd")
            case other:
                print("Invalid choice. Please try again.")