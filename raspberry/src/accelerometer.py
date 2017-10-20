import smbus
import time
from threading import Thread


class Accelerometer(Thread):
    def __init__(self, run_event):
        Thread.__init__(self)
        self.run_event = run_event
        self.bus = smbus.SMBus(1)  # starts at I2C bus line 1
        self.scale = 2  # number of g's of accelerometer when reading is 16353
        self.address = 0x68  # I2C accelerometer address
        self.power_mgmt_1 = 0x6b  # register of power management 1
        self.reg_acc_x = 0x3b
        self.reg_acc_y = 0x3d
        self.reg_acc_z = 0x3f
        self.accel_x = 0.0
        self.accel_y = 0.0
        self.accel_z = 0.0

    # reads a word from I2C bus 1.
    def read_word(self, register):
        high = self.bus.read_byte_data(self.address, register)
        low = self.bus.read_byte_data(self.address, register+1)
        val = (high << 8) + low
        return val

    # converts word reading into complement of 2
    def read_word_2c(self, register):
        val = self.read_word(register)
        if val >= 0x8000:
            return -((65535 - val) + 1)
        else:
            return val

    def run(self):
        # get out of power saving mode
        self.bus.write_byte_data(self.address, self.power_mgmt_1, 0)

        while self.run_event.is_set():
            self.accel_x = self.read_word_2c(self.reg_acc_x)*self.scale/32767.
            self.accel_y = self.read_word_2c(self.reg_acc_y)*self.scale/32767.
            self.accel_z = self.read_word_2c(self.reg_acc_z)*self.scale/32767.
            time.sleep(0.01)
