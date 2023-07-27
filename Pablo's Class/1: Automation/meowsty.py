'''
Julia Yu and Skye Weaver Worster

Misty is now Meowsty. No FUR-ther explanation provided. (please laugh at the pun)

Audio files are in Other Resources > For Fun > MistyMedia > Misty Sounds > cat. You can also download them by running the mediaSync file.
'''

# import statements
from mistyPy.Robot import Robot
from mistyPy.Events import Events

misty = Robot("131.229.41.135")  # Misty robot with your IP
last_place = ""  # last place Misty was touched (starts empty)

# audio volumes
purr1 = 5
purr2 = 5
meow1 = 1
meow2 = 1
meow3 = 1
hiss = 1


def _BumpSensor(data):  # when bumped, program ends
    misty.UnregisterAllEvents()  # unregister all events
    misty.ChangeLED(0, 0, 0)  # turn off LED
    misty.StopAudio()  # stop audio
    print("byeeeee")


def _CapTouch(message):
    '''
    Cap touch sensors send event data when touched and released. We want some sounds (purrs) to play as long as they're being touched. We want others to play when touched, then stop.
    '''
    try:  # catch irrelevant/malformed data
        global last_place  # tracks last place Misty was touched

        # true if touch, false if release
        touched = message["message"]["isContacted"]
        part_touched = message["message"]["sensorPosition"]  # sensor source

        if part_touched != last_place:  # if two parts touched at same time
            misty.StopAudio()  # stop audio
            misty.ChangeLED(0, 0, 0)  # turn off LED
            last_place = ""  # ignore older event, proceed with new touch

        if last_place == "":  # if first time touching a place
            last_place = part_touched  # record what part we've touched

            # if-else statements on part_touched
            if part_touched == "Chin" and touched:
                misty.PlayAudio("purr1.mp3", purr1)
                misty.TransitionLED(0, 0, 0, 255, 100, 255,
                                    "TransitOnce", 2000)
                print("chin scritches <3")

            elif part_touched == "HeadLeft" and touched:
                misty.PlayAudio("meow1.mp3", meow1)
                print("left scritches")

            elif part_touched == "HeadRight" and touched:
                misty.PlayAudio("meow2.mp3", meow2)
                print("right scritches")

            elif part_touched == "HeadBack" and touched:
                misty.PlayAudio("meow3.mp3", meow3)
                print("back scritches")

            elif part_touched == "HeadFront" and touched:
                misty.PlayAudio("purr2.mp3", purr2)
                print("front scritches")

            elif part_touched == "Scruff" and touched:
                misty.PlayAudio("hiss.mp3", hiss)
                print("HISS")

        else:  # if a place has already been touched:
            # purring: have to manually stop audio when stop touching
            # single-sound places: sound will stop automatically on completion

            if last_place == part_touched == "Chin":  # if we stop touching the chin
                misty.StopAudio()  # stop audio
                # transition between pink and off over 2 seconds, repeatedly
                misty.TransitionLED(255, 100, 255, 0, 0,
                                    0, "TransitOnce", 2000)
                last_place = ""  # clear last place touched

            if last_place == part_touched == "HeadLeft":  # if we stop touching HL
                last_place = ""

            if last_place == part_touched == "HeadRight":
                last_place = ""

            if last_place == part_touched == "HeadBack":
                last_place = ""

            if last_place == part_touched == "HeadFront":
                misty.StopAudio()  # stop audio
                last_place = ""

            if last_place == part_touched == "Scruff":
                last_place = ""

    except Exception as e:
        print("EXCEPTION:", e)


if __name__ == "__main__":
    # register for cap touch, keep event alive
    misty.RegisterEvent(event_name="scratches", event_type=Events.TouchSensor,
                        keep_alive=True, callback_function=_CapTouch)

    # register for bumps to stop program
    misty.RegisterEvent(event_name="stop", event_type=Events.BumpSensor,
                        keep_alive=True, callback_function=_BumpSensor)
