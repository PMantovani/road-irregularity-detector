""" main module """
from __future__ import print_function
import sys
import pickle
from gps import GPS
from MPUThread import MPUThread
from gpiozero import LED
from MeasurementProcessor import MeasurementProcessor
import numpy as np

class Main(object):
    """ main class """

    def __init__(self):
        self.status = 0

        # thread objects
        self.gps = GPS()
        self.gps.setDaemon(True)
        self.mpu = MPUThread()
        self.mpu.setDaemon(True)
        # start gps and mpu threads
        self.gps.start()
        self.mpu.start()

        # start leds
        self.good_led = LED(17)
        self.regular_led = LED(27)
        self.bad_led = LED(22)
        self.turn_on_all_leds()

        self.svm = pickle.load(open('../../data/model_3_qualities.sav', 'rb'))
        self.measurements = MeasurementProcessor()

    def main(self):
        """ executes main block """

        try:
            while True:

                while not self.measurements.is_buffer_full():
                    acc_x, acc_y, acc_z = self.mpu.getAccelerationValue()
                    gyr_x, gyr_y, gyr_z = self.mpu.getGyroscopeValue()
                    speed = self.gps.getSpeed()
                    latitude = self.gps.getLatitude()
                    longitude = self.gps.getLongitude()
                    gps_validity = self.gps.is_valid()

                    measurement_unit = [acc_x, acc_y, acc_z, gyr_x, gyr_y, gyr_z,
                                        speed, latitude, longitude, gps_validity]
                    self.measurements.add_measurement(measurement_unit)

                measurements_output = self.measurements.get_processed_output()
                indicators = np.reshape(measurements_output[:14], (1, -1))

                road_quality = self.svm.predict(indicators)[0]

                if road_quality == 1:
                    self.bad_led.on()
                    self.regular_led.off()
                    self.good_led.off()
                elif road_quality == 2:
                    self.bad_led.off()
                    self.regular_led.on()
                    self.good_led.off()
                else:
                    self.bad_led.off()
                    self.regular_led.off()
                    self.good_led.on()

        except KeyboardInterrupt:
            self.exit()
            return

    def turn_off_all_leds(self):
        self.bad_led.off()
        self.regular_led.off()
        self.good_led.off()

    def turn_on_all_leds(self):
        self.bad_led.on()
        self.regular_led.on()
        self.good_led.on()

    def exit(self):
        """ kill all threads """

        print('Closed all threads successfully')
        sys.exit()
        return


if __name__ == "__main__":
    MAIN = Main()
    MAIN.main()
