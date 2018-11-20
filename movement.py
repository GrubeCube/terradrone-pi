#! /usr/bin/env python3

# Author: Gabriel Tamborski
# Author: Thomas Gruber
# Version: 0.9, 11/20/18

import RPi.GPIO as io


class MovementManager:

    LEFT_BACK_DIRECTION_PIN         = 31
    LEFT_BACK_MOTOR_PIN             = 32
    LEFT_FRONT_DIRECTION_PIN        = 33
    LEFT_FRONT_MOTOR_PIN            = 36
    RIGHT_BACK_DIRECTION_PIN        = 35
    RIGHT_BACK_MOTOR_PIN            = 38
    RIGHT_FRONT_DIRECTION_PIN       = 37
    RIGHT_FRONT_MOTOR_PIN           = 40

    class Motor:

        DEFAULT_FREQUENCY   = 100
        DEFAULT_DUTY_CYCLE  = 50

        frequency = DEFAULT_FREQUENCY
        is_moving = False


        def __init__(self, direction_pin, motor_pin):
            self.direction_pin = direction_pin
            self.motor_pin = motor_pin

            io.setwarnings(False)

            io.setmode(io.BOARD)
            io.setup(self.motor_pin, io.OUT)
            io.setup(self.direction_pin, io.OUT)

            self.motor = io.PWM(self.motor_pin, self.frequency)

            # disable movement until start is called
            self.motor.stop()


        def start(self):
            if not self.is_moving and self.frequency != 0:
                # set motor direction
                direction = io.HIGH if frequency < 0 else io.LOW
                io.output(self.direction_pin, direction)

                # set frequency (speed)
                abs_freq = abs(self.frequency)
                self.motor.ChangeFrequency(abs_freq)
                self.motor.start(DEFAULT_DUTY_CYCLE)

                self.is_moving = True


        def stop(self):
            if self.is_moving:
                self.motor.stop()
                self.is_moving = False


    motors = dict()
    is_moving = False


    def __init__(self):
        self.motors["left_back"] = Motor(LEFT_BACK_DIRECTION_PIN, LEFT_BACK_MOTOR_PIN)
        self.motors["left_front"] = Motor(LEFT_FRONT_DIRECTION_PIN, LEFT_FRONT_MOTOR_PIN)
        self.motors["right_back"] = Motor(RIGHT_BACK_DIRECTION_PIN, RIGHT_BACK_MOTOR_PIN)
        self.motors["right_front"] = Motor(RIGHT_FRONT_DIRECTION_PIN, RIGHT_FRONT_MOTOR_PIN)


    def forward(self):
        if not self.is_moving:
            for key, motor in self.motors.items():
                if "left" in key:
                    motor.frequency = -Motor.DEFAULT_FREQUENCY
                elif "right" in key:
                    motor.frequency = Motor.DEFAULT_FREQUENCY
                motor.start()

            self.is_moving = True


    def backward(self):
        if not self.is_moving:
            for key, motor in self.motors.items():
                if "left" in key:
                    motor.frequency = Motor.DEFAULT_FREQUENCY
                elif "right" in key:
                    motor.frequency = -Motor.DEFAULT_FREQUENCY
                motor.start()

            self.is_moving = True


    def rotate_right(self):
        if not self.is_moving:
            for motor in self.motors.values():
                motor.frequency = Motor.DEFAULT_FREQUENCY
                motor.start()

            self.is_moving = True


    def rotate_left(self):
        if not self.is_moving:
            for motor in self.motors.values():
                motor.frequency = -Motor.DEFAULT_FREQUENCY
                motor.start()

            self.is_moving = True


    def stop(self):
        if self.is_moving:
            for motor in self.motors.values():
                motor.stop()
            self.is_moving = False
