from gpiozero import LED
from time import sleep

led = LED(17)
dir  = LED(18)

def Go(rps):
	pps = rps * 200
 	t = 1/pps
	fb = 0 if rps < 0 else 1
	if fb == 1: dir.on()
	if fb == 0: dir.off()
	while True:
		led.on()
		time.sleep(t)
		led.off()
		time.sleep(t)
