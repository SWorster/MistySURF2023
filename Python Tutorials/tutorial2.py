'''
Skye Weaver Worster
Misty Tutorial #2
'''

# import statements
from mistyPy.Robot import Robot
from mistyPy.Events import Events
from mistyPy.EventFilters import EventFilters

misty = Robot("131.229.41.135")  # Robot object with your IP
driving_time = 5  # the time Misty will drive for, in seconds
driving_speed = 10  # Misty's linear velocity
driving_angle = 0  # Misty's angular velocity
volume = 2  # volume of Misty's audio responses
is_driving = False  # whether Misty is currently moving
threshold = 0.2  # distance in meters that will make Misty stop
min_speed = 0.1  # the minimum speed at which Misty is still considered to be "driving"
TOF_debounce = 5  # Time of Flight event debounce, in milliseconds
DE_debounce = 500  # DriveEncoders event debounce, in milliseconds


def _TimeOfFlight(data):  # callback for time of flight
    global threshold, is_driving, volume   # global variables

    try:  # try-except block catches malformed/irrelevant responses
        distance = data["message"]["distanceInMeters"]  # distance variable
        status = data["message"]["status"]  # 0 if valid reading

        # if Misty is too close to an obstacle while driving
        if (distance < threshold and status == 0 and is_driving):

            # print to console
            print(f"Misty is {distance} meters from an obstacle")
            misty.ChangeLED(255, 0, 0)  # change LED to red
            misty.PlayAudio("s_Joy2.wav", volume=volume)  # play audio clip
            misty.Stop()  # stop moving
            is_driving = False  # record that Misty has stopped
            print("Stopped: Obstacle")  # print to console
            misty.UnregisterAllEvents()  # unregister from all events (ends program)
            # reset hazard detection
            misty.UpdateHazardSettings(revertToDefault=True)
    except Exception as e:
        print(e)  # ignore irrelevant data


def _DriveEncoders(data):  # callback for movement
    global min_speed, is_driving, volume  # global variables

    try:  # try-except block catches malformed/irrelevant responses

        left_vel = data["message"]["leftVelocity"]  # left vel from data
        right_vel = data["message"]["rightVelocity"]  # right vel from data

        if (left_vel+right_vel > min_speed):  # compare to speed threshold
            is_driving = True  # if moving, record that it's driving

        if (left_vel+right_vel < min_speed and is_driving):  # if stopped after having moved
            misty.ChangeLED(0, 255, 0)  # change LED to green
            misty.PlayAudio("s_Joy4.wav", volume=volume)  # play audio clip
            print("Stopped: time limit reached")  # print to console
            misty.UnregisterAllEvents()  # unregister from all events (ends program)
            # reset hazard detection
            misty.UpdateHazardSettings(revertToDefault=True)
    except Exception as e:
        print(e)


if __name__ == "__main__":

    print("Going on an adventure!")  # print message to console
    misty.ChangeLED(0, 0, 255)  # change Misty's LED to blue (RGB)
    misty.UnregisterAllEvents()  # unregister from all previous events
    misty.UpdateHazardSettings(disableTimeOfFlights=True)  # ignore TOF sensors

    # Subscribe to center TOF
    front_center = misty.RegisterEvent("CenterTimeOfFlight", Events.TimeOfFlight, condition=[
        EventFilters.TimeOfFlightPosition.FrontCenter], debounce=TOF_debounce, keep_alive=True, callback_function=_TimeOfFlight)

    # subscribe to DriveEncoders
    movement = misty.RegisterEvent(
        "DriveEncoders", Events.DriveEncoders, keep_alive=True, debounce=DE_debounce, callback_function=_DriveEncoders)

    # Misty drives straight forward at speed 10 for 5 seconds
    misty.DriveTime(linearVelocity=driving_speed,
                    angularVelocity=driving_angle, timeMs=driving_time*1000)
