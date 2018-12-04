import RPi.GPIO as io

class Motor:

    def __init__(self, dirPinNum, motorPinNum):
        self.dirPinNum = dirPinNum
        self.motorPinNum = motorPinNum

        io.setwarnings(False)
        io.setmode(io.BOARD)
        io.setup(self.motorPinNum, io.OUT)
        io.setup(self.dirPinNum, io.OUT)
        self.motor = io.PWM(self.motorPinNum, 100)
        self.motor.stop()

    def SetSpeed(self, speed):
        if speed == 0: self.motor.stop(); return
        dirSet = io.HIGH if speed < 0 else io.LOW
        speedAbs = abs(speed)
        self.motor.ChangeFrequency(speedAbs)
        self.motor.start(50)


if __name__ == "__main__":
    M = Motor(10, 11)
    M.SetSpeed(130)
    print('Hello')
        
        
