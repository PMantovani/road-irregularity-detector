from threading import Thread
import os
import time

class FileWriter(Thread):

    def __init__(self, run_event, gps, mpu, my_input):
        Thread.__init__(self)
        self.run_event = run_event
        self.mpu = mpu
        self.gps = gps
        self.my_input = my_input

    def run(self):
        # creates folder if it doesn't exist
        folder_path = "../data"
        if not os.path.exists(folder_path):
            os.makedirs(folder_path)
        # create file in this folder
        with open(folder_path + "/data.csv", 'w') as f:
            f.write("Road Status,")
            f.write("Accelerometer X,")
            f.write("Accelerometer Y,")
            f.write("Accelerometer Z,")
            f.write("Gyroscope X,")
            f.write("Gyroscope Y,")
            f.write("Gyroscope Z,")
            f.write("Latitude,")
            f.write("Longitude,")
            f.write("Speed,")
            f.write("Time\n")

            while self.run_event.is_set():
                time_num = time.time()
                time_str = "{:.5f}".format(time_num)

                acc_x, acc_y, acc_z = self.mpu.getAccelerationValue()
                gyr_x, gyr_y, gyr_z = self.mpu.getGyroscopeValue()

                f.write(str(self.my_input.getStatus()) + ",")
                f.write(str(acc_x) + ",")
                f.write(str(acc_y) + ",")
                f.write(str(acc_z) + ",")
                f.write(str(gyr_x) + ",")
                f.write(str(gyr_y) + ",")
                f.write(str(gyr_z) + ",")
                f.write(str(self.gps.getLatitude()) + ",")
                f.write(str(self.gps.getLongitude()) + ",")
                f.write(str(self.gps.getSpeed()) + ",")
                f.write(time_str + "\n")
                time.sleep(0.05)