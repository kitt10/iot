#FILE WITH FUNCTIONS USED IN ESP8266

import config
import machine
import time

in_led = machine.Pin(2, machine.Pin.OUT)
if (config.PARAMS['ENABLE_EXTERNAL_LED']):
    out_led = machine.Pin(config.GPIO['EXTERNAL_LED'], machine.Pin.OUT)
if (config.PARAMS['ENABLE_BUZZER']):
    buzzer = machine.Pin(config.GPIO['BUZZER'], machine.Pin.OUT)
    buzzer.value(0)

def internal_led_blick(count,delay):  
    if (config.PARAMS['ENABLE_INTERNAL_LED']):
        for i in range(count):
            in_led.off()
            time.sleep_ms(delay)
            in_led.on()
            time.sleep_ms(delay)       

def external_led_blick(count, delay):
    if (config.PARAMS['ENABLE_EXTERNAL_LED']):
        for i in range(count):
            out_led.on()
            time.sleep_ms(delay)
            out_led.off()
            time.sleep_ms(delay)

def beep(count, delay):
    if (config.PARAMS['ENABLE_BUZZER']):
        for i in range(count):
            buzzer.value(1)
            time.sleep_ms(delay)
            buzzer.value(0)
            time.sleep_ms(delay)           