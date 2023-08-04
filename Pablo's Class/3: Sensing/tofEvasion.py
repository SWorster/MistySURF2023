'''
Skye Weaver Worster '25J

Misty evades obstacles while driving forward.

Our robot's left TOF isn't sending data frequently. This means Misty refuses to see obstacles on the left, or she continually sees them even when they aren't there. There's no way to fix this, as far as I know.

Also, I'm not doing "sliding window" tactics due to sanity constraints. If you think this is necessary, I can sacrifice some of my will to live in exchange for emotional validation upon completion.

WARNING: this code disables Misty's TOF sensors, so she won't automatically stop at table edges and other drops. They are only re-enabled if the program is terminated via the bump sensors. Be careful!
'''

from mistyPy.Robot import Robot
from mistyPy.Events import Events
from mistyPy.EventFilters import EventFilters

misty = Robot("131.229.41.135")  # Robot object with your IP

vel = 10  # Misty's linear velocity when driving straight
ang = 40  # Misty's angular velocity in hard turns
turn_v = 10  # Misty's linear velocity when turning
turn_a = 60  # Misty's angular velocity when turning

min_d = 0.1  # distance in meters that will make Misty stop/reverse
obs_d = 0.3  # distance where Misty registers obstacle
TOF_debounce = 10  # Time of Flight event debounce, in milliseconds
num_readings = 10  # number of readings to take before calling move function

clip = "VineBoom.mp3"  # audio to play on completion
volume = 5  # volume of audio clip

# ! DO NOT EDIT THESE
sensors = [False, False, False]  # left, center, right TOF
back = False  # back TOF
count = 0  # counts number of readings taken


def _BumpSensor(data):  # terminates program
    misty.UnregisterAllEvents()  # unregister from all events (ends program)
    misty.Stop()  # stop moving
    misty.ChangeLED(0, 0, 0)  # LED off
    misty.PlayAudio(clip, volume)  # play audio clip
    print("Stopped: Bump Sensor")  # print to console
    misty.UpdateHazardSettings(revertToDefault=True)  # reset hazards


def _Back(data):  # rear TOF callback
    global back
    try:
        distance = data["message"]["distanceInMeters"]  # distance variable
        status = data["message"]["status"]  # 0 if valid reading
        if distance < min_d and status == 0:  # if obstacle too close
            back = True  # obstacle close
        move()  # call movement function
    except Exception as e:
        print("Back TOF Error:", e)


def _TOF(data):  # callback for time of flight
    global sensors
    try:
        distance = data["message"]["distanceInMeters"]  # distance variable
        status = data["message"]["status"]  # 0 if valid reading
        ID = data["message"]["sensorId"]

        if distance < min_d and status == 0:  # obstacle too close, can't move forward
            sensors = [True, True, True]  # as if all sensors detect obs

        else:  # no emergency
            match ID:
                case "toffr": x = 2  # right
                case "toffc": x = 1  # center
                case "toffl": x = 2  # left

            if distance < obs_d and status == 0:  # sees obstacle ahead
                sensors[x] = True  # record True

            elif distance > obs_d:  # doesn't see obstacle
                sensors[x] = False  # record False

        move()  # call movement function

    except Exception as e:
        print("TOF Error:", e)


def move():
    global count
    count += 1  # increment counter

    if count >= num_readings:  # if trigger reached, issue move command
        total = sum(sensors)  # how many sensors detect obstacle
        print(sensors, back, total)

        if total == 0:
            misty.Drive(vel, 0)  # drive forward
        elif total == 1:
            if sensors[0] or sensors[1]:  # left or center
                misty.Drive(turn_v, -turn_a)  # turn right
            else:  # right
                misty.Drive(turn_v, turn_a)  # turn left
        elif total == 2:
            if not sensors[0]:  # center and right
                if back:  # back obstacle
                    misty.Drive(0, ang)  # turn hard left
                else:  # back clear
                    misty.Drive(-turn_v, -turn_a)  # turn back right
            elif not sensors[1]:  # left and right
                if back:
                    misty.Drive(0, ang)  # turn hard left
                else:
                    misty.Drive(-turn_v, turn_a)  # turn back left
            elif not sensors[2]:  # left and center
                if back:
                    misty.Drive(0, -ang)  # turn hard right
                else:
                    misty.Drive(-turn_v, turn_a)  # turn back left
        elif total == 3:  # panic mode
            if back:
                misty.Drive(0, ang)  # turn hard left
            else:
                misty.Drive(-turn_v, -turn_a)  # turn back right

        count = 0  # reset count


if __name__ == "__main__":
    print("Going on an adventure!")  # print message to console
    misty.ChangeLED(0, 0, 255)  # change Misty's LED to blue (RGB)
    misty.UnregisterAllEvents()  # unregister from all previous events
    misty.UpdateHazardSettings(disableTimeOfFlights=True)  # ignore TOF sensors

    # Subscribe to TOF sensors
    misty.RegisterEvent("CenterTimeOfFlight", Events.TimeOfFlight, condition=[
                        EventFilters.TimeOfFlightPosition.FrontCenter], debounce=TOF_debounce, keep_alive=True, callback_function=_TOF)

    misty.RegisterEvent("RightTimeOfFlight", Events.TimeOfFlight, condition=[
                        EventFilters.TimeOfFlightPosition.FrontRight], debounce=TOF_debounce, keep_alive=True, callback_function=_TOF)

    misty.RegisterEvent("LeftTimeOfFlight", Events.TimeOfFlight, condition=[
                        EventFilters.TimeOfFlightPosition.FrontLeft], debounce=TOF_debounce, keep_alive=True, callback_function=_TOF)

    misty.RegisterEvent("BackTimeOfFlight", Events.TimeOfFlight, condition=[
                        EventFilters.TimeOfFlightPosition.Back], debounce=TOF_debounce, keep_alive=True, callback_function=_Back)

    # register for bump sensor
    misty.RegisterEvent("BumpSensor", Events.BumpSensor,
                        keep_alive=True, callback_function=_BumpSensor)

    ''' old version of movement behavior
        if back:  # if back obstacle
            if total == 0:  # no front obstacle
                misty.Drive(vel, 0)  # drive forward

            elif total == 1:  # one sensor detecting obstacle
                if sensors[0]:  # center
                    misty.Drive(0, ang)  # turn hard left
                elif sensors[1]:  # right
                    misty.Drive(turn_v, turn_a)  # turn left
                elif sensors[2]:  # left
                    misty.Drive(turn_v, -turn_a)  # turn right

            elif total == 2:  # two sensors detecting obstacle
                if not sensors[0]:  # left and right
                    misty.Drive(0, ang)  # turn hard left
                elif not sensors[1]:  # left and center
                    misty.Drive(0, -ang)  # hard turn right
                elif not sensors[2]:  # right and center
                    misty.Drive(0, ang)  # hard turn left

            # all sensors detecting obstacle (emergency override)
            elif total == 3:
                misty.Drive(0, ang)  # turn hard left

        else:  # no back obstacle
            if total == 0:  # no front obstacle
                misty.Drive(vel, 0)  # drive forward

            elif total == 1:  # one sensor detecting obstacle
                if sensors[0]:  # center
                    misty.Drive(-vel, 0)  # drive straight back
                elif sensors[1]:  # right
                    misty.Drive(turn_v, turn_a)  # turn left
                elif sensors[2]:  # left
                    misty.Drive(turn_v, -turn_a)  # turn right

            elif total == 2:
                if not sensors[0]:  # left and right
                    misty.Drive(-vel, 0)  # drive straight back
                elif not sensors[1]:  # left and center
                    misty.Drive(0, -ang)  # hard turn right
                elif not sensors[2]:  # right and center
                    misty.Drive(0, ang)  # hard turn left

            elif total == 3:
                misty.Drive(-vel, 0)  # drive straight back
                '''
