'''
Skye Weaver Worster

This code forcibly resets and clears everything from Misty. It's very useful to provide a clean slate when debugging. It can also be used during other programs using the following:

import os
os.system('python3 <path-to-file>/reset.py')

I would strongly encourage alternate methods of resetting Misty, like unregistering in your code or using the Misty Studio reset option in Settings. This should only be used to quickly transition out of a program that isn't stopping properly. It shouldn't be used to set Misty's preconditions before running a program, or to gracefully end a running program.
'''

from mistyPy.Robot import Robot  # import robot class

print("reset")  # print to console
misty = Robot("131.229.41.135")  # Misty robot with your IP
misty.MoveHead(0, 0, 0)  # head to neutral
misty.MoveArms(80, 80)  # arms down to neutral
misty.UnregisterAllEvents()  # unregister events
misty.UpdateHazardSettings(revertToDefault=True)  # reset hazards
misty.Stop()  # stop moving treads
misty.SetDisplaySettings(True)  # reset display
misty.ChangeLED(0, 0, 0)  # LED off

# I'm not commenting all of these. Documentation exists for a reason.
misty.CancelSkill()
misty.CancelFaceTraining()
misty.StopArTagDetector()
misty.StopArTagDetector()
misty.StopAudio()
misty.StopAvStreaming()
misty.StopCascadeClassifier()
misty.StopFaceDetection()
misty.StopFaceRecognition()
misty.StopKeyPhraseRecognition()
misty.StopLocatingDockingStation()
misty.StopMapping()
misty.StopObjectDetector()
misty.StopObstacleDetection()
misty.StopPoseEstimation()
misty.StopQrTagDetector()
misty.StopSlamStreaming()
misty.StopSpeaking()
misty.StopSpeakingAzure()
misty.StopRecordingAudio()
misty.StopTracking()
misty.StopWifiHotspot()
