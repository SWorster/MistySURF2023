# Bump Sensing Demos
##### Skye Weaver Worster '25J

## `bumpDrive.py`

In this program, Misty drives forward until something touches one of her bump sensors.

Although declaring a main function is often useful for longer programs, it isn't necessary. In this demo, we have a callback function for the bump sensor, followed by the rest of the code.

First, we tell Misty to ignore her TOF sensors to prevent overreaction. This means she won't stop at ledges, so be careful! We then tell her to drive forward indefinitely.

The callback stops Misty, checks that one of Misty's bump sensors has been triggered, and changes her LED depending on which sensor was contacted. It then plays a short audio clip, unregisters all events, and reverts the hazard settings.

## `bumpWallFollow.py`

This program uses Misty's bump sensors to have her follow a wall. After the callbacks, we disable the hazard settings to ignore the TOF sensors, then register for the bump sensors and drive encoders. We then start driving forward slowly.

Let's move up to the `_BumpSensor()` callback. When Misty is bumped, she stops and checks whether another bumper is also hit. If it is, the program ends. Otherwise, we track the bumper we just hit in `current`. Depending on which bumper is hit, the LED changes to a different color and Misty drives away from the point of contact for a certain time. For example, hitting the front right bumper has Misty back up while turning right.

When a bumper is released, we check whether it matches the `current` bumper. If it's a match, we set `current` to `None`.

We've now defined how Misty reacts when hit, but we also need to tell her what to do once she's moved back and then get her to drive forward again. This behavior is in the `_DriveEncoders` callback. Unlike `_BumpSensor()`, which is called when the event occurs, the `_DriveEncoders` callback is triggered at regular intervals.

If Misty is bumped, we switch to `backup` mode. In this mode, we find the combined velocity of the left and right treads and use this value to determine whether Misty has moved backwards. If Misty is moving but hasn't been flagged as `driving` yet, we flag her as `driving`. If she's stopped but hasn't driven yet, we still need to wait for her to start moving. If she's stopped after having driven, we know she's completed the backing-up movement and can start moving forwards again. This behavior prevents us from accidentally telling Misty to move forward when she hasn't moved backwards yet.