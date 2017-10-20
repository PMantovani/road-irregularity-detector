import time
import gps

if __name__ == "__main__":
    my_gps = gps.GPS()
    my_gps.start()

    while True:
        print ("Latitude: " + str(my_gps.msg.latitude))
        print ("Longitude: " + str(my_gps.msg.longitude))
        time.sleep(1)
