import time
import numpy as np

class MeasurementProcessor(object):

    # constants
    SPEED_LIMIT = 15
    TOTAL_SAMPLING_TIME = 10

    def __init__(self):
        self.measurements = []
        self.start_time = 0
        self.end_time = 0
        self.start_latitude = -1
        self.start_longitude = -1
        self.latest_latitude = -1
        self.latest_longitude = -1

    def add_measurement(self, single_measurement):
        speed = single_measurement[6]
        gps_signal_validity = single_measurement[9]
        latitude = single_measurement[7]
        longitude = single_measurement[8]

        if speed < MeasurementProcessor.SPEED_LIMIT or not gps_signal_validity:
            self.__reset_bufer()
            return False

        if not self.measurements:
            self.start_time = time.time()
            self.start_latitude = latitude
            self.start_longitude = longitude

        self.measurements.append(single_measurement[:9])
        self.end_time = time.time()
        self.latest_latitude = latitude
        self.latest_longitude = longitude
        return True

    def is_buffer_full(self):
        return (self.end_time - self.start_time) > MeasurementProcessor.TOTAL_SAMPLING_TIME

    def get_processed_output(self):
        np_array = np.array(self.measurements)
        variance = np.var(np_array, axis=0)
        mean = np.mean(np_array, axis=0)

        self.__reset_bufer()

        return [mean[0], variance[0], mean[1], variance[1], mean[2], variance[2],
                mean[3], variance[3], mean[4], variance[4], mean[5], variance[5],
                mean[6], variance[6], self.start_latitude, self.start_longitude,
                self.latest_latitude, self.latest_longitude]

    def __reset_bufer(self):
        self.measurements = []
        self.start_time = 0
        self.end_time = 0
