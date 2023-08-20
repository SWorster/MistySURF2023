'''
Skye Weaver Worster '25J

This code forcibly resets and clears everything from Misty.

It is STRONGLY RECOMMENDED to read the accompanying walkthrough before running this. There may be unintended consequences to using this code.
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

# Cancels and stops every process or skill
misty.DisableAudioService()
misty.DisableAvStreamingService()
misty.DisableCameraService()
misty.DisableSlamService()
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

# re-enables these
misty.EnableAudioService()
misty.EnableAvStreamingService()
misty.EnableCameraService()
misty.EnableSlamService()
