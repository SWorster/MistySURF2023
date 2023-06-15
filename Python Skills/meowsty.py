'''
Misty is now Meowsty. No FUR-ther explanation provided.
(please laugh at the pun)

'''
from mistyPy.Robot import Robot
from mistyPy.Events import Events


def _BumpSensor(data):  # when bumped, program ends
    misty.UnregisterAllEvents()
    print("byeeeee")


def _CapTouch(message):
    '''
    cap touch sensors send event data when touched and released.
    we want some sounds (purrs) to play as long as they're being touched
    we want others to play when touched, then stop
    '''
    try:
        global lastPlace  # tracks last place Misty was touched

        # true if touch, false if release
        touched = message["message"]["isContacted"]
        partTouched = message["message"]["sensorPosition"]  # sensor source

        # print(touched, partTouched, lastPlace) # useful for debugging

        # if two parts touched at same time:
        if partTouched != lastPlace:
            misty.StopAudio()  # stop audio
            lastPlace = ""  # ignore older event, proceed with new touch

        # if first time touching a place
        if lastPlace == "":
            lastPlace = partTouched

            if partTouched == "Chin" and touched:
                misty.PlayAudio("A_purr1.mp3", 10)
                misty.TransitionLED(0, 0, 0, 255, 100, 255,
                                    "TransitOnce", 2000)
                print("chin scritches <3")

            elif partTouched == "HeadLeft" and touched:
                misty.PlayAudio("A_meow1.mp3", 5)
                print("left scritches")

            elif partTouched == "HeadRight" and touched:
                misty.PlayAudio("A_meow2.mp3", 5)
                print("right scritches")

            elif partTouched == "HeadBack" and touched:
                misty.PlayAudio("A_meow3.mp3", 5)
                print("back scritches")

            elif partTouched == "HeadFront" and touched:
                misty.PlayAudio("A_purr2.mp3", 10)
                print("front scritches")

            elif partTouched == "Scruff" and touched:
                misty.PlayAudio("A_hiss.mp3", 2)
                print("HISS")

        # if a place has already been touched:
        else:
            # purring: have to manually stop audio when stop touching
            # single-sound places: sound will stop automatically on completion

            if lastPlace == "Chin":
                # if we stop touching the chin
                if touched == False and partTouched == "Chin":
                    misty.StopAudio()  # stop audio
                    misty.TransitionLED(255, 100, 255, 0, 0,
                                        0, "TransitOnce", 2000)
                    lastPlace = ""

            if lastPlace == "HeadLeft":
                # if we stop touching HL
                if touched == False and partTouched == "HeadLeft":
                    lastPlace = ""

            if lastPlace == "HeadRight":
                if touched == False and partTouched == "HeadRight":
                    lastPlace = ""

            if lastPlace == "HeadBack":
                if touched == False and partTouched == "HeadBack":
                    lastPlace = ""

            if lastPlace == "HeadFront":
                if touched == False and partTouched == "HeadFront":
                    misty.StopAudio()  # stop audio
                    lastPlace = ""

            if lastPlace == "Scruff":
                if touched == False and partTouched == "Scruff":
                    lastPlace = ""

    except Exception as e:
        print("EXCEPTION:", e)


if __name__ == "__main__":
    misty = Robot("131.229.41.135")

    global lastPlace  # tracks the last place Misty was touched
    lastPlace = ""

    try:
        # register for captouch, keep event alive
        misty.RegisterEvent(event_name="scratches", event_type=Events.TouchSensor,
                            callback_function=_CapTouch, keep_alive=True)

        # register for bumps to stop program
        misty.RegisterEvent(event_name="stop", event_type=Events.BumpSensor,
                            callback_function=_BumpSensor, keep_alive=True)

        misty.KeepAlive()

    except Exception as ex:
        print(ex)
