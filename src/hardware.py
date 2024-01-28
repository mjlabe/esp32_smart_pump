from time import sleep

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
    pump_relay = Relay(env.RELAY_PUMP)

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
    pump_relay.off()


def request_post(message):
    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        if gc.mem_free() < 102000:
            gc.collect()
        conn, addr = sock.accept()
        conn.settimeout(3.0)
        print("Got a connection from %s" % str(addr))
        request = conn.recv(1024)
        conn.settimeout(None)

        conn.send("HTTP/1.1 200 OK\n")
        conn.send("Content-Type: text/html\n")
        conn.send("Connection: close\n\n")
        conn.sendall(message)
    except OSError as e:
        conn.close()
        print("Connection closed")
    finally:
        conn.close()
        print("Connection closed")


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
        self.pin = Pin(pin, Pin.IN)

    def status(self):
        return self.pin()
