void setup() {
  Serial.begin(9600);
  pinMode(13, OUTPUT);
  pinMode(12, OUTPUT);
  pinMode(11, OUTPUT);
}
void loop() {
  Serial.println("Hello from Arduino!");
  delay(1000);
  int n = Serial.read() - '0';
  allOff();
  if (n % 3 == 0) {
    digitalWrite(13,1);
  }
  else if (n % 3 == 1) {
    digitalWrite(12,1);
  }
  else if (n % 3 == 2) {
    digitalWrite(11,1);
  }
  Serial.println(n);
}

void allOff(){
  digitalWrite(13,0);
  digitalWrite(12,0);
  digitalWrite(11,0);
}