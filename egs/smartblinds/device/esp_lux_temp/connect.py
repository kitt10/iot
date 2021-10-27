import network
import time
import ujson as json

def connect():
    config = open("config.json", "r")
    cfg = json.load(config)
    config.close()

    sta_if = network.WLAN(network.STA_IF)
    ap_if = network.WLAN(network.AP_IF)
    ap_if.active(False)
    if not sta_if.isconnected():
        sta_if.active(True)
        sta_if.connect(cfg["wifi"]['ssid'],cfg["wifi"]['passwd'])
        while not sta_if.isconnected():
            time.sleep_ms(500)