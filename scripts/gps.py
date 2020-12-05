#!/usr/bin/python
# -*- coding:utf-8 -*-

import time

from startup import power_up
from shutdown import power_down

from atCMD import send_at
from atCMD import send_at_get_result

def init_gps():
    print('-> Start GPS session...')
    send_at('AT+CGNSPWR=1','OK',0.1)
    send_at('AT+CGNSCOLD','OK',0.1)

def get_gps_position():
	noFix = True
	while noFix:
		rec_buff = send_at_get_result('AT+CGNSINF','+CGNSINF: ',1)
		if('OK' in rec_buff.decode()):
			if ',,,' in rec_buff or '1,,' in rec_buff:
				print('  -> NO FIX YET')
				#rec_null = False
				print(rec_buff.decode())
				time.sleep(1)
			else:
				noFix = False
				#print("  -> Got a FIX")
				nema_raw = rec_buff.split('+CGNSINF: ')[1]
				return nema_raw.split('\r')[0]
		time.sleep(0.5)

if __name__ == '__main__':
    try:
        power_up()
        init_gps()
      	while True:
           nema_raw = get_gps_position()
           nema = nema_raw.split(',')
           year = nema[2][0:4]
           month = nema[2][4:6]
           day = nema[2][6:8]
           hour = nema[2][8:10]
           minute = nema[2][10:12]
           second = nema[2][12:14]
           lat = nema[3]
           lon = nema[4]
           alt = nema[5]
           print(year+' '+month+' '+day)
           print(hour+':'+minute+':'+second)
           print('Latitude: '+lat)
           print('Longitude: '+lon)
           print('Altitude: '+alt)
           print('Satellites in View: '+nema[14])
           print('------------------------')
    except:
	    print('Exception')
     	power_down()
