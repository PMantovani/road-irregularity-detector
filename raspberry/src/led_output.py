""" main module """
from __future__ import print_function
import sys
import pickle
import json
from datetime import datetime
import numpy as np
import serial
from MPUThread import MPUThread
from gpiozero import LED
from MeasurementProcessor import MeasurementProcessor
from GsmDevice import GsmDevice
from GsmHttpConnection import GsmHttpConnection
from GsmApnConfiguration import GsmApnConfiguration
from GsmException import GsmException
from gps import GPS
from threading import Lock

class Main(object):
    """ main class """

    def __init__(self):
        self.status = 0

        # start gps/gsm mux pin
        self.mux = LED(4)
        self.mux.on()

        self.serial_lock = Lock()

        # thread objects
        self.mpu = MPUThread()
        self.mpu.setDaemon(True)
        # start mpu thread
        self.mpu.start()

        # GSM configuration
        self.serial = serial.Serial('/dev/ttyS0', 9600)
        self.gsm = GsmDevice(self.serial)
        self.apn_config = GsmApnConfiguration("zap.vivo.com.br", "vivo", "vivo")
        self.gsm_http_config = GsmHttpConnection("monetovani.com", "", "roads_api.php")
        self.gsm_http_config.set_method('POST')

        self.gps = GPS(self.serial, self.serial_lock)
        self.gps.setDaemon(True)
        self.gps.start()

        # start leds
        self.good_led = LED(17)
        self.regular_led = LED(27)
        self.bad_led = LED(22)
        self.turn_on_all_leds()

        self.svm = pickle.load(open('../../data/model_3_qualities.sav', 'rb'))
        self.measurements = MeasurementProcessor()

        self.detections_buffer = []

    def main(self):
        """ executes main block """

        try:
            while True:

                while not self.measurements.is_buffer_full():
                    acc_x, acc_y, acc_z = self.mpu.getAccelerationValue()
                    gyr_x, gyr_y, gyr_z = self.mpu.getGyroscopeValue()
                    speed = self.gps.get_speed()
                    latitude, longitude = self.gps.get_coordinates()
                    gps_validity = self.gps.is_valid()

                    measurement_unit = [acc_x, acc_y, acc_z, gyr_x, gyr_y, gyr_z,
                                        speed, latitude, longitude, gps_validity]
                    if not self.measurements.add_measurement(measurement_unit):
                        self.turn_off_all_leds()

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

                speed = measurements_output[12]
                start_lat = measurements_output[14]
                start_lng = measurements_output[15]
                end_lat = measurements_output[16]
                end_lng = measurements_output[17]
                detection_time = str(datetime.now())

                self.serial_lock.acquire() # disables serial in GPS for GSM mux
                self.serial.reset_input_buffer() # frees any GPS stuff in read buffer
                self.mux.toggle() # enables GSM to talk
                self.send_detection_to_server([road_quality, speed, start_lat, start_lng,
                                               end_lat, end_lng, detection_time])
                self.mux.toggle() # enables GPS to talk
                self.serial_lock.release()

        except KeyboardInterrupt:
            self.exit()
            return

    def build_request(self, detections):
        obj_representation = []
        for detection in detections:
            obj_representation.append({'sensor_id':       '1',
                                       'quality':         detection[0],
                                       'speed':           detection[1],
                                       'start_latitude':  detection[2],
                                       'start_longitude': detection[3],
                                       'end_latitude':    detection[4],
                                       'end_longitude':   detection[5],
                                       'course':          '360',
                                       'reading_date':    detection[6]})


        data_json = json.dumps(obj_representation)
        return data_json

    def send_detection_to_server(self, detection_body):
        self.detections_buffer.append(detection_body)

        body = self.build_request(self.detections_buffer)
        self.gsm_http_config.set_body(body)

        try:
            code, body = self.gsm.send_http(self.gsm_http_config, self.apn_config)
            print('HTTP request successful.')
            print('Response Code: ' + code)
            print('Response Body: ' + body)
            self.detections_buffer = []
        except GsmException as e:
            print(e.message)

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
