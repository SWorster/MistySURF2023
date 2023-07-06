'''
Skye Weaver Worster

Pablo's Instructions: Have the sequence of motions from the "Obj Interaction" Activity printed out and a graphical representation of the path visualized (forward 30cm; left 45 degrees; forward 55cm; right 15 degrees; etc). basically, run previous activity and record movement/position data, then display on top of provided map


Ignoring how this requires the previous program - I remember you don't want me to use mapping. The only other ways to record her movement are:
- DriveEncoders. Requires calculus (rate of movement, duration since last update).
- IMU. Unreliable measurements and intensive data-gathering. Doesn't record absolute position, so calculus required.
- logging exact movement instructions. Completely inaccurate, as intended and actual movement vary drastically.

This would be damn near impossible with any of these methods. Using mapping would at least make a solution plausible. A possible procedure would be:

- get map of known area
- find position in map
- move (either programmatic or from controller)
- at set interval, get current pose
- save pose to file with timestamp
- on movement completion, stop getting data
- load map of area
- for each timestamped entry, plot position

Alternatively, there is a built-in tracking functionality. It seems designed to work with some path-following and drive-to-location commands. Setting a path will return a list of waypoints Misty will hit. I'll need to confer with Julia to get more info about how this might work.
'''