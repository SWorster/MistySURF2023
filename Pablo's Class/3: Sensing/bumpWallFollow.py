"""
Skye Weaver Worster '25J

Misty uses her bump sensors to follow a wall. She halts when more than one bumper is pressed.

WARNING: this code disables Misty's TOF sensors, so she won't automatically stop at table edges and other drops. They are only re-enabled if the program is terminated via the bump sensors. Be careful!
"""

from mistyPy.Robot import Robot
from mistyPy.Events import Events

misty = Robot("131.229.41.135")  # robot with your IP
clip = "meow1.mp3"  # clip to play on completion
volume = 10  # volume for audio
DE_debounce = 100  # drive encoders debounce

# driving parameters
lin_vel = 10  # linear velocity for driving forward
lin_turn = 5  # linear velocity for backing up turn. Don't set this too low!
ang_vel = 80  # angular velocity for backing up turn
d_time = 1500  # drive time for backing up turn, in milliseconds
min_speed = 1  # the minimum speed at which Misty is still considered to be "driving"

# ! Do not change these!
current = None  # which bumper we're using for turning in place
backup = False  # whether Misty is in backup mode
driving = False  # whether Misty is moving while in backup mode


def _DriveEncoders(data):
    global backup, driving

    try:
        if current != None:  # if touching something
            backup = True  # start backup mode

        if backup:  # if in backup mode (regardless of whether still in contact)
            left_vel = abs(data["message"]["leftVelocity"])
            right_vel = abs(data["message"]["rightVelocity"])
            vel = left_vel + right_vel  # total velocity

            if (
                vel > min_speed and not driving
            ):  # if moving and haven't flipped driving yet
                driving = True  # have started driving
            elif vel < min_speed and not driving:  # if haven't started driving yet
                pass  # wait for treads to start moving
            # if not moving anymore (DriveTime ended)
            elif vel < min_speed and driving:
                backup = False  # end backup mode
                driving = False  # no longer driving
                misty.Drive(lin_vel, 0)  # go forward

        print(" backup", backup, "driving", driving)

    except Exception as e:
        print("DriveEncoders error:", e)


def _BumpSensor(data):
    global current

    if data["message"]["isContacted"] == True:  # if Misty hits something
        misty.Stop()  # stop moving (should happen automatically)

        name = data["message"]["sensorId"]  # get name

        if current != None:  # if multiple bumpers hit, end program
            misty.Stop()  # stop moving
            misty.ChangeLED(0, 0, 0)  # LED off
            misty.PlayAudio(clip, volume)
            misty.UnregisterAllEvents()  # unregister and reset hazards
            misty.UpdateHazardSettings(revertToDefault=True)

        else:  # if only one bumper hit
            current = name  # set current

            # behavior for each bumper
            if name == "bfr":  # front right
                misty.ChangeLED(255, 0, 0)  # red
                misty.DriveTime(-lin_turn, ang_vel, d_time)  # go back right
            elif name == "bfl":  # front left
                misty.ChangeLED(0, 255, 0)  # green
                misty.DriveTime(-lin_turn, -ang_vel, d_time)  # go back left
            elif name == "brr":  # back right
                misty.ChangeLED(0, 0, 255)  # blue
                misty.DriveTime(lin_turn, ang_vel, d_time)  # go front right
            elif name == "brl":  # back left
                misty.ChangeLED(255, 160, 0)  # yellow
                misty.DriveTime(lin_turn, -ang_vel, d_time)  # go front left

    else:  # if sensor released
        misty.ChangeLED(0, 0, 0)  # LED off

        name = data["message"]["sensorId"]  # get name
        if name == current:
            current = None

    print("current", current)


# ignore TOF sensors
misty.UpdateHazardSettings(disableTimeOfFlights=True)

# register for bump sensor
misty.RegisterEvent("BumpSensor", Events.BumpSensor,
                    keep_alive=True, callback_function=_BumpSensor)

# subscribe to DriveEncoders
misty.RegisterEvent("DriveEncoders", Events.DriveEncoders, keep_alive=True,
                    debounce=DE_debounce, callback_function=_DriveEncoders)

misty.Drive(lin_vel, 0)  # drive forward slowly
