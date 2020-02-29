
void setup() {
  pinMode(7, OUTPUT);
  Serial.begin(9600);
}

void loop() {
  if (Serial.available() > 0) {
    char c = Serial.read();
    if (c == 'i') {
      digitalWrite(7, HIGH);
    }
    if (c == 'j') {
      digitalWrite(7, LOW);
    }
  }
}
