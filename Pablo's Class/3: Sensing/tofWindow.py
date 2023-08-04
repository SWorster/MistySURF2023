'''
Skye Weaver Worster '25J

Misty drives forward until she is close to an obstacle. The distance is determined through a sliding window of time-of-flight measurements.

This is a modified version of Python Tutorial #2.

WARNING: this code disables Misty's TOF sensors, so she won't automatically stop at table edges and other drops. They are only re-enabled if the program is terminated via the bump sensors. Be careful!
'''


# import statements
from mistyPy.Robot import Robot
from mistyPy.Events import Events
from mistyPy.EventFilters import EventFilters

misty = Robot("131.229.41.135")  # Robot object with your IP

driving_time = 5  # the time Misty will drive for, in seconds
driving_speed = 10  # Misty's linear velocity
driving_angle = 0  # Misty's angular velocity

threshold = 0.3  # distance in meters that will make Misty stop
min_speed = 0.1  # the minimum speed at which Misty is still considered to be "driving"
invalid_measurement = 1.3  # replace invalid measurements with this value

TOF_debounce = 5  # Time of Flight event debounce, in milliseconds
DE_debounce = 500  # DriveEncoders event debounce, in milliseconds
window_size = 10  # how many measurements to store

tof_stop = "s_Joy2.wav"  # audio for TOF stop
time_stop = "s_Joy4.wav"  # audio for time stop
tof_v = 5  # tof_stop volume
time_v = 5  # time_stop volume

# ! DO NOT EDIT THESE
window = []  # empty list to store data over time
is_driving = False  # whether Misty is currently moving


def _TimeOfFlight(data):  # callback for time of flight
    global is_driving, window  # global variables

    try:  # try-except block catches malformed/irrelevant responses
        distance = data["message"]["distanceInMeters"]  # distance variable
        status = data["message"]["status"]  # 0 if valid reading

        if status != 0:  # if some error
            distance = invalid_measurement  # record long-range distance

        window.append(distance)  # append dist to window list
        if len(window) >= window_size:  # if list is full
            del window[0]  # delete first element

        avg = sum(window)/len(window)  # get and print average
        print(avg)

        # if Misty is too close to an obstacle while driving
        if avg < threshold and status == 0 and is_driving:
            misty.Stop()  # stop moving
            print(f"Misty is {avg} meters from an obstacle")
            misty.UnregisterAllEvents()  # unregister from all events (ends program)
            misty.ChangeLED(255, 0, 0)  # change LED to red
            misty.PlayAudio(tof_stop, tof_v)  # play audio clip
            print("Stopped: Obstacle")
            # reset hazard detection
            misty.UpdateHazardSettings(revertToDefault=True)

    except Exception as e:
        print(e)  # ignore irrelevant data


def _DriveEncoders(data):  # callback for movement
    global is_driving
    try:  # try-except block catches malformed/irrelevant responses
        left_vel = data["message"]["leftVelocity"]  # left vel from data
        right_vel = data["message"]["rightVelocity"]  # right vel from data

        if (left_vel+right_vel > min_speed):  # compare to speed threshold
            is_driving = True  # if moving, record that it's driving

        if (left_vel+right_vel < min_speed and is_driving):  # if stopped after having moved
            misty.UnregisterAllEvents()  # unregister from all events (ends program)
            misty.ChangeLED(0, 255, 0)  # change LED to green
            misty.PlayAudio(time_stop, time_v)  # play audio clip
            print("Stopped: time limit reached")  # print to console
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
    misty.RegisterEvent("CenterTimeOfFlight", Events.TimeOfFlight, condition=[
                        EventFilters.TimeOfFlightPosition.FrontCenter], debounce=TOF_debounce, keep_alive=True, callback_function=_TimeOfFlight)

    # subscribe to DriveEncoders
    misty.RegisterEvent("DriveEncoders", Events.DriveEncoders, keep_alive=True,
                        debounce=DE_debounce, callback_function=_DriveEncoders)

    # Misty drives forward
    misty.DriveTime(linearVelocity=driving_speed,
                    angularVelocity=driving_angle, timeMs=driving_time*1000)
