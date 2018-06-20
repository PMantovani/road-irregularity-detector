# -*- coding: utf-8 -*-

import numpy as np
import csv
from scipy.fftpack import fft
import matplotlib.pyplot as plt

bad_arr = []
good_arr = []
time_arr = []
rows_bad = 0
rows_good = 0
sample_period_bad = 0
sample_period_good = 0

with open('C:\\Users\\pmant\\Desktop\\steady_bad_road.csv', 'r') as raw_data:
    csv_reader = csv.reader(raw_data)

    for i, row in enumerate(csv_reader):
        if i == 0:
            continue # this will skip header line
        elif i == 1:
            start_time = float(row[10]) # set our initial start_time
        elif i == 2:
            sample_period_bad = float(row[10]) - start_time

        acc_x = float(row[1])
        acc_y = float(row[2])
        acc_z = float(row[3])
        gyr_x = float(row[4])
        gyr_y = float(row[5])
        gyr_z = float(row[6])
        speed = float(row[9])
        time_arr.append(float(row[10]))

        # bad_arr.append([acc_x, acc_y, acc_z, gyr_x, gyr_y, gyr_z])
        bad_arr.append(gyr_x)
        rows_bad += 1

with open('C:\\Users\\pmant\\Desktop\\steady_good_road.csv', 'r') as raw_data:
    csv_reader = csv.reader(raw_data)

    for i, row in enumerate(csv_reader):
        if i == 0:
            continue # this will skip header line
        elif i == 1:
            start_time = float(row[10]) # set our initial start_time
        elif i == 2:
            sample_period_good = float(row[10]) - start_time

        acc_x = float(row[1])
        acc_y = float(row[2])
        acc_z = float(row[3])
        gyr_x = float(row[4])
        gyr_y = float(row[5])
        gyr_z = float(row[6])
        speed = float(row[9])
        time_arr.append(float(row[10]))

        # good_arr.append([acc_x, acc_y, acc_z, gyr_x, gyr_y, gyr_z])
        good_arr.append(gyr_x)
        rows_good += 1

yf_bad = fft(bad_arr)
xf_bad = np.linspace(0, 1.0/(2.0*sample_period_bad), rows_bad//2)
yf_good = fft(good_arr)
xf_good = np.linspace(0, 1.0/(2.0*sample_period_good), rows_good//2)
plt.plot(xf_bad, 2.0/rows_bad * np.abs(yf_bad[0:rows_bad//2]), '-b')
plt.plot(xf_good, 2.0/rows_bad * np.abs(yf_good[0:rows_good//2]), '--r')
plt.legend(['Via em mas condicoes', 'Via em boas condicoes'])
plt.grid()
plt.show()
