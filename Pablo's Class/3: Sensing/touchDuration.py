'''
Skye Weaver Worster

Misty waits to be touched, then counts how many times she's touched. She plays a different song clip for each number of touches.
'''

from mistyPy.Robot import Robot
from mistyPy.Events import Events
import time

misty = Robot("131.229.41.135")  # robot object with your IP
wait = 3  # number of seconds to wait after last touch

# volumes for audio clips
vol0 = 10
vol1 = 10
vol2 = 10
vol3 = 10

# ! Do not change this, it could break things!
touched = False  # whether Misty is being touched
count = 0  # number of times Misty is touched
t = time.time()  # time of last contact


def _BumpSensor(data):
    global t
    t = 0  # ends while loop in main
    misty.Stop()  # stop moving
    misty.UnregisterAllEvents()  # unregister all
    misty.ChangeLED(0, 0, 0)  # LED off
    misty.StopAudio()  # stop audio
    print("end of program")


def _TouchSensor(data):
    global touched

    if data["message"]["isContacted"] and not touched:  # if touched
        misty.ChangeLED(0, 255, 0)  # green
        global count
        count += 1  # increment global counter
        touched = True

    elif data["message"]["isContacted"] == False and touched:  # if not touched
        misty.ChangeLED(0, 0, 0)  # off
        global t
        t = time.time()  # record new starting time
        touched = False


if __name__ == "__main__":

    # register for touch sensor
    misty.RegisterEvent("TouchSensor", Events.TouchSensor, condition=None,
                        keep_alive=True, callback_function=_TouchSensor)

    # register for bump sensor
    misty.RegisterEvent("BumpSensor", Events.BumpSensor, condition=None,
                        keep_alive=True, callback_function=_BumpSensor)

    while True:  # infinite loop
        if time.time() > (t+wait):  # if time is x seconds more than last touch
            break
    if count == 1:
        print(f"Misty was touched {count} time!")
    else:
        print(f"Misty was touched {count} times!")

    # play a different song for each number of touches
    if count == 0:
        misty.PlayAudio("A_LacrimosaShort.m4a", volume=vol0)
        misty.ChangeLED(50, 0, 200)  # dark blue/purple
        time.sleep(12.5)
    elif count == 1:
        misty.PlayAudio("A_Mahler5opening.m4a", volume=vol1)
        misty.ChangeLED(200, 150, 0)  # yellow
        time.sleep(29)
    elif count == 2:
        misty.PlayAudio("A_CarelessWhisper.mp3", volume=vol2)
        misty.ChangeLED(255, 0, 50)  # purple
        time.sleep(14.3)
    elif count == 3:
        misty.PlayAudio("A_MiiChannel.mp3", volume=vol3)
        misty.ChangeLED(50, 200, 255)  # teal
        time.sleep(8.5)

    misty.ChangeLED(0, 0, 0)
    misty.StopAudio()
    misty.UnregisterAllEvents()  # unregister
