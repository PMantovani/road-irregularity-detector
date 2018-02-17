from threading import Thread
import os
import time

class FileWrite(Thread):

    def __init__(self, run_event, gps, accelerometer, my_input):
        Thread.__init__(self)
        self.run_event = run_event
        self.my_accelerometer = accelerometer
        self.my_gps = gps
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
            f.write("Latitude,")
            f.write("Longitude,")
            f.write("Speed,")
            f.write("Time\n")

            while self.run_event.is_set():
                time_num = time.time()
                time_str = "{:.5f}".format(time_num)

                f.write(str(self.my_input.status) + ",")
                f.write(str(self.my_accelerometer.accel_x) + ",")
                f.write(str(self.my_accelerometer.accel_y) + ",")
                f.write(str(self.my_accelerometer.accel_z) + ",")
                f.write(str(self.my_gps.latitude) + ",")
                f.write(str(self.my_gps.longitude) + ",")
                f.write(str(self.my_gps.speed) + ",")
                f.write(time_str + "\n")
                time.sleep(0.01)