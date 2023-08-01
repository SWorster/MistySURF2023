'''
Skye Weaver Worster

Misty drives until bumped (stop and change light depending on bumper touched). She does not resume moving after contact.

WARNING: this code disables Misty's TOF sensors, so she won't automatically stop at table edges and other drops. They are only re-enabled if the program is terminated via the bump sensors. Be careful!
'''

from mistyPy.Robot import Robot

misty = Robot("131.229.41.135")  # robot with your IP

print(misty.UpdateHazardSettings(disableTimeOfFlights=True))


