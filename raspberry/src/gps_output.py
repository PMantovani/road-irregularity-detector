import serial
from GsmDevice import GsmDevice

my_serial = serial.Serial('/dev/ttyS0', 115200, timeout=5)
while True:
    gps = GsmDevice(my_serial)
    gps.enable_gps()
    print(gps.get_gps_info())