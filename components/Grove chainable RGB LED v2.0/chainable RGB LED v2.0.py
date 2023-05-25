import machine
import neopixel

num_leds = 3  # Number of LEDs in the chain
in_pin = 4    # Input pin (DIN)
out_pin = 5   # Output pin (DOUT)

np = neopixel.NeoPixel(machine.Pin(in_pin), num_leds)

def set_led_color(red, green, blue):
    for i in range(num_leds):
        np[i] = (red, green, blue)
    np.write()

# color red
set_led_color(255,0, 255)