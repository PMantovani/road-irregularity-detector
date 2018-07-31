""" main module """
from __future__ import print_function
import threading
from gps import GPS 
from MPUThread import MPUThread
from file_writer import FileWriter
from gpiozero import LED, Button

class Main(object):
    """ main class """

    def __init__(self):    
        self.BAD_LED_PIN = 22
        self.REGULAR_LED_PIN = 27
        self.GOOD_LED_PIN = 17
        self.NO_EVAL_BT_PIN = 0
        self.BAD_BT_PIN = 11
        self.REGULAR_BT_PIN = 9
        self.GOOD_BT_PIN = 10

        self.bad_led = LED(self.BAD_LED_PIN)
        self.regular_led = LED(self.REGULAR_LED_PIN)
        self.good_led = LED(self.GOOD_LED_PIN)

        self.no_eval_bt = Button(self.NO_EVAL_BT_PIN)
        self.no_eval_bt.when_pressed = self.no_evaluation_bt_pressed

        self.bad_bt = Button(self.BAD_BT_PIN)
        self.bad_bt.when_pressed = self.bad_bt_pressed

        self.regular_bt = Button(self.REGULAR_BT_PIN)
        self.regular_bt.when_pressed = self.regular_bt_pressed

        self.good_bt = Button(self.GOOD_BT_PIN)
        self.good_bt.when_pressed = self.good_bt_pressed

        self.status = 0

        # thread objects
        self.gps = GPS()
        self.gps.setDaemon(True)
        self.mpu = MPUThread()
        self.mpu.setDaemon(True)
        self.file_writer = FileWriter(self.gps, self.mpu, self)
        self.file_writer.setDaemon(True)


    def main(self):
        """ executes main block """

        # start gps and mpu threads
        self.gps.start()
        self.mpu.start()

        # starts logging to file
        self.file_writer.start()

        try:
            while True:
                pass
        except KeyboardInterrupt:
            return

    def no_evaluation_bt_pressed(self):
        self.status = 0
        self.bad_led.off()
        self.regular_led.off()
        self.good_led.off()
        print('no eval')

    def bad_bt_pressed(self):
        self.status = 1
        self.bad_led.on()
        self.regular_led.off()
        self.good_led.off()
        print('bad')


    def regular_bt_pressed(self):
        self.status = 2
        self.bad_led.off()
        self.regular_led.on()
        self.good_led.off()
        print('regular')

    def good_bt_pressed(self):
        self.status = 3
        self.bad_led.off()
        self.regular_led.off()
        self.good_led.on()
        print('good')

    def getStatus(self):
        return self.status


if __name__ == "__main__":
    MAIN = Main()
    MAIN.main()
