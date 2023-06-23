'''
Skye Weaver Worster

Misty looks around, trying to find my face. If she finds it, she starts following me with her head. If not, she is sad and the program ends.

Target has to be known, and their name must be provided.
'''

# import statements
from mistyPy.Robot import Robot
from mistyPy.Events import Events
from mistyPy.EventFilters import EventFilters
import time

# parameters you can/should change
misty = Robot("131.229.41.135")  # Misty robot with your IP
person = "Skye"  # person to look for
FR_debounce = 500  # facial recognition debounce
AP_debounce = 100  # actuator position debounce
volume = 2  # volume for audio clips

# Don't change these! It might break things.
seen = False  # whether looking at person
hPitch = None  # tracks head pitch
hYaw = None  # tracks head yaw

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


def _BumpSensor(data):
    # ends program when bumped
    try:
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
    # behavior for when misty has found someone to follow

    global person
    name = data["message"]["label"]

    # sees person of interest
    if name == person:
        global hYaw, hPitch, seen

        # get face location
        bearing = data["message"]["bearing"]
        distance = data["message"]["distance"]
        elevation = data["message"]["elevation"]

        # ? make tolerance relative to distance? no idea if this works, or if it helps
        if distance > 100:
            t = 3
        else:
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
    '''
    when she sees someone, she processes it
    if it's a known person, she stops and fixates on that person
    not sure how timing will work on this. might have to stop her before processing if it takes too long
    '''

    try:  # try to get face name, compare against known faces
        face = data["message"]["label"]  # face from data
        print(face)

        # if known: stop, unregister and reregister to start second phase
        if face == person:
            misty.Halt()  # stop moving
            misty.ChangeLED(0, 255, 0)  # LED green
            misty.PlayAudio("s_Joy2.wav", volume=volume)  # play audio

            print(f"Hello, {face}! I'm now following you!")

            misty.UnregisterAllEvents()  # unregister events
            time.sleep(1)  # give time to unregister

            # register for BumpSensor (halts execution)
            misty.RegisterEvent("BumpSensor", Events.BumpSensor,
                                callback_function=_BumpSensor)

            # register for FR @ 500ms
            # TODO: update comment if this has changed
            misty.RegisterEvent("FaceRecognition", Events.FaceRecognition, debounce=FR_debounce, keep_alive=True,
                                callback_function=_Follow)

            # register for HeadPitch/HeadYaw @ 100ms
            misty.RegisterEvent("ActuatorPositionHP", Events.ActuatorPosition, [
                EventFilters.ActuatorPosition.HeadPitch], debounce=AP_debounce, keep_alive=True, callback_function=_HeadPitch)

            misty.RegisterEvent("ActuatorPositionHY", Events.ActuatorPosition, [
                EventFilters.ActuatorPosition.HeadYaw], debounce=AP_debounce, keep_alive=True, callback_function=_HeadYaw)

            misty.KeepAlive()  # keep events live

    # this shouldn't run unless data is corrupted
    except:
        print("except")


if __name__ == "__main__":
    print("Going on an adventure!")
    misty.UnregisterAllEvents()  # unregister
    misty.ChangeLED(0, 0, 255)  # LED blue

    misty.MoveHead(-20, 0, 0)  # forward and up for better view

    # register for facial recognition
    misty.RegisterEvent("FaceRecognition", Events.FaceRecognition,
                        callback_function=_FaceRecognition, debounce=500, keep_alive=True)

# register for actuator position head pitch
    misty.RegisterEvent("ActuatorPositionHP", Events.ActuatorPosition, [
                        EventFilters.ActuatorPosition.HeadPitch], debounce=50, keep_alive=True, callback_function=_HeadPitch)

# register for actuator position head yaw
    misty.RegisterEvent("ActuatorPositionHY", Events.ActuatorPosition, [
                        EventFilters.ActuatorPosition.HeadYaw], debounce=50, keep_alive=True, callback_function=_HeadYaw)

# register for bump sensor
    misty.RegisterEvent("BumpSensor", Events.BumpSensor,
                        callback_function=_BumpSensor)

    time.sleep(1)  # give time for registration
    misty.StartFaceRecognition()  # start facial recognition

    # move Misty's head to the right, then left, then return to center. Misty will stop moving when she sees a person
    misty.MoveHead(move_pitch, roll, max_right, velocity)  # move to right
    while hYaw > right_threshold:  # wait until fully right
        pass
    misty.MoveHead(move_pitch, roll, max_left, velocity)  # move to left
    while hYaw < left_threshold:  # wait until fully left
        pass
    misty.MoveHead(move_pitch, roll, center_threshold,
                   velocity)  # move to center
    while hYaw > center_threshold:  # wait until fully centered
        pass

    # If we make it to this point, Misty hasn't seen target
    misty.PlayAudio("s_Sadness.wav", volume=volume)  # play sad noise
    print("Didn't see anyone :(")
    misty.ChangeLED(255, 0, 0)  # LED red
    time.sleep(1)  # wait for audio to finish

    # pass a dummy arg to BumpSensor callback, which ends the program
    _BumpSensor(1)
