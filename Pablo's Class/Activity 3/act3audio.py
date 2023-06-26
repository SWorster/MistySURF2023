'''
Skye Weaver Worster

WORK IN PROGRESS

Start Misty at pose0; emit a sound, and have misty drive to face the sound origin
(How hard is it to have Misty learn and recognize a key phrase?)
(Can misty count claps? maybe an exercise where she moves/stops depending on num claps)
'''

from mistyPy.Robot import Robot
from mistyPy.Events import Events
import os
import time

misty = Robot("131.229.41.135")  # robot object
STDM_debounce = 1000  # SourceTrackDataMessage debounce, in ms


def _SourceTrackDataMessage(data):
    try:
        sectors = data["message"]["voiceActivitySectors"]
        if sectors[0]:
            misty.ChangeLED(255, 0, 0)
        elif sectors[1]:
            misty.ChangeLED(255, 200, 0)
        elif sectors[2]:
            misty.ChangeLED(0, 255, 0)
        elif sectors[3]:
            misty.ChangeLED(0, 0, 255)
        else:
            misty.ChangeLED(0, 0, 0)
        print(sectors)
    except Exception as e:
        print(e)


if __name__ == "__main__":

    # register for SourceTrackDataMessage
    misty.RegisterEvent("SourceTrackDataMessage", Events.SourceTrackDataMessage, condition=None,
                        debounce=STDM_debounce, keep_alive=True, callback_function=_SourceTrackDataMessage)

    print(misty.StartRecordingAudio("test"))

    time.sleep(5)
    misty.StopRecordingAudio()

    misty.UnregisterAllEvents()
