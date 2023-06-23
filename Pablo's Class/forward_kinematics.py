'''
Forward Kinematics

Misty follows a given set of instructions. Students figure out how she'll look at the end.

Here's a code with some sample instructions.

This code starts with a reset, because it helps to start from the same place every time. Of course, you'll need to move the robot back to its original position yourself, but this should cover the head and arms.

WARNING: This code has Misty ignore her Time of Flight sensors! She won't detect table edges, obstacles, etc. We've been having trouble with the TOFs, so I'll remove this once I find a fix.
'''

# TODO: should I give param names? Example: misty.ChangeLED(red=0, green=255, blue=0)

from mistyPy.Robot import Robot
import os
import time

misty = Robot("131.229.41.135")

# clean slate. should print "reset"
os.system('python3 /Users/skyeworster/Desktop/reset.py')
time.sleep(2)

# ignore TOF sensors
misty.UpdateHazardSettings(disableTimeOfFlights=True)

# start of instructions
misty.ChangeLED(0, 0, 255)  # LED turns blue
misty.PlayAudio("s_Joy2.wav", volume=10)  # play sound
time.sleep(1)

# movement 1: drive forward for 3 seconds at speed 30
misty.Drive(30, 0)  # send drive command
time.sleep(3)
misty.Stop()  # send stop command
time.sleep(2)

# movement 2: turn head to the left 45 degrees
misty.MoveHead(0, 0, 45, 90) # yaw=45, velocity=90
time.sleep(3)

# movement 3: move arms up
misty.MoveArms(0, 0)
time.sleep(3)

# end of instructions
misty.ChangeLED(0, 255, 0)  # LED turns green
misty.PlayAudio("s_Joy4.wav", volume=10)  # play sound


# reset hazard settings
misty.UpdateHazardSettings(revertToDefault=True)
