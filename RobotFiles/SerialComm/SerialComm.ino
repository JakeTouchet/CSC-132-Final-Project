#define dataSize 3

void setup() {
  Serial.begin(9600);
}

byte data[dataSize] = {0,0,0};
void loop() {
  delay(10);
  // Discard all but the last bytes in buffer
  while (Serial.available() > dataSize){
    byte discard = Serial.read();
  }
  // If buffer is equal to data then transfer data
  if (Serial.available() == dataSize){
    for (size_t i = 0; i < dataSize; i++)
    {
      data[i] = Serial.read();
    }      
    printData();
  }      
}

void printData(){
  if (Serial.availableForWrite()){
    for (size_t i = 0; i < dataSize; i++)
    {
      Serial.print(data[i]); Serial.print(" ");
    }
    Serial.println();      
  }  
}