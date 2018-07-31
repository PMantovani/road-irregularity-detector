import csv
import numpy as np
import matplotlib
import matplotlib.pyplot as plt

x_axis_good = []
y_axis_good = []
x_axis_regular = []
y_axis_regular = []
x_axis_bad = []
y_axis_bad = []

with open('C:\\Users\\pmant\\Documents\\Repositories\\' +
          'road-irregularity-detector\\data\\processed_data.csv', 'r') as p_data:
    csv_reader = csv.reader(p_data)  

    for i, row in enumerate(csv_reader):
        if i == 0:
            continue
        if i > 10000:
            break

        status = float(row[0])
        if status == 1:
            # y_axis_bad.append(float(row[2]))
            y_axis_bad.append(float(row[6]))
            x_axis_bad.append(float(row[13]))
        elif status == 2:
            y_axis_regular.append(float(row[6]))
            x_axis_regular.append(float(row[13]))
        else:
            # y_axis_good.append(float(row[2]))
            if float(row[13]) < 1000:
                y_axis_good.append(float(row[6]))
                x_axis_good.append(float(row[13]))

fig, ax = plt.subplots()
ax.plot(x_axis_good, y_axis_good, 'o')
if (len(x_axis_regular) > 0):
    ax.plot(x_axis_regular, y_axis_regular, 'yo')
if (len(x_axis_bad) > 0):
    ax.plot(x_axis_bad, y_axis_bad, 'ro')
plt.show()