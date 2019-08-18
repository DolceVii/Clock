#!/usr/bin/env python3

import RPi.GPIO as GPIO
import time
import datetime
from threading import Thread

global memory
global loopa

memory = 0
loopa = 0

GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)
 
# GPIO ports for the 7seg pins
segments =  (11,4,23,8,7,10,18,25,12)
# 7seg_segment_pins (11,7,4,2,1,10,5,3) +  100R inline
 
for segment in segments:
    GPIO.setup(segment, GPIO.OUT)
    GPIO.output(segment, 0)
 
# GPIO ports for the digit 0-3 pins 
digits = (22,27,17,24)
# 7seg_digit_pins (12,9,8,6) digits 0-3 respectively
 
for digit in digits:
    GPIO.setup(digit, GPIO.OUT)
    GPIO.output(digit, 0)
 
num = {
    ' ':(1,1,1,1,1,1,1),
    '0':(0,0,0,0,0,0,1),
    '1':(1,0,0,1,1,1,1),
    '2':(0,0,1,0,0,1,0),
    '3':(0,0,0,0,1,1,0),
    '4':(1,0,0,1,1,0,0),
    '5':(0,1,0,0,1,0,0),
    '6':(0,1,0,0,0,0,0),
    '7':(0,0,0,1,1,1,1),
    '8':(0,0,0,0,0,0,0),
    '9':(0,0,0,0,1,0,0)}

GPIO.output(12, 1)

def FiveSecond():
    global memory
    memory = 1
    while memory == 1:
        global loopa
        loopa = 1
        time.sleep(5)
        loopa = 2
        time.sleep(5)
        loopa = 3
        time.sleep(5)
 
try:
    if memory == 0:
        FiveSecondThread = Thread(target = FiveSecond) 
        FiveSecondThread.start()
        memory = 1

    while True:
        if loopa == 1:
            GPIO.output(12, 1)
            n = time.ctime()[11:13]+time.ctime()[14:16]
            s = str(n).rjust(4)
            for digit in range(4):
                for loop in range(0,7):
                    GPIO.output(segments[loop], num[s[digit]][loop])
                    if (int(time.ctime()[18:19])%2 == 0) and (digit == 0):
                        GPIO.output(25, 0)
                    else:
                        GPIO.output(25, 1)
                GPIO.output(digits[digit], 1)
                time.sleep(0.004)
                GPIO.output(digits[digit], 0)

        if loopa == 2:
            m = datetime.datetime.now()
            m = m.strftime("%d%m")
            g = str(m).rjust(4)
            for digit3 in range(4):
                for loopss in range(0,7):
                    GPIO.output(segments[loopss], num[g[digit3]][loopss])
                GPIO.output(digits[digit3], 1)
                if (GPIO.input(27) == False):
                    GPIO.output(12,1)
                else:
                    GPIO.output(12,0)
                time.sleep(0.004)
                GPIO.output(digits[digit3], 0)
                if (GPIO.input(27) == False):
                    GPIO.output(12,1)
                else:
                    GPIO.output(12,0)

        if loopa == 3:
            GPIO.output(12, 1)
            GPIO.output(25, 1)
            f = time.ctime()[20:26]
            d = str(f).rjust(4)
            for digit2 in range(4):
                for loops in range(0,7):
                    GPIO.output(segments[loops], num[d[digit2]][loops])  
                GPIO.output(digits[digit2], 1)
                time.sleep(0.004)
                GPIO.output(digits[digit2], 0)
              
finally:
    GPIO.cleanup()
    memory = 0
