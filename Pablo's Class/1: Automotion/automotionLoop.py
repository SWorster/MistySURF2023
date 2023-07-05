'''
Skye Weaver Worster

Misty looks around, trying to find the target's face. Her search loops forever until she sees the target. If she finds it, she starts following the target with her head. Target has to be known, and their name must be provided. To end program, hit bump sensor.

I struggled with the head-following behavior (see comment block below). Might come back to this later.
'''

# import statements
from mistyPy.Robot import Robot
from mistyPy.Events import Events
from mistyPy.EventFilters import EventFilters
import time

# parameters you can/should change
misty = Robot("131.229.41.135")  # Misty robot with your IP
person = "test"  # person to look for
FR_debounce = 500  # facial recognition debounce
AP_debounce = 100  # actuator position debounce
volume = 2  # volume for audio clips
start_pitch = -20  # starting pitch for head (recommend looking up)


# parameters for Misty's searching movement. The thresholds are a bit less than the maximum values, just in case the head motors don't complete the movement. I don't recommend changing these, except maybe velocity.
velocity = 50  # speed for movement
max_left = 81  # left yaw
left_threshold = 75  # for detecting head placement
max_right = -81  # right yaw
right_threshold = -75  # for detecting head placement
center_yaw = -1  # for last movement command only
center_threshold = 0.1  # for detecting head placement
move_pitch = -20  # head pitch
roll = 0  # head roll (should always be 0)

# ! Don't change these! It might break things.
seen = False  # whether looking at person
hPitch = None  # tracks head pitch
hYaw = None  # tracks head yaw


def _BumpSensor(data):
    # ends program when bumped
    try:
        global seen
        seen = True  # stops searching, if active
        misty.ChangeLED(0, 0, 0)  # LED off
        misty.UnregisterAllEvents()  # unregister events
        misty.StopFaceRecognition()  # stop facial recognition
        print("end of program")  # confirm program has ended
    except Exception as e:
        print("\nCOULD NOT END PROGRAM", e, "\n")


def _HeadPitch(data):
    # gets current head pitch, passes to global var
    global hPitch
    hPitch = data["message"]["value"]


def _HeadYaw(data):
    # gets current head yaw, passes to global var
    global hYaw
    hYaw = data["message"]["value"]


def _Follow(data):
    # behavior for when Misty has found someone to follow

    global person
    name = data["message"]["label"]  # name of person Misty sees

    # if she sees person of interest
    if name == person:
        global hYaw, hPitch, seen

        # get face location
        bearing = data["message"]["bearing"]
        distance = data["message"]["distance"]
        elevation = data["message"]["elevation"]

        '''
        I gave Misty a window at the center of her vision where she won't move to center your face. Without this, she'll keep moving her head to center you if you're even the slightest bit off. I recommend 2 "units" as a good baseline.
    
        I attempted to make the tolerances relative to distance. If you're within 100 centimeters, Misty will try to center your face if you're more than 2 units from center. Otherwise, she'll only move if you get 3 units off. I'm not sure how much this helps, but it doesn't break anything.
        
        Another issue is that there's no concrete way to translate the bearing/elevation distance to head position. If given a constant rate (say, move by 1 degree each time this callback runs), Misty will take a very long time to adjust. If this rate is too high (say, 5 degrees), she will overcompensate and miss the tolerance window. I decided that the most time-efficient way (for me) to fix this was to scale the rate with how far off-center the face is. There's no exact science here, and the numbers are (almost) completely arbitrary. The only calculation I did was to ensure that none of these will produce a movement that sends her head to the other side of the tolerance window.
        
        The movement duration (default .4 sec) has to be less than the debounce for facial recognition (default .5 sec). Misty needs time to complete each movement, or the movement commands will overlap and cause her to continually overshoot your face.
        
        Because this entire section is basically me throwing stuff at a wall to see what sticks, I'm not going to bother making these variables/tolerances global yet. I plan on coming back to this once I have more experience (and sanity).
        '''

        if distance > 100:  # if you're far away, larger window
            t = 3
        else:  # if you're closer, smaller window
            t = 2

        # if within tolerance (centered enough in frame)
        if abs(bearing) <= t and abs(elevation) <= t:
            if seen is False:  # if just spotted person
                seen = True  # record success
                misty.ChangeLED(0, 255, 0)  # LED green
                misty.PlayAudio("s_Joy4.wav", volume=volume)  # play audio

        # if not within tolerance
        else:
            misty.ChangeLED(255, 255, 0)  # LED yellow
            seen = False  # person not centered

            y = hYaw  # current yaw

            # scale to anticipate target speed
            if abs(bearing) <= 3:
                b_factor = 1
            elif abs(bearing) <= 7:
                b_factor = 1.2
            else:
                b_factor = 1.6

            # if abs(bearing) > t:
            y = hYaw + bearing*b_factor

            p = hPitch  # current pitch

            # scale to anticipate target speed
            if abs(elevation) <= 3:
                e_factor = 1
            if abs(elevation) <= 7:
                e_factor = 1.5  # 1.3
            else:
                e_factor = 2  # 1.8

            # if abs(elevation) > t:
            p = hPitch + elevation*e_factor

            misty.MoveHead(pitch=p, yaw=y, duration=.4)  # move head


def _FaceRecognition(data):
    # when she sees someone, she processes it
    # if it's a known person, she stops and fixates on that person

    try:  # try to get face name, compare against known faces
        face = data["message"]["label"]  # face from data
        print(face)

        # if known: stop, unregister and reregister to start second phase
        if face == person:
            misty.Halt()  # stop moving
            misty.ChangeLED(0, 255, 0)  # LED green
            misty.PlayAudio("s_Joy2.wav", volume=volume)  # play audio

            print(f"Hello, {face}! I'm now following you!")

            # unregister searching FR
            misty.UnregisterEvent(Events.FaceRecognition)
            time.sleep(1)  # give time to unregister)

            # register for follow FR
            misty.RegisterEvent("FaceRecognition", Events.FaceRecognition,
                                debounce=FR_debounce, keep_alive=True, callback_function=_Follow)

    except Exception as e:  # this shouldn't run unless data is corrupted
        print("Searching error:", e)


def moveRight():  # moves head right
    global move_pitch, roll, max_right, velocity, hYaw, right_threshold

    misty.MoveHead(move_pitch, roll, max_right, velocity)  # move to right

    # don't proceed until fully right or target seen
    while (hYaw > right_threshold) and not seen:
        pass

    if not seen:  # if target not seen, move left
        moveLeft()


def moveLeft():  # moves head left
    global move_pitch, roll, max_left, velocity, hYaw, left_threshold

    misty.MoveHead(move_pitch, roll, max_left, velocity)  # move to left

    # don't proceed until fully left or target seen
    while (hYaw < left_threshold) and not seen:
        pass

    if not seen:  # if target not seen, move right
        moveRight()


if __name__ == "__main__":
    print("Going on an adventure!")
    misty.UnregisterAllEvents()  # unregister
    misty.ChangeLED(0, 0, 255)  # LED blue

    misty.MoveHead(start_pitch, 0, 0)  # forward and up for better view

    # register for bump sensor
    misty.RegisterEvent("BumpSensor", Events.BumpSensor,
                        callback_function=_BumpSensor)

    # register for facial recognition
    misty.RegisterEvent("FaceRecognition", Events.FaceRecognition,
                        callback_function=_FaceRecognition, debounce=FR_debounce, keep_alive=True)

    # register for actuator position head pitch
    misty.RegisterEvent("ActuatorPositionHP", Events.ActuatorPosition, [
                        EventFilters.ActuatorPosition.HeadPitch], debounce=AP_debounce, keep_alive=True, callback_function=_HeadPitch)

    # register for actuator position head yaw
    misty.RegisterEvent("ActuatorPositionHY", Events.ActuatorPosition, [
                        EventFilters.ActuatorPosition.HeadYaw], debounce=AP_debounce, keep_alive=True, callback_function=_HeadYaw)

    time.sleep(1)  # give time for registration
    misty.StartFaceRecognition()  # start facial recognition

    if not seen:  # if target not seen, move right
        moveRight()
