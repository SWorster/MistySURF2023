'''
This code forcibly resets and clears everything from Misty. It's very useful to provide a clean slate when debugging. It can also be used during other programs using the following:

import os
os.system('python3 <path-to-file>/reset.py')
'''

from mistyPy.Robot import Robot

print("reset")
misty = Robot("131.229.41.135")
misty.MoveHead(0, 0, 0)
misty.MoveArms(80, 80)

misty.UnregisterAllEvents()

misty.UpdateHazardSettings(revertToDefault=True)

misty.Stop()
misty.SetDisplaySettings(True)
misty.ChangeLED(0, 0, 0)

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
