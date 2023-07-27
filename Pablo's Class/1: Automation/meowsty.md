# Meowsty
##### By Skye Worster '25J

This program has Misty act like a cat.

We begin by registering for two events: the bump sensors, and the capacitive touch sensors.

The bump sensor callback is used to end the program. It unregisters from all events and turns off the LED and sound.

The capacitative touch sensors send two relevant pieces of information. The first is the location that was touched. We can use a series of `if-else` statements to produce different behaviors for each location. The second is whether the touch is beginning or ending. We don't want to start behavior when we stop touching Misty, so we'll need to handle touches and releases differently.

One critical design choice we made in this program was to only run the behavior for the most recent part touched. We store the name of the most recent contact in `last_place`.

When Misty senses a new contact, she checks whether this contact is also `last_place`. If it isn't, we stop any behaviors left over from the older place using `StopAudio` and `ChangeLED`. We also clear `last_place` because we've moved on to a new location.

Next, we check whether `last_place` is empty. The only case when it isn't empty is when it matches the name of the place we just touched. This means that we're only handling first touches. We record the name of this location in `last_place` and use `if` statements to give Misty different behaviors.

Most of these behaviors are just a short audio clip and a console message, but there are two exceptions. `HeadFront` and `Chin` will play a long audio clip, and `Chin` will turn on Misty's LED. These behaviors will end either in the `else` section below, or in the first `last_place` check above.

The `else` part of the large conditional handles cases where `last_place` has a value of some sort. This could mean that we've stopped touching an old place or that we've stopped touching the most recent place. If we've stopped touching an old place, we don't want to do anything - this was already handled in the `last_place` check above. If we've stopped touching the current place, we clear `last_place`, and stop the audio and LED if needed.