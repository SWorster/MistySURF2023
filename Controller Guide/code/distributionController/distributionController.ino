// Joystick pins, can be adjusted according to physical wiring
#define VRX_PIN A1  // Arduino pin connected to VRX pin
#define VRY_PIN A0  // Arduino pin connected to VRY pin
#define SW_PIN 7    // Arduino pin connected to SW pin

// Digital pin in the board that the buttons are connected to via jumper cables, can be adjusted as needed
#define TREAD_BTN 6
#define ARM_BTN 5
#define HEAD_BTN 4
#define EXIT_BTN 3

int xValue = 0;  // To store value of the X axis
int yValue = 0;  // To store value of the Y axis

// get the state of the button: 0 = low, 1 = high (or 0 = unpressed, 1 = pressed)
int yellowState = 0;
int blueState = 0;
int greenState = 0;
int redState = 0;

int mode = 1;               // mode variable for the serial monitor
const int timeDelay = 150;  // adjust this to change the amount of time each loop iteration takes in milliseconds (the higher it is, the more data you'll miss)

int treadState; // current state the button is in
int lastYellowState = LOW; // track the previous state the button was in

int armState;
int lastBlueState = LOW;

int headState;
int lastGreenState = LOW;

int stopState;
int lastRedState = LOW;

// time since each button was pressed
unsigned long lastTreadTime = 0;
unsigned long lastArmTime = 0;
unsigned long lastHeadTime = 0;
unsigned long lastStopTime = 0;

unsigned long debounceDelay = 150; // the debounce time; increase if the output flickers

void setup() {
  Serial.begin(9600);  // start the serial monitor at a baudrate of 9600 (baudrate it the number of bits a second it reads in)
  while (!Serial);    // will hold the program here while the serial monitor is not initialized

  // identifies everything as an input (button input something to board -> do something)
  pinMode(TREAD_BTN, INPUT);
  pinMode(ARM_BTN, INPUT);
  pinMode(HEAD_BTN, INPUT);
  pinMode(EXIT_BTN, INPUT);
}

void loop() {
  // read analog X and Y analog values (analog meaning it can evaluate to many different values)
  xValue = analogRead(VRX_PIN);
  yValue = analogRead(VRY_PIN);

  // check for the current status of the buttons (digital because that means it can only be 2 values: high or low)
  yellowState = digitalRead(TREAD_BTN);
  blueState = digitalRead(ARM_BTN);
  greenState = digitalRead(HEAD_BTN);
  redState = digitalRead(EXIT_BTN);

  // update the time since the buttons were pressed if the state hasn't changed
  if (yellowState != lastYellowState) lastTreadTime = millis();
  if (blueState != lastBlueState) lastArmTime = millis();
  if (greenState != lastGreenState) lastHeadTime = millis();
  if (redState != lastRedState) lastStopTime = millis();

  // debounce for the buttons
  // treads
  if ((millis() - lastTreadTime) > debounceDelay) { // if the debounce threshold has been exceded
    if (yellowState != treadState) { // if the button state changed
      treadState = yellowState;
      if (treadState == HIGH) mode = 1; // if the button is pressed, change the mode
    }
  }

  // arms
  if ((millis() - lastArmTime) > debounceDelay) {
    if (blueState != armState) {
      armState = blueState;
      if (armState == HIGH) mode = 2;
    }
  }

  // head
  if ((millis() - lastHeadTime) > debounceDelay) {
    if (greenState != headState) {
      headState = greenState;
      if (headState == HIGH) mode = 3;
    }
  }

  // stop
  if ((millis() - lastStopTime) > debounceDelay) {
    if (redState != stopState) {
      stopState = redState;
      if (stopState == HIGH) mode = 4;
    }
  }

  // save the readings from this loop iteration for the next
  lastYellowState = yellowState;
  lastBlueState = blueState;
  lastGreenState = greenState;
  lastRedState = redState;

  // print to serial monitor to port data to python through pyserial
  Serial.print(xValue);
  Serial.print(" ");
  Serial.print(yValue);
  Serial.print(" ");
  Serial.println(mode);
  delay(timeDelay);
}
