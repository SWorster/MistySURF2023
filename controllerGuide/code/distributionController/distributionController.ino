#define VRX_PIN  A1
#define VRY_PIN  A0
#define SW_PIN   7
#define YELLOW_BTN  6
#define BLUE_BTN  5
#define GREEN_BTN 4
#define RED_BTN 3

int xValue = 0;
int yValue = 0;
int yellowState = 0;
int blueState = 0;
int greenState = 0;
int redState = 0;

int mode = 1;
const int timeDelay = 150;

void setup() {
  Serial.begin(9600);
  while (!Serial);
  pinMode(YELLOW_BTN, INPUT);
  pinMode(BLUE_BTN, INPUT);
  pinMode(GREEN_BTN, INPUT);
  pinMode(RED_BTN, INPUT);
}

void loop() {
  xValue = analogRead(VRX_PIN);
  yValue = analogRead(VRY_PIN);

  yellowState = digitalRead(YELLOW_BTN);
  blueState = digitalRead(BLUE_BTN);
  greenState = digitalRead(GREEN_BTN);
  redState = digitalRead(RED_BTN);

  if (yellowState == HIGH){
      mode = 1;
  }
  if (blueState == HIGH){
      mode = 2;
  }
  if (greenState == HIGH){
      mode = 3;
  }
  if (redState == HIGH){
      mode = 4;
  }

  Serial.print(xValue);
  Serial.print(" ");
  Serial.print(yValue);
  Serial.print(" ");
  Serial.println(mode);
  delay(timeDelay);
}
