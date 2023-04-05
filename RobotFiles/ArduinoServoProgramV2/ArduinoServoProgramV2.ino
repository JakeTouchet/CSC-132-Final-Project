// Car servo controller program
// Version 2.0.0
// Written 4/5/23

#include "Servo.h"

// Timer and data pins
#define pinTimer 3
#define pinData 4

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

const byte pulseWidth = 100000; // micro second width of each data pulse
const byte dataSize = 16;
bool recievedData[dataSize];

byte timerStart = 0;
byte speed = 0;
byte direction = 0;


void setup() {
  Serial.begin(9600); // Allows for usb debugging through Tools > Serial Monitor/Serial Plotter

  pinMode(pinTimer, INPUT_PULLUP);
  pinMode(pinData, INPUT);
  attachInterrupt(digitalPinToInterrupt(pinTimer), onInterrupt, RISING);
}

void loop() {
  // put your main code here, to run repeatedly:
  
}

void onInterrupt(){
  noInterrupts(); //Disable interrupts until data read is completed
  readData();
  interrupts(); // Re enables interrupts
}

void readData(){
  
  delayMicroseconds(pulseWidth);
  for (int i; i < dataSize; i++)
  {
    recievedData[i] = digitalRead(pinData);
    delayMicroseconds(pulseWidth);
  }    

  Serial.print("Time = " + String(millis()) + " | ");
  for (bool i : recievedData){
    Serial.print(i);
    pause(1000000);
  }
  Serial.println();

  readSection(&direction, 0, 2);
  readSection(&speed, 3, 7);
  readSection(&timerStart, 8, 15);

  Serial.print("Direction=" + String(direction)); Serial.print(" | Speed=" + String(speed)); Serial.print(" | StartTimer=" + String(timerStart));
  Serial.println();
}

void pause(unsigned long micro){
  unsigned long start = micros();
  while (micros() - start < micro){
    start = start;
  }
}

void readSection(byte* var, byte startIndex, byte endIndex){
  byte temp = 0;
  for (int i = 0; i <= endIndex-startIndex; i++){
    temp += recievedData[i+startIndex] * (pow(2,i) + 0.1);
  }
  *var = temp;
  
}