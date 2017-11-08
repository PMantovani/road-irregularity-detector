from __future__ import print_function
import time
import gps
import accelerometer
import threading
import requests
import json


class Main:
    def __init__(self):
        self.API_URL = 'http://localhost:8080/api.php'
        self.ACCEL_SCALE = 8
        self.ACCEL_LIMIT = 4
        self.SPEED_LIMIT = 30
        self.SLEEP_AFTER_REQ = 10
        self.SLEEP_REPEAT = 0.01

        run_event = threading.Event()
        run_event.set()

        # starts gps thread
        my_gps = gps.GPS(run_event)
        my_gps.start()

        # starts accelerometer thread
        my_accelerometer = accelerometer.Accelerometer(run_event)
        my_accelerometer.start()
        my_accelerometer.set_accelerometer_scale(self.ACCEL_SCALE)

        # prints console header
        self.print_header()

        # keeps forever in the loop until a keyboard interrupt is detected
        try:
            while True:
                abs_accel_z = abs(my_accelerometer.accel_z)
                signal_validity = my_gps.signal_validity
                longitude = my_gps.longitude
                latitude = my_gps.latitude
                speed = my_gps.speed

                self.print_log(abs_accel_z, signal_validity, longitude, latitude, speed)

                # gps signal not available or speed under 30km/h
                if not signal_validity or speed < self.SPEED_LIMIT:
                    continue
                # irregularity detected! send request to server
                elif abs_accel_z > self.ACCEL_LIMIT:
                    req_json = json.dumps({'latitude': latitude, 'longitude': longitude,
                                           'accelerometer': abs_accel_z, 'speed': speed})
                    headers = {'Content-Type': 'application/json'}
                    response = requests.post(self.API_URL, data=req_json, headers=headers)
                    print("*** Hole detected! HTTP Return: " + response.reason + " (" +
                          str(response.status_code) + ") ***")
                    time.sleep(self.SLEEP_AFTER_REQ)

                time.sleep(self.SLEEP_REPEAT)

        except KeyboardInterrupt:
            run_event.clear()
            my_gps.join()
            my_accelerometer.join()
            print("Closed all threads successfully!")

    @staticmethod
    def print_header():
        print("|\tDetection Status\t|\tGPS Status\t|\tSpeed Threshold\t|\tAcceleration\t"
              "|\tLatitude\t|\tLongitude\t|\tSpeed")

    def print_log(self, acc, val, lat, lng, spd):
        if acc < self.ACCEL_LIMIT:
            acc_status = "No Detection"
        else:
            acc_status = "Detection"

        if val:
            gps_status = "GPS Signal Valid"
        else:
            gps_status = "No GPS Signal"

        if spd < self.SPEED_LIMIT:
            spd_status = "Speed under threshold"
        else:
            spd_status = "Speed above threshold"

        print("|\t" + acc_status + "\t|\t" + gps_status + "\t|\t" + spd_status + "\t|\t" + str(acc) + "\t|\t" +
              str(lat) + "\t|\t" + str(lng) + "\t|\t" + str(spd))


# main entry point
if __name__ == "__main__":
    main = Main()
