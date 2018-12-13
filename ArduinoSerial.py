'''
Created on May 10, 2017

@author: Gabriel
'''
from tkinter import *
import serial
import time

arduino = serial.Serial('/dev/ttyUSB2', 9600, timeout=.1)
time.sleep(2)

new = True
mssg = None

print('Connected')

def SendToArduino():
    mssg = bytes('a', 'UTF-8')
    arduino.write(mssg)
    arduino.flush()

