'''
Skye Weaver Worster

Misty moves/turns towards the loudest sound. Can be stopped with bump sensors.

WARNING: this code disables Misty's TOF sensors, so she won't automatically stop at table edges and other drops. They are only re-enabled if the program is terminated via the bump sensors. Be careful!
'''

from mistyPy.Robot import Robot
from mistyPy.Events import Events
import time

misty = Robot("131.229.41.135")  # robot object
STDM_debounce = 100  # SourceTrackDataMessage debounce, in ms
trigger = 20  # sound volume that causes movement
filename = "test" # name of file, will be appended with .wav

# speeds for movement
v_front = 20
v_back = -20
v_right = 20
v_left = -20


def _BumpSensor(data):
    # ends program when bumped
    misty.Stop()  # stop moving
    misty.StopRecordingAudio()  # stop recording audio
    misty.ChangeLED(0, 0, 0)  # LED off
    misty.UnregisterAllEvents()  # unregister events
    misty.UpdateHazardSettings(revertToDefault=True)  # default TOF
    print("end of program")  # confirm program has ended


def _SourceTrackDataMessage(data):
    misty.ChangeLED(0, 255, 0)
    try:
        # get array of 360 values
        polar = data["message"]["voiceActivityPolar"]

        # average value for each sector
        front = (sum(polar[0:45]) + sum(polar[315:360])) / 90
        right = sum(polar[45:135]) / 90
        back = sum(polar[135:225]) / 90
        left = sum(polar[225:315]) / 90

        sectors = [front, right, back, left]  # list of sector values
        s_max = max(sectors)  # maximum volume

        if s_max > trigger:  # if sound is loud enough to trigger movement
            place = sectors.index(s_max)  # find where loudest avg sound is
            if place == 0:  # front
                misty.ChangeLED(255, 0, 0)  # red
                misty.Drive(v_front, 0)  # drive forward
            elif place == 1:  # right
                misty.ChangeLED(255, 200, 0)  # yellow
                misty.Drive(0, v_right)  # turn right
            elif place == 2:  # back
                misty.ChangeLED(0, 255, 0)  # green
                misty.Drive(v_back, 0)  # drive backward
            elif place == 3:  # left
                misty.ChangeLED(0, 0, 255)  # blue
                misty.Drive(0, v_left)  # turn left

    except Exception as e:  # error handling
        print("Error:", e)


if __name__ == "__main__":
    misty.UpdateHazardSettings(disableTimeOfFlights=True)  # ignore TOF

    # register for bump sensor
    misty.RegisterEvent("BumpSensor", Events.BumpSensor,
                        callback_function=_BumpSensor)

    misty.StartRecordingAudio(f"{filename}.wav")  # start listening

    time.sleep(1)  # give time for fans to stop
    misty.ChangeLED(255, 0, 0)
    
    # register for SourceTrackDataMessage
    misty.RegisterEvent("SourceTrackDataMessage", Events.SourceTrackDataMessage,
                        debounce=STDM_debounce, keep_alive=True, callback_function=_SourceTrackDataMessage)
