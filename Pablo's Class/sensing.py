'''
Sensing Modalities

This code can be used to test all of Misty's sensory capabilities. The following is a list of events and commands we can use (filtered to exclude completion messages, various notifications, etc).

Proprioception
    - ActuatorPosition (arms/head)
    - DriveEncoders (treads)
    - IMU (vestibular)
    - LocomotionCommand (change in velocity)

Audio
    - KeyPhraseRecognized (use with StartkeyPhraseRecognition)
    - SourceTrackDataMessage
    - SourceFocusConfigMessage
    - VoiceRecord (use with CaptureSpeech)
    
Visual
    - FaceRecognition (use with StartFaceDetection, StartFaceRecognition)
    - FaceTraining (use with StartFaceTraining)
    - TimeOfFlight
    - ArTagDetection (use with StartArTagDetector)
    - ObjectDetection (use with StartObjectDetector)
    - WorldState

Tactile
    - BumpSensor
    - TouchSensor

This is a lot, so I'm cutting most of them. Most don't make sense for a demo, anyways.
'''

from mistyPy.Robot import Robot
from mistyPy.Events import Events
import os
import time
import keyboard

################################################################################################
#                                       PROPRIOCEPTION                                         #
################################################################################################


def _ActuatorPosition(data):
    print("\n\nActuatorPosition\n", data)
    misty.Speak("Actuator Position data printed", speechRate=2)


def _DriveEncoders(data):
    print("\n\nDriveEncoders\n", data)
    misty.Speak("Drive Encoders data printed", speechRate=2)


def _IMU(data):
    print("\n\nIMU\n", data)
    misty.Speak("I M U data printed", speechRate=2)


def _LocomotionCommand(data):
    print("\n\nLocomotionCommand\n", data)
    misty.Speak("Locomotion Command data printed", speechRate=2)


def proprioception():
    '''
    Misty will verbally tell us when each of these are sent.
    I can't think of a better way to demo these.
    '''
    mode()
    misty.RegisterEvent("ActuatorPosition", Events.ActuatorPosition, condition=None,
                        debounce=10000, keep_alive=True, callback_function=_ActuatorPosition)

    time.sleep(2.5)

    misty.RegisterEvent("DriveEncoders", Events.DriveEncoders, condition=None,
                        debounce=10000, keep_alive=True, callback_function=_DriveEncoders)

    time.sleep(2.5)

    misty.RegisterEvent("IMU", Events.IMU, condition=None,
                        debounce=10000, keep_alive=True, callback_function=_IMU)

    time.sleep(2.5)

    misty.RegisterEvent("LocomotionCommand", Events.LocomotionCommand,
                        condition=None, keep_alive=True, callback_function=_LocomotionCommand)


################################################################################################
#                                         FACIAL                                               #
################################################################################################

def _FaceRecognition(data):
    print(data)
    if data["message"]["label"] is not ("unknown_person" or None):
        misty.Speak("Hello ", data["message"]["label"])


def facial():
    mode()
    misty.StartFaceRecognition()
    misty.RegisterEvent("FaceRecognition", Events.FaceRecognition, condition=None,
                        debounce=1000, keep_alive=True, callback_function=_FaceRecognition)


################################################################################################
#                                           TOF                                                #
################################################################################################

def _TimeOfFlight(data):
    print(data)
    # TODO: something interesting here?


def tof():
    '''
    The boring half of the visual capabilities.
    '''
    mode()
    misty.RegisterEvent("TimeOfFlight", Events.TimeOfFlight, condition=None,
                        debounce=1000, keep_alive=True, callback_function=_TimeOfFlight)


################################################################################################
#                                        TACTILE                                               #
################################################################################################

def _BumpSensor(data):
    name = data["sensorName"]
    type = data["message"]["isContacted"]
    print(name, type)
    name = name[:5]
    if type:
        misty.Speak("Bumped ", name)
    else:
        misty.Speak("Released ", name)


def _TouchSensor(data):
    name = data["sensorPosition"]
    type = data["message"]["isContacted"]
    print(name, type)
    if type:
        misty.Speak("Touched ", name)
    else:
        misty.Speak("Released ", name)


def tactile():
    '''
    Misty talks whenever she's touched. Fun!
    '''
    mode()
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
    mode()

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
    os.system('python3 /Users/skyeworster/Desktop/reset.py')
    print("program ended")


def mode():
    misty.UnregisterAllEvents()
    misty.StopFaceRecognition()
    misty.StopSpeaking()


if __name__ == "__main__":
    misty = Robot("131.229.41.135")

    # clean slate. should print "reset"
    os.system('python3 /Users/skyeworster/Desktop/reset.py')
    time.sleep(2)

    # ignore TOF sensors
    misty.UpdateHazardSettings(disableTimeOfFlights=True)

    keyboard.on_press_key("t", tactile())
    keyboard.on_press_key("p", proprioception())
    keyboard.on_press_key("f", facial())
    keyboard.on_press_key("o", tof())
    keyboard.on_press_key("a", audio())
    keyboard.on_press_key("e", end())
