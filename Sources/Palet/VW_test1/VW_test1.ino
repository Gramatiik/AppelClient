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
        
        if(numTrame == NUMPALET) //ciorrespond-t-elle a mon ID ?
        {
          Signal();
          delay(DELAY * 1000); // temps de desactivation
        }
      }
    }
}

void Signal(){
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

