from machine import Pin, PWM
import time

red_pin = Pin(0, Pin.OUT)
green_pin = Pin(1, Pin.OUT)
blue_pin = Pin(2, Pin.OUT)

red_pwm = PWM(red_pin)
green_pwm = PWM(green_pin)
blue_pwm = PWM(blue_pin)

red_value = 0
green_value = 0
blue_value = 0

while True:

    for i in range(0, 512):
        red_value = i
        blue_value = 511 - i
        red_pwm.duty(red_value)
        blue_pwm.duty(blue_value)
        time.sleep(0.01)

    for i in range(0, 512):
        green_value = i
        red_value = 511 - i
        green_pwm.duty(green_value)
        red_pwm.duty(red_value)
        time.sleep(0.01)

    for i in range(0, 512):
        blue_value = i
        green_value = 511 - i
        blue_pwm.duty(blue_value)
        green_pwm.duty(green_value)
        time.sleep(0.01)