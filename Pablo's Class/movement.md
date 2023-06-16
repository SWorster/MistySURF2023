# Movement Commands

Adapted from the documentation found [here](https://docs.mistyrobotics.com/misty-ii/web-api/api-reference/#movement).

Unless otherwise specified, these commands return `True` if there are no errors. If you need more info here on error/response parsing, let me know and I'll write a whole tutorial on it.

### Drive

```python
Drive(linearVelocity, angularVelocity)
```

`linearVelocity`: from -100 to 100 (full backwards to full forwards)

`angularVelocity`: from -100 to 100 (full clockwise to full counterclockwise)


### DriveTime

```python
DriveTime(linearVelocity, angularVelocity, timeMs, degree)
```

`linearVelocity`: from -100 to 100 (full backwards to full forwards)

`angularVelocity`: from -100 to 100 (full clockwise to full counterclockwise)

`timeMs`: duration in milliseconds

`degree`: number of degrees to turn

### DriveTrack

```python
DriveTrack(leftTrackSpeed, rightTrackSpeed)
```

`leftTrackSpeed`: speed of left track, from -100 to 100

`rightTrackSpeed`: speed of right track, from -100 to 100


### Halt

```python
Halt()
```

Stops treads, arms, and head. Compare to `Stop()`, which only stops the treads.

No return value.

### Stop

```python
Stop(hold)
```

`hold`: optional, default `False`. If `True`, Misty will resist being moved. __For our purposes, never provide a parameter for__ `Stop()`__.__

### MoveArm

```python
MoveArm(arm, position, velocity, units)
```

`arm`: which arm to move. Can be `"left"`,  `"right"`, or  `"both"`.

`position`: position to move arm to. 0 = straight forward, 90 = straight down, -29 = max upward.

`velocity`: speed from 0 to 100

`units`: optional, can be `"position"` (default),  `"degrees"`, or  `"radians"`.


### MoveArms

```python
MoveArms(leftArmPosition, rightArmPosition, leftArmVelocity, rightArmVelocity, units)
```

`leftArmPosition` and `rightArmPosition`: position to move arm to. 0 = straight forward, 90 = straight down, -29 = max upward.


`leftArmVelocity` and `rightArmVelocity`: speed from 0 to 100

`units`: optional, can be `"position"` (default),  `"degrees"`, or  `"radians"`.


### MoveHead

```python
MoveHead(pitch, roll, yaw, velocity, duration, units)
```

`pitch`: up/down position, from -40 (up) to 26 (down)

`roll`: left/right tilt, from -40 (left) to 40 (right)

`yaw`: left/right tilt, from -81 (right) to 81 (left)

`velocity`: optional, default 10

`duration`: optional, time in seconds

`units`: optional, can be `"degrees"` (default),  `"position"`, or  `"radians"`.

__Note:__ you must pass exactly one of `velocity` or `duration`, not both or neither.

# ALPHA, DO NOT USE

### DriveArc

```python
DriveArc(heading, radius, timeMs, reverse)
```

`heading`: absolute heading Misty will be at when arc is complete. 0 and 360 are straight, 90 is left, 180 and -180 are behind, 270 and -90 are right

`radius`: radius of arc in meters

`timeMs`: duration in milliseconds

`reverse`: optional boolean, `False` by default. If `True`, Misty drives in reverse

__Note:__ Misty's current heading is  `yaw` from the IMU.

### DriveHeading

```python
DriveHeading(heading, distance, timeMs, reverse)
```

`heading`: absolute heading Misty should maintain. 0 and 360 are straight, 90 is left, 180 and -180 are behind, 270 and -90 are right

`distance`: distance to drive

`timeMs`: duration in milliseconds

`reverse`: optional boolean, `False` by default. If `True`, Misty drives in reverse

__Note:__ This is only useful to make small corrections (> 2 degrees) to get very precise headings.
