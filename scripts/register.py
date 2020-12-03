#!/usr/bin/python

import RPi.GPIO as GPIO
import serial
import time

from startup import power_up
from shutdown import power_down

from atCMD import send_at
from atCMD import send_at_get_result

enable_dbg_output = False

ser = serial.Serial('/dev/ttyAMA0',115200)
ser.flushInput()

def checkSIM():
    print('Checking SIM status')
    if(send_at('AT+CPIN?','READY',1)==1):
        print('-> SIM ready')
        return 1
    else:
        if(send_at('AT+CPIN?','SIM PIN',1)==1):
            print('-> SIM pin required!')
            return 0
        else:
			print('-> SIM error')
			return 2

# useful for sim cards that have no lte contract
def roamingFix():
    # set preferred mode to automatic (other options are lte or gsm only)
    send_at('AT+CNMP=2','OK',1)

def register():
    print('Try to register network...')
    if(checkSIM()):
        roamingFix()
        # enable network registration
        send_at('AT+CREG=1','OK',1)
        # wait for successful registration
        print('Registering...')
        while(send_at('AT+CREG?','1,1',1)!=1):
            time.sleep(1)
        print('Success!')
        buff = send_at_get_result('AT+COPS?','OK',1)
        print('Registered to: '+buff.split(',')[2])
        

def main():
    try:
        power_up()
        register()
        power_down()
    except:
        if ser != None:
            ser.close()


	if ser != None:
			ser.close()


if __name__ == "__main__":
    main()

