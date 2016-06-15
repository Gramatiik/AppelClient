#!/usr/bin/env python
# -*- coding: latin-1 -*-

"""
SCRIPT DE TEST DU CLAVIER NUMERIQUE
"""

"""
--pins for each cols and rows--

 4 3 2
 v v v
|1|2|3| < 10
|4|5|6| < 22
|7|8|9| < 27
|*|0|H| < 17
"""

import pigpio, time

def toDigit(index_col, index_row):
	"Convertit le tuple (ligne, colone) du clavier numerique en nombre et le retourne en string "
	digit = None

	digit = 3 * index_row + 1 # nombre minimum pour la ligne
	return digit + index_col # ajouter le numero de la colone pour obtenir le nombre

pi = pigpio.pi()


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

while 1:
	for col in enumerate(cols):
		if pi.read(col[1]) == 0:
			for row in enumerate(rows):
				pi.write(row[1], 1)
				time.sleep(0.005) # petit interval entre les transitions
				if pi.read(col[1]) == 1:
					print "button pressed on col {0} and row {1}".format(col[1], row[1]) # affichage des coordonnées de la touche appuyée
					tch = str(toDigit(col[0], row[0]))
					if tch == "10" and current_value != "": # touvhe valider "*" appuyée
						print "Enter pressed ! your value is {0}".format(current_value)
						current_value = "" # remise à zero de la valeur après validation
					elif tch == "12": # touche reset "#" appuyée
						current_value = ""
					elif tch == "11": # touche "0" appuyée
						current_value = current_value + "0"
					else:
						current_value = current_value + tch

				pi.write(row[1], 0)
				time.sleep(0.005) # petit interval entre les transitions
			time.sleep(0.2) # délai entre deux appuie de touche

pi.stop()