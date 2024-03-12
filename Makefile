DEVICE ?= usbserial-0001
BOARD ?= ESP8266
PROJECT ?= sump_pump
FIRMWARE ?= ESP32_GENERIC-20240222-v1.22.2.bin

.PHONY: sync
sync:
	rshell -p /dev/tty.$(DEVICE) -b 115200 "cp -r src/* /pyboard"

.PHONY: terminal
terminal:
	picocom /dev/tty.$(DEVICE) -b 115200

.PHONY: erase
erase:
	esptool.py --port /dev/tty.$(DEVICE) erase_flash

.PHONY: flash
flash:
	esptool.py --port /dev/tty.$(DEVICE) -b 115200 write_flash -z 0x1000 dependencies/$(FIRMWARE)

.PHONY: exe
exe:
	yes | python -m nuitka --follow-imports src/main.py \
	&& mv $(PROJECT).bin bin/$(PROJECT)
