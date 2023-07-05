'''
Skye Weaver Worster

WORK IN PROGRESS: still having some issues. Misty sometimes bumps into the wall and doesn't back up at all.

Misty drives until bumped (stop and change light depending on bumper touched). She does not resume moving after contact.

WARNING: This code temporarily disables Misty's TOF sensor hazards, so she won't automatically stop at table edges and other drops. Be careful!
'''

from mistyPy.Robot import Robot
from mistyPy.Events import Events
import time

misty = Robot("131.229.41.135")  # robot with your IP
volume = 2  # volume for audio
lin_vel = 10  # linear velocity
ang_vel = 80  # angular velocity
d_time = 1500  # drive time for bump, in milliseconds
DE_debounce = 100  # drive encoders debounce
min_speed = 1  # the minimum speed at which Misty is still considered to be "driving"

# ! Do not change these!
contact = [False, False, False, False]  # which sensors are contacted
back_up = False  # tracks whether Misty is backing up
free = True  # tracks whether Misty is driving forward


def _DriveEncoders(data):
    global back_up, contact, lin_vel, free

    try:

        # get velocity from data
        left_vel = abs(data["message"]["leftVelocity"])
        right_vel = abs(data["message"]["rightVelocity"])
        vel = left_vel+right_vel  # total velocity

        # governs behavior when backing up
        if not free:  # doing back-up movement
            if vel > min_speed:  # if moving
                if not back_up:  # first time seeing movement
                    print("back_up=true")
                    back_up = True  # misty has just started moving back
                else:  # misty has already been moving
                    pass  # do nothing
            else:  # misty not moving
                if back_up:  # if misty has completed the drive
                    print("free=true")
                    back_up = False  # no longer driving backwards
                    free = True  # now moving freely again
                    misty.Drive(lin_vel, 0)  # go forward
                else:  # misty has not begun driving
                    pass  # do nothing

        print(back_up, free)

    except Exception as e:
        print("DriveEncoders error:", e)


def _BumpSensor(data):
    global contact, free

    if data["message"]["isContacted"] == True:  # if Misty hits something
        # misty.Stop()  # stop moving (should happen automatically)
        free = False  # no longer moving freely

        name = data["message"]["sensorId"]  # get name
        print(name)

        # record which bumper was hit
        if name == "bfr":  # front right
            misty.ChangeLED(255, 0, 0)  # red
            contact[0] = True
        elif name == "bfl":  # front left
            misty.ChangeLED(0, 255, 0)  # green
            contact[1] = True
        elif name == "brr":  # back right
            misty.ChangeLED(0, 0, 255)  # blue
            contact[2] = True
        elif name == "brl":  # back left
            misty.ChangeLED(255, 160, 0)  # yellow
            contact[3] = True

        if sum(contact) > 1:  # multiple contacts, end program
            misty.Stop()
            misty.ChangeLED(0, 0, 0)  # LED off
            misty.PlayAudio("meow1.mp3", volume=volume)
            misty.UnregisterAllEvents()  # unregister and reset hazards
            misty.UpdateHazardSettings(revertToDefault=True)

        elif sum(contact) == 1:  # if only one contact
            if name == "bfr":  # front right
                misty.DriveTime(-lin_vel, ang_vel, d_time)  # go back right
            if name == "bfl":  # front left
                misty.DriveTime(-lin_vel, -ang_vel, d_time)  # go back left
            if name == "brr":  # back right
                misty.DriveTime(lin_vel, ang_vel, d_time)  # go front right
            if name == "brl":  # back left
                misty.DriveTime(lin_vel, -ang_vel, d_time)  # go front left

    else:  # if data["message"]["isContacted"] == False:  # if sensor released
        name = data["message"]["sensorId"]  # get name
        misty.ChangeLED(0, 0, 0)  # LED off
        if name == "bfr":  # front right
            contact[0] = False
        if name == "bfl":  # front left
            contact[1] = False
        if name == "brr":  # back right
            contact[2] = False
        if name == "brl":  # back left
            contact[3] = False

    print(contact)


if __name__ == "__main__":

    # ignore TOF sensors
    misty.UpdateHazardSettings(disableTimeOfFlights=True)

    # register for bump sensor
    misty.RegisterEvent("BumpSensor", Events.BumpSensor,
                        keep_alive=True, callback_function=_BumpSensor)

    # subscribe to DriveEncoders
    misty.RegisterEvent("DriveEncoders", Events.DriveEncoders, keep_alive=True,
                        debounce=DE_debounce, callback_function=_DriveEncoders)

    misty.Drive(lin_vel, 0)  # drive forward slowly
