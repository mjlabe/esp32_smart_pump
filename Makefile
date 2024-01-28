DEVICE ?= usbserial-0001

.PHONY: sync
sync:
	rshell -p /dev/tty.$(DEVICE) -b 115200 "cp -r src/esp32/* /pyboard"

.PHONY: terminal
terminal:
	picocom /dev/tty.$(DEVICE) -b 115200

.PHONY: erase
erase:
	esptool.py --port /dev/tty.$(DEVICE) erase_flash

.PHONY: install
install:
	esptool.py --port /dev/tty.$(DEVICE) write_flash -z 0x1000 dependencies/ESP32_GENERIC-20231005-v1.21.0.bin

.PHONY: exe
exe:
	yes | python -m nuitka --follow-imports src/midi_api/for_those_about_to_rock.py \
	&& mv for_those_about_to_rock.bin bin/for_those_about_to_rock
