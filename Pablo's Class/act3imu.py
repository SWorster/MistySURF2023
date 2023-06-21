'''
Proprioception sensing
'''

from mistyPy.Robot import Robot
from mistyPy.Events import Events


def _BumpSensor(data):
    if data["message"]["isContacted"]:
        misty.ChangeLED(255, 255, 255)
        misty.StopAudio()


def _IMU(data):
    global neutral

    # print("\n\nIMU\n", data)
    m = data["message"]
    t = 1  # tolerance

    red = 0
    green = 0
    blue = 0

    pv = m["pitch"]
    if pv > t:
        red = 50
    elif pv > 360-t:
        red = 255

    rv = m["roll"]
    if rv > t:
        green = 50
    elif rv < -t:
        green = 255

    yv = m["yawVelocity"]
    if yv > t:
        blue = 50
    elif yv < -t:
        blue = 255

    misty.ChangeLED(red, green, blue)

    t = .2
    v = 5
    xa = m["xAcceleration"]
    if xa > t:
        misty.PlayAudio("A_kittycat.mp3",volume=v)
        neutral[3] = False
    elif xa < -t:
        misty.PlayAudio("A_Circus.mp3",volume=v)
        neutral[3] = False
    else:
        neutral[3] = True

    ya = m["yAcceleration"]
    # if ya > t:
    #     misty.PlayAudio("A_VineBoom.mp3",volume=v)
    #     neutral[4] = False
    # elif ya < -t:
    #     misty.PlayAudio("A_RickrollShort.mp3",volume=v)
    #     neutral[4] = False
    # else:
    #     neutral[4] = True

    za = m["zAcceleration"]
    # if za > -9.75:
    #     misty.PlayAudio("A_secrettunnel.mp3",volume=v) # down
    #     neutral[5] = False
    # elif za < -9.85:
    #     misty.PlayAudio("A_CarelessWhisper.mp3",volume=v) # up
    #     neutral[5] = False
    # else:
    #     neutral[5] = True

    print(pv, rv, yv)
    print("                                                 ", xa, ya, za)
    # if neutral[0] and neutral[1] and neutral[2]:
    #     misty.ChangeLED(0, 0, 0)
    if neutral[3] and neutral[4] and neutral[5]:
        misty.StopAudio()

    misty.StopAudio()


if __name__ == "__main__":
    global neutral
    neutral = [True, True, True, True, True, True]  # pv, rv, yv, xa, ya, za

    misty = Robot("131.229.41.135")
    misty.RegisterEvent("IMU", Events.IMU, condition=None,
                        debounce=10, keep_alive=True, callback_function=_IMU)

    misty.RegisterEvent("BumpSensor", Events.BumpSensor, condition=None,
                        keep_alive=True, callback_function=_BumpSensor)
