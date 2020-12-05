#!/usr/bin/python

import RPi.GPIO as GPIO
import serial
import time

from startup import power_up
from shutdown import power_down

from atCMD import send_at
from atCMD import send_at_get_result
from atCMD import send_at_add_msg

from register import checkSIM

MQTT_PORT = '1883'
MQTT_SERVER = 'test.mosquitto.org'

def mqttPublish(topic,message):
    print('-> Publish '+message+' to '+topic)
    if('0' in send_at_get_result('AT+SMSTATE?','OK',0.1)):
        initConnection()
    send_at_add_msg('AT+SMPUB="'+topic+'",'+str(len(message))+',0,0','>',0.1,message)

def initConnection():
    send_at_get_result('AT+SMDISC','OK',1) #disconnect from what might be a broken pipe
    send_at('AT+CGMR','OK',0.1)
    send_at('AT+CMEE=0','OK',0.1)
    send_at('AT+CSQ','OK',0.1)
    send_at('AT+CPSI?','OK',0.1)
    send_at('AT+CGREG?','+CGREG: 0,1',0.1)
    
    if('0,0' in send_at_get_result('AT+CNACT?','OK',0.1)):
        send_at('AT+CNACT=0,1','OK',0.5)
        
    if('0' not in send_at_get_result('AT+CACID?','OK',0.1)):
        send_at('AT+CACID=0','OK',0.1)
        
    if('0' in send_at_get_result('AT+SMSTATE?','OK',0.1)):
        send_at('AT+SMCONF="CLIENTID","id"','OK',0.1)
        send_at('AT+SMCONF="URL","'+MQTT_SERVER+'","'+MQTT_PORT+'"','OK',0.1)
        send_at('AT+SMCONF="KEEPTIME",60','OK',0.1)
        send_at('AT+SMCONF="QOS",1','OK',0.1)
        send_at('AT+SMCONN','OK',1)
    
def main():
    try:
        power_up()
        checkSIM()
        mqttPublish('sim','test')
        power_down()
    except:
        print('Exception')
        power_down()


if __name__ == "__main__":
    main()

