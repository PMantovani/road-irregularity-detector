""" main module """
from __future__ import print_function
import threading
from gps import GPS 
from MPUThread import MPUThread
import numpy as np
from gpiozero import LED
import time

class Main(object):
    """ main class """

    def __init__(self):
        self.status = 0
        # self.run_event = threading.Event()
        # self.run_event.set()

        # thread objects
        # self.gps = GPS(self.run_event)
        self.gps = GPS()
        self.gps.setDaemon(True)
        # self.mpu = MPUThread(self.run_event)
        self.mpu = MPUThread()
        self.mpu.setDaemon(True)
        self.good_led = LED(17)
        self.good_led.off()
        self.regular_led = LED(27)
        self.regular_led.off()
        self.bad_led = LED(22)
        self.bad_led.off()

    def main(self):
        """ executes main block """

        # start gps and mpu threads
        self.gps.start()
        self.mpu.start()

        with open("log.txt", "w") as f:
            while True:
                try:
                    speed = self.gps.getSpeed()
                    lat = self.gps.getLatitude()
                    lon = self.gps.getLongitude()
                    acc_x, acc_y, acc_z = self.mpu.getAccelerationValue()
                    gyr_x, gyr_y, gyr_z = self.mpu.getGyroscopeValue()
                    self.good_led.toggle()
                    localtime = time.asctime( time.localtime(time.time()) )

                    my_string = ( "Speed: " + str(round(speed,1)) + "km/h \t" +
                        "Latitude: " + str(round(lat,5)) + "\t" +
                        "Longitude: " + str(round(lon,5)) + "\t" +
                        "Acc X: " + str(round(acc_x,3)) + "g \t" +
                        #   "Acc Y: " + str(acc_y) + "g \t" +
                        "Acc Z: " + str(round(acc_z,3)) + "g \t" +
                        "Gyr X: " + str(round(gyr_x,3)) + "deg/s \t" +
                        #   "Gyr Y: " + str(gyr_y) + "deg/s \t" +
                        "Gyr Z: " + str(round(gyr_z,3)) + "deg/s \t" + localtime + "\n" )
                    print(my_string)
                    f.write(my_string)
                    time.sleep(1)

                except KeyboardInterrupt:
                    self.kill_threads()
                    return


    def kill_threads(self):
        """ kill all threads """

        # self.run_event.clear()
        self.gps.join()
        self.mpu.join()
        print('Closed all threads successfully')
        return


if __name__ == "__main__":
    MAIN = Main()
    MAIN.main()
