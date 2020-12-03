#!/usr/bin/python

import RPi.GPIO as GPIO
import serial
import time

enable_dbg_output = False

ser = serial.Serial('/dev/ttyAMA0',115200)
ser.flushInput()

rec_buff = ''

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


def send_at_get_result(command,back,timeout):
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
			return rec_buff
		else:
			if(enable_dbg_output): print(rec_buff.decode())
			return rec_buff
	else:
		if(enable_dbg_output): print(command + ' no response')
		return rec_buff



if __name__ == '__main__':
	try:
		print('Will issue AT Test CMD')
		enable_dbg_output = True
		send_at('AT','OK',1)
	except:
		if ser != None:
			ser.close()


	if ser != None:
			ser.close()

