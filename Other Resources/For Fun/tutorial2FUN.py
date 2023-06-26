'''
Skye Weaver Worster

This was done entirely for fun, so I'm not updating/documenting it at all. Use at your own risk.
'''

# import statements
from mistyPy.Robot import Robot
from mistyPy.Events import Events
from mistyPy.EventFilters import EventFilters

misty = Robot("131.229.41.135")  # Robot object with your IP
limit = .2  # how close Misty will get to an obstacle
volume = 10  # audio volume
TOF_debounce = 10  # TOF debounce (milliseconds)
drive_v = 10  # drive linear velocity
drive_a = 0  # drive angular velocity
drive_t = 5  # drive time (seconds)

# DO NOT CHANGE THESE
is_driving = False  # whether Misty is driving
drive_trigger = 1  # speed at which is_driving is True
stopped = 0.001  # speed at which is_driving is False


def tof_callback(data):  # callback for TOF
    global is_driving, limit
    try:
        distance = data["message"]["distanceInMeters"]
        if (distance < limit and is_driving):  # if driving into obstacle
            print("Misty is", distance, "meters from an obstacle")
            misty.ChangeLED(255, 0, 0)
            misty.PlayAudio("A_RickrollShort.mp3", volume)
            misty.Stop()  # stop driving
            is_driving = False  # no longer driving
            print("Stopped: Obstacle")
            misty.UnregisterAllEvents()  # unregister
    except:
        pass


def move_callback(data):  # callback for movement
    global is_driving
    try:
        # get l/r velocities
        l_vel = data["message"]["leftVelocity"]
        r_vel = data["message"]["rightVelocity"]

        if (l_vel+r_vel > 1):  # if driving fast enough
            is_driving = True  # driving

        if (l_vel+r_vel < stopped and is_driving):  # if stopped
            misty.ChangeLED(0, 255, 0)
            misty.PlayAudio("A_VineBoom.mp3", volume)
            print("Stopped: time limit reached")
            misty.UnregisterAllEvents()  # unregister
    except:
        pass


if __name__ == "__main__":
    print("Going on an adventure!")
    misty.ChangeLED(0, 0, 255)

    try:
        # Subscribe to center TOF
        misty.RegisterEvent("CenterTimeOfFlight", Events.TimeOfFlight, condition=[
                            EventFilters.TimeOfFlightPosition.FrontCenter], debounce=TOF_debounce, keep_alive=True, callback_function=tof_callback)

        # subscribe to locomotionCommand
        misty.RegisterEvent("DriveEncoders", Events.DriveEncoders,
                            keep_alive=True, callback_function=move_callback)

        misty.DriveTime(drive_v, drive_a, drive_t*1000)  # drive

    except Exception as ex:
        print(ex)
