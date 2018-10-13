import csv
from continuous_transformer import ContinuousTransformer

axis_independent = True
two_classes = True

transformer = ContinuousTransformer()
transformer.set_axis_independent(axis_independent)

path = 'C:\\Users\\pmant\\Documents\\Repositories\\road-irregularity-detector\\data\\'
raw_filepath = path + 'raw_data.csv'
out_filepath = path + 'processed_data'
if two_classes:
    out_filepath += '_2'
if axis_independent:
    out_filepath += '_axis_indep'
out_filepath += '.csv'

with open(raw_filepath, 'r') as raw_data:
    csv_reader = csv.reader(raw_data)

    for i, row in enumerate(csv_reader):
        transformer.add_reading(row)

with open(out_filepath, 'w') as out_file:

    if axis_independent:
        out_file.write('Road Status,')
        out_file.write('Accelerometer Mean,')
        out_file.write('Accelerometer Variance,')
        out_file.write('Gyroscope Mean,')
        out_file.write('Gyroscope Variance,')
    else:
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

        if two_classes:
            if row[0] == 2:
                row[0] = 1
            elif row[0] == 3:
                row[0] = 2

        for j, column in enumerate(row):
            out_file.write(str(column))

            if j != len(row)-1:
                out_file.write(',') # print comma except for last row

        if i != len(summary_array)-1:
            out_file.write('\n') # print new line in all rows except last
