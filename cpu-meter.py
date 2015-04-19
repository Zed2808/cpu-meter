#!/usr/bin/python

import RPi.GPIO as GPIO
import subprocess
import math

# Set up GPIO using BCM numbering and disable warnings
GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)

# Set pin number for each LED
led0 = 4
led1 = 17
led2 = 27
led3 = 22
led4 = 18
led5 = 23
led6 = 24
led7 = 25
led8 = 15
led9 = 14

# Put all LED pins into a list
leds = [led0, led1, led2, led3, led4, led5, led6, led7, led8, led9]

# Set all LED pins as outputs and set them LOW
GPIO.setup(leds, GPIO.OUT)
GPIO.output(leds, GPIO.LOW)

try:
	while(True):
		top = subprocess.Popen(['top', '-bn2'], stdout=subprocess.PIPE)
		grep = subprocess.Popen(['grep', 'Cpu(s)'], stdin=top.stdout, stdout=subprocess.PIPE)
		sed = subprocess.Popen(['sed', 's/.*, *\([0-9.]*\)%* id.*/\\1/'], stdin=grep.stdout, stdout=subprocess.PIPE)
		awk = subprocess.Popen(['awk', '{print 100 - $1}'], stdin=sed.stdout, stdout=subprocess.PIPE)
		output = subprocess.check_output(['awk', 'NR==2'], stdin=awk.stdout)
		percent = float(output.split()[0])
		rounded = int(math.ceil(percent/10))

		print percent
		GPIO.output(leds, GPIO.LOW)
		GPIO.output(leds[:rounded], GPIO.HIGH)
except KeyboardInterrupt: # Runs until keyboard interrupt, then runs GPIO cleanup
	GPIO.cleanup()
