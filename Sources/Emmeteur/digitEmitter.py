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
	"Checks if given string is a number between 0 and 99"
	if userInput.isdigit() and len(userInput) <= 2:
		if int(userInput) <= 9:
			userInput = userInput.zfill(2) # number must be 2 chars in length
		return True;
	else:
		return False;

def toDigit(index_col, index_row):
	"Converts the row and column to the physical digit number and returns it in string"
	digit = None
	digit = 3 * index_row + 1 #minimum number for row
	return str(digit + index_col) # add column number to get the right digit

def sendToPuck(number_str):
	"Sends a call to the given number"
	for x in range(0,5):
		while not tx.ready():
			time.sleep(0.1)
		time.sleep(0.1)
		tx.put("SB"+number_str+"F")
	print "\t\tDone !"

"""
Variable initialization
"""
TX  = 25 # RF data emitter GPIO pin
BPS = 1000 # bauds speed
pi  = pigpio.pi()
tx  = vw.tx(pi, TX, BPS)

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

"""
Core script
"""
while 1:
	for col in enumerate(cols):
		if pi.read(col[1]) == 0:
			for row in enumerate(rows):
				
				pi.write(row[1], 1)
				time.sleep(0.005) # small sleeps between transition
				
				if pi.read(col[1]) == 1:
					tch = toDigit(col[0], row[0]) # last pressed digit
					
					if tch == "10": # valid button pressed
						if current_value != "" and verifInput(current_value):
								
							print "Sending  ! your value is {0}".format(current_value)
							sendToPuck(current_value)

						else:
							print "Veuillez entrer un nombre valide..."
						
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
