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
from GsmThread import GsmThread

class Main(object):
    """ main class """

    def __init__(self):
        self.status = 0

        # thread objects
        self.mpu = MPUThread()
        self.mpu.setDaemon(True)
        # start mpu thread
        self.mpu.start()

        # GSM configuration
        self.gsm = GsmThread(GsmDevice(serial.Serial('/dev/ttyS0', 115200)))
        self.gsm.set_apn_config(GsmApnConfiguration("zap.vivo.com.br", "vivo", "vivo"))
        self.gsm_http_config = GsmHttpConnection("monetovani.com")
        self.gsm.set_http_config(self.gsm_http_config)
        self.gsm.setDaemon(True)
        self.gsm.start()

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
                    speed = self.gsm.get_speed()
                    latitude, longitude = self.gsm.get_coordinates()
                    gps_validity = self.gsm.get_gps_validity()

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

                self.send_detection_to_server([road_quality, speed, start_lat, start_lng,
                                               end_lat, end_lng, detection_time])


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

        self.gsm.trigger_http_request()
        # wait for HTTP response
        while not self.gsm.has_http_response():
            pass

        code, body = self.gsm.get_http_response()

        if code == -1:
            print('GSM Exception while sending HTTP Request')
        else:
            print('HTTP request successful.')
            print('Response Code: ' + code)
            print('Response Body: ' + body)
            self.detections_buffer = []


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
