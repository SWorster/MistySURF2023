# Automation: Face Recognition and Tracking

##### By Skye Worster '25J

These two programs, `automationHalts.py` and `automationLoop.py`, demonstrate Misty's facial recognition abilities.

The bulk of this guide can be followed from either program; only the looping and halting behavior differs.

## Main

Let's start with the main function. We unregister all events first, to ensure that no processes are running from other programs. We then center the head and tilt it slightly up, so that Misty has a better view of the room.

Now we register for the events we'll need. `BumpSensor` is how we'll end the program. Take a look at the `_BumpSensor` callback. We unregister from all events and stop facial recognition, and also change `seen` to `True`. We'll talk about `seen` in more detail later on; it tracks whether Misty currently sees the person she's looking for. Changing it to `True` tricks the searching behavior/loop into thinking that we've seen a person, which stops Misty's head movement and/or ends the loop.

The next callback is `FaceRecognition`. We compare the name Misty sends us to the person we're looking for. If there's a match, we stop Misty's movements and unregister from `FaceRecognition`. However, we still need to use facial recognition to follow the person's face, right? We register for `FaceRecognition` again, but give it the callback function `_Follow`. This lets us treat all future `FaceRecognition` events with a different set of instructions.

Finally, we register for `ActuatorPosition`. This tells us Misty's current head position. However, we only want data for the pitch and yaw. We can make use of a feature of Misty's Python SDK called event filtering. We give `Events.ActuatorPosition` as the `event_type`, then give `EventFilters.ActuatorPosition.HeadYaw` or `EventFilters.ActuatorPosition.HeadPitch` as the `condition`. The callbacks for these events store the values for pitch and yaw in global variables so that they can be accessed by other callbacks when needed.

Now we need to transition to the searching behavior. We use the command `StartFaceRecognition` to do... exactly what it says on the tin. Misty will now start trying to find faces and send us data about them. If the target isn't seen immediately, we start moving right.

## Face Detection

In the `moveRight` function, we send Misty a command to move her head right. While she does this, we continually check her head yaw against a threshold. When she hits that value or sees her target, the `while` loop ends.

Because this `while` loop could have ended for two reasons, we now need to check that reason to see whether we should continue with the searching movement. If it stopped because Misty saw the target, we don't want to continue the searching behavior. Otherwise, we begin moving to the left.

`moveLeft` follows the same logic as its predecessor. In `automationLoop.py`, we return to `moveRight` if we don't see our target. This loop between right and left only ends if Misty sees the target or if a bump sensor is pressed. In `automationHalts.py`, we continue to `moveCenter` instead.

In `moveCenter`, we move Misty's head to the center and wait until Misty sees the target or hits the center. If she doesn't see the target, we call the `_BumpSensor` callback with a dummy argument (callbacks are functions too!). This ends the program.

If Misty sees the target at any point during this process, she stops what she's doing and begins tracking the target's face.

## Face Tracking: A Lesson in Uncertainty

Responses from the `FaceRecognition` event contain the location of the face in Misty's vision. `bearing` is the horizontal position, `elevation` is the vertical position, and `distance` is the distance as calculated from Misty's occipital (3D)cameras. We can use these values to turn Misty's head towards us.

The main issue with these values is the lack of units. `distance` is measured in centimeters, but `bearing` and `elevation` have no clear units. (0,0) is the center, and negative directions correspond to the top and right.

I gave Misty a window at the center of her vision where she won't move to center your face. Without this, she'll keep moving her head to center you if you're even the slightest bit off. I recommend 2 "units" as a good baseline. The size of this window scales a bit with distance. If you're within `t_dist` centimeters, Misty will try to center your face if you're more than `t_close` units from center. Otherwise, she'll only move if you get `t_far` units off.

Another issue is that there's no concrete way to translate the bearing/elevation distance to head position. If given a constant rate (say, move by 1 degree each time this callback runs), Misty will take a very long time to adjust. If this rate is too high (say, 5 degrees), she will overcompensate and miss the tolerance window. I decided that the most time-efficient way (for me) to fix this was to scale the rate with how far off-center the face is. Essentially, if the face is suddenly far from the center, it must be moving quickly; Misty's head should move quickly to keep up.

There's no exact science here, and the numbers are (almost) completely arbitrary. The only calculation I did was to ensure that none of these will produce a movement that sends her head to the other side of the tolerance window. The reader is encouraged to experiment with these values and find a better solution!

The movement duration (default .4 sec) has to be less than the debounce for facial recognition (default .5 sec). Misty needs time to complete each movement, or the movement commands will overlap and cause her to continually overshoot your face.