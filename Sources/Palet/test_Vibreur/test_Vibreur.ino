void setup() {
  pinMode(12, OUTPUT); //led
  pinMode(10, OUTPUT); //vibreur
}

void loop() {
  digitalWrite(10, HIGH);
  blinkLed();
  digitalWrite(10, LOW);
  delay(5000);
  
}

void blinkLed()
{
  for(int i=0; i<20; i++) //2 secondes au total
  {
    digitalWrite(12, HIGH);
    delay(50);
    digitalWrite(12, LOW);
    delay(50);
  }
}

