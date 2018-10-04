import csv
import math
import time
from continuous_transformer import ContinuousTransformer

transformer = ContinuousTransformer()

with open('C:\\Users\\pmant\\Documents\\Repositories\\' +
          'road-irregularity-detector\\data\\raw_data.csv', 'r') as raw_data:
    csv_reader = csv.reader(raw_data)

    for i, row in enumerate(csv_reader):
        transformer.add_reading(row)

with open('C:\\Users\\pmant\\Documents\\Repositories\\' +
          'road-irregularity-detector\\data\\processed_data_2.csv', 'w') as out_file:

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
    out_file.write('End Longitude,')
    out_file.write('Epoch Time\n')

    summary_array = transformer.get_summary_array()
    for i, row in enumerate(summary_array):

        if (row[0] == 2):
            row[0] = 1
        elif(row[0] == 3):
            row[0] = 2

        out_file.write(str(row[0]) + ',' + str(row[1]) + ',' + str(row[2]) + ',' +
                       str(row[3]) + ',' + str(row[4]) + ',' + str(row[5]) + ',' +
                       str(row[6]) + ',' + str(row[7]) + ',' + str(row[8]) + ',' +
                       str(row[9]) + ',' + str(row[10]) + ',' + str(row[11]) + ',' +
                       str(row[12]) + ',' + str(row[13]) + ',' + str(row[14]) + ',' +
                       str(row[15]) + ',' + str(row[16]) + ',' + str(row[17]) + ',' +
                       str(row[18]) + ',' + str(row[19]))
        if i != len(summary_array)-1:
            out_file.write('\n') # print new line in all rows except last
