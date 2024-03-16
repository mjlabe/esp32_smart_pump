# ESP Smart Pump

Programmatically control pumps around the house with custom parameters and logging.

## Getting started

This app is designed to be used with the [Simple Event Logging](https://github.com/mjlabe/simple_event_logging) app, but 
can be used standalone.

### Assembly

Assemble device as shown in TBD (or however you want and set the pins below).

### Configuration

1. Create a file under `src` named `env.py`
2. Add the following variables and values you desire:
   1. TIME_ON_MIN = 30 (minimum time you want the pump to run^)
   2. TIME_OFF_MIN = 10 (minimum time you want the pump to turn off^)
   3. WIFI_SSID = "your wifi ssid" *
   4. WIFI_PASSWD = "your_wifi_password" *
   5. LOG_URL = "http://url_for_logging/api/log" *
   6. RELAY_PUMP = 19
   7. SENSOR_WATER_LOW = 25

> Note:
> 
> `^` Times should be greater than 10s to avoid short cycling and damaging the motor
> 
> `*` WiFi connection and API are not required. Software will run without it.

### Setup

Run the following command to flash the board with the code:

1. `make erase`
2. `make flash`
3. `make sync`

## Usage

TBD