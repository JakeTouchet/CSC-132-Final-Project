void setup() {
  Serial.begin(9600);
}
int n = 0;
void loop() {
  Serial.println("Hello from Arduino!");
  delay(1000);
  if (Serial.available())
    n = Serial.read();
  if (Serial.availableForWrite())
    Serial.println(n);
}
