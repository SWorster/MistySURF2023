# IMU Demo
##### Skye Weaver Worster '25J

This program has Misty's LED turn different colors depending on her pitch and roll.

I typically use the bump sensors to end programs early, but it's so easy to hit them when manipulating Misty that I went with the head touch sensors instead. The `_TouchSensor()` callback simply ends the program by unregistering from all events.

The `_IMU()` callback gets Misty's current pitch and roll. These measurements can range from -360 to 360, and there are a few degrees of inaccuracy. This means that an actual roll of 0 could be sent as -360 to -355, from -5 to 5, and from 355 to 360. The easiest way to fix this is to add 360 to values less than -180 and subtract 360 from values over 180. This creates a -180 to 180 range with 0 as neutral. Our hypothetical roll of 0 can now only be a value from -5 to 5, which is much more realistic and easy to deal with.

We then compare the pitch and roll to a tolerance value `t` we've set. If `t` is too low, Misty will overreact to the slightest movement. A value of 3 to 5 seems to work quite well. Misty's LED changes color for each direction she is tilted.