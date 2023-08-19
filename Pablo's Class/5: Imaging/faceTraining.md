# Face Training Demo

##### Skye Weaver Worster '25J

This program trains Misty on the face in front of her. The person's name must be specified in `name` before the program begins.

We unregister all previous events, then register for `FaceTraining` so that we can get information on the face training process. We then tell Misty to `StartFaceTraining` on the given `name`.

In the `_FaceTraining` callback, we detect whether the face training process has ended. Once the training is successful, we unregister from the `FaceTraining` events and the program ends.