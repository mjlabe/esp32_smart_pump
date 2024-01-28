from time import sleep

from hardware import LED, Relay, Sensor, request_post

import env


def monitor_water():
    led_pump = LED(env.LED_PUMP)
    relay_pump = Relay(env.RELAY_PUMP)

    sensor_water_low = Sensor(pin=9)
    sensor_water_high = Sensor(pin=10)

    on_time = 0
    cycle_time = 0

    while True:
        if sensor_water_high.status() == 1 and cycle_time > 30:
            relay_pump.on()
            led_pump.on()
            on_time += 1
            request_post('{"pump": "on"}')

        elif sensor_water_low.status() == 0:
            relay_pump.off()
            led_pump.off()
            on_time = 0
            cycle_time += 1
            request_post('{"pump": "off"}')

        sleep(1)

        # if pump is on for more than defined on time, shut off for defined cooldown time
        if on_time > env.TIME_ON_MAX:
            relay_pump.off()
            led_pump.off()

            sleep(env.TIME_COOLDOWN)
