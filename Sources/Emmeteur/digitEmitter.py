#!/usr/bin/env python
# -*- coding: latin-1 -*-

"""
--pins for each cols and rows--

 4 3 2
 v v v
|1|2|3| < 10
|4|5|6| < 22
|7|8|9| < 27
|*|0|H| < 17
"""

import time, pigpio, vw, os, sys

"""
Functions definition
"""
def verifInput(userInput):
	"Verifie si la chaine donnée est un nombre compris entre 0 et 99"
	if userInput.isdigit() and len(userInput) <= 2:
		return True;
	else:
		return False;

def toDigit(index_col, index_row):
	"Convertit le tuple (ligne, colone) du clavier numerique en nombre et le retourne en string "
	digit = None
	digit = 3 * index_row + 1 # nombre minimum pour la ligne
	return str(digit + index_col) # ajouter le numero de la colone pour obtenir le nombre

def sendToPuck(number_str):
	"Envoie un message au palet numero 'number_str'"
	for x in range(0,5):
		while not tx.ready():
			time.sleep(0.1)
		time.sleep(0.1)
		tx.put("SB"+number_str+"F")
	print "\t\tTerminé !"

"""
Initialisation des variables
"""
TX  = 25 # pin GPIO data emetteur RF
BPS = 1000 # vitesse en bauds
pi  = pigpio.pi()
tx  = vw.tx(pi, TX, BPS)

#pins pour le clavier numerique
cols = [4, 3, 2] #pins colones
rows = [10, 22, 27, 17] # pins lignes

current_value = ""

for col in cols:
	pi.set_mode(col, pigpio.INPUT)
	pi.set_pull_up_down(col, pigpio.PUD_UP)
	pi.set_glitch_filter(col, 2500)

for row in rows:
	pi.set_mode(row, pigpio.OUTPUT)
	pi.write(row, 0)

"""
Script principal
"""
while 1:
	for col in enumerate(cols):
		if pi.read(col[1]) == 0:
			for row in enumerate(rows):
				
				pi.write(row[1], 1)
				time.sleep(0.005) # petit interval entre chaque tranqition
				
				if pi.read(col[1]) == 1:
					tch = toDigit(col[0], row[0]) # dernier digit appuyé
					
					if tch == "10": # touche validé "*" appuyée
						if current_value != "" and verifInput(current_value):

							if int(current_value) <= 9:
								current_value = current_value.zfill(2) # le nombre doit faire 2 caractères
								
							print "Sending  ! your value is {0}".format(current_value)
							sendToPuck(current_value)

						else:
							print "Veuillez entrer un nombre valide..."
						
						current_value = "" # remise à zero de la valeur actuelle après envoie
					
					elif tch == "12": # appuie sur le bouton reset "#"
						current_value = ""
					
					elif tch == "11": # appuie sur la touche "0"
						current_value = current_value + "0"
					
					else:
						current_value = current_value + tch

				pi.write(row[1], 0)
				time.sleep(0.005) # petit interval entre les transitions
			
			time.sleep(0.2) #temps minimum entre 2 appue (pour eviter les repetitions)
