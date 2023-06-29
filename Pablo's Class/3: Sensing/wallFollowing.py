'''
Skye Weaver Worster

Misty drives until bumped (stop and change light depending on bumper touched). She does not resume moving after contact.

WARNING: This code temporarily disables Misty's TOF sensor hazards, so she won't automatically stop at table edges and other drops. Be careful!
'''

from mistyPy.Robot import Robot
from mistyPy.Events import Events
import time

misty = Robot("131.229.41.135")  # robot with your IP
volume = 2  # volume for audio
lin_vel = 10  # linear velocity
ang_vel = 50  # angular velocity
d_time = 2000  # drive time for bump, in milliseconds
DE_debounce = 100  # drive encoders debounce
min_speed = .1  # the minimum speed at which Misty is still considered to be "driving"

# ! Do not change these!
contact = [False, False, False, False]  # which sensors are contacted
is_driving = False  # tracks whether Misty is driving
free = True # driving freely vs post-bump movement



def _DriveEncoders(data):
    global is_driving, contact, lin_vel, free

    try:
        
        # get velocity from data
        left_vel = abs(data["message"]["leftVelocity"])
        right_vel = abs(data["message"]["rightVelocity"])
        vel = left_vel+right_vel # total velocity
        
        # governs behavior when backing up
        if not free: # doing back-up movement
            if vel > min_speed: # if moving
                if not is_driving: # first time seeing movement
                    is_driving = True # misty has just started moving back
                else: # misty has already been moving
                    pass # do nothing
            else: # misty not moving
                if is_driving: # if misty has completed the drive
                    free = True # now moving freely again
                    misty.Drive(lin_vel, 0) # go forward
                else: # misty has not begun driving
                    pass # do nothing
        
        print(is_driving, free)
        '''
        # if sum(contact) == 0: # no longer touching anything
        #     if vel > min_speed: # if moving
        #         if not is_driving: # first time seeing movement
        #             is_driving = True
        #             misty.Drive(lin_vel, 0)

        # if stopped and touching something
        # do nothing
        # else:
        
            # if stopped and not touching
                # if first time (is_driving False)
                    # drive forward
                # if not first time (is_driving True)
                    # pass
            
            
            # if driving, is_driving=True 
                # pass
            
    
        
        # if left_vel+right_vel > min_speed:
        #     if is_driving: # if already driving
        #         print(".",end="")
        #     else:  # if started moving
        #         is_driving = True  # if moving, record that it's driving
        #         print("started driving")

        # if left_vel+right_vel < min_speed and is_driving:  # if stopped after having driven
        #     print("stopped driving")
        #     is_driving = False # record that we've stopped
        #     if sum(contact) == 0: # no longer touching anything
        #         misty.Drive(lin_vel, 0)  # drive forward slowly
        '''

    except Exception as e:
        print("DriveEncoders error:", e)


def _BumpSensor(data):
    global contact, free
    
    if data["message"]["isContacted"]:  # if Misty hits something
        #misty.Stop()  # stop moving (should happen automatically)
        free = False # no longer moving freely
        
        name = data["message"]["sensorId"]  # get name
        print(name)
        
        # record which bumper was hit
        if name == "bfr":  # front right
            misty.ChangeLED(255, 0, 0)  # red
            contact[0] = True
        if name == "bfl":  # front left
            misty.ChangeLED(0, 255, 0)  # green
            contact[1] = True
        if name == "brr":  # back right
            misty.ChangeLED(0, 0, 255)  # blue
            contact[2] = True
        if name == "brl":  # back left
            misty.ChangeLED(255, 160, 0)  # yellow
            contact[3] = True

        if sum(contact) > 1:  # multiple contacts, end program
            misty.Stop()
            misty.ChangeLED(0, 0, 0)  # LED off
            misty.PlayAudio("A_meow1.mp3", volume=volume)
            misty.UnregisterAllEvents()  # unregister and reset hazards
            misty.UpdateHazardSettings(revertToDefault=True)
        
        else:  # if only one contact
            if name == "bfr":  # front right
                misty.DriveTime(-lin_vel, ang_vel, d_time)  # go back right
            if name == "bfl":  # front left
                misty.DriveTime(-lin_vel, -ang_vel, d_time)  # go back left
            if name == "brr":  # back right
                misty.DriveTime(lin_vel, ang_vel, d_time)  # go front right
            if name == "brl":  # back left
                misty.DriveTime(lin_vel, -ang_vel, d_time)  # go front left

    elif data["message"]["isContacted"] == False:  # if sensor released
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
    misty.RegisterEvent("BumpSensor", Events.BumpSensor, condition=None,
                        keep_alive=True, callback_function=_BumpSensor)

    # subscribe to DriveEncoders
    misty.RegisterEvent("DriveEncoders", Events.DriveEncoders, keep_alive=True,
                        debounce=DE_debounce, callback_function=_DriveEncoders)

    misty.Drive(lin_vel, 0)  # drive forward slowly
