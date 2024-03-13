import esp
import gc

try:
    import usocket as socket
except:
    import socket

from hardware import connect
from api import respond
from sump_pump.pump_simple import PumpSimple

esp.osdebug(None)


def run():
    print("Initializing...")
    pump = PumpSimple()
    pump.relay_pump.off()

    print("Starting Server...")
    try:
        # start server
        try:
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.bind(("", 80))
            sock.listen(5)
        except Exception as e:
            print(f"Error with wireless connection: {e}")

        # main loop
        print("Monitoring...")
        time_on = 0
        while True:
            # try:
            #     if gc.mem_free() < 102000:
            #         gc.collect()
            #     conn, addr = sock.accept()
            #     conn.settimeout(3.0)
            #     print("Got a connection from %s" % str(addr))
            #     request = conn.recv(1024)
            #     conn.settimeout(None)
            #
            #     respond(conn, "")
            # except OSError as e:
            #     conn.close()
            #     print("Connection closed")
            # except Exception as e:
            #     print(f"Error: {e}")
            # finally:
            #     conn.close()
            #     print("Connection closed")

            print("Checking levels")
            print(f"Time On: {time_on}")
            time_on = pump.check_water_level(time_on)
    except:
        print("ERROR: Shutting down...")
        pump.relay_pump.off()


def main():
    try:
        connect()
    except Exception as e:
        print(f"Error connecting to WiFi: {e}")
    run()


if __name__ == "__main__":
    main()
