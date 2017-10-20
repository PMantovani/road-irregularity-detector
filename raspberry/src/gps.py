import serial
import time
import sys
import pynmea2

port = '/dev/ttyS0'

try:
    my_serial = serial.Serial(port, 9600, timeout=5)

    while True:
        data = my_serial.readline()
	if (data.startswith("$GPGGA")):
		msg = pynmea2.parse(data)
        	print 'Latitude: ' + str(msg.latitude)
        	print 'Longitude: ' + str(msg.longitude)

except Exception as e:
    sys.stderr.write('Error reading serial port %s: %s\n' % (type(e).__name__, e))
