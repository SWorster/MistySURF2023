# Vision Demos
##### Skye Weaver Worster '25J

## `visionFaces.py`

This code has Misty play a different audio clip for each face she sees. She has to already know the face, and the names have to be hard-coded into the program.

In the main function, we unregister from preexisting events and stop any running face recognition. We register for the bump sensor, which allows us to stop the program at any time. We get the list of faces Misty knows using the `GetKnownFaces()` command. We then start facial recognition, which has Misty start looking for faces, and register for face recognition events, which lets Misty tell us who she finds.

In the `_FaceRecognition()` callback, we get the name of the person Misty sees. If she doesn't know the person, she'll respond with `"unknown person"` or `None`, so we ignore those cases and keep looking. If she knows the person, we stop facial recognition and unregister from the event so that she only reacts once. We register for the `AudioPlayComplete` event, which sends us a message when Misty finishes playing an audio file. We then play a specific audio file for whichever person Misty saw. Once that file finishes, the `_AudioPlayComplete()` callback is triggered, which prints a message and ends the program.

## `visionObject.py`

This program has the same behavior as the last one, but with objects instead of faces. The objects have to be in Misty's list of known objects, and the responses for each object have to be hard-coded into the program.

We start in the main function, where we begin object detection and register for `ObjectDetection`, `AudioPlayComplete`, and `BumpSensor`. `BumpSensor` and `AudioPlayComplete` have the same functionality as in `visionFaces.py`. The object detection callback tells us what object Misty saw, and has a different response for each.