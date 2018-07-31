""" main module """
from __future__ import print_function
import threading
import time
import sys
import numpy as np
from gps import GPS
from MPUThread import MPUThread
from gpiozero import LED
import requests
import json
from datetime import datetime

class Main(object):
    """ main class """

    def __init__(self):
        self.status = 0
        self.API_URL = 'http://192.168.137.1/api.php'

        # thread objects
        self.mpu = MPUThread()
        self.mpu.setDaemon(True)
        # start gps and mpu threads
        self.mpu.start()

        # start leds
        self.good_led = LED(17)
        self.regular_led = LED(27)
        self.bad_led = LED(22)

        # constants
        self.TOTAL_SAMPLING_TIME = 10
        self.REGULAR_LIMIT = 0.15
        self.BAD_LIMIT = 0.35

    def main(self):
        """ executes main block """

        with open("log.csv", 'w') as f:
            try:
                while True:
                    measurements = []
                    start_time = time.time()
                    curr_time = time.time()
                    while curr_time - start_time < self.TOTAL_SAMPLING_TIME:
                        curr_time = time.time()
                        acc_x, acc_y, acc_z = self.mpu.getAccelerationValue()
                        gyr_x, gyr_y, gyr_z = self.mpu.getGyroscopeValue()
                        measurements.append([acc_x, acc_y, acc_z, gyr_x, gyr_y, gyr_z])
                        time.sleep(0.0005)

                    end_time = time.asctime( time.localtime(time.time()) )
                    np_array = np.array(measurements)
                    variance = np.var(np_array, axis=0)
                    print("Variance: " + str(variance[2]) + "\tArray size: " + str(len(measurements)) + "\tTime: " + end_time )

                    if variance[2] < self.REGULAR_LIMIT:
                        # good road
                        self.bad_led.off()
                        self.regular_led.off()
                        self.good_led.on()
                    elif variance[2] < self.BAD_LIMIT:
                        # regular road
                        self.bad_led.off()
                        self.regular_led.on()
                        self.good_led.off()
                        self.send_request(2)
                    else:
                        # bad road
                        self.bad_led.on()
                        self.regular_led.off()
                        self.good_led.off()
                        self.send_request(1)

            except KeyboardInterrupt:
                self.kill_threads()
                return

    def turn_off_all_leds(self):
        self.bad_led.off()
        self.regular_led.off()
        self.good_led.off()

    def turn_on_all_leds(self):
        self.bad_led.on()
        self.regular_led.on()
        self.good_led.on()

    def kill_threads(self):
        print('Closed all threads successfully')
        sys.exit()
        return

    def send_request(self, quality):
        req_json = json.dumps({'latitude': -25.451290, 'longitude': -49.233794,
                                           'quality': quality,
                                           'reading_date': str(datetime.now())})
        headers = {'Content-Type': 'application/json'}
        response = requests.post(self.API_URL, data=req_json, headers=headers)
        print("*** Hole detected! HTTP Return: " + response.reason + " (" +
                str(response.status_code) + ") ***")


if __name__ == "__main__":
    MAIN = Main()
    MAIN.main()
