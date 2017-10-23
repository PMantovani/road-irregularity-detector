import time
import gps
import accelerometer
import threading
import os

if __name__ == "__main__":
    run_event = threading.Event()
    run_event.set()

    # starts gps thread
    my_gps = gps.GPS(run_event)
    my_gps.start()

    # starts accelerometer thread
    my_accelerometer = accelerometer.Accelerometer(run_event)
    my_accelerometer.start()

    # creates folder if it doesn't exist
    folder_path = "../data"
    if not os.path.exists(folder_path):
        os.makedirs(folder_path)
    # create file in this folder
    with open(folder_path + "/data.csv", 'w') as f:
        f.write("Accelerometer X,")
        f.write("Accelerometer Y,")
        f.write("Accelerometer Z,")
        f.write("Latitude,")
        f.write("Longitude,")
        f.write("Speed,")
        f.write("Time,\n")

        # keeps forever in the loop until a keyboard interrupt is detected
        try:
            while True:
                f.write(str(my_accelerometer.accel_x) + ",")
                f.write(str(my_accelerometer.accel_y) + ",")
                f.write(str(my_accelerometer.accel_z) + ",")
                f.write(str(my_gps.latitude) + ",")
                f.write(str(my_gps.longitude) + ",")
                f.write(str(my_gps.speed) + ",")
                f.write(str(time.time()) + "\n")
                time.sleep(0.01)
        except KeyboardInterrupt:
            run_event.clear()
            my_gps.join()
            my_accelerometer.join()
            print "Closed all threads successfully!"
