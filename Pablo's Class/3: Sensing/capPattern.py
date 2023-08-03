'''
Skye Weaver Worster '25J

Misty waits to be touched, then counts how many times she's touched. She plays a different song clip for each number of touches.
'''

from mistyPy.Robot import Robot
from mistyPy.Events import Events
import time

misty = Robot("131.229.41.135")  # robot object with your IP
wait = 3  # number of seconds to wait after last touch

# audio clips and volumes, LED colors
t0 = "LacrimosaShort.m4a"
vol0 = 10
c0 = [50, 0, 200]  # dark blue/purple
t1 = "Mahler5Short.m4a"

vol1 = 40
c1 = [200, 150, 0]  # yellow

t2 = "CarelessWhisperShort.m4a"
vol2 = 10
c2 = [255, 0, 50]  # purple

t3 = "MiiChannelShort.m4a"
vol3 = 10
c3 = [50, 200, 255]  # teal

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
    global touched, count, t

    if data["message"]["isContacted"] and not touched:  # if touched
        misty.ChangeLED(0, 255, 0)  # green
        count += 1  # increment global counter
        touched = True

    elif data["message"]["isContacted"] == False and touched:  # if not touched
        misty.ChangeLED(0, 0, 0)  # off
        t = time.time()  # record new starting time
        touched = False


def _AudioPlayComplete(data):  # when audio stops
    misty.ChangeLED(0, 0, 0)  # LED off
    misty.StopAudio()  # stop playing audio clips
    misty.UnregisterAllEvents()  # unregister


if __name__ == "__main__":
    misty.StopAudio()  # stops preexisting audio

    # register for touch sensor
    misty.RegisterEvent("TouchSensor", Events.TouchSensor,
                        keep_alive=True, callback_function=_TouchSensor)

    # register for bump sensor
    misty.RegisterEvent("BumpSensor", Events.BumpSensor,
                        keep_alive=True, callback_function=_BumpSensor)

    print("tap my head!")

    while True:  # infinite loop
        if time.time() > (t+wait):  # if time is x seconds more than last touch
            break

    misty.UnregisterEvent("TouchSensor")  # unregister from touch sensor

    if count == 1:
        print(f"Misty was touched {count} time!")
    else:
        print(f"Misty was touched {count} times!")

    # register for audio completion
    misty.RegisterEvent("AudioPlayComplete", Events.AudioPlayComplete,
                        keep_alive=True, callback_function=_AudioPlayComplete)

    match count:  # play a different song for each number of touches
        case 0:
            misty.PlayAudio(t0, vol0)
            misty.ChangeLED(c0[0], c0[1], c0[2])
        case 1:
            misty.PlayAudio(t1, vol1)
            misty.ChangeLED(c1[0], c1[1], c1[2])
        case 2:
            misty.PlayAudio(t2, vol2)
            misty.ChangeLED(c2[0], c2[1], c2[2])
        case 3:
            misty.PlayAudio(t3, vol3)
            misty.ChangeLED(c3[0], c3[1], c3[2])
