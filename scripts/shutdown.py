#!/usr/bin/python

import RPi.GPIO as GPIO
import serial
import time

enable_dbg_output = False

ser = serial.Serial('/dev/ttyAMA0',115200)
ser.flushInput()

power_key = 4
rec_buff = ''

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

def send_at(command,back,timeout):
	rec_buff = ''
	ser.write((command+'\r\n').encode())
	time.sleep(timeout)
	if ser.inWaiting():
		time.sleep(0.1 )
		rec_buff = ser.read(ser.inWaiting())
	if rec_buff != '':
		if back not in rec_buff.decode():
			if(enable_dbg_output):
				print(command + ' ERROR')
				print(command + ' back:\t' + rec_buff.decode())
				print('retry...')
			time.sleep(1)
   			send_at(command,back,timeout)
			return 0
		else:
			if(enable_dbg_output): print(rec_buff.decode())
			return 1
	else:
		if(enable_dbg_output): print(command + ' no response')
		return 0

try:
	power_down()
except:
	if ser != None:
		ser.close()


if ser != None:
		ser.close()

