from machine import Pin, ADC
import time

adc = ADC(0)

while True:

    adc_value = adc.read()

    temperature = (adc_value- 0)

    print("Temperature: %.2f Degrees" % temperature)

    time.sleep(1)