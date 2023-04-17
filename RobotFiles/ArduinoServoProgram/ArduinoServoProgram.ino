// Car servo controller program
// Version 1.0.1
// Written 4/5/23

#include "Servo.h"

// Binary Value Pins, gets turned into a 4bit integer in the readBinary() function
#define binInput0 A0
#define binInput1 A1
#define binInput2 A2
#define binInput3 A3
#define binInput4 A4
#define binInput5 A5
#define binInput6 12

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

// byte version of binary input used to direction 
// the correction action to perform
byte direction = 0;
byte speed = 0;

void setup() {
  Serial.begin(9600); // Allows for usb debugging through Tools > Serial Monitor/Serial Plotter

  // Sets binary pins to INPUT
  pinMode(binInput0, INPUT);
  pinMode(binInput1, INPUT);
  pinMode(binInput2, INPUT);
  pinMode(binInput3, INPUT);

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
}

void loop() {
  // Main program
  direction = readBinDirection();
  speed = readBinSpeed(); // Speed is a global variable so will be accessed in function call
  
  // selects what action to perform based on direction number
  if (speed == 0) {
    carStop();
  }
  else if (direction == 0) {
   carForward();
  }
  else if (direction == 1) {
   carBackward();
  }
  else if (direction == 2) {
   carRight();
  }
  else if (direction == 3) {
   carLeft();
  }
  else {
   carStop();
  }
  delay(1);
}

int readBinDirection(){
  // Reads the two data pins for direction
  // and returns a number [0, 3]
  return((digitalRead(binInput0) == HIGH) * 1
       + (digitalRead(binInput1) == HIGH) * 2);
}
int readBinSpeed(){
  // Reads the two data pins for speed
  // and returns a number [0, 3]
  return((digitalRead(binInput2) == HIGH) * 1
       + (digitalRead(binInput3) == HIGH) * 2);
}


void carForward(){
  switch (speed) {
    case 0:
      // Speed is zero so stop
      carStop();
      break;
    case 1:
      // Forward low speed
      servoFrontRight.writeMicroseconds(1332);
      servoFrontLeft.writeMicroseconds(1668);

      servoBackLeft.writeMicroseconds(1668);
      servoBackRight.writeMicroseconds(1332);
      break;
    case 2:
      // Forward medium speed
      servoFrontRight.writeMicroseconds(1166);
      servoFrontLeft.writeMicroseconds(1834);

      servoBackLeft.writeMicroseconds(1834);
      servoBackRight.writeMicroseconds(1166);
      break;
    case 3:
      // Forward max speed
      servoFrontRight.writeMicroseconds(1000);
      servoFrontLeft.writeMicroseconds(2000);

      servoBackLeft.writeMicroseconds(2000);
      servoBackRight.writeMicroseconds(1000);
      break;
    default:
      // If speed is somehow outside range [0, 3]
      // then stop
      carStop();
  }
}

void carBackward(){
  switch (speed) {
    case 0:
      // Speed is zero so stop
      carStop();
      break;
    case 1:
      // Backward low speed
      servoFrontRight.writeMicroseconds(1668);
      servoFrontLeft.writeMicroseconds(1332);

      servoBackLeft.writeMicroseconds(1332);
      servoBackRight.writeMicroseconds(1668);
      break;
    case 2:
      // Backward medium speed
      servoFrontRight.writeMicroseconds(1834);
      servoFrontLeft.writeMicroseconds(1166);

      servoBackLeft.writeMicroseconds(1166);
      servoBackRight.writeMicroseconds(1834);
      break;
    case 3:
      // Backward max speed
      servoFrontRight.writeMicroseconds(2000);
      servoFrontLeft.writeMicroseconds(1000);

      servoBackLeft.writeMicroseconds(1000);
      servoBackRight.writeMicroseconds(2000);
      break;
    default:
      // If speed is somehow outside range [0, 3]
      // then stop
      carStop();
  }
}

void carRight(){
  switch (speed) {
    case 0:
      // Speed is zero so stop
      carStop();
      break;
    case 1:
      // Right low speed
      servoFrontRight.writeMicroseconds(1668);
      servoFrontLeft.writeMicroseconds(1668);

      servoBackLeft.writeMicroseconds(1668);
      servoBackRight.writeMicroseconds(1668);
      break;
    case 2:
      // Right medium speed
      servoFrontRight.writeMicroseconds(1834);
      servoFrontLeft.writeMicroseconds(1834);

      servoBackLeft.writeMicroseconds(1834);
      servoBackRight.writeMicroseconds(1834);
      break;
    case 3:
      // Right max speed
      servoFrontRight.writeMicroseconds(2000);
      servoFrontLeft.writeMicroseconds(2000);

      servoBackLeft.writeMicroseconds(2000);
      servoBackRight.writeMicroseconds(2000);
      break;
    default:
      // If speed is somehow outside range [0, 3]
      // then stop
      carStop();
  }
}

void carLeft(){
  switch (speed) {
    case 0:
      // Speed is zero so stop
      carStop();
      break;
    case 1:
      // Left low speed
      servoFrontRight.writeMicroseconds(1332);
      servoFrontLeft.writeMicroseconds(1332);

      servoBackLeft.writeMicroseconds(1332);
      servoBackRight.writeMicroseconds(1332);
      break;
    case 2:
      // Left medium speed
      servoFrontRight.writeMicroseconds(1166);
      servoFrontLeft.writeMicroseconds(1166);

      servoBackLeft.writeMicroseconds(1166);
      servoBackRight.writeMicroseconds(1166);
      break;
    case 3:
      // Left max speed
      servoFrontRight.writeMicroseconds(1000);
      servoFrontLeft.writeMicroseconds(1000);

      servoBackLeft.writeMicroseconds(1000);
      servoBackRight.writeMicroseconds(1000);
      break;
    default:
      // If speed is somehow outside range [0, 3]
      // then stop
      carStop();
  }
}

void carStop(){
  // Stops car
  servoFrontRight.writeMicroseconds(1500);
  servoFrontLeft.writeMicroseconds(1500);

  servoBackLeft.writeMicroseconds(1500);
  servoBackRight.writeMicroseconds(1500);
}



