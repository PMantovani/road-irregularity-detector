import serial
from GsmDevice import GsmDevice

my_serial = serial.Serial('/dev/ttyS0', 115200, timeout=5)
gps = GsmDevice(my_serial)
gps.enable_gps()
while True:
    print(gps.get_gps_info())