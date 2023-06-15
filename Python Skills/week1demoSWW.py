# import statements
from mistyPy.Robot import Robot
from mistyPy.Events import Events
from mistyPy.EventFilters import EventFilters
import time
import os


def _BumpSensor(data):
    '''
    there's no graceful way to end anything, so...
    when in doubt, terminate via command line
    '''
    try:
        print("bumped")

        # should print "reset" to console
        os.system('python3 /Users/skyeworster/Desktop/reset.py')

        misty.UnregisterAllEvents()  # just in case
        misty.StopFaceRecognition()

        # if this doesn't print, pick a god and pray
        print("end of program (misty bumped)")
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
    '''
    behavior for when misty has found someone to follow
    '''

    global senpai
    name = data["message"]["label"]

    # sees person of interest
    if name == senpai:
        global hYaw
        global hPitch
        global seen

        bearing = data["message"]["bearing"]
        distance = data["message"]["distance"]
        elevation = data["message"]["elevation"]

        # TODO make tolerance relative to distance?
        # no idea if this works, or if it helps
        if distance > 100:
            t = 3
        else:
            t = 2

        # if within tolerance (centered enough in frame)
        if abs(bearing) <= t and abs(elevation) <= t:
            if seen is False:
                seen = True
                misty.ChangeLED(0, 255, 0)
                misty.PlayAudio("s_Joy4.wav", volume=2)

        # not within tolerance
        # TODO put everything below in the else statement?
        # don't need to move anything
        else:
            misty.ChangeLED(255, 255, 0)
            seen = False

            # TODO everything below this used to be outside the else statement
            # see how it works ig

            y = hYaw  # current yaw

            # scale to anticipate target speed
            if abs(bearing) <= 3:
                bfactor = 1
            elif abs(bearing) <= 7:
                bfactor = 1.2
            else:
                bfactor = 1.6

            # if abs(bearing) > t:
            y = hYaw + bearing*bfactor

            p = hPitch  # current pitch

            # scale to anticipate target speed
            if abs(elevation) <= 3:
                efactor = 1
            if abs(elevation) <= 7:
                efactor = 1.5  # 1.3
            else:
                efactor = 2  # 1.8

            # if abs(elevation) > t:
            p = hPitch + elevation*efactor

            misty.MoveHead(pitch=p, yaw=y, duration=.4)


def _FaceRecognition(data):
    '''
    when she sees someone, she processes it
    if it's a known person, she stops and fixates on that person
    not sure how timing will work on this. might have to stop her before processing if it takes too long
    '''

    # try to get face name, compare against known faces

    print("FR")
    try:
        face = data["message"]["label"]
        print(face)

        # if known: stop, unreg and rereg to start second phase
        if face == senpai:
            misty.Halt()
            misty.ChangeLED(0, 255, 0)
            misty.PlayAudio("s_Joy2.wav", volume=2)

            print("Hello, {}! I'm now following you!".format(face))

            misty.UnregisterAllEvents()
            time.sleep(1)

            # register for BumpSensor (halts execution)
            misty.RegisterEvent("BumpSensor", Events.BumpSensor,
                                callback_function=_BumpSensor)

            # register for FR @ 500ms
            # TODO: update comment if this has changed
            misty.RegisterEvent("FaceRecognition", Events.FaceRecognition,
                                callback_function=_Follow, keep_alive=True, debounce=500)

            # register for HeadPitch/HeadYaw @ 100ms
            misty.RegisterEvent("ActuatorPositionHP", Events.ActuatorPosition, [
                EventFilters.ActuatorPosition.HeadPitch], debounce=100, keep_alive=True, callback_function=_HeadPitch)

            misty.RegisterEvent("ActuatorPositionHY", Events.ActuatorPosition, [
                EventFilters.ActuatorPosition.HeadYaw], debounce=100, keep_alive=True, callback_function=_HeadYaw)

            misty.KeepAlive()  # keep events live

    # this shouldn't run unless data is corrupted
    except:
        print("except")


if __name__ == "__main__":
    misty = Robot("131.229.41.135")
    print("Going on an adventure!")
    misty.UnregisterAllEvents()
    misty.ChangeLED(0, 0, 255)

    global hPitch
    global hYaw
    global seen
    seen = False
    global senpai
    senpai = "Skye"


    misty.MoveHead(-20, 0, 0)

    misty.RegisterEvent("FaceRecognition", Events.FaceRecognition,
                        callback_function=_FaceRecognition, debounce=500, keep_alive=True)

    misty.RegisterEvent("ActuatorPositionHP", Events.ActuatorPosition, [
                        EventFilters.ActuatorPosition.HeadPitch], debounce=50, keep_alive=True, callback_function=_HeadPitch)

    misty.RegisterEvent("ActuatorPositionHY", Events.ActuatorPosition, [
                        EventFilters.ActuatorPosition.HeadYaw], debounce=50, keep_alive=True, callback_function=_HeadYaw)

    misty.RegisterEvent("BumpSensor", Events.BumpSensor,
                        callback_function=_BumpSensor)

    time.sleep(1)
    misty.StartFaceRecognition()

    misty.MoveHead(-20, 0, -81, 50)

    while hYaw > -80:
        pass

    misty.MoveHead(-20, 0, 81, 50)

    while hYaw < 75:
        pass

    print("here")
    misty.MoveHead(-20, 0, -10, 50)

    while hYaw > 0.1:
        pass

    misty.PlayAudio("s_Sadness.wav", volume=2)
    print("didn't see anyone :(")
    misty.ChangeLED(255,0,0)
    time.sleep(1)
    _BumpSensor(1)
