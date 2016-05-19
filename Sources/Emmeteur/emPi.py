#!/usr/bin/env python
# -*- coding: latin-1 -*-
import time, pigpio, vw, os, sys

def usage():
   return "usage : Passer le numero du palet a faire sonner en parametre au script"

def verifInput(str):
   "Vérifie si la chaine est un nombre entre 0 et 99"
   if str.isdigit() and len(str) <= 2:
      return True;
   else:
      return False;

TX  = 25 # pin GPIO data emetteur RF
BPS = 1000 # vitesse en bauds
pi  = pigpio.pi()
tx  = vw.tx(pi, TX, BPS)

if len(sys.argv) == 2:

   objStr = sys.argv[1]
   
   if verifInput(objStr): # 0 <= objstr <= 99 ?
      if int(objStr) <= 9 :
         objStr = objStr.zfill(2) # pour que le nombre fasse toujours 2 caractères

      print "\tEnvoi de la trame au palet {}".format(objStr)

      for x in range(0,5):
         while not tx.ready():
            time.sleep(0.1)
         time.sleep(0.1)
         tx.put("SB"+objStr+"F")
         print "\t\tAttempt {}".format(x)
   else:
      print "veuillez entrer un nombre valide..."
else:
   print usage()

tx.cancel()
pi.stop()
