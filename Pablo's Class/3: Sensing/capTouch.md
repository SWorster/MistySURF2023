# Capacitive Touch Demos
##### Skye Weaver Worster '25J

## capDrive.py

This program has Misty move when her head is touched. It disables TOF hazards, so Misty will not detect or avoid ledges. Be careful!

The bump sensor callback is used to end the program. It unregisters the events, stops Misty, stops audio, and resets the hazard settings.

The touch sensor callback determines whether Misty is being touched or released. If touched, Misty will start moving forward. If released, she stops.

A possible extension of this program would be to deal with multiple touch locations. For example, touching two places on her head and releasing one of them currently stops Misty, despite still being touched. How would we prevent this behavior?

## capPattern.py

This program has Misty count how many times she's touched, then performs a different behavior for each number.

In the main section, Misty registers for the touch and bump sensors. The bump callback is used to stop the program, and is useful for debugging but not necessary for normal operation. This callback also changes `t = 0`, which ends a `while` loop in the main section (more on that later).

The touch sensor is what does the counting for us. If Misty hasn't been touched and detects a new touch, we increment the `count` of touches she's felt and track that she's currently being `touched`. If she's being released from a touch, we set the time of last contact `t` to the current time.

In the main function, we enter an infinite `while` loop that breaks when the current time is `wait` seconds greater than the time of last contact `t`. Because the touch callback sets `t` to the current time whenever Misty is released, We essentially have a `wait`-second window to touch Misty again before she moves on.

After recording all the touches, we register for the `AudioPlayComplete` event, which sends a message when Misty finishes playing an audio clip. She plays a different clip for each number of touches, so this allows us to continue in the program without specifying a certain number of seconds to wait for. The `_AudioPlayComplete()` callback simply turns off the LED and unregisters all events, ending the program.