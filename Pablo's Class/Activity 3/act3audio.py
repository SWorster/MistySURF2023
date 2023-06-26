'''
Skye Weaver Worster

WORK IN PROGRESS

Start Misty at pose0; emit a sound, and have misty drive to face the sound origin
(How hard is it to have musty learn and recognize a key phrase?)
(Can misty count claps? maybe an exercise where she moves/stops depending on num claps)
'''

from mistyPy.Robot import Robot
from mistyPy.Events import Events
import os
import time


def _KeyPhraseRecognized(data):
    print(data)


def _SourceTrackDataMessage(data):
    print(data)


def _SourceFocusConfigMessage(data):
    print(data)


def _VoiceRecord(data):
    print(data)


def audio():
    '''
    TODO: I'm not doing any work on this section until I get some practice with Misty's audio.
    '''

    misty.RegisterEvent("KeyPhraseRecognized", Events.KeyPhraseRecognized, condition=None,
                        debounce=1000, keep_alive=True, callback_function=_KeyPhraseRecognized)

    misty.RegisterEvent("SourceTrackDataMessage", Events.SourceTrackDataMessage, condition=None,
                        debounce=1000, keep_alive=True, callback_function=_SourceTrackDataMessage)

    misty.RegisterEvent("SourceFocusConfigMessage", Events.SourceFocusConfigMessage, condition=None,
                        debounce=1000, keep_alive=True, callback_function=_SourceFocusConfigMessage)

    misty.RegisterEvent("VoiceRecord", Events.VoiceRecord, condition=None,
                        debounce=1000, keep_alive=True, callback_function=_VoiceRecord)




def end():
    misty.UnregisterAllEvents()
    os.system('python3 /Users/skyeworster/Desktop/reset.py')
    print("program ended")


if __name__ == "__main__":
    misty = Robot("131.229.41.135")

    # clean slate. should print "reset"
    # os.system('python3 /Users/skyeworster/Desktop/reset.py')
    # time.sleep(2)

    # ignore TOF sensors
    misty.UpdateHazardSettings(disableTimeOfFlights=True)
