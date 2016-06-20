#include <VirtualWire.h>
#include <VirtualWire_Config.h>
#include "Config.h"

String numTrame;

void setup()
{
    pinMode(PINLED, OUTPUT);

    vw_setup(1000);  // bauds
    vw_rx_start();
}

void loop()
{
    uint8_t buf[VW_MAX_MESSAGE_LEN];
    uint8_t buflen = VW_MAX_MESSAGE_LEN;

    if (vw_get_message(buf, &buflen)) //un message est détecté
    {
      //verifications de la trame :
      if( buflen == 5 && buf[0] == 'S' & buf[1] == 'B' && buf[4] == 'F' ) //la trame est OK
      {
        numTrame = String((char)buf[2]);
        numTrame += (char)buf[3];
        
        if(numTrame == NUMPALET) //correspond-t-elle a mon ID ?
        {
          Signal(SIGNALPATTERN);
          delay(DELAY * 1000); // temps de desactivation
        }
      }
    }
}

void Signal(int number){
  switch(number) 
  {
    case 1:
    Signal_1();
    break;

    case 2:
    Signal_2();
    break;

    case 3:
    Signal_3();
    break;

    default:
    Signal_1();
  }
}

void Signal_1() { //signal simple
  digitalWrite(PINVIBRO, HIGH);
  for(int i=0; i<20; i++)
  {
    digitalWrite(PINLED, HIGH);
    delay(100);
    digitalWrite(PINLED, LOW);
    delay(100);
  }
  digitalWrite(PINVIBRO, LOW);
}

void Signal_2() { // signal double vibration, clignottement plus lent
  digitalWrite(PINVIBRO, HIGH);
  for (int i=0; i<5; i++)
  {
    digitalWrite(PINLED, HIGH);
    delay(100);
    digitalWrite(PINLED, LOW);
    delay(100);
  }
  digitalWrite(PINVIBRO, LOW);
  delay(200);
  digitalWrite(PINVIBRO, HIGH);
  for (int i=0; i<5; i++)
  {
    digitalWrite(PINLED, HIGH);
    delay(100);
    digitalWrite(PINLED, LOW);
    delay(100);
  }
  digitalWrite(PINVIBRO, LOW);
}

void Signal_3() //Signal vibrations plus rapides, clignottement led synchro
{
  for (int i=0; i<10; i++)
  {
    digitalWrite(PINVIBRO, HIGH);
    digitalWrite(PINLED, HIGH);
    delay(300);
    digitalWrite(PINVIBRO, LOW);
    digitalWrite(PINLED, LOW);
    delay(300);
  }
}

