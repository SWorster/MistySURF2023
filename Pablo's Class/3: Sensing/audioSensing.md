# Audio Sensing Demo

##### By Skye Weaver Worster '25J

This program uses Misty's audio localization to determine and move towards the source of the loudest sound.

First, we update the TOF hazards so that Misty won't jump at shadows. Unfortunately, this means she also won't stop at ledges, so be very careful when running this program.

We register for the bump sensor, which allows us to stop the program. The `_BumpSensor` callback stops Misty's movements, stops recording audio, unregisters from events, and resets the hazard settings.

We then start recording audio into a file. When Misty starts recording audio, she turns her fans off to limit the impact they have on her hearing. We wait a second for the fans to stop, then register for the `SourceTrackDataMessage` event. This events sends us the volume of sound Misty detects from each of 360 degrees. In the `_SourceTrackDataMessage` callback, we access an array of these values and get the average volume for each of four sectors. We determine which sector is the loudest and compare its average volume to a trigger value. This will prevent Misty from reacting to ambient noise. She then drives towards this direction.