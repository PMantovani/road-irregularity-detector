import serial
import sys
from threading import Thread


class GPS(Thread):
    def is_valid(self):
        return self.signal_validity

    def __init__(self, run_event):
        Thread.__init__(self)
        self.port = '/dev/ttyS0'
        self.speed = 9600
        self.run_event = run_event
        self.signal_validity = False
        self.latitude = 0.
        self.longitude = 0.
        self.speed = 0.

    @staticmethod
    def convert_degrees(degrees, minutes):
        return degrees + minutes/60.

    def calculate_decimal(self, value, direction):
        degrees = int(value/100)
        minutes = float(value) - (100*degrees)
        abs_degree = self.convert_degrees(degrees, minutes)
        if direction == 'W' or direction == 'S':
            abs_degree *= -1.
        return abs_degree

    def parse_gprmc(self, msg):
        params = msg.split(',')

        if params[2] == 'V':  # checks validity of signal
            self.signal_validity = False
            return
        else:
            self.signal_validity = True

        # calculates latitude
        self.latitude = round(self.calculate_decimal(float(params[3]), params[4]), 5)
        self.longitude = round(self.calculate_decimal(float(params[5]), params[6]), 5)
        self.speed = round(float(params[7])*1.852, 2)  # converts from knots to km/h

        return self.latitude, self.longitude, self.speed

    def run(self):
        try:
            my_serial = serial.Serial(self.port, self.speed, timeout=5)

            while self.run_event.is_set():
                data = my_serial.readline()
                if data.startswith("$GPRMC"):
                    self.parse_gprmc(data)

        except Exception as e:
            sys.stderr.write('Error reading serial port %s: %s\n' % (type(e).__name__, e))