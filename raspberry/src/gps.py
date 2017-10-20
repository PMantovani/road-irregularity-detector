import serial
import time
import sys
import pynmea2
import threading


class GPS(threading.Thread):
    def __init__(self):
        self.port = '/dev/ttyS0'
        self.speed = 9600
        self.msg = None

    def run(self):
        try:
            my_serial = serial.Serial(self.port, self.speed, timeout=5)

            while True:
                data = my_serial.readline()
                if data.startswith("$GPGGA"):
                    self.msg = pynmea2.parse(data)

        except Exception as e:
            sys.stderr.write('Error reading serial port %s: %s\n' % (type(e).__name__, e))