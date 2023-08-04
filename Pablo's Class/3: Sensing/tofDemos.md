# Time of Flight Demos
##### Skye Weaver Worster '25J

## `tofWindow.py`

This program has Misty drive forward until she detects an object at a certain distance. This distance is determined by taking the average of the last several measurements, which limits the effect of inaccurate sensor readings.

This is a modified version of the second Python tutorial. This explanation assumes the reader is familiar with the basic concepts in that tutorial.

In the main function, we unregister from previous events and turn off hazard behaviors. We subscribe to the center TOF sensor and the `DriveEncoders` event. Note that the TOF registration uses `EventFilters` to only receive data from a single sensor. Misty then drives forward for a specified time.

In the `_TimeOfFlight()` callback, we get the distance in meters and the measurement status from the data. The status field will be 0 if the measurement is valid, so we can replace that value with a distance that won't affect the average too much.

We append the distance measurement to a list, deleting the oldest measurement if the list is too long. We then take the average of the distances in the list. If Misty is driving and the average is too close to an obstacle, Misty stops moving and the program ends.

The `_DriveEncoders()` callback ensures the program ends after Misty's drive command ends. If the sum of the tread velocities is greater than some value, we track that Misty is driving. If Misty has started driving but is below that speed, we know the `DriveTime()` command has elapsed. We end the program by unregistering from all events.

## `tofEvasion.py`

This code has Misty drive forward and evade obstacles. If an object is in front of her, she can turn to evade it. If it's too close, she can turn and reverse. She also detects objects behind her so she can decide whether to back up or turn in place.

In the main function, we unregister from any preexisting events and ignore the TOF hazard behavior. We then register for the three forward and one rear TOF events. If we registered for all the TOF sensors in a single event, Misty simply sends whichever sensor she most recently got data from. To counteract this, we create four separate events and have Misty give us data on all of them.

We also register for the bump sensor, which terminates the program by stopping Misty and unregistering from all events.

In order to have Misty decide how to avoid obstacles, she needs to know where those obstacles are. We don't want her to back up if there's something behind her, so the `_Back()` callback handles rear TOF sensor data. If we get a valid reading that there's an obstacle close behind Misty, we change the global variable `back` to `True`. We also call the `move()` function, which we'll get to in a minute.

The `_TOF()` callback handles all three of the forward-facing TOF sensors. This makes things simpler than having three separate functions with the same process. We get the distance measurement, validity status, and sensor ID from the data. If the distance measurement is valid and shows an object very close to Misty, we record that all three sensors are detecting an object. This induces a "panic" behavior in `move()` later.

If there's no emergency, we figure out which sensor we're dealing with and change the corresponding element in the `sensors` array. If an object is detected within a certain range, we record `True` for that sensor. If we don't see an object, or if the reading is invalid, we record `False`. 

The `move()` function is called every time we get a sensor reading from Misty. If the TOF debounce is 10 ms, that means `move()` is being called about every 2.5 ms. If we send Misty move commands that frequently, they can overload her system and cause unpredictable and dangerous behavior. To counteract this, we only send a move command every `num_readings` calls.

When we reach `num_readings`, we make a decision based on the data we have. First, we get the sum of the elements in `sensors`. Because Python treats `True` as 1 and `False` as 0, this tells us how many sensors are detecting an obstacle. If there are no obstacles in front of Misty, we tell her to move forward. If only the left or right sensors detect an obstacle, we turn the opposite way while still moving forward. If only the center detects an obstacle, we turn right by default.

If two sensors detect an obstacle, Misty needs to take greater evasive action. Instead of turning while moving forward, she will either turn in place or turn while moving backward (if the back is clear).

If all three sensors detect an obstacle, we're in panic mode. This could happen naturally or as a result of an object very close to Misty. Misty either turns in place or turns while moving backwards.

Note that this program uses only the most recent TOF reading for each sensor, instead of taking the average like in `tofWindow.py`. The implementation of this functionality is left as an exercise for the reader.