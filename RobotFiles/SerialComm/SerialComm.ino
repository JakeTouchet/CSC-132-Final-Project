void setup() {
  Serial.begin(9600);
}
int n = 0;
void loop() {
  delay(1);
  if (Serial.available())
    n = Serial.read();
  if (Serial.availableForWrite())
    Serial.println(n);
}
