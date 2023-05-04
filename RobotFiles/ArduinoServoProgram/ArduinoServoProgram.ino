// Car servo controller program
// Version 2.1.0
// Written 4/29/23

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

// Expected number of bytes in a command
#define dataSize 4

// Data array
byte data[dataSize] = {0,0,0,0};

// Control variables
unsigned short int timerStart = 0;
byte speed = 0;
byte direction = 0;

// Command Timer
unsigned long commandTimeStop = 0;

// PWM offset from stop speed (1000 ~ 1500) CCW (1500 ~ 2000) CW
int offset;

void setup() {
  Serial.begin(38400); // Allows for usb communication

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
}

void loop() {
  // Discard all but the last three bytes in buffer
  while (Serial.available() > dataSize){
    byte discard = Serial.read();
  }
  // If buffer is equal to data then transfer data
  if (Serial.available() == dataSize){
    // Read data from buffer
    for (size_t i = 0; i < dataSize; i++)
    {
      data[i] = Serial.read();
    }      
    // Assign the first two bytes to timer
    timerStart = data[0] * 256 + data[1];
    // Assign one byte to speed
    speed = data[2];
    // Assign one byte to direction
    direction = data[3];

    // Calculate the time to stop timer based movement
    commandTimeStop = millis() + timerStart * 10;
    printData(); // Send verification it received the data
    changeAction(); // Update the servo behavior
  }     

  // stop car once timer ends
  if (commandTimeStop < millis() && timerStart != 0){
    carStop();
    timerStart = 0;
  }
}

void changeAction(){
  offset = 16*speed;
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

void carForward(){
  Serial.println("Forward");  
  // Forward max speed
  int calibratedOffset = int(offset * 0.86f);
  servoFrontRight.writeMicroseconds(1500 - offset);
  servoFrontLeft.writeMicroseconds(1500 + calibratedOffset);

  servoBackLeft.writeMicroseconds(1500 + calibratedOffset);
  servoBackRight.writeMicroseconds(1500 - offset);
}

void carBackward(){
  Serial.println("Backward");
  // Backward max speed
  servoFrontRight.writeMicroseconds(1500 + offset);
  servoFrontLeft.writeMicroseconds(1500 - offset);

  servoBackLeft.writeMicroseconds(1500 - offset);
  servoBackRight.writeMicroseconds(1500 + offset);
  }

void carRight(){
  Serial.println("Right");
  // Right max speed
  servoFrontRight.writeMicroseconds(1500 + offset);
  servoFrontLeft.writeMicroseconds(1500 + offset);

  servoBackLeft.writeMicroseconds(1500 + offset);
  servoBackRight.writeMicroseconds(1500 + offset);
}

void carLeft(){
  Serial.println("Left");
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
  // Sends a message back with a copy of the information received and formatted
  if (Serial.availableForWrite()){
    for (size_t i = 0; i < dataSize; i++)
    {
      Serial.print(data[i]); Serial.print(" ");
    }
    Serial.println();      
    Serial.print(String(timerStart, DEC) + " " + String(speed, DEC) + " " + String(direction, DEC));
  }  
}