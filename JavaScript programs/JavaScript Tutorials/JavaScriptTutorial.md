# Programming with Web API

##### Skye Weaver Worster

Misty’s creators have provided a [tutorial](https://docs.mistyrobotics.com/misty-ii/web-api/tutorials/) page, but it is difficult for a beginner to follow (or anyone, really). I have adapted those instructions below. The following tutorial should be appropriate for students that have completed CSC 210 or 212 and have limited Java or JavaScript experience.

Because the only connection between our computer and Misty is via HTTP, we can use nearly any programming language to create and receive these HTTP requests. However, JavaScript is the most supported option for working with Misty.

## Understanding Web API

Your JS code will use HTTP requests to give commands and receive data. Misty has a set of commands that she understands; these are listed in the [API reference](https://docs.mistyrobotics.com/misty-ii/web-api/api-reference/). Note that each command has an associated endpoint, formatted as a web address. We’ll use [Axios](https://docs.mistyrobotics.com/misty-ii/web-api/overview/#sending-requests-to-misty) to easily create and send these requests.

There are three types of requests. GET requests ask for data from Misty, POST requests give commands to Misty, and DELETE requests tell Misty to erase files. For the most part, we’ll be using GET and POST requests.

Let’s take `ChangeLED` as an example. [This command](https://docs.mistyrobotics.com/misty-ii/web-api/api-reference/#changeled) is accessed through a POST request, so we’ll use the `axios.post()` method. `post()` takes two parameters: the IP address of the command’s endpoint, and an object containing the parameters for that command. The endpoint is at `MISTY-IP/api/led`, so our request now looks as follows:

```javascript
axios.post("http://" + ip + "/api/led")
```

Now we need to attach the parameters that this command requires. The parameters are grouped into a dictionary, with parameter names as keys.

```javascript
let data = {
    "red": 255,
    "green": 0,
    "blue": 255
};
```

Our POST request is now complete! 

```javascript
axios.post("http://" + ip + "/api/led", data)
```

We’ll also be using [WebSockets](https://docs.mistyrobotics.com/misty-ii/web-api/overview/#getting-live-data-from-misty) to collect live data from Misty. This data will come to us in a continuous stream. You can learn more about subscribing to WebSockets in the second tutorial.

You can run your code by dragging and dropping the HTML file into your browser, or by using the Live Server extension on VS Code to automatically run the file in your browser. Be sure to open the developer console in your browser, as important messages will be printed there.

## Starter Code

Begin with the following starter code:

```html
<!DOCTYPE html>
<html>
<head>
    <meta charset="utf-8" />
    <title>Tutorial | Changing Misty's LED</title>
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <script src="https://unpkg.com/axios/dist/axios.min.js"></script>
</head>
<body>
    <script>
        YOUR CODE GOES HERE
    </script>
</body>
</html>
```

The JavaScript code for your program will go between the `<script>` tags in the `<body>`.

Misty uses an HTTP library called Axios to handle network communication. This library is included using the `<script src="https://unpkg.com/axios/dist/axios.min.js">` line in the `<head>` section.

If your code will reference Misty’s light sensors or cameras, you will need to include the `lightSocket.js` [script](https://github.com/SWorster/MistySURF2023/blob/ec0f306566716595591b53d1d1412dea6e0f9f23/JavaScript%20Tutorials/lightSocket.js). We recommend moving this file to the same location as your code. Add the following line to the bottom of the `<head>` section:

```html
<script src="lightSocket.js"></script>
```

If `lightSocket.js` is in a different location, you will need to provide the local path to it inside the quotes.

## Tutorial #1: Changing LED

The full program for the following tutorial can be found [here](https://github.com/SWorster/MistySURF2023/blob/ec0f306566716595591b53d1d1412dea6e0f9f23/JavaScript%20Tutorials/tutorial1.html).

Begin by declaring your robot’s IP address as a global constant value:

```javascript
const ip = "MISTY-IP-ADDRESS-HERE";
```

We then create an object with three parameters to store a color value.

```javascript
let data = {
    "red": 255,
    "green": 0,
    "blue": 255
};
```

We now need to send this data to Misty and tell her to change her LED. The Axios `post()` method takes a webpage address as a string parameter and sends an HTTP POST request. If we make the data and command part of the address, we can communicate with Misty.

```javascript
axios.post("http://" + ip + "/api/led", data)
```

Axios is [promise-based](https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Global_Objects/Promise). This means we can give it values that haven’t been declared yet and promise that we will give it those values later. When the method finally receives the promised data, it will execute. This allows us to run [asynchronous code](https://developer.mozilla.org/en-US/docs/Web/JavaScript/Guide/Using_promises).

We can chain a `then()` method onto the one we just wrote so that when the promise is fulfilled, we can print to the console.

```javascript
axios.post("http://" + ip + "/api/led", data)
	.then(function (response) {
        console.log(`ChangeLED was a ${response.data.status}`);
    })
```

When Misty receives our POST request, she will return a response saying whether she was successful or not in changing her LED. If we don’t receive a response, we need to tell the user that we’ve found a problem. We do this by chaining a `catch()` method.

```javascript
axios.post("http://" + ip + "/api/led", data)
	.then(function (response) {
        console.log(`ChangeLED was a ${response.data.status}`);
    })
    .catch(function (error) {
        console.log(`There was an error with the request ${error}`);
    })
```

Run this code and check your console to see the response Misty gives.

This can also be accomplished without Axios, using the built-in `Promise` class. We do not recommend using this unless you are already familiar with `Promise`.

```javascript
Promise.race([
    fetch('http://MISTY-IP-ADDRESS-HERE/api/led', {
        method: 'POST',
        body: '{ "red":0,"green":0,"blue":255 }'
    }),
    new Promise((_, reject) => setTimeout(() => reject(new Error('timeout')), 10000))
])
.then(response => response.json())
.then(jsonData => console.log(jsonData))
```


## Tutorial #2: Driving Straight

The full program for the following tutorial can be found [here](https://github.com/SWorster/MistySURF2023/blob/ec0f306566716595591b53d1d1412dea6e0f9f23/JavaScript%20Tutorials/tutorial2.html).

This program has the robot drive straight forward for a set time or until it sees an obstacle. To accomplish this, we need to subscribe to Misty’s WebSocket connections (essentially, we need to view the data Misty is collecting in real time).

This project requires the `lightSocket.js` file, which can be added as explained above.

> **Note**
> This tutorial originally used the `LocomotionCommand` event. This event does not work as intended, because it does not send a message when Misty’s velocity is 0; the code fails to terminate as a result. Instead, we will use `DriveEncoders`. Feel free to peruse the [documentation](https://docs.mistyrobotics.com/misty-ii/web-api/tutorials/#using-sensors-websockets-and-locomotion) this code was based on, but be aware that it does not function.

Start by declaring Misty’s IP:

```javascript
const ip = "MISTY-IP-ADDRESS-HERE";
```

To keep track of whether Misty has started driving, we’ll declare a mutable boolean. Note that this is an alteration to the original code and does not appear in the documentation.

```javascript
let is_driving = false;
```

We need to declare an object that holds Misty’s vision and movement data. This new `LightSocket` object is given the IP address and a function called `openCallback`.

```javascript
let socket = new LightSocket(ip, openCallback);
```

We then declare the `openCallback` function. We’ll be doing three things in this function: subscribing to the `TimeOfFlight` WebSocket, subscribing to the `DriveEncoders` WebSocket, and sending a `DriveTime` command. Let’s start by letting the user know that the socket is open.

```javascript
function openCallback() {
    console.log("socket opened");
}
```

Now we subscribe to the Time Of Flight (TOF) sensor. This sensor emits light, measures how long it takes that light to bounce back to the sensor, and calculates the distance. In `openCallback`:

```javascript
socket.Subscribe("CenterTimeOfFlight", "TimeOfFlight", 100, "SensorPosition", "==", "Center", null, _centerTimeOfFlight);
```

The `Subscribe()` method takes the following [parameters](https://docs.mistyrobotics.com/misty-ii/web-api/overview/#formatting-the-subscribe-message):

1. `eventName`: gives this event a unique name. We’re calling it `"CenterTimeOfFlight"`
2. `msgType`: specifies which data stream we’re subscribing to. We’re using `"TimeOfFlight"`
3. `debounceMs`: specifies how often Misty sends us her TOF data, in milliseconds. We’re using 100 ms, or .1 seconds.
4. The next three parameters specify which TOF sensor we’re listening to. Otherwise, we would get the data from all of Misty’s TOF sensors. These three parameters form an inequality, saying that we’re looking at the sensor that is positioned in the center.
   1. `property`: `"SensorPosition"`
   2. `inequality`: `==`
   3. `value`: `"Center"`
5. `returnProperty`: an optional parameter which we don’t need at the moment, `null`
6. `eventCallback`: the callback function that will trigger when we receive Misty’s data. We’re calling it `_centerTimeOfFlight`

Now we subscribe to the `DriveEncoders` socket. This sends us data about the movement of Misty’s treads. We only need to give the `eventName`, `msgType`, `debounceMs`, and `eventCallback` parameters. We don’t need to specify which sensor we’re listening to.

```javascript
socket.Subscribe("DriveEncoders", "DriveEncoders", 50, null, null, null, null, _driveEncoders);
```

Next, we need to give Misty the drive command. First, we declare an object with the movement we want.

```javascript
let data = {
    LinearVelocity: 50,
    AngularVelocity: 0,
    TimeMS: 5000
};
```

Now we use an Axios POST request. The post method should be familiar from the previous tutorial, but note that the address has changed from `/api/led` to `/api/drive/time`. When we receive a response, we print the result to the console. If there’s an issue, we log the error to the console.

```javascript
axios.post("http://" + ip + "/api/drive/time", data)
    .then(function (response) {
        console.log(`DriveTime was a ${response.data.status}`);
    })
    .catch(function (error) {
        console.log(`There was an error with the request ${error}`);
    }); 
```

Remember how we referenced the `_centerTimeOfFlight` and `_driveEncoders` callback functions earlier? Now it’s time to make them! These are the functions that will run once Misty sends us her data.

The `_centerTimeOfFlight` function needs to parse the TOF data and tell Misty to stop if she gets too close to something. We declare the function with a data parameter.

```javascript
let _centerTimeOfFlight = function (data) {};
```

The data we’ll be receiving might not actually have relevant data (it might be registration or error messages). Use a `try-catch` block to handle these cases. We won’t need to put anything inside the `catch` statement, because we just want to ignore non-numerical data.

```javascript
try {};
catch(e) {};
```

In the `try` block, we find the distance from the data Misty’s sending and print it to the console.

```javascript
try {
let distance = data.message.distanceInMeters;
console.log(distance);
};
```

We want Misty to stop when that distance is less than a certain value. Let’s use 0.2 meters. We then make our Axios POST request, which now contains `/api/drive/stop` and will stop Misty when sent. Inside the `try` block:

```javascript
if (distance < 0.2) {
    axios.post("http://" + ip + "/api/drive/stop")
    .then(function (response) {
        console.log(`Stop was a ${response.data.status}`);
    })
    .catch(function (error) {
        console.log(`There was an error with the request ${error}`);
    });
};
```

Next, we make the `_driveEncoders` callback function. This will track whether Misty is moving, and unsubscribe us from the WebSockets when she stops. We first check whether Misty has started driving. We could do this with either the left or right tread velocities, but for accuracy we can take the average.

```javascript
let _driveEncoders = function (data) {
try {
    velocity = (data.message.leftVelocity + data.message.rightVelocity) /2;
    if (velocity > 0.01){
        is_driving = true;
    }
```

If Misty has started driving and the velocity reaches 0, we know that she’s stopped. In our conditional statement, we use `===` to denote strict equality; the numbers have to be the same data type. Inside the conditional, we print our output to the console and unsubscribe from the sockets.

```javascript
if (velocity === 0 && is_driving) {
    console.log("DriveEncoders received linear velocity as", velocity);
    socket.Unsubscribe("CenterTimeOfFlight");
    socket.Unsubscribe("DriveEncoders");
}
```

At the very bottom of our script, we finally connect to Misty. When this line is reached, the openCallback function is called.

```javascript
socket.Connect();
```


## Tutorial #3: Computer Vision and Facial Recognition

The full program for the following tutorial can be found [here](https://github.com/SWorster/MistySURF2023/blob/ec0f306566716595591b53d1d1412dea6e0f9f23/JavaScript%20Tutorials/tutorial3.html).

This program uses Misty’s facial recognition capabilities. Misty will check whether she knows a given name. If she knows the name and sees that person, she will greet the person. If she does not know the name, Misty will use facial recognition to learn the person’s face.

This project requires the `lightSocket.js` file, which can be added as explained above.

Begin by declaring global variables. Provide the IP address, choose the name you’d like Misty to recognize or learn, and set `onList` to `false`. In a real-world application, we would create a form where users can give Misty their name.

```javascript
const ip = "MISTY-IP-ADDRESS-HERE"
const you = "YOUR-NAME"
let onList = false;
```

We declare an instance of `LightSocket`, like we did previously.

```javascript
let socket = new LightSocket(ip, openCallback);
```

We’ll need a `sleep` function to give Misty processing time later. It uses the built-in `Promise` class instead of Axios.

```javascript
function sleep(ms) {
    return new Promise(resolve => setTimeout(resolve, ms));
}
```

Next, we’ll work on our callbacks. The function `openCallback` now uses the `async` [keyword](https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Statements/async_function). This is another way of allowing asynchronous behavior in JavaScript, but it doesn’t require chaining `then()` and `catch()` like Axios methods. An asynchronous function will contain a line with the keyword `await` and a promise function. It will stop at that line and wait for the promise function to run. This implementation allows Misty to run its facial recognition program while our code waits for it to finish.

`openCallback` first unsubscribes from any existing facial recognition sockets, then waits 3 seconds.

```javascript
async function openCallback() {
socket.Unsubscribe("FaceRecognition");
	await sleep(3000);
}
```

Now we check if the given name is stored in Misty’s memory. We use an Axios GET request to access the endpoint for the `GetKnownFaces` command. In `openCallback`:

```javascript
axios.get("http://" + ip + "/api/faces")
```

This will return the list of faces Misty knows. We use the `then()` method to parse Misty’s response, store the list in a variable, and print the list to the console.

```javascript
axios.get("http://" + ip + "/api/faces")
    .then(function (res) {
        let faceArr = res.data.result;
        console.log("Learned faces:", faceArr);
    }
```

We then loop through the list of names and compare each to the given name. If we find a match, we change `onList` to `true`. In `then()`:

```javascript
for (let i = 0; i < faceArr.length; i++) {
    if (faceArr[i] === you) {
        onList = true;
    }
}
```

Next, subscribe to the `FaceRecognition` socket. Set the `eventName` and `msgType` to `"FaceRecognition"`, `debounceMs` to 200, and `eventCallback` to `_FaceRecognition`. In `then()`:

```javascript
socket.Subscribe("FaceRecognition", "FaceRecognition", 200, null, null, null, null, _FaceRecognition);
```

Finally, we use an `if-else` statement to branch into the two paths. These reference functions we haven’t made yet that will handle the behavior for each option. In `then()`:

```javascript
if (onList) {
    console.log("You were found on the list!");
    startFaceRecognition();
}
else {
    console.log("You're not on the list...");
    startFaceTraining();
}
```

Now let’s make those two functions. In `startFaceRecognition`, the person was found on the list. Print a message to the console that Misty is starting facial recognition, and make an Axios POST request to access the `StartFaceRecognition` command. 

```javascript
function startFaceRecognition() {
    console.log("starting face recognition");
    axios.post("http://" + ip + "/api/faces/recognition/start");
}
```

Because `StartFaceRecognition` is a `FaceRecognition` WebSocket event, this will trigger the callback `_FaceRecognition` that we’ll make later.

The other branch is that Misty doesn’t know this person and needs to learn their face. We’ll make an asynchronous function called `startFaceTraining` and print a message to the console. An Axios POST request accesses the endpoint for the `StartFaceTraining` command and provides the given name.

```javascript
async function startFaceTraining() {
    console.log("starting face training");
    axios.post("http://" + ip + "/api/faces/training/start", { FaceId: you });
};
```

Next, we give Misty some time to learn the face and print to the console when she’s done. In `startFaceTraining`:

```javascript
await sleep(20000);
console.log("face training complete");
```

Now we want Misty to try to recognize the face she just learned. We do this with another Axios POST request:

```javascript
axios.post("http://" + ip + "/api/faces/recognition/start");
```

Finally, we make the `_FaceRecognition` callback to handle data from the `FaceRecognition` event. As with the previous tutorial, we need to handle non-relevant event data with a `try-catch` block.

```javascript
function _FaceRecognition(data) {
    try {}
    catch (e) {
        console.log("Error: " + e);
    }
}
```

The person’s name that Misty detected is stored in `data.message.label`. In a conditional, we compare that label to `"unknown person"`, `null`, and `undefined`. If the label is none of those, Misty has detected a known person.

```javascript
try {
    if (data.message.label !== "unknown person" && data.message.label !== null && data.message.label !== undefined) {}
}
```

If the person is recognized, print a message to the console greeting the person. Then unsubscribe from the `FaceRecognition` socket and access the endpoint for the `StopFaceRecognition` command. Inside the `try` block:

```javascript
try {
    if (data.message.label !== "unknown person" && data.message.label !== null && data.message.label !== undefined) {
        console.log(`A face was recognized. Hello there ${data.message.label}!`);
        socket.Unsubscribe("FaceRecognition");
        axios.post("http://" + ip + "/api/faces/recognition/stop");
    }
}
```

At the very bottom of the script, we open the connection to Misty.

```javascript
socket.Connect();
```

This program has a rather obvious edge case: what if Misty knows the person’s name you give her, but doesn’t see that person? Solutions to this problem are left as an exercise for the reader.


## Tutorial #4: Taking Pictures

The full program for the following tutorial can be found [here](https://github.com/SWorster/MistySURF2023/blob/ec0f306566716595591b53d1d1412dea6e0f9f23/JavaScript%20Tutorials/tutorial4.html).

This program lets Misty take a photo when she detects a face.

This project requires the `lightSocket.js` file, which can be added as explained above.

We start by declaring our global variables. In addition to our usual `IP` and `socket`, we have `subscribed` to record whether we’re subscribed to `FaceRecognition` events and `firstTime` to track whether we’ve sent a command to start face detection.

```javascript
const ip = "MISTY-IP-ADDRESS-HERE";
let socket = new LightSocket(ip, openCallback);
let subscribed;
let firstTime = true;
```

Like with the third tutorial, we need a `sleep` function.

```javascript
function sleep(ms) {
    return new Promise(resolve => setTimeout(resolve, ms));
}
```

We’re using an asynchronous `openCallback` function again. Set `subscribed` to `false`, because we haven’t subscribed to `FaceRecognition` events yet. Unsubscribe from any existing `FaceRecognition` events, and wait 8 seconds for the subscription to end. This should feel familiar after the third tutorial.

```javascript
async function openCallback() {
    subscribed = false;
    socket.Unsubscribe("FaceRecognition");
    await sleep(8000);
}
```

Now we subscribe to `FaceRecognition`.

```javascript
socket.Subscribe("FaceRecognition", "FaceRecognition", 1000, null, null, null, null, _FaceRecognition);
```

We’ll need a `_FaceRecognition` function to handle the data once we’re subscribed. Inside this function, print a message to signal that facial recognition has begun. Now that we’re subscribed to `FaceRecognition`, we should update `subscribed` to `true`.

```javascript
async function _FaceRecognition(data) {
    console.log("CV callback called: ", data);
    if (!subscribed) {
        subscribed = true;
    }
}
```

Misty will continue subscribing and unsubscribing from `FaceRecognition` as she takes pictures of people, but we can keep face detection active the entire time. The global variable `firstTime` is true if we haven’t yet sent the command to begin face detection. In that case, we need to send an Axios POST request to the endpoint for the `StartFaceDetection` command. Inside `_FaceRecognition`:

```javascript
console.log("CV callback called: ", data);
    if (!subscribed) {
        subscribed = true;
        if (firstTime) {
            axios.post("http://" + ip + "/api/faces/recognition/start")
            .catch((err) => {
                console.log(err);
            });
            firstTime = false;
        }
    }
}
```

The first `FaceRecognition` we receive after subscribing will be a registration message that we want to ignore. Because we don’t want to run the rest of our code in this callback, we return at the end of the `subscribed` conditional. The next time we receive `FaceRecognition` data, the rest of our `_FaceRecognition` function will run.

```javascript
console.log("CV callback called: ", data);
if (!subscribed) {
    subscribed = true;
    if (firstTime) {…}
    return
}
```

Now Misty needs to take a picture! Let’s start by planning for errors and creating a `try-catch` block.

```javascript
async function _FaceRecognition(data) {
    console.log("CV callback called: ", data);
    if (!subscribed) {…}
    try {}
    catch (err) {
        console.log(err);
    }
}
```

Inside the `try` block, use an Axios GET request to access the endpoint for the `TakePicture` command. There are several parameters for this command that we pass in the address.

1. `Base64`: `null`, so that Misty doesn’t return the image as a base-64 string.
2. `FileName`: we set this to `fileName`, a variable we’ll define later. If we don’t provide a name here, Misty won’t save the photo to her file system.
3. `Width`: set to 1920
4. `Height`: set to 1080
5. `DisplayOnScreen`: set to `false`, so that Misty doesn’t display the image on her screen.
6. `OverwriteExisting`: set to `true`, so that we overwrite old images with the same name.

```javascript
axios.get("http://" + ip + "/api/cameras/rgb", {
    params: {
        Base64: null,
        FileName: fileName,
        Width: 1920,
        Height: 1080,
        DisplayOnScreen: false,
        OverwriteExisting: true
    }
})
```

We use a `then()` method to print the response and save messages to the console.

```javascript
axios.get("http://" + ip + "/api/cameras/rgb", {
    params: {…}
})
    .then(function (res) {
        console.log(res);
        console.log("Image saved with fileName: '" + fileName + "'");
    });
```

We now need to go back and define `fileName`. Above the Axios GET request, use the `Date` object to give each picture a unique name and the `toLocaleString()` method to convert it to a string. We have to format the string to omit invalid characters with several uses of the `replace()` method.

```javascript
let fileName = new Date().toLocaleString().replace(/[/]/g, ".").replace(/[:]/g, ".").replace(/[ ]/g, "_").replace(",", "") + "_Face";
```

When the photo-taking process is complete, we need to continue the program. At the end of the `try` block, call `openCallback`. Your `_FaceRecognition` function should now be organized as follows:

```javascript
async function _FaceRecognition(data) {
    console.log("CV callback called: ", data);
    if (!subscribed) {
        subscribed = true;
        if (firstTime) {…}
        return
    }
    try {
        let fileName = new Date()…;
        axios.get("http://" + ip + "/api/cameras/rgb", {
            params: {…}
        })
            .then(function (res) {…});
        openCallback();
    }
    catch (err) {
        console.log(err);
    }
}
```

Finally, call `socket.Connect()` to connect to Misty.

```javascript
socket.Connect();
```

Congratulations! You’ve completed all four tutorials!
