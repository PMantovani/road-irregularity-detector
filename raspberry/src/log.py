""" main module """
from __future__ import print_function
import threading
import gps
import accelerometer
import file_write

class Main(object):
    """ main class """

    def __init__(self):
        self.status = 0
        self.run_event = threading.Event()
        self.run_event.set()

        # thread objects
        self.my_gps = gps.GPS(self.run_event)
        self.my_accelerometer = accelerometer.Accelerometer(self.run_event)
        self.my_file_write = file_write.FileWrite(self.run_event, self.my_gps,
                                                  self.my_accelerometer, self)

    def main(self):
        """ executes main block """

        # start gps and accelerometer threads
        self.my_gps.start()
        self.my_accelerometer.start()

        try:
            while self.status == 0:
                reading = self.read_key()
                if reading == 'q':
                    self.kill_threads()
                    return

            # starts logging to file
            self.my_file_write.start()

            while True:
                reading = self.read_key()
                if reading == 'q':
                    self.kill_threads()
                    return

        except KeyboardInterrupt:
            self.kill_threads()
            return

    def read_key(self):
        """ reads an input from stdin and returns it. Also verifies if it's between 1 and 3
            and assigns to status """
        read_input = raw_input('Enter road condition (1-bad, 2-regular, 3-good, q-quit): ')
        if read_input == '1' or read_input == '2' or read_input == '3':
            self.status = read_input
        elif read_input != 'q':
            print('Invalid value. Enter a value from 1 to 3.')
        return read_input

    def kill_threads(self):
        """ kill all threads """
        self.run_event.clear()
        self.my_gps.join()
        self.my_accelerometer.join()
        if self.status != 0:
            self.my_file_write.join()
        print('Closed all threads successfully')
        return



if __name__ == "__main__":
    MAIN = Main()
    MAIN.main()
