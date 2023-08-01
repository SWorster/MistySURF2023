# Bump Sensing Demos
##### Skye Weaver Worster '25J

## bumpDrive.py

In this program, Misty drives forward until something touches one of her bump sensors.

Although declaring a main function is often useful for longer programs, it isn't necessary. In this demo, we have a callback function for the bump sensor, but no proper main.

First, we tell Misty to ignore her TOF sensors to prevent overreaction. This means she won't stop at ledges, so be careful! We then tell her to drive forward indefinitely.

The callback stops Misty, checks that one of Misty's bump sensors has been triggered, and changes her LED depending on which sensor was contacted. It then plays a short audio clip, unregisters all events, and reverts the hazard settings.

## bumpWallFollow.py

