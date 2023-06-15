'''
Misty hears a sentence and repeats it.
No speech parsing capabilities, unfortunately.
'''

# import statements
from mistyPy.Robot import Robot
from mistyPy.Events import Events
import os

def _VoiceRecord(data):
    # if recorded successfully
    if data["message"]["success"]:
        # register for audio completion event
        misty.RegisterEvent("AudioPlayComplete", Events.AudioPlayComplete, callback_function=_AudioPlayComplete)
        
        # start playing sound. end of sound triggers callback
        misty.PlayAudio("capture_Dialogue.wav",volume=50)
        print("playing audio")
        

def _AudioPlayComplete(data):
    # if the audio stops playing
    if data["message"]["metaData"]["name"] == "capture_Dialogue.wav":
        os.system('python3 /Users/skyeworster/Desktop/reset.py') # unregister
        print("done")

if __name__ == "__main__":
    misty = Robot("131.229.41.135")
    print("Going on an adventure!")
    misty.UnregisterAllEvents()
    misty.ChangeLED(0, 0, 255)

    # register for voice recording events
    misty.RegisterEvent("VoiceRecord", Events.VoiceRecord, callback_function=_VoiceRecord)
    
    # capture speech, triggering callback
    misty.CaptureSpeech(requireKeyPhrase=False)
    print("recording")
