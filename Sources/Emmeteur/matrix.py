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

import pigpio, time

def toDigit(index_col, index_row):
	touche = None

	touche = 3 * index_row + 1 #minimum number for row
	touche = touche + index_col # add column number to get the right digit 
	return touche

pi = pigpio.pi()


cols = [4, 3, 2] #columns pins
rows = [10, 22, 27, 17] # rows pins

current_value = ""

for col in cols:
	pi.set_mode(col, pigpio.INPUT)
	pi.set_pull_up_down(col, pigpio.PUD_UP)
	pi.set_glitch_filter(col, 2500)

for row in rows:
	pi.set_mode(row, pigpio.OUTPUT)
	pi.write(row, 0)
	
# infinite app loop
while 1:
	for col in enumerate(cols):
		if pi.read(col[1]) == 0:
			for row in enumerate(rows):
				pi.write(row[1], 1)
				time.sleep(0.005) # small sleeps between transition
				if pi.read(col[1]) == 1:
					#print "button pressed on col {0} and row {1}".format(col[1], row[1]) #display pins for row and column pressed
					tch = str(toDigit(col[0], row[0]))
					if tch == "10" and current_value != "": # valid button pressed
						print "Enter pressed ! your value is {0}".format(current_value)
						current_value = "" # reset value after validating it
					elif tch == "12": # reset button pressed
						current_value = ""
					elif tch == "11": # 0 digit pressed
						current_value = current_value + "0"
					else:
						current_value = current_value + tch

				pi.write(row[1], 0)
				time.sleep(0.005) # small sleeps between transition
			time.sleep(0.2) #wait between two inputs

pi.stop()
