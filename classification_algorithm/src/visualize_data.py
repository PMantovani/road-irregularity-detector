import numpy as np
import matplotlib.pyplot as plt
import csv

values = np.empty([30000, 11])

with open('C:\Users\pmant\Documents\Repositories\\road-irregularity-detector\data\quatro_barras.csv', 'rb') as csvfile:
    reader = csv.reader(csvfile)
    i = 0
    first_line = True

    for row in reader:
        if not first_line:
            values[i] = row
            i += 1
        else:
            first_line = False

plt.subplot(3,1,1)
plt.plot(values[:,1], '.', label='Acc X')
plt.plot(values[:,2], '.', label='Acc Y')
plt.plot(values[:,3], '.', label='Acc Z')
plt.xlabel('time (s)')
plt.ylabel('Acceleration (g)')

plt.subplot(3,1,2)
plt.plot(values[9000:10000,4], '.', label='Gyr X')
# plt.plot(values[:,5], '.', label='Gyr Y')
# plt.plot(values[:,6], '.', label='Gyr Z')
plt.xlabel('time (s)')
plt.ylabel('X Acceleration')

plt.subplot(3,1,3)
plt.plot(values[:,9], '.', label='Speed')
plt.xlabel('time (s)')
plt.ylabel('Speed km/h')

plt.show()