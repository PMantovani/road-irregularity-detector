import serial
import time
import sys
from micropyGPS import MicropyGPS

port = '/dev/ttyS0'
my_gps = MicropyGPS()

try:
    my_serial = serial.Serial(port, 9600, timeout=5)

    while True:
        data = my_serial.read(16)
        my_gps.update(data)

        print my_gps.latitude
        print my_gps.longitude
        print my_gps.speed
        time.sleep(1)

except Exception as e:
    sys.stderr.write('Error reading serial port %s: %s\n' % (type(e).__name__, e))
