#include "Servo.h"

// Binary Value Pins, gets turned into a 4bit integer in the readBinary() function
#define binInput0 A1
#define binInput1 A2
#define binInput2 A3
#define binInput3 A4

#define demo0 12
#define demo1 11
#define demo2 10
#define demo3 9

Servo servo;
void setup() {
    Serial.begin(9600); // Allows for usb debugging through Tools > Serial Monitor/Serial Plotter

  // Sets binary pins to INPUT
  pinMode(binInput0, INPUT);
  pinMode(binInput1, INPUT);
  pinMode(binInput2, INPUT);
  pinMode(binInput3, INPUT);

  // Sets demo pins to OUTPUT
  pinMode(demo0, OUTPUT);
  pinMode(demo1, OUTPUT);
  pinMode(demo2, OUTPUT);
  pinMode(demo3, OUTPUT);

  pinMode(3, OUTPUT);
  servo.attach(3);
}

void loop() {
  // put your main code here, to run repeatedly:
  digitalWrite(demo0, digitalRead(binInput0));
  digitalWrite(demo1, digitalRead(binInput1));
  digitalWrite(demo2, digitalRead(binInput2));
  digitalWrite(demo3, digitalRead(binInput3));

  servo.write(0);
}
