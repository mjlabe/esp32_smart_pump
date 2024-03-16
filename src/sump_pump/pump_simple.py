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

    def check_water_level(self, time_on) -> int:
        try:
            # if the water is high, turn on pump for TIME_ON_MIN
            if self.sensor_water_high.high():
                print("sensor_water_high.high")
                self.relay_pump.on()
                self.led_pump.on()

                request_post(
                    {
                        "device": str(self.device),
                        "state": "on",
                        "cause": "sensor_water_high.high"
                    }
                )

                print(f"SLEEP {env.TIME_ON_MIN}")
                sleep(env.TIME_ON_MIN)
                time_on += env.TIME_ON_MIN

            self.relay_pump.off()
            self.led_pump.off()

            request_post(
                {
                    "device": str(self.device),
                    "state": "off",
                    "cause": "TIME_ON_MAX"
                }
            )

            print(f"SLEEP {env.TIME_OFF_MIN}")
            sleep(env.TIME_OFF_MIN)
            time_on = 0

            return time_on

        except Exception as error:
            # if there is an error, ignore it; we don't want to burn out the motor
            print(error)
            request_post(
                {
                    "device": str(self.device),
                    "state": "off",
                    "cause": "error"
                }
            )
            self.relay_pump.off()
            self.led_pump.off()
            sleep(env.TIME_OFF_MIN)
