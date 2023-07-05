'''
Skye Weaver Worster

Forward Kinematics

Misty follows a given set of instructions. Students figure out how she'll look at the end. This is an example of the sort of code we can use to give Misty instructions.

This code starts with a reset, because it helps to start from the same place every time. Of course, you'll need to move the robot back to its original position yourself, but this should cover the head and arms.

WARNING: This code has Misty ignore her Time of Flight sensors! She won't detect table edges, obstacles, etc. This resets when the code finishes, but be prepared to stop Misty while she's driving.
'''

from mistyPy.Robot import Robot
import time

misty = Robot("131.229.41.135")  # robot object with your IP
volume = 5  # audio volume

# drive command
drive_l = 30  # linear velocity
drive_a = 0  # angular velocity
drive_t = 3  # time

# head command
pitch = 0
roll = 0
yaw = 45
head_v = 90  # velocity of head movement

# arm command
left = 20  # left arm position
right = -30  # right arm position
arm_v = 90  # velocity of arm movement


misty.MoveArms(90, 90, 80, 80)  # arms straight down
misty.MoveHead(0, 0, 0)  # head to neutral

# ignore TOF sensors
misty.UpdateHazardSettings(disableTimeOfFlights=True)

# start of instructions
misty.ChangeLED(0, 0, 255)  # LED turns blue
misty.PlayAudio("s_Joy2.wav", volume=volume)  # play sound
time.sleep(1)

# movement 1: drive forward for 3 seconds at speed 30
misty.Drive(drive_l, drive_a)  # send drive command
time.sleep(drive_t)  # wait
misty.Stop()  # send stop command
time.sleep(2)

# movement 2: turn head to the left 45 degrees
misty.MoveHead(pitch, roll, yaw, head_v)  # move head
time.sleep(3)

# movement 3: move arms up
misty.MoveArms(left, right, arm_v, arm_v)  # arm movement
time.sleep(3)

# end of instructions
misty.ChangeLED(0, 255, 0)  # LED turns green
misty.PlayAudio("s_Joy4.wav", volume=volume)  # play sound

# reset hazard settings
misty.UpdateHazardSettings(revertToDefault=True)
print("done")
