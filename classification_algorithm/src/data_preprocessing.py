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
        if len(row) < 11:
            continuous_arr = []
            continue # this will skip header line
        elif continuous_arr == []:
            start_time = float(row[10]) # set our initial start_time

        road_status = int(row[0])
        acc_x = float(row[1])
        acc_y = float(row[2])
        acc_z = float(row[3])
        gyr_x = float(row[4])
        gyr_y = float(row[5])
        gyr_z = float(row[6])
        lat = float(row[7])
        lng = float(row[8])
        speed = float(row[9])
        curr_time = float(row[10])

        if len(continuous_arr) == 0:
            initial_road_status = road_status

        if curr_time - start_time >= 10:
            np_array = np.array(continuous_arr)
            variance = np.var(np_array, axis=0)
            mean = np.mean(np_array, axis=0)

            out_arr.append([mean[0], mean[1], variance[1], mean[2],
                            variance[2], mean[3], variance[3], mean[4], variance[4],
                            mean[5], variance[5], mean[6], variance[6], mean[7], variance[7],
                            continuous_arr[0][8], continuous_arr[0][9],
                            continuous_arr[len(continuous_arr)-1][8], continuous_arr[len(continuous_arr)-1][9]])

            continuous_arr = []
            start_time = float(row[10])
        elif speed < 15 or initial_road_status != road_status or road_status == 0:
            continuous_arr = []
            start_time = float(row[10])
        else:
            # s_accel = math.sqrt(acc_x**2 + acc_y**2 + acc_z**2)
            # s_gyro = math.sqrt(gyr_x**2 + gyr_y**2 + gyr_z**2)
            # continuous_arr.append([road_status, s_accel, s_gyro, speed])
            continuous_arr.append([road_status, acc_x, acc_y, acc_z, gyr_x, gyr_y, gyr_z, speed, lat, lng])

with open('C:\\Users\\pmant\\Documents\\Repositories\\' +
          'road-irregularity-detector\\data\\processed_data.csv', 'w') as out_file:

    out_file.write('Road Status,')
    out_file.write('Accelerometer X Mean,')
    out_file.write('Accelerometer X Variance,')
    out_file.write('Accelerometer Y Mean,')
    out_file.write('Accelerometer Y Variance,')
    out_file.write('Accelerometer Z Mean,')
    out_file.write('Accelerometer Z Variance,')
    out_file.write('Gyroscope X Mean,')
    out_file.write('Gyroscope X Variance,')
    out_file.write('Gyroscope Y Mean,')
    out_file.write('Gyroscope Y Variance,')
    out_file.write('Gyroscope Z Mean,')
    out_file.write('Gyroscope Z Variance,')
    out_file.write('Speed Mean,')
    out_file.write('Speed Variance,')
    out_file.write('Start Latitude,')
    out_file.write('Start Longitude,')
    out_file.write('End Latitude,')
    out_file.write('End Longitude\n')

    for i, row in enumerate(out_arr):

        # if (row[0] == 2):
        #     row[0] = 1
        # elif(row[0] == 3):
        #     row[0] = 2

        out_file.write(str(row[0]) + ',' + str(row[1]) + ',' + str(row[2]) + ',' +
                       str(row[3]) + ',' + str(row[4]) + ',' + str(row[5]) + ',' +
                       str(row[6]) + ',' + str(row[7]) + ',' + str(row[8]) + ',' +
                       str(row[9]) + ',' + str(row[10]) + ',' + str(row[11]) + ',' +
                       str(row[12]) + ',' + str(row[13]) + ',' + str(row[14]) + ',' +
                       str(row[15]) + ',' + str(row[16]) + ',' + str(row[17]) + ',' +
                       str(row[18]))
        if i != len(out_arr)-1:
            out_file.write('\n') # print new line in all rows except last
