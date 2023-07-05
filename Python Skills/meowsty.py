'''
Skye Weaver Worster

Misty is now Meowsty. No FUR-ther explanation provided. (please laugh at the pun)

Audio files are in Other Resources > For Fun > MistyMedia > Misty Sounds > cat. You can also download them by running the mediaUpload file.
'''

# import statements
from mistyPy.Robot import Robot
from mistyPy.Events import Events

misty = Robot("131.229.41.135")  # Misty robot with your IP
last_place = ""  # tracks the last place Misty was touched

# audio volumes
purr1 = 10
purr2 = 10
meow1 = 5
meow2 = 5
meow3 = 5
hiss = 3


def _BumpSensor(data):  # when bumped, program ends
    misty.UnregisterAllEvents()  # unregister all events
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

        # print(touched, part_touched, last_place) # useful for debugging

        # if two parts touched at same time
        if part_touched != last_place:
            misty.StopAudio()  # stop audio
            last_place = ""  # ignore older event, proceed with new touch

        # if first time touching a place
        if last_place == "":
            last_place = part_touched  # record what part we've touched

            # if-else statements on part_touched
            if part_touched == "Chin" and touched:
                misty.PlayAudio("A_purr1.mp3", purr1)
                misty.TransitionLED(0, 0, 0, 255, 100, 255,
                                    "TransitOnce", 2000)
                print("chin scritches <3")

            elif part_touched == "HeadLeft" and touched:
                misty.PlayAudio("A_meow1.mp3", meow1)
                print("left scritches")

            elif part_touched == "HeadRight" and touched:
                misty.PlayAudio("A_meow2.mp3", meow2)
                print("right scritches")

            elif part_touched == "HeadBack" and touched:
                misty.PlayAudio("A_meow3.mp3", meow3)
                print("back scritches")

            elif part_touched == "HeadFront" and touched:
                misty.PlayAudio("A_purr2.mp3", purr2)
                print("front scritches")

            elif part_touched == "Scruff" and touched:
                misty.PlayAudio("A_hiss.mp3", hiss)
                print("HISS")

        # if a place has already been touched:
        else:
            # purring: have to manually stop audio when stop touching
            # single-sound places: sound will stop automatically on completion

            if last_place == "Chin":
                # if we stop touching the chin
                if touched == False and part_touched == "Chin":
                    misty.StopAudio()  # stop audio
                    # pulse between pink and off over 2 seconds, repeatedly
                    misty.TransitionLED(255, 100, 255, 0, 0,
                                        0, "TransitOnce", 2000)
                    last_place = ""  # clear last place touched

            if last_place == "HeadLeft":
                # if we stop touching HL
                if touched == False and part_touched == "HeadLeft":
                    last_place = ""

            if last_place == "HeadRight":
                if touched == False and part_touched == "HeadRight":
                    last_place = ""

            if last_place == "HeadBack":
                if touched == False and part_touched == "HeadBack":
                    last_place = ""

            if last_place == "HeadFront":
                if touched == False and part_touched == "HeadFront":
                    misty.StopAudio()  # stop audio
                    last_place = ""

            if last_place == "Scruff":
                if touched == False and part_touched == "Scruff":
                    last_place = ""

    except Exception as e:
        print("EXCEPTION:", e)


if __name__ == "__main__":
    try:
        # register for cap touch, keep event alive
        misty.RegisterEvent(event_name="scratches", event_type=Events.TouchSensor,
                            callback_function=_CapTouch, keep_alive=True)

        # register for bumps to stop program
        misty.RegisterEvent(event_name="stop", event_type=Events.BumpSensor,
                            callback_function=_BumpSensor, keep_alive=True)

    except Exception as ex:
        print(ex)
