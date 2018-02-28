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
        self.run_event = threading.Event()
        self.run_event.set()

        # thread objects
        self.gps = GPS(self.run_event)
        self.mpu = MPUThread(self.run_event)
        self.file_writer = FileWriter(self.run_event, self.gps, self.mpu, self)

    def main(self):
        """ executes main block """

        # start gps and mpu threads
        self.gps.start()
        self.mpu.start()

        try:
            while self.status == 0:
                reading = self.read_key()
                if reading == 'q':
                    self.kill_threads()
                    return

            # starts logging to file
            self.file_writer.start()

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

    def getStatus(self):
        return self.status

    def kill_threads(self):
        """ kill all threads """

        self.run_event.clear()
        self.gps.join()
        self.mpu.join()
        if self.status != 0:
            self.file_writer.join()
        print('Closed all threads successfully')
        return


if __name__ == "__main__":
    MAIN = Main()
    MAIN.main()
