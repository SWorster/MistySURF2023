# import statements
from mistyPy.Robot import Robot
from mistyPy.Events import Events
from mistyPy.EventFilters import EventFilters

# callback for TOF
def tof_callback(data):
    global isDriving
    try:
        distance = data["message"]["distanceInMeters"]
        if (distance < 0.2 and isDriving):
            print("Misty is", distance, "meters from an obstacle")
            misty.ChangeLED(255, 0, 0)
            misty.PlayAudio("s_Joy2.wav", 10)
            misty.DriveTime(linearVelocity=0, angularVelocity=0, timeMs=2000)
            isDriving = False
            print("Stopped: Obstacle")
            misty.UnregisterAllEvents()
    except:
        pass

# callback for movement
def move_callback(data):
    global isDriving
    try:
        lvel = data["message"]["leftVelocity"]
        rvel = data["message"]["rightVelocity"]
        if (lvel+rvel > 0.01):
            isDriving = True
        if (lvel+rvel < 0.001 and isDriving):
            misty.ChangeLED(0, 255, 0)
            misty.PlayAudio("s_Joy4.wav", 1)
            print("Stopped: time limit reached")
            misty.UnregisterAllEvents()
    except:
        pass


if __name__ == "__main__":
    misty = Robot("MISTY-IP-ADDRESS-HERE")  # Robot object with your IP 
    print("Going on an adventure!")
    misty.ChangeLED(0, 0, 255)

    global isDriving
    isDriving = False

    try:
        # Subscribe to center TOF
        front_center = misty.RegisterEvent("CenterTimeOfFlight", Events.TimeOfFlight, condition=[EventFilters.TimeOfFlightPosition.FrontCenter], debounce=5, keep_alive=True, callback_function=tof_callback)

        # subscribe to locomotionCommand
        movement = misty.RegisterEvent(
            "DriveEncoders", Events.DriveEncoders, callback_function=move_callback, keep_alive=True)

        misty.DriveTime(
            linearVelocity=10, angularVelocity=0, timeMs=5000)

        # Use the keep_alive() function if you want to keep the main thread alive, otherwise the event threads will also get killed once processing has stopped
        misty.KeepAlive()

    except Exception as ex:
        print(ex)
