#!/usr/bin/python

import RPi.GPIO as GPIO
import serial
import time

from atCMD import send_at

enable_dbg_output = False

ser = serial.Serial('/dev/ttyAMA0',115200)
ser.flushInput()

power_key = 4

def power_down():
    	if(send_at('AT','OK',1)!=1):
    	    print('Already powered off')
    	else :
  			print('Shutting SIM7070X down...')
			GPIO.setmode(GPIO.BCM)
			GPIO.setwarnings(False)
			GPIO.setup(power_key,GPIO.OUT)
			time.sleep(0.1)
			GPIO.output(power_key,GPIO.HIGH)
			time.sleep(2)
			GPIO.output(power_key,GPIO.LOW)
			time.sleep(1)
			ser.flushInput()
			while(send_at('AT','OK',1)==1):
    	  			time.sleep(1)
    	     		send_at('AT','OK',1)
	
    	print('SIM7070X is sleeping!')

if __name__ == '__main__':
	try:
		power_down()
	except:
		if ser != None:
			ser.close()
	
	
	if ser != None:
			ser.close()

