'''
Skye Weaver Worster

Trains Misty on the face in front of her. Be sure to specify the target's name below.
'''

from mistyPy.Robot import Robot
from mistyPy.Events import Events

misty = Robot("131.229.41.135")  # robot object
name = "test"  # the target's name, with no spaces or special characters


def _FaceTraining(data):  # callback for face training

    try:  # handles irrelevant/malformed data
        # if process is complete, unregister from FT event and start recognition
        if data["message"]["isProcessComplete"]:  # when face training ends
            print(f"Face training complete! Hello, {name}!")
            misty.UnregisterEvent("FaceTraining")  # unregister from FT event
            misty.ChangeLED(0, 0, 0)  # LED off
    except Exception as e:
        print("Facial Recognition error:", e)


if __name__ == "__main__":

    # unregister from all events to clear existing facial recognition
    misty.UnregisterAllEvents()

    # register for face training events
    misty.RegisterEvent("FaceTraining", Events.FaceTraining,
                        keep_alive=True, callback_function=_FaceTraining)

    misty.StartFaceTraining(name)  # start face training
