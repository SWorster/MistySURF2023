# import statements
from mistyPy.Robot import Robot
from mistyPy.Events import Events

# callback for face training
def _FaceTraining(data):
    
    # if process is complete, unregister from FT event and start recognition
    try:
        if data["message"]["isProcessComplete"]:
            print("face training complete")
            misty.UnregisterEvent("FaceTraining")
            misty.StartFaceRecognition()
    except:
        pass
    
# callback for all face recognition events
def _FaceRecognition(data):
    try:
        # Use an if statement to check that label does not equal "unknown person" or None. label is included in the message returned by FaceRecognition WebSocket events.
        name = data["message"]["label"]
        if (name != "unknown person" and name != None):
            # If the face is recognized, print a message to greet the person by name.
            print("A face was recognized. Hello there, " + name + "!");
            misty.StopFaceRecognition()
            print("unregistering from all events")
            misty.UnregisterAllEvents()
            print("program complete")
    except:
        pass

if __name__ == "__main__":
    misty = Robot("MISTY-IP-ADDRESS-HERE")  # Robot object with your IP

    # Create a global constant called you and assign it to a string with your name.
    global you
    you = "YourName"

    # Initialize another variable called onList and set its value to false.
    global onList
    onList = False
    
    # unregister from all events to clear existing facial recognition
    print("unregistering")
    misty.UnregisterAllEvents()
    
    # register for face recognition events
    misty.RegisterEvent("FaceRecognition", Events.FaceRecognition, callback_function=_FaceRecognition, keep_alive=True)
    
    # Store the list of known faces in the faceArr variable and print this list.
    faceJSON = misty.GetKnownFaces().json()
    faceArr = faceJSON["result"]
    print("Learned faces:", faceArr)
    
    # onList is True if your name is in the array
    if you in faceArr:
        onList = True
    
    # Use an if, else statement to execute startFaceRecognition if onList is true and to execute startFaceTraining if otherwise.
    if onList:
        print("You were found on the list!")
        print("starting face recognition")
        misty.StartFaceRecognition()
        
    else:
        print("You're not on the list...")
        print("starting face training")
        
        # register for FT events
        misty.RegisterEvent("FaceTraining", Events.FaceTraining, callback_function=_FaceTraining, keep_alive=True)
        
        misty.StartFaceTraining(you)
    
    misty.KeepAlive()