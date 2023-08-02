'''
Skye Weaver Worster '25J

Misty looks around, trying to find the target's face. Her search loops forever until she sees the target. If she finds it, she starts following the target with her head. Target has to be known, and their name must be provided. To end program, hit bump sensor.
'''

# import statements
from mistyPy.Robot import Robot
from mistyPy.Events import Events
from mistyPy.EventFilters import EventFilters
import time

# setup parameters
misty = Robot("131.229.41.135")  # Misty robot with your IP
person = "test"  # person to look for
FR_debounce = 500  # facial recognition debounce
AP_debounce = 100  # actuator position debounce

# audio parameters
audio_found = "s_Joy2.wav"  # audio when first found
audio_seen = "s_Joy4.wav"  # audio when within tolerance
volume = 10  # volume for audio clips

# searching parameters
# The thresholds are a bit less than the maximum values, just in case the head motors don't complete the movement. I don't recommend changing these, except maybe velocity.
velocity = 70  # speed for movement (recommend 50)
start_pitch = -20  # starting pitch for head (recommend looking up)
max_right = -81  # full right yaw
right_threshold = -70  # for detecting head placement in moveRight
max_left = 81  # full left yaw
left_threshold = 70  # for detecting head placement in moveLeft
roll = 0  # head roll (should always be 0)

# * parameters for Misty's face-tracking movement. Fiddling with these might yield better results, so feel free to experiment
t_dist = 100  # distance requiring larger center window
t_close = 2  # size of center window when close
t_far = 3  # size of center window when far
duration = .4  # ! duration of each head movement. must be less than FR_debounce!

# bearing parameters
# if target within b_dist1 of center, scale movement by b1
# else if target within b_dist2 of center, scale movement by b2
# else scale by b3
b_dist1 = 3  # distance from center where scale b1 is applied
b1 = 1  # scaling factor when bearing within b_dist1
b_dist2 = 7  # distance from center where scale b2 is applied
b2 = 1.2  # scaling factor when bearing within b_dist2
b3 = 1.6  # scaling factor when bearing outside b_dist2

# elevation parameters
e_dist1 = 3  # distance from center where scale e1 is applied
e1 = 1  # scaling factor when elevation within e_dist1
e_dist2 = 7  # distance from center where scale e2 is applied
e2 = 1.5  # scaling factor when elevation within e_dist2
e3 = 2  # scaling factor when elevation outside e_dist2

# ! Don't change these!
seen = False  # whether looking at person
hPitch = None  # tracks head pitch
hYaw = None  # tracks head yaw


def _BumpSensor(data):  # ends program when bumped
    misty.UnregisterAllEvents()  # unregister events
    global seen
    seen = True  # stops following, if active
    misty.ChangeLED(0, 0, 0)  # LED off
    misty.StopFaceRecognition()  # stop facial recognition
    print("end of program")  # confirm program has ended


def _HeadPitch(data):  # gets current head pitch, passes to global var
    global hPitch
    hPitch = data["message"]["value"]


def _HeadYaw(data):  # gets current head yaw, passes to global var
    global hYaw
    hYaw = data["message"]["value"]


def _Follow(data):  # behavior for when Misty has found someone to follow
    name = data["message"]["label"]  # name of person Misty sees
    if name == person:  # if she sees person of interest
        global seen

        # get face location
        bearing = data["message"]["bearing"]
        distance = data["message"]["distance"]
        elevation = data["message"]["elevation"]

        if distance > t_dist:  # center window scales with distance
            t = t_far
        else:
            t = t_close

        # if within tolerance (centered enough in frame)
        if abs(bearing) <= t and abs(elevation) <= t:
            if seen is False:  # if just spotted person
                seen = True  # record success
                misty.ChangeLED(0, 255, 0)  # LED green
                misty.PlayAudio(audio_seen, volume=volume)  # play audio

        # if not within tolerance
        else:
            misty.ChangeLED(255, 255, 0)  # LED yellow
            seen = False  # person not centered

            # scale to anticipate target speed
            if abs(bearing) <= b_dist1:
                b_factor = b1
            elif abs(bearing) <= b_dist2:
                b_factor = b2
            else:
                b_factor = b3

            if abs(bearing) > t:
                y = hYaw + bearing*b_factor
            else:  # if within tolerance, don't move
                y = hYaw

            # scale to anticipate target speed
            if abs(elevation) <= e_dist1:
                e_factor = e1
            if abs(elevation) <= e_dist2:
                e_factor = e2
            else:
                e_factor = e3

            if abs(elevation) > t:
                p = hPitch + elevation*e_factor
            else:  # if within tolerance, don't move
                p = hPitch

            misty.MoveHead(p, roll, y, duration=duration)  # move head


def _FaceRecognition(data):  # searches for target
    try:  # try to get face name, compare against known faces
        face = data["message"]["label"]  # face from data
        print(face)

        # if known: stop, unregister and re-register to start second phase
        if face == person:
            global seen
            seen = True  # stops while loops
            misty.Halt()  # stop moving
            misty.ChangeLED(0, 255, 0)  # LED green
            misty.PlayAudio(audio_found, volume=volume)  # play audio
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
    misty.MoveHead(start_pitch, roll, max_right, velocity)  # move to right

    while hYaw > right_threshold and not seen:
        pass  # don't proceed until fully right or target seen

    if not seen:  # if target not seen, move left
        moveLeft()


def moveLeft():  # moves head left
    misty.MoveHead(start_pitch, roll, max_left, velocity)  # move to left

    while hYaw < left_threshold and not seen:
        pass  # don't proceed until fully left or target seen

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
