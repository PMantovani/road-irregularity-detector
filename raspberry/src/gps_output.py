import serial

my_serial = serial.Serial('/dev/ttyS0', 9600, timeout=5)
while True:
    data = my_serial.readline()
    print(data)