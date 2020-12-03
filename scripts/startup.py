#!/usr/bin/python

import RPi.GPIO as GPIO
import serial
import time

from atCMD import send_at

enable_dbg_output = False

ser = serial.Serial('/dev/ttyAMA0',115200)
ser.flushInput()

power_key = 4

def power_up():
	if(send_at('AT','OK',1)==1):
	    print('Already active')
	else :
		print('SIM7070X is starting...')
		GPIO.setmode(GPIO.BCM)
		GPIO.setwarnings(False)
		GPIO.setup(power_key,GPIO.OUT)
		time.sleep(0.1)
		GPIO.output(power_key,GPIO.HIGH)
		time.sleep(2)
		GPIO.output(power_key,GPIO.LOW)
		time.sleep(1)
		ser.flushInput()
		while(send_at('AT','OK',1)==0):
	  		time.sleep(1)
	     	send_at('AT','OK',1)
	print('SIM7070X is ready!')


if __name__ == '__main__':
	try:
		power_up()
	except:
		if ser != None:
			ser.close()


	if ser != None:
			ser.close()

