import RPi.GPIO as gpio
from gpiozero import LED
import math

def Set_Speed(speed):
    gpio.cleanup()

    dirpin = 14
    mpin = 15

    dir = LED(dirpin)
    mag = math.abs(speed)
    if speed < 0:
        dir.on()
    else:
        dir.off()

    gpio.setmode(gpio.BOARD)
    gpio.setup(mpin, gpio.OUT)
    motor = gpio.PWM(mpin, speed)

    if speed != 0:
        motor.start(50)
    else:
        motor.start(0)