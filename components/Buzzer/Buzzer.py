import machine
import time

BUZZER_PIN = machine.Pin(4, machine.Pin.OUT)

def buzzer_on():
    BUZZER_PIN.on()

def buzzer_off():
    BUZZER_PIN.off()

while True:
    buzzer_on()
    time.sleep(1)
    buzzer_off()
    time.sleep(1)
