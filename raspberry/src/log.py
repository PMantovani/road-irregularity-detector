""" main module """
from __future__ import print_function
import threading
from gps import GPS 
from MPUThread import MPUThread
from file_writer import FileWriter

class Main(object):
    """ main class """

    def __init__(self):
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

        try:
            while self.status == 0:
                reading = self.read_key()
                if reading == 'q':
                    return

            # starts logging to file
            self.file_writer.start()

            while True:
                reading = self.read_key()
                if reading == 'q':
                    return

        except KeyboardInterrupt:
            return

    def read_key(self):
        """ reads an input from stdin and returns it. Also verifies if it's between 1 and 3
            and assigns to status """

        read_input = raw_input('Enter road condition (0-no recording, 1-bad, 2-regular, 3-good, q-quit): ')
        if read_input == '0' or read_input == '1' or read_input == '2' or read_input == '3':
            self.status = read_input
        elif read_input != 'q':
            print('Invalid value. Enter a value from 0 to 3.')
        return read_input

    def getStatus(self):
        return self.status


if __name__ == "__main__":
    MAIN = Main()
    MAIN.main()
