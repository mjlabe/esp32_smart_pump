from time import sleep

from hardware import LED, Relay, Sensor, request_post

import env as env


class PumpSimple:
    def __init__(self):
        self.led_pump = LED(env.LED_PUMP)
        self.relay_pump = Relay(env.RELAY_PUMP)
        self.sensor_water_high = Sensor(pin=env.SENSOR_WATER_HIGH)
        try:
            self.device = env.PUMP_DEVICE
        except Exception:
            self.device = "pump"

    def check_water_level(self):
        try:
            print(f"sensor_water_high value: {self.sensor_water_high.value()}")
            # if the water is high, turn on pump for TIME_ON_MIN
            if self.sensor_water_high.high():
                print("sensor_water_high.high")
                self.relay_pump.on()
                self.led_pump.on()

                message = {
                    "device": str(self.device),
                    "state": "on",
                    "cause": "sensor_water_high.high"
                }

                request_post(str(message))

                print("SLEEP")

                sleep(env.TIME_ON_MIN)

                print("i+=1")

            # if the water is not high, turn off the TIME_OFF_MIN
            else:
                print("sensor_water_high.low")
                self.relay_pump.off()
                self.led_pump.off()

                message = {
                    "device": str(self.device),
                    "state": "off",
                    "cause": "sensor_water_high.low"
                }

                request_post(str(message))

                sleep(env.TIME_OFF_MIN)

                i = 0

            # if pump is on for more than defined on time, shut off for defined cooldown time
            print("check cooldown")
            if i * env.TIME_ON_MIN > env.TIME_ON_MAX:
                print("TIME_ON_MAX")
                self.relay_pump.off()
                self.led_pump.off()

            message = {
                "device": str(self.device),
                "state": "off",
                "cause": "TIME_ON_MAX"
            }
            request_post(str(message))

            sleep(env.TIME_OFF_MIN)
            i = 0

        except Exception as error:
            # if there is an error, ignore it; we don't want flooding
            print(error)

        finally:
            sleep(env.TIME_OFF_MIN)
