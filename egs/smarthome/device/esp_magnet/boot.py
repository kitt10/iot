import esp
import gc
import network
import machine
import time
import config
import functions

esp.osdebug(None)
esp.sleep_type(0)
gc.collect()

def connect():
    sta_if = network.WLAN(network.STA_IF)
    ap_if = network.WLAN(network.AP_IF)
    ap_if.active(False)
    if not sta_if.isconnected():
        sta_if.active(True)
        sta_if.connect(config.WIFI['SSID'],config.WIFI['PASSWD'])
        while not sta_if.isconnected():
            time.sleep_ms(500)

connect()
functions.internal_led_blick(4,100)
functions.external_led_1_blick(2,100)
functions.external_led_2_blick(2,100)