import numpy as np
import math

'''Transforms individual readings into continuous ones'''
class ContinuousTransformer(object):

    def __init__(self):
        self.axis_independent = False
        self.quality = 0
        self.summary_array = []
        self.max_means = [0] * 7
        self.max_variances = [0] * 7
        self.continuous_readings = []
        self.start_time = 0
        self.times_called = 0

    def set_axis_independent(self, axis_independent):
        self.axis_independent = axis_independent

    def add_reading(self, individual_reading):
        self.times_called += 1
        if len(individual_reading) < 11:
            self.__reset_continuous()
            return

        try:
            road_status = int(individual_reading[0])
            acc_x = float(individual_reading[1])
            acc_y = float(individual_reading[2])
            acc_z = float(individual_reading[3])
            gyr_x = float(individual_reading[4])
            gyr_y = float(individual_reading[5])
            gyr_z = float(individual_reading[6])
            lat = float(individual_reading[7])
            lng = float(individual_reading[8])
            speed = float(individual_reading[9])
            curr_time = float(individual_reading[10])
        except ValueError:
            print self.times_called

        if not self.continuous_readings:
            self.quality = road_status
            self.start_time = curr_time

        if (road_status != self.quality or speed > 200 or speed < 15 or
                lat > 90 or lat < -90 or lng > 180 or lng < -180):
            self.__reset_continuous()
            return

        if self.axis_independent:
            acc = math.sqrt(acc_x**2 + acc_y**2 + acc_z**2)
            gyr = math.sqrt(gyr_x**2 + gyr_y**2 + gyr_z**2)
            self.continuous_readings.append([road_status, acc, gyr, lat, lng, speed, curr_time])
        else:
            self.continuous_readings.append([road_status, acc_x, acc_y, acc_z, gyr_x,
                                            gyr_y, gyr_z, lat, lng, speed, curr_time])

        if curr_time - self.start_time >= 10:
            self.__insert_to_summary_array()
            return

    def get_summary_array(self):
        return self.summary_array
        # result = []
        # for row in self.summary_array:
        #     row[1] /= self.max_means[0]
        #     row[2] /= self.max_variances[0]
        #     row[3] /= self.max_means[1]
        #     row[4] /= self.max_variances[1]
        #     row[5] /= self.max_means[2]
        #     row[6] /= self.max_variances[2]
        #     row[7] /= self.max_means[3]
        #     row[8] /= self.max_variances[3]
        #     row[9] /= self.max_means[4]
        #     row[10] /= self.max_variances[4]
        #     row[11] /= self.max_means[5]
        #     row[12] /= self.max_variances[5]
        #     row[13] /= self.max_means[6]
        #     row[14] /= self.max_variances[6]
        #     result.append(row)

        # return result

    def __reset_continuous(self):
        self.quality = 0
        self.continuous_readings = []

    def __insert_to_summary_array(self):
        np_array = np.array(self.continuous_readings)
        variance = np.var(np_array, axis=0)
        mean = np.mean(np_array, axis=0)

        # for i in xrange(len(self.max_means)):
        #     if i == 6:
        #         self.max_means[i] = max(self.max_means[i], abs(mean[9]))
        #         self.max_variances[i] = max(self.max_variances[i], abs(variance[9]))
        #     else:
        #         self.max_means[i] = max(self.max_means[i], abs(mean[i+1]))
        #         self.max_variances[i] = max(self.max_variances[i], abs(variance[i+1]))

        if self.axis_independent:
            self.summary_array.append(
                [mean[0], mean[1], variance[1], mean[2], variance[2], mean[5], variance[5],
                self.continuous_readings[0][3], self.continuous_readings[0][4],
                self.continuous_readings[len(self.continuous_readings)-1][3],
                self.continuous_readings[len(self.continuous_readings)-1][4],
                self.continuous_readings[len(self.continuous_readings)-1][5]])
        else:
            self.summary_array.append(
                [mean[0], mean[1], variance[1], mean[2], variance[2], mean[3], variance[3],
                mean[4], variance[4], mean[5], variance[5], mean[6], variance[6], mean[9], variance[9],
                self.continuous_readings[0][7], self.continuous_readings[0][8],
                self.continuous_readings[len(self.continuous_readings)-1][7],
                self.continuous_readings[len(self.continuous_readings)-1][8],
                self.continuous_readings[len(self.continuous_readings)-1][10]])

        self.__reset_continuous()
