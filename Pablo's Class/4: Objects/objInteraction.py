'''
Skye Weaver Worster

WORK IN PROGRESS OBVIOUSLY

Pablo's Instructions: 1) turn in place until seeing object A; 2) keep turning until seeing object B), then return half the rotation (from A to B) and then advance until passing "through" the two objects. The idea is that, if we place two objects a couple feet apart, Misty should be able to pass "through" them.
'''


from mistyPy.Robot import Robot
from mistyPy.Events import Events
import time

misty = Robot("131.229.41.135")  # robot with your IP
volume = 3  # volume for audio
ang_vel = 0  # angular velocity for searching turn
OD_debounce = 1000  # object detection debounce in ms
min_confidence = .5  # minimum confidence required to send report
obj1 = "bottle"  # object to the left
obj2 = "backpack"  # object to the right
tol = 10  # tolerance for movement, in degrees
d_dist = 2  # driving distance, in meters
d_time = 10  # time to drive forward, in seconds

# ! Do not change these!
yaw1 = None
yaw2 = None
yaw = None
avg = 0


def _BumpSensor(data):
    misty.Stop()  # stop moving
    misty.StopObjectDetector()  # stop detecting objects
    misty.UnregisterAllEvents()  # unregister all
    misty.ChangeLED(0, 0, 0)  # LED off
    misty.StopAudio()  # stop audio
    misty.UpdateHazardSettings(revertToDefault=True)  # reset TOFs
    print("end of program")


def _yaw(data):
    global yaw
    yaw = data["message"]["yaw"]  # get yaw


def _ObjectDetection(data):
    object = data["message"]["description"]
    print(object)  # print what Misty sees

    global obj1, obj2, avg

    if yaw1 == None and object == obj1:
        left = data["message"]["imageLocationLeft"]
        right = data["message"]["imageLocationRight"]

        avg = (right+left)/2

    elif object == obj2:
        left = data["message"]["imageLocationLeft"]
        right = data["message"]["imageLocationRight"]

        avg = (right+left)/2


if __name__ == "__main__":

    # ignore TOF sensors
    misty.UpdateHazardSettings(disableTimeOfFlights=True)

    # register for bump sensor
    misty.RegisterEvent("BumpSensor", Events.BumpSensor,
                        keep_alive=True, callback_function=_BumpSensor)

    misty.StartObjectDetector(min_confidence, 0, 5)  # start detection

    # register for object detection
    misty.RegisterEvent("ObjectDetection", Events.ObjectDetection,
                        debounce=OD_debounce, keep_alive=True, callback_function=_ObjectDetection)

    misty.RegisterEvent("Yaw", Events.IMU, debounce=10,
                        keep_alive=True, callback_function=_yaw)

    # obj1 to Misty's left
    misty.Drive(0, -ang_vel)  # turn left
    while not (140 < avg < 180):  # turn until obj1 in range
        pass

    misty.Stop()  # stop moving

    yaw1 = yaw  # record and print yaw1
    print(yaw1)

    # obj2 to Misty's right
    misty.Drive(0, ang_vel)  # turn right
    while not (140 < avg < 180):  # turn until obj2 in range
        pass

    misty.Stop()  # stop moving

    yaw2 = yaw  # record yaw
    print(yaw2)
    
    # stop OD and unregister events
    misty.StopObjectDetector()
    misty.UnregisterEvent("ObjectDetection")
    misty.UnregisterEvent("IMU")

    # convert yaw values to range 0-360
    yaw1 = yaw1 % 360
    yaw2 = yaw2 % 360

    # if y1 and y2 in "normal" range
    if yaw2 > yaw1:
        middle = (yaw1+yaw2)/2

    # if y2 smaller than y1 (straddling 0-360 line)
    elif yaw1 > yaw2:
        # average anyway, then flip across circle, then convert to range 0-360
        middle = (180 - (yaw1+yaw2)/2) % 360
    
    else:
        middle = yaw1 # if something goes wrong, drive towards obj1

    misty.DriveHeading(middle, d_dist, d_time*1000)

    time.sleep(d_time) # wait until drive done
    _BumpSensor(1)
