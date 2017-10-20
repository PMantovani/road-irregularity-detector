import time
import gps
import threading

if __name__ == "__main__":
    run_event = threading.Event()
    run_event.set()

    my_gps = gps.GPS(run_event)
    my_gps.start()

    try:
        while True:
            print ("Latitude: " + str(my_gps.msg.latitude))
            print ("Longitude: " + str(my_gps.msg.longitude))
            time.sleep(1)
    except KeyboardInterrupt:
        run_event.clear()
        my_gps.join()
        print "Closed all threads successfully"
