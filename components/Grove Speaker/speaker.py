import machine
import time

SPEAKER_PIN = machine.Pin(4, machine.Pin.OUT)

def play_tone(frequency, duration):
    period_us = int(1000000 / frequency)
    half_period_us = int(period_us / 2)
    cycles = int(duration * frequency)

    for _ in range(cycles):
        SPEAKER_PIN.on()
        time.sleep_us(half_period_us)
        SPEAKER_PIN.off()
        time.sleep_us(half_period_us)

super_mario_theme = [
    659, 659, 0, 659, 0, 523, 659, 0, 784, 0, 392, 0, 523, 0, 392, 0,
    330, 0, 440, 0, 494, 0, 466, 0, 440, 0, 392, 0, 659, 0, 784, 0,
    880, 0, 698, 0, 784, 0, 659, 0, 523, 0, 587, 0, 494, 0, 523, 0,
    392, 0, 330, 0, 440, 0, 494, 0, 466, 0, 440, 0, 392, 0, 659, 0,
    784, 0, 880, 0, 698, 0, 784, 0, 659, 0, 523, 0, 587, 0, 494, 0
]

super_mario_durations = [
    0.2, 0.2, 0.2, 0.2, 0.2, 0.2, 0.4, 0.2, 0.2, 0.2, 0.2, 0.2, 0.2, 0.2, 0.4, 0.2,
    0.2, 0.2, 0.2, 0.2, 0.2, 0.2, 0.2, 0.2, 0.2, 0.2, 0.2, 0.2, 0.4, 0.2, 0.2, 0.2,
    0.2, 0.2, 0.2, 0.2, 0.2, 0.2, 0.2, 0.2, 0.2, 0.2, 0.2, 0.2, 0.2, 0.2, 0.2, 0.2,
    0.2, 0.2, 0.2, 0.2, 0.2, 0.2, 0.2, 0.2, 0.2, 0.2, 0.4, 0.2, 0.2, 0.2, 0.2, 0.2,
    0.2
]