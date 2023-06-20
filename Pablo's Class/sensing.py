'''
Sensing Modalities

This code can be used to test some of Misty's sensory capabilities. The following is the list of events and commands this code uses. Most of the sensory capabilities are boring and don't make sense for a demo, so I was generous with what I cut.

Because I haven't done any work with audio yet, I've left that section incomplete.

Proprioception
    - ActuatorPosition (arms/head)
    - DriveEncoders (treads)
    - IMU (vestibular)

Audio 
    - KeyPhraseRecognized (use with StartKeyPhraseRecognition)
    - SourceTrackDataMessage
    - SourceFocusConfigMessage
    - VoiceRecord (use with CaptureSpeech)
    
Visual
    - FaceRecognition (use with StartFaceDetection)
    - TimeOfFlight

Tactile
    - BumpSensor
    - TouchSensor
'''

from mistyPy.Robot import Robot
from mistyPy.Events import Events
import os
import time

################################################################################################
#                                       PROPRIOCEPTION                                         #
################################################################################################


def _ActuatorPosition(data):
    print("\n\nActuatorPosition\n", data)


def _DriveEncoders(data):
    print("\n\nDriveEncoders\n", data)


def _IMU(data):
    print("\n\nIMU\n", data)


def proprioception():
    '''
    I can't think of a better way to demo these than to print the data.
    '''
    misty.RegisterEvent("ActuatorPosition", Events.ActuatorPosition, condition=None,
                        debounce=3000, keep_alive=True, callback_function=_ActuatorPosition)

    time.sleep(.9)

    misty.RegisterEvent("DriveEncoders", Events.DriveEncoders, condition=None,
                        debounce=3000, keep_alive=True, callback_function=_DriveEncoders)

    time.sleep(.9)

    misty.RegisterEvent("IMU", Events.IMU, condition=None,
                        debounce=3000, keep_alive=True, callback_function=_IMU)


################################################################################################
#                                         FACIAL                                               #
################################################################################################

def _FaceRecognition(data):
    print(data)
    if data["message"]["label"] is not ("unknown_person" or None):
        misty.Speak("Hello {}".format(
            data["message"]["label"]), None, None, None, True, "tts")
        misty.StopFaceRecognition()
        again = input("Search again? y/n ")
        if again == "n":
            end()
        else:
            print("Continuing")
            misty.StartFaceRecognition()


def facial():
    misty.StartFaceRecognition()
    misty.RegisterEvent("FaceRecognition", Events.FaceRecognition, condition=None,
                        debounce=1000, keep_alive=True, callback_function=_FaceRecognition)


################################################################################################
#                                           TOF                                                #
################################################################################################

def _TimeOfFlight(data):
    name = data["message"]["sensorPosition"]
    d = data["message"]["distanceInMeters"]
    if data["message"]["status"] == 0:
        if name in ["Right", "Left", "Center", "Back"] and d < .2:
            print(name, d)
        elif d > .06:
            # pass due to bottom TOF sensor malfunction
            # print(name, d)
            pass


def tof():
    '''
    The boring half of the visual capabilities.
    '''
    misty.RegisterEvent("TimeOfFlight", Events.TimeOfFlight,
                        condition=None, keep_alive=True, callback_function=_TimeOfFlight)


################################################################################################
#                                        TACTILE                                               #
################################################################################################

def _BumpSensor(data):
    name = data["message"]["sensorId"]
    hit = data["message"]["isContacted"]
    print(name, hit)
    if hit:
        misty.ChangeLED(255, 0, 0)
        misty.PlayAudio("A_meow1.mp3", 10)
    else:
        misty.ChangeLED(0, 0, 0)
        misty.PlayAudio("A_meow2.mp3", 10)


def _TouchSensor(data):
    name = data["message"]["sensorPosition"]
    hit = data["message"]["isContacted"]
    print(name, hit)
    if hit:
        misty.ChangeLED(0, 255, 0)
        misty.PlayAudio("A_purr1.mp3", 30)
    else:
        misty.ChangeLED(0, 255, 0)
        misty.StopAudio()


def tactile():
    '''
    Misty becomes a cat whenever she's touched. Fun!
    '''
    misty.RegisterEvent("BumpSensor", Events.BumpSensor, condition=None,
                        keep_alive=True, callback_function=_BumpSensor)
    misty.RegisterEvent("TouchSensor", Events.TouchSensor, condition=None,
                        keep_alive=True, callback_function=_TouchSensor)


################################################################################################
#                                         AUDIO                                                #
################################################################################################

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

################################################################################################
#                                       MAIN                                                   #
################################################################################################


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

    # TODO: add in a = audio
    print("t = tactile, p = proprioception, f = facial, o = time of flight, e = end")
    hit = input("Specify mode: ")

    if hit == "t":
        print("tactile")
        tactile()
    elif hit == "p":
        proprioception()
    elif hit == "f":
        facial()
    elif hit == "o":
        tof()
    # elif hit == "a":
    #     audio()
    else:
        end()
