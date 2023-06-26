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

3. Misty doesn't pick up claps consistently. They're loud, but short. Have tried debounce of 5, 100, 500. None help Misty detect claps. Waiting on guidance before proceeding.

'''

from mistyPy.Robot import Robot
from mistyPy.Events import Events
import time

misty = Robot("131.229.41.135")  # robot object
STDM_debounce = 100  # SourceTrackDataMessage debounce, in ms
t = 3  # listening time, in seconds
v = 2 # volume

# ! DO NOT CHANGE
count = -1 # starting number of claps. first isn't counted, because Misty picks up her own fan noise for a bit


def _SourceTrackDataMessage(data):
    global count

    try:
        # get array of 360 values
        polar = data["message"]["voiceActivityPolar"]

        # average value for each sector
        front = (sum(polar[0:45]) + sum(polar[315:360])) / 90
        right = sum(polar[45:135]) / 90
        back = sum(polar[135:225]) / 90
        left = sum(polar[225:315]) / 90

        print(round(front), round(right), round(back),
              round(left))  # useful for debugging

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

        # TODO: I made this test specific to the front because I'm currently sitting in front of Misty. I'll make this more general once I iron out everything
        if front > 30: # if loud sound detected in front of Misty
            count += 1
            print(f"                         {count}")

    except Exception as e:
        print(e)


if __name__ == "__main__":
    misty.StopAudio()

    misty.StartRecordingAudio("test")  # start listening
    
    time.sleep(1) # give time for fans to stop
    
    # register for SourceTrackDataMessage
    misty.RegisterEvent("SourceTrackDataMessage", Events.SourceTrackDataMessage, condition=None,
                        debounce=STDM_debounce, keep_alive=True, callback_function=_SourceTrackDataMessage)
    
    time.sleep(t)  # time for listening
    misty.StopRecordingAudio()  # stop listening
    misty.UnregisterAllEvents()  # unregister
    misty.ChangeLED(0,0,0)
    
    # play different audio clip depending on how many claps detected
    if count == 0:
        misty.PlayAudio("A_Lacrimosa.mp3",v*3)
    elif count == 1:
        misty.PlayAudio("A_RickrollShort.mp3",v)
    elif count == 2:
        misty.PlayAudio("A_CarelessWhisper.mp3",v)
    elif count == 3:
        misty.PlayAudio("A_Circus.mp3",v)
    elif count == 4:
        misty.PlayAudio("A_megalovania.m4a",v)
    
    time.sleep(2) # stop audio after a while
    misty.StopAudio()
