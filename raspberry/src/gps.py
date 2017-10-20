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

    def parse_gprmc(self, msg):
        params = msg.split(',')

        if params[2] == 'V':  # checks validity of signal
            self.signal_validity = False
            return
        else:
            self.signal_validity = True

        # calculates latitude
        self.latitude = float(params[3])
        if params[4] == 'S':
            self.latitude *= -1.

        self.longitude = float(params[5])
        if params[6] == 'W':
            self.longitude *= -1.

        self.speed = float(params[7])*1.852

    def run(self):
        try:
            my_serial = serial.Serial(self.port, self.speed, timeout=5)

            while self.run_event.is_set():
                data = my_serial.readline()
                if data.startswith("$GPRMC"):
                    self.parse_gprmc(data)

        except Exception as e:
            sys.stderr.write('Error reading serial port %s: %s\n' % (type(e).__name__, e))