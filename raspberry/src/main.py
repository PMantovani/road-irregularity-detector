import time
import gps
import accelerometer
import threading

if __name__ == "__main__":
    run_event = threading.Event()
    run_event.set()

    # starts gps thread
    my_gps = gps.GPS(run_event)
    my_gps.start()

    # starts accelerometer thread
    my_accelerometer = accelerometer.Accelerometer(run_event)
    my_accelerometer.start()

    # keeps forever in the loop until a keyboard interrupt is detected
    try:
        while True:
            print ("Latitude: " + str(my_gps.msg.latitude))
            print ("Longitude: " + str(my_gps.msg.longitude))
            print ("Accelerometer X: " + str(my_accelerometer.accel_x))
            print ("Accelerometer Y: " + str(my_accelerometer.accel_y))
            print ("Accelerometer Z: " + str(my_accelerometer.accel_z))
            time.sleep(1)
    except KeyboardInterrupt:
        run_event.clear()
        my_gps.join()
        my_accelerometer.join()
        print "Closed all threads successfully!"
