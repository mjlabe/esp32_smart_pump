from time import sleep
import urequests as requests

try:
    import usocket as socket
except:
    import socket

from machine import Pin
import network
import gc

import env


def connect(ssid=env.WIFI_SSID, password=env.WIFI_PASSWD):
    station = network.WLAN(network.STA_IF)

    station.active(True)
    station.connect(ssid, password)
    
    led_power = LED(env.LED_POWER)
    led_error = LED(env.LED_ERROR)
    relay_pump = Relay(env.RELAY_PUMP)

    led_error.on()
    
    connect_timeout = 30
    
    for s in range(0, connect_timeout):
        if station.isconnected():
            print('Connection successful')
            print(station.ifconfig())
            led_error.off()

        else:
            led_power.blink(repeat=3, delay=0.1)
            led_power.blink(repeat=3, delay=0.5)

    # ESP32 GPIO 26
    led_power.on()

    # RELAY OFF
    relay_pump.off()


def request_post(message):
    print(f"POST {message}")
    try:
        requests.post(
            url=env.LOG_URL,
            json=message
        )
    except Exception as error:
        print(error)


class LED:
    def __init__(self, pin):
        self.pin = Pin(pin, Pin.OUT)
        self.off()

    def blink(self, repeat, delay):
        for _ in range(repeat):
            # RELAY ON
            self.pin.value(1)
            # relay.value(0)
            sleep(delay)
            # RELAY ON
            self.pin.value(0)
            # relay.value(0)
            sleep(delay)
            
    def on(self):
        self.pin.value(1)      
        
    def off(self):
        self.pin.value(0)


class Relay:
    def __init__(self, pin):
        self.pin = Pin(pin, Pin.OUT)
        self.off()

    def on(self):
        self.pin.value(1)

    def off(self):
        self.pin.value(0)


class Sensor:
    def __init__(self, pin):
        self.pin = Pin(pin, mode=Pin.IN, pull=Pin.PULL_UP)

    def low(self):
        is_low = self.pin.value()
        sleep(1)
        is_low = is_low and self.pin.value()
        return not is_low

    def high(self):
        is_high = not self.pin.value()
        sleep(1)
        is_high = is_high and not self.pin.value()
        return is_high

    def value(self):
        return self.pin.value()
