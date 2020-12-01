#!/usr/bin/env python3
########################################################################
# Filename    : I2CLCD1602.py
# Description : Use the LCD display data
# Author      : freenove
# modification: 2018/08/03
########################################################################
from PCF8574 import PCF8574_GPIO
from Adafruit_LCD1602 import Adafruit_CharLCD
import RPi.GPIO as GPIO

from time import sleep, strftime
from datetime import datetime
 
ledPin = 11
buttonPin = 12

def setup():
    GPIO.setmode(GPIO.BOARD)
    GPIO.setup(ledPin , GPIO.OUT)
    GPIO.setup(buttonPin, GPIO.IN , pull_up_down=GPIO.PUD_UP)
    
def get_ip():
    cmd = "hostname -I | cut -d\' \' -f1"
    return check_output(cmd, shell=True).decode("utf-8").strip()
 
 
def get_cpu_temp():     # get CPU temperature and store it into file "/sys/class/thermal/thermal_zone0/temp"
    tmp = open('/sys/class/thermal/thermal_zone0/temp')
    cpu = tmp.read()
    tmp.close()
    return '{:.2f}'.format( float(cpu)/1000 ) + ' C'
 
def get_time_now():     # get system time
    return datetime.now().strftime(' %H:%M %d/%m %a')
    
def loop():
    curValue = 0
  
    mcp.output(3,1)     # turn on LCD backlight
    lcd.begin(16,2)     # set number of LCD lines and columns
    
    while(True):         
        if GPIO.input(buttonPin)==GPIO.LOW:
            GPIO.output(ledPin,GPIO.HIGH)
            curValue += 1
            lcd.clear()
        else:
            GPIO.output(ledPin,GPIO.LOW)
    
        
        if curValue == 0:
            #lcd.clear()
            lcd.setCursor(0,0)  # set cursor position
            #lcd.message( 'CPU: ' + get_cpu_temp()+'\n' )# display CPU temperature
            lcd.message(' Current Time : \n' )
            lcd.message( get_time_now() )   # display the 
            sleep(.01)
        
        if curValue == 1:
            #lcd.clear()
            lcd.setCursor(0,0)
            lcd.message( 'CPU: ' + get_cpu_temp() + '\n' )
            lcd.message( 'IP: ' + get_ip())
            #sleep(1)
           
        if curValue == 2:
            #lcd.clear()
            lcd.setCursor(0,0)
            lcd.message('   Happy \n Christmas! ')
            #sleep(1)
            
        if curValue == 3:
            curValue = -1
 
def destroy():
    lcd.clear()
    
PCF8574_address = 0x27  # I2C address of the PCF8574 chip.
PCF8574A_address = 0x3F  # I2C address of the PCF8574A chip.
# Create PCF8574 GPIO adapter.
try:
    mcp = PCF8574_GPIO(PCF8574_address)
except:
    try:
        mcp = PCF8574_GPIO(PCF8574A_address)
    except:
        print ('I2C Address Error !')
        exit(1)
# Create LCD, passing in MCP GPIO adapter.
lcd = Adafruit_CharLCD(pin_rs=0, pin_e=2, pins_db=[4,5,6,7], GPIO=mcp)

if __name__ == '__main__':
    print ('Program is starting ... ')
    setup()
    try:
        loop()
    except KeyboardInterrupt:
        destroy()

