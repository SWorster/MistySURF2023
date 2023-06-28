'''
Skye Weaver Worster
Misty Tutorial 1
'''

# Import Robot module
from mistyPy.Robot import Robot

# Create a Robot object with Misty's IP address
# We can now send commands to the "misty" object, instead of having to deal with HTTP requests ourselves.
misty = Robot("131.229.41.135")  # takes IP address as a string in quotes

# Change Misty's LED to blue (RGB)
misty.ChangeLED(0, 0, 255)
