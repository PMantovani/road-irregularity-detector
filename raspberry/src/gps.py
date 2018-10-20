from threading import Thread

class GPS(Thread):
    def __init__(self, serial):
        Thread.__init__(self)
        self.serial = serial
        self.signal_validity = False
        self.latitude = 0.
        self.longitude = 0.
        self.speed = 0.
        self.enabled = True

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

        # tries to parse all values, but if failed, set signal_validity to false
        try:
            lat_raw = float(params[3])
            lng_raw = float(params[5])
            speed_raw = float(params[7])

            # calculates latitude, longitude and speed
            self.latitude = round(self.calculate_decimal(lat_raw, params[4]), 5)
            self.longitude = round(self.calculate_decimal(lng_raw, params[6]), 5)
            self.speed = round(speed_raw*1.852, 2)  # converts from knots to km/h
            self.signal_validity = True
        except ValueError:
            self.signal_validity = False

        return self.latitude, self.longitude, self.speed

    def get_latitude(self):
        return self.latitude

    def get_longitude(self):
        return self.longitude

    def get_coordinates(self):
        return self.latitude, self.longitude

    def get_speed(self):
        return self.speed
        
    def is_valid(self):
        return self.signal_validity

    def disable_serial(self):
        self.enabled = False

    def enable_serial(self):
        self.enabled = True

    def run(self):
        try:
            while True:
                if self.enabled:
                    data = self.serial.readline()
                    if data.startswith("$GPRMC"):
                        self.parse_gprmc(data)

        except Exception:
            return
