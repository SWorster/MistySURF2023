'''
Skye Weaver Worster

WORK IN PROGRESS

So far, I've made Misty change LED color depending on where the loudest sound is originating.

Pablo's instructions:
Start Misty at pose0; emit a sound, and have misty drive to face the sound origin
(How hard is it to have Misty learn and recognize a key phrase?)
(Can misty count claps? maybe an exercise where she moves/stops depending on num claps)

1. How do we know when to listen for a sound? It could be too short and not picked up by our debounce value. Additionally, driving to face the sound could be challenging- we'd have to use and record yaw values, then translate that to movement. Not fun, but doable.

2. Haven't tried this yet.

3. Same as with #1: we don't know if Misty will pick up a clap consistently. Further experimentation required.

'''

from mistyPy.Robot import Robot
from mistyPy.Events import Events
import time

misty = Robot("131.229.41.135")  # robot object
STDM_debounce = 500  # SourceTrackDataMessage debounce, in ms
t = 10  # listening time, in seconds


def _SourceTrackDataMessage(data):
    try:
        # get array of 360 values
        polar = data["message"]["voiceActivityPolar"]

        # average value for each sector
        front = (sum(polar[0:45]) + sum(polar[315:360])) / 90
        right = sum(polar[45:135]) / 90
        back = sum(polar[135:225]) / 90
        left = sum(polar[225:315]) / 90

        # print(round(front), round(right), round(back), round(left))  # useful for debugging

        sectors = [front, right, back, left]  # list of sector values
        place = sectors.index(max(sectors))  # find where loudest avg sound is
        if place == 0:  # front
            misty.ChangeLED(255, 0, 0)  # red
        elif place == 1:  # right
            misty.ChangeLED(255, 200, 0)  # yellow
        elif place == 2:  # back
            misty.ChangeLED(0, 255, 0)  # green
        elif place == 3:  # left
            misty.ChangeLED(0, 0, 255)  # blue

    except Exception as e:
        print(e)


if __name__ == "__main__":

    # register for SourceTrackDataMessage
    misty.RegisterEvent("SourceTrackDataMessage", Events.SourceTrackDataMessage, condition=None,
                        debounce=STDM_debounce, keep_alive=True, callback_function=_SourceTrackDataMessage)

    misty.StartRecordingAudio("test")  # start listening
    time.sleep(t)  # time for listening
    misty.StopRecordingAudio()  # stop listening

    misty.UnregisterAllEvents()  # unregister
