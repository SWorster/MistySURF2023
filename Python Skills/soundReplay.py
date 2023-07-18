'''
Skye Weaver Worster

Misty hears a sentence and repeats it. No speech parsing capabilities, unfortunately.
'''

# import statements
from mistyPy.Robot import Robot
from mistyPy.Events import Events

misty = Robot("131.229.41.135")
volume = 50  # playback volume


def _VoiceRecord(data):
    if data["message"]["success"]:  # if recorded successfully
        # register for audio completion event
        misty.RegisterEvent(
            "AudioPlayComplete", Events.AudioPlayComplete, callback_function=_AudioPlayComplete)

        # start playing sound. end of sound triggers callback
        misty.PlayAudio("capture_Dialogue.wav", volume=volume)
        print("playing audio")


def _AudioPlayComplete(data):
    # if the audio stops playing
    if data["message"]["metaData"]["name"] == "capture_Dialogue.wav":
        misty.UnregisterAllEvents()  # unregister from all events
        print("done")


if __name__ == "__main__":
    print("Going on an adventure!")
    misty.UnregisterAllEvents()  # unregister from all previous events
    misty.ChangeLED(0, 0, 255)  # change LED to blue

    # register for voice recording events
    misty.RegisterEvent("VoiceRecord", Events.VoiceRecord,
                        callback_function=_VoiceRecord)

    # capture speech, triggering callback
    misty.CaptureSpeech(requireKeyPhrase=False)
    print("recording")
