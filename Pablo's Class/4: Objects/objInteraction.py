'''
Skye Weaver Worster

Pablo's Instructions: Have Misty turn around until three specific objects are seen, then she should move to "bump" into them in a specific sequence. ex: she recognizes a ball and a chair, so she bumps the ball towards the chair

I guess my problem with this one is that Misty can see where objects are in her field of vision, but doesn't know where they are spatially. She can see a ball and a chair, but can't calculate where they are in space, much less how to move one towards the other.

ObjectDetection returns the following:
    "confidence": 0.8139669,
    "created": "2021-12-01T19:58:55.7851953Z",
    "description": "tv",
    "id": 0,
    "imageLocationBottom": 280.026581,
    "imageLocationLeft": 0.497694016,
    "imageLocationRight": 165.202759,
    "imageLocationTop": 147.299713,
    "labelId": 72,
    "pitch": 0.202373847,
    "sensorId": "cv",
    "yaw": -0.217731148

Not sure what pitch/yaw refer to; could be Misty's p/y when she takes an image to analyse. That would make the imageLocation fields the bounds of the object in question, but I'm not sure what the units for those values are. Degrees, maybe?

I suppose we could use imageLocation to get the approximate location of the object. I could then move Misty's head towards it, following it over time? I already have some functional (albeit janky) head-following behavior from the automotion demos. I could also have Misty follow the object physically. Either of these would be much more reliable than solving a complex spatial mapping problem without AR tags.

Alternatively, I could figure out how AR tags work. This would make the spatial relations so much easier (or just possible at all). It would look something like:
- find a ball
- find an AR tag on that ball
- get absolute position of ball
- find a chair
- find an AR tag on that chair
- get absolute position of chair
- do math to find trajectory of ball to chair
- calculate pose to start at
- drive to pose
- recalculate to ensure alignment
- move forward at rate for time
- done
'''