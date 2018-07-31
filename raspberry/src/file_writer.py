from threading import Thread
import os
import time

class FileWriter(Thread):

    def __init__(self, gps, mpu, my_input):
        Thread.__init__(self)
        self.mpu = mpu
        self.gps = gps
        self.my_input = my_input

    def run(self):
        # creates folder if it doesn't exist
        folder_path = "../../data"
        if not os.path.exists(folder_path):
            os.makedirs(folder_path)
        # create file in this folder
        with open(folder_path + "/raw_data.csv", 'a') as f:
            # f.write("Road Status,")
            # f.write("Accelerometer X,")
            # f.write("Accelerometer Y,")
            # f.write("Accelerometer Z,")
            # f.write("Gyroscope X,")
            # f.write("Gyroscope Y,")
            # f.write("Gyroscope Z,")
            # f.write("Latitude,")
            # f.write("Longitude,")
            # f.write("Speed,")
            # f.write("Time\n")

            reset_status = True

            while True:
                current_status = self.my_input.getStatus()

                if current_status != 0:
                    if reset_status == True:
                        f.write("\n\n")
                        reset_status = False
                    time_num = time.time()
                    time_str = "{:.5f}".format(time_num)

                    acc_x, acc_y, acc_z = self.mpu.getAccelerationValue()
                    gyr_x, gyr_y, gyr_z = self.mpu.getGyroscopeValue()

                    f.write(str(current_status) + ",")
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
                    time.sleep(0.001)
                else:
                    reset_status = True