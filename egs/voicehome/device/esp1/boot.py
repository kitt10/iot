import esp
import gc
import network
import machine
import time
import config

esp.osdebug(None)
# esp.sleep_type(0)
gc.collect()
# time.sleep(6)

def connect():
    sta_if = network.WLAN(network.STA_IF)
    ap_if = network.WLAN(network.AP_IF)
    ap_if.active(False)
    if not sta_if.isconnected():
        print('connecting to network...')
        sta_if.active(True)
        sta_if.connect(config.WIFI['SSID'],config.WIFI['PASSWD'])
        while not sta_if.isconnected():
            time.sleep_ms(500)
    print('network config:', sta_if.ifconfig())

connect()