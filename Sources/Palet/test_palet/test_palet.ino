#include "Config.h"

void setup()
{
    pinMode(PINLED, OUTPUT);
    pinMode(PINVIBRO, OUTPUT);
}

void loop()
{
  Signal();
  delay(DELAY * 1000); // temps de desactivation
}

void Signal()
{
  digitalWrite(PINVIBRO, HIGH);
  for(int i=0; i<20; i++)
  {
    digitalWrite(PINLED, HIGH);
    delay(50);
    digitalWrite(PINLED, LOW);
    delay(50);
  }
  digitalWrite(PINVIBRO, LOW);
}

