from machine import Pin
import time
from ntptime import settime
import config
import functions

class PirSensor:

  def __init__(self):
    self.pir = Pin(config.GPIO['PIR'], Pin.IN)
    self.motion = False

  def handle_interrupt(self, pin):
    self.motion = True
    global interrupt_pin
    interrupt_pin = pin  

  def catch_motion(self):
    self.pir.irq(trigger=Pin.IRQ_RISING, handler=self.handle_interrupt)
    while True:
      if self.motion:
        functions.external_led_blick(1,1000)
        functions.beep(1,1000)
        self.motion = False
        return True