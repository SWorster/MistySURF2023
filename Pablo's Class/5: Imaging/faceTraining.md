# Face Training Demo

##### Skye Weaver Worster '25J

This program trains Misty on the face in front of her. The person's name must be specified in `name` before the program begins.

## The Code

We unregister all previous events, then register for `FaceTraining` so that we can get information on the face training process. We then tell Misty to `StartFaceTraining` on the given `name`.

In the `_FaceTraining` callback, we detect whether the face training process has ended. Once the training is successful, we unregister from the `FaceTraining` events and the program ends.

## How to Perform Face Training

Ensure the room is well-lit. Hold your face in front of Misty's cameras and begin the program. A blue light on the side of Misty's head will turn on when she begins face training. Keep your face still until the blue light disappears (at most 20 seconds).
