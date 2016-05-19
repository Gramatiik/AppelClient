#!/usr/bin/env python
# -*- coding: latin-1 -*-

import time

import pigpio

import vw

TX=25 # pin GPIO data emetteur RF
BPS=1000 # vitesse en bauds
pi = pigpio.pi()
tx = vw.tx(pi, TX, BPS)

quit = False

while quit == False :

   objStr = raw_input("Entrez le numero du palet : ")

   if objStr.isdigit() and  len(objStr) <= 2:

      if int(objStr) <= 9 :
         objStr = objStr.zfill(2) # pour que le nombre fasse toujours 2 octets

      print "\tEnvoi de la trame au palet {}".format(objStr)

      for x in range(0, 5): # envoie 5 fois la trame pour assurer la reception

         while not tx.ready():
            time.sleep(0.1)

         time.sleep(0.1)

         tx.put("SB"+objStr+"F") # format normalisé de la trame

         print "\t\tAttempt {}".format(x)

tx.cancel()

pi.stop()
