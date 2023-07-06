'''
Skye Weaver Worster

WORK IN PROGRESS OBVIOUSLY

Pablo's Instructions: 1) turn in place until seeing object A; 2) keep turning until seeing object B), then return half the rotation (from A to B) and then advance until passing "through" the two objects. The idea is that, if we place two objects a couple feet apart, Misty should be able to pass "through" them.
'''


from mistyPy.Robot import Robot
from mistyPy.Events import Events

misty = Robot("131.229.41.135")  # robot with your IP
volume = 3  # volume for audio
lin_vel = 10  # linear velocity
ang_vel = 0  # angular velocity
OD_debounce = 1000  # object detection debounce in ms
min_confidence = .2 # minimum confidence required to send report

# ! Do not change these!
yaw1=None
yaw2=None
yaw=None
avg=0

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

    if yaw1==None and object == "bottle":
        left = data["message"]["imageLocationLeft"]
        right = data["message"]["imageLocationRight"]
        
        global avg
        avg = (right+left)/2
    elif object == "backpack":
        left = data["message"]["imageLocationLeft"]
        right = data["message"]["imageLocationRight"]
        
        global avg
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

    misty.RegisterEvent("Yaw", Events.IMU, debounce = 10, keep_alive=True, callback_function=_yaw)
    # misty.Drive(lin_vel, ang_vel)
    
    
    
    # bottle to Misty's left
    misty.Drive(0,-10) # turn left
    while not (140<avg<180): # turn until bottle in range
        pass
    
    misty.Stop() # stop moving

    yaw1 = yaw # record and print yaw1
    print(yaw1)
    
    # backpack to Misty's right
    misty.Drive(0,10) # turn right
    while not (140<avg<180): # turn until backpack in range
        pass
    
    misty.Stop() # stop moving

    yaw2 = yaw # record yaw
    print(yaw2)
    
    misty.UnregisterAllEvents()
    misty.StopObjectDetector()
    

    