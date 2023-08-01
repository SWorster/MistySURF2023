'''
Skye Weaver Worster '25J

Takes driving parameters, moves Misty, and creates a graph of her tread movement. All globals can be edited to change Misty's behavior, graph properties, etc.

Be sure to replace the directory paths!
'''

# import statements
from mistyPy.Robot import Robot
from mistyPy.Events import Events
import os
import time
import matplotlib.pyplot as plt
import pandas
import numpy

# paths to directories. Replace with yours!
csv_directory = "/Users/skyeworster/Desktop/csv"
plot_directory = "/Users/skyeworster/Desktop/plots"

misty = Robot("131.229.41.135")  # Misty robot with your IP
mode = "d"  # d = Drive, a = DriveTrack, t = DriveTime
l = 100  # d,t= linear, a= left
r = 20  # d,t= angular, a= right
t = 3  # time
ui = False  # change to True to enable user interface
debounce = 10  # DriveEncoders debounce in milliseconds

# plot settings
width = 10  # plot width
height = 20  # plot height
dpi = 800  # dots per inch
show = False  # if True, shows graph immediately on completion


def _DriveEncoders(data):
    # Writes data from DriveEncoders message to file in csv format
    m = data["message"]  # get message (makes things easier to read)
    sec1 = m["created"]  # get time
    sec2 = float(sec1[17:-1])  # splice to get seconds only
    print(sec2, ",", m["leftVelocity"], ",", m["rightVelocity"],
          ",", m["leftDistance"], ",", m["rightDistance"], file=f)
    f.flush()  # pushes buffer to file


def getInput():
    # get user input to determine which drive command to use
    print("d = Drive, a = DriveTrack, t = DriveTime")
    print("If DriveTrack, params are left vel, right vel, time")
    print("Else, params are lin vel, ang vel, time")
    print("Example: d 100 60 5")
    response = input("Type mode").split()

    if len(response) != 4:  # use defaults
        print("Using default params: d 50 50 5")
        response = ["d", 50, 50, 5]

    mode = response[0]  # parse response
    l = int(response[1])
    r = int(response[2])
    t = int(response[3])
    if mode != "a" or "t":
        mode = "d"  # default to Drive if improper format

    return mode, l, r, t


if __name__ == "__main__":

    if ui:  # if user interface desired
        mode, l, r, t = getInput()  # set params from input

    os.chdir(csv_directory)  # change directory to csv folder

    now = time.strftime('%d%m%y_%H%M%S')  # name uses time, prevents overwrite
    name = f"{mode}_{l}_{r}_{t}_{now}.csv"
    f = open(name, "w")  # open file for writing

    # write headers to file
    print("timeMs,leftVelocity,rightVelocity,leftDistance,rightDistance", file=f)

    misty.UnregisterAllEvents()  # unregister preexisting events

    misty.UpdateHazardSettings(disableTimeOfFlights=True)  # ignore TOF sensors
    misty.ChangeLED(0, 0, 255)  # LED blue

    # register for DriveEncoders event to record data
    misty.RegisterEvent("DriveEncoders", Events.DriveEncoders,
                        debounce=debounce, keep_alive=True, callback_function=_DriveEncoders)

    # drive commands and title formatting
    if mode == "t":  # DriveTime
        misty.DriveTime(l, r, t*1000)
        time.sleep(t+.3)
        title = "DTime Lin {} Ang {} Time {}".format(l, r, t)
    elif mode == "a":  # DriveTrack
        misty.DriveTrack(l, r)
        time.sleep(t)
        misty.Stop()
        title = "DTrack Left {} Right {} Time {}".format(l, r, t)
    else:  # Drive
        misty.Drive(l, r)
        time.sleep(t)
        misty.Stop()
        title = "Drive Lin {} Ang {} Time {}".format(l, r, t)

    # unregister and reset Misty
    misty.ChangeLED(0, 255, 0)  # LED green
    misty.UnregisterAllEvents()  # unregister events
    misty.UpdateHazardSettings(revertToDefault=True)  # default hazards

    f.close()  # close csv file
    f2 = open(name, "r")  # reopen to read
    df = pandas.read_csv(f2)  # export to pandas DataFrame
    f2.close()  # close file

    # get DataFrames of each column
    sec = pandas.DataFrame(df, columns=["timeMs"])
    lv = pandas.DataFrame(df, columns=["leftVelocity"])
    rv = pandas.DataFrame(df, columns=["rightVelocity"])
    ld = pandas.DataFrame(df, columns=["leftDistance"])
    rd = pandas.DataFrame(df, columns=["rightDistance"])

    secs = sec.to_numpy()  # convert time to numpy array
    p1 = secs[0]  # scale to starting value
    secs -= p1
    # only seconds is considered, not minutes, so we have to account for the gap
    secs[secs < 0] += 60

    lds = ld.to_numpy()  # to numpy array
    l1 = lds[0]
    lds -= l1  # scale to first value

    rds = rd.to_numpy()
    r1 = rds[0]
    rds -= r1  # scale to first value

    plt.figure(figsize=(width, height))  # set figure size
    fig, ax = plt.subplots(2, 1, sharex=True)  # two plots sharing x axis
    vel = ax[0]  # first plot object
    dis = ax[1]  # second plot object

    # left/right vel in black, labelled
    vel.plot(secs, lv, color="black", label="left")
    vel.plot(secs, rv, color="red", label="right")
    vel.set_title(title)  # title for entire figure
    vel.set_ylabel('Velocity (mm/s)')  # y axis label
    vel.grid(True)  # grid
    vel.legend()  # legend displays labels

    # left/right dist, no label (share with first)
    dis.plot(secs, lds, color="black")
    dis.plot(secs, rds, color="red")
    dis.set_xlabel(f'Time in sec, over {t} sec')  # x axis for both plots
    dis.set_ylabel('Distance (mm) 0-scaled')  # y axis label
    dis.grid(True)  # grid

    os.chdir(plot_directory)  # navigate to directory
    plt.savefig(title, dpi=dpi)  # title and save with desired DPI

    if show:
        plt.show()  # pulls up graph in window. programs runs until that graph is closed
