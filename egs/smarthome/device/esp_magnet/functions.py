#FILE WITH FUNCTIONS USED IN ESP8266

import config
import machine
import time

in_led = machine.Pin(2, machine.Pin.OUT)
if (config.PARAMS['ENABLE_EXTERNAL_LED_1']):
    out_led_1 = machine.Pin(config.GPIO['EXTERNAL_LED_1'], machine.Pin.OUT)
if (config.PARAMS['ENABLE_EXTERNAL_LED_2']):
    out_led_2 = machine.Pin(config.GPIO['EXTERNAL_LED_2'], machine.Pin.OUT)    

def internal_led_blick(count,delay):  
    if (config.PARAMS['ENABLE_INTERNAL_LED']):
        for i in range(count):
            in_led.off()
            time.sleep_ms(delay)
            in_led.on()
            time.sleep_ms(delay)       

def external_led_1_blick(count, delay):
    if (config.PARAMS['ENABLE_EXTERNAL_LED_1']):
        for i in range(count):
            out_led_1.on()
            time.sleep_ms(delay)
            out_led_1.off()
            time.sleep_ms(delay)

def external_led_2_blick(count, delay):
    if (config.PARAMS['ENABLE_EXTERNAL_LED_2']):
        for i in range(count):
            out_led_2.on()
            time.sleep_ms(delay)
            out_led_2.off()
            time.sleep_ms(delay)                  