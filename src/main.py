from api import start_server
from hardware import connect

import esp

esp.osdebug(None)


def main():
    connect()
    start_server()


if __name__ == "__main__":
    main()
