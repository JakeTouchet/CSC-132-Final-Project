// Car servo controller program
// Version 2.0.0
// Written 4/18/23

#include <Servo.h>

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

#define dataSize 3

byte data[dataSize] = {0,0,0};

byte timerStart = 0;
byte speed = 0;
byte direction = 0;

unsigned long commandTimeStop = 0;

bool checkData;

void setup() {
  Serial.begin(9600); // Allows for usb debugging through Tools > Serial Monitor/Serial Plotter

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

  // Sets the initial state of the Servos
  // Stops the servos
  carStop();

  checkData = false;
}

void loop() {
  // put your main code here, to run repeatedly:
  while (Serial.available() > dataSize){
    byte discard = Serial.read();
  }
  // If buffer is equal to data then transfer data
  if (Serial.available() == dataSize){
    for (size_t i = 0; i < dataSize; i++)
    {
      data[i] = Serial.read();
    }      
    timerStart = data[0];
    speed = data[1];
    direction = data[2];
    printData();
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

void printData(){
  if (Serial.availableForWrite()){
    for (size_t i = 0; i < dataSize; i++)
    {
      Serial.print(data[i]); Serial.print(" ");
    }
    Serial.println();      
    Serial.print(String(timerStart, DEC) + " " + String(speed, DEC) + " " + String(direction, DEC));
  }  
}