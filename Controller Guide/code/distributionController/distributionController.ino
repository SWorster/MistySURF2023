// Joystick pins, can be adjusted according to physical wiring
#define VRX_PIN  A1 // Arduino pin connected to VRX pin
#define VRY_PIN  A0 // Arduino pin connected to VRY pin
#define SW_PIN   7  // Arduino pin connected to SW pin

// Digital pin in the board that the buttons are connected to via jumper cables, can be adjusted as needed
#define TREAD_BTN  6
#define ARM_BTN  5
#define HEAD_BTN 4
#define EXIT_BTN 3

int xValue = 0; // To store value of the X axis
int yValue = 0; // To store value of the Y axis

// get the state of the button: 0 = low, 1 = high (or 0 = unpressed, 1 = pressed)
int yellowState = 0;
int blueState = 0;
int greenState = 0;
int redState = 0;

int mode = 1; // mode variable for the serial monitor
const int timeDelay = 150; // adjust this to change the amount of time each loop iteration takes in milliseconds (the higher it is, the more data you'll miss)

void setup() {
  Serial.begin(9600); // start the serial monitor at a baudrate of 9600 (baudrate it the number of bits a second it reads in)
  while (!Serial); // will hold the program here while the serial monitor is not initialized
  pinMode(TREAD_BTN, INPUT); // identifies everything as an input (button input something to board -> do something)
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

  // change mode accordingly if button is pressed
  if (yellowState == HIGH){ // treads
      mode = 1;
  }
  if (blueState == HIGH){ // arms
      mode = 2;
  }
  if (greenState == HIGH){ // head
      mode = 3;
  }
  if (redState == HIGH){ // cancel
      mode = 4; 
  }

  // print to serial monitor to port data to python through pyserial
  Serial.print(xValue);
  Serial.print(" ");
  Serial.print(yValue);
  Serial.print(" ");
  Serial.println(mode);
  delay(timeDelay);
}
