// Car servo controller program
// Version 2.0.0
// Written 4/18/23

#include "Servo.h"

// Timer and data pins
#define pinTrigger 2
#define pinData0 A1
#define pinData1 A2
#define pinData2 A3
#define pinData3 A4

// Pins for the servo control lines
#define servoControlFrontLeft 10
#define servoControlFrontRight 6

#define servoControlBackLeft 9
#define servoControlBackRight 5

// global variables
// Declares the servos 
Servo servoFrontRight; // Right side servo
Servo servoFrontLeft; // Left side servo

Servo servoBackRight; // Right side servo
Servo servoBackLeft; // Left side servo

const unsigned long pulseWidth = 12; // micro second width of each data pulse
const byte dataSize = 16;
bool recievedData[dataSize];

byte timerStart = 0;
byte speed = 0;
byte direction = 0;

unsigned long commandTimeStop = 0;

bool checkData;

void setup() {
  Serial.begin(9600); // Allows for usb debugging through Tools > Serial Monitor/Serial Plotter

  pinMode(pinTrigger, INPUT_PULLUP);
  pinMode(pinData0, INPUT);
  pinMode(pinData1, INPUT);
  pinMode(pinData2, INPUT);
  pinMode(pinData3, INPUT);
  attachInterrupt(digitalPinToInterrupt(pinTrigger), onInterrupt, RISING);

  // Sets the servo control pins to OUTPUT
  pinMode(servoControlFrontLeft, OUTPUT);
  pinMode(servoControlFrontRight, OUTPUT); 

  pinMode(servoControlBackLeft, OUTPUT);
  pinMode(servoControlBackRight, OUTPUT); 

  // attaches the servos to correct pin to control it.
  servoFrontRight.attach(servoControlFrontRight);   
  servoFrontLeft.attach(servoControlFrontLeft);

  servoBackRight.attach(servoControlBackRight);   
  servoBackLeft.attach(servoControlBackLeft);

  // Sets the intial state of the Servos
  // Stops the servos
  carStop();

  checkData = false;
}

void loop() {
  // put your main code here, to run repeatedly:
  if (checkData){
    readData();
    commandTimeStop = millis() + timerStart * 10; // Time the arduino should stop moving
    checkData = false;
  }

  if (timerStart == 0){
    if (speed == 0){
    carStop();
    }
    else{
      switch (direction){
        case 0: // Forward
          carForward();
          break;
        case 1: // Backward
          carBackward();
          break;
        case 2: // Right
          carRight();
          break;
        case 3: // Left
          carLeft();
          break;
        default:
          carStop();
      }
    }
  }
  else {
    if (commandTimeStop >= millis()){
      if (speed == 0){
        carStop();
      }
      else{
        switch (direction){
          case 0: // Forward
            carForward();
            break;
          case 1: // Backward
            carBackward();
            break;
          case 2: // Right
            carRight();
            break;
          case 3: // Left
            carLeft();
            break;
          default:
            carStop();
        }
      }
    }
    else {
      carStop();
    }
  }
    
}

void onInterrupt(){
  noInterrupts(); //Disable interrupts until data read is completed
  checkData = true;
  interrupts(); // Re enables interrupts
}

void readData(){
  direction = 0;
  speed = 0;
  timerStart = 0;
  
  delay(pulseWidth);
  for (int i = 0; i < dataSize/4; i++)
  {
    recievedData[4*i] = digitalRead(pinData0);
    recievedData[4*i+1] = digitalRead(pinData1);
    recievedData[4*i+2] = digitalRead(pinData2);
    recievedData[4*i+3] = digitalRead(pinData3);
    delay(pulseWidth);
  }    

  Serial.print("Time = " + String(millis()) + " | ");

  int counter = 1;
  for (bool i : recievedData){
    Serial.print(i);
    if (counter % 4 == 0){
      Serial.print(" ");
    }
    counter++;
  }
  Serial.println();

  readSection(&direction, 0, 2);
  readSection(&speed, 3, 7);
  readSection(&timerStart, 8, 15);

  Serial.print("Direction=" + String(direction)); Serial.print(" | Speed=" + String(speed)); Serial.print(" | StartTimer=" + String(timerStart));
  Serial.println();
}

void readSection(byte* var, byte startIndex, byte endIndex){
  byte temp = 0;
  for (int i = 0; i <= endIndex-startIndex; i++){
    temp += recievedData[i+startIndex] * (pow(2,i) + 0.1);
  }
  *var = temp;
  
}

void carForward(){
  Serial.println("Forward");
  int offset = 16*speed;
  // Forward max speed
  servoFrontRight.writeMicroseconds(1500 - offset);
  servoFrontLeft.writeMicroseconds(1500 + offset);

  servoBackLeft.writeMicroseconds(1500 + offset);
  servoBackRight.writeMicroseconds(1500 - offset);
}

void carBackward(){
  Serial.println("Backward");
  int offset = 16*speed;
  // Backward max speed
  servoFrontRight.writeMicroseconds(1500 + offset);
  servoFrontLeft.writeMicroseconds(1500 - offset);

  servoBackLeft.writeMicroseconds(1500 - offset);
  servoBackRight.writeMicroseconds(1500 + offset);
  }

void carRight(){
  Serial.println("Right");
  int offset = 16*speed;
  // Right max speed
  servoFrontRight.writeMicroseconds(1500 + offset);
  servoFrontLeft.writeMicroseconds(1500 + offset);

  servoBackLeft.writeMicroseconds(1500 + offset);
  servoBackRight.writeMicroseconds(1500 + offset);
}

void carLeft(){
  Serial.println("Left");
  int offset = 16*speed;
  // Left max speed
  servoFrontRight.writeMicroseconds(1500 - offset);
  servoFrontLeft.writeMicroseconds(1500 - offset);

  servoBackLeft.writeMicroseconds(1500 - offset);
  servoBackRight.writeMicroseconds(1500 - offset);
}

void carStop(){
  // Stops car
  servoFrontRight.writeMicroseconds(1500);
  servoFrontLeft.writeMicroseconds(1500);

  servoBackLeft.writeMicroseconds(1500);
  servoBackRight.writeMicroseconds(1500);
}
