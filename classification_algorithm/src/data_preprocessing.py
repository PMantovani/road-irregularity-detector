import csv
import math
import time
import numpy as np

continuous_arr = []
out_arr = []

with open('C:\\Users\\pmant\\Documents\\Repositories\\' +
          'road-irregularity-detector\\data\\raw_data.csv', 'r') as raw_data:
    csv_reader = csv.reader(raw_data)

    for i, row in enumerate(csv_reader):
        if i == 0:
            continue # this will skip header line
        elif i == 1:
            start_time = int(row[10]) # set our initial start_time

        road_status = int(row[0])
        acc_x = float(row[1])
        acc_y = float(row[2])
        acc_z = float(row[3])
        gyr_x = float(row[4])
        gyr_y = float(row[5])
        gyr_z = float(row[6])
        speed = float(row[9])
        curr_time = float(row[10])

        if curr_time - start_time >= 10:
            np_array = np.array(continuous_arr)
            variance = np.var(np_array, axis=0)
            mean = np.mean(np_array, axis=0)

            out_arr.append([round(mean[0]), mean[1], variance[1], mean[2],
                            variance[2], mean[3], variance[3]])

            continuous_arr = []
            start_time = float(row[10])
        elif speed < 15:
            continuous_arr = []
            start_time = float(row[10])
        else:
            s_accel = math.sqrt(acc_x**2 + acc_y**2 + acc_z**2)
            s_gyro = math.sqrt(gyr_x**2 + gyr_y**2 + gyr_z**2)
            continuous_arr.append([road_status, s_accel, s_gyro, speed])

with open('C:\\Users\\pmant\\Documents\\Repositories\\' +
          'road-irregularity-detector\\data\\processed_data.csv', 'w') as out_file:

    out_file.write('Road Status,')
    out_file.write('Accelerometer Mean,')
    out_file.write('Accelerometer Variance,')
    out_file.write('Gyroscope Mean,')
    out_file.write('Gyroscope Variance,')
    out_file.write('Speed Mean,')
    out_file.write('Speed Variance\n')

    for i, row in enumerate(out_arr):
        out_file.write(str(row[0]) + ',' + str(row[1]) + ',' + str(row[2]) + ',' +
                       str(row[3]) + ',' + str(row[4]) + ',' + str(row[5]) + ',' + str(row[6]))
        if i != len(out_arr)-1:
            out_file.write('\n') # print new line in all rows except last
