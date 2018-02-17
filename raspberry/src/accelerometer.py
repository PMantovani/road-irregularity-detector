from threading import Thread
import time
import smbus

class Accelerometer(Thread):
    def __init__(self, run_event):
        Thread.__init__(self)
        self.run_event = run_event
        self.bus = smbus.SMBus(1)  # starts at I2C bus line 1
        self.scale = 2  # number of g's of accelerometer when reading is 16353

        # register constants
        self.MPU_ADDRESS = 0x68  # I2C accelerometer address
        self.REG_PWR_MGMT_1 = 0x6b  # register of power management 1
        self.REG_ACC_X_OFFSET_H = 0x06  # registers for offset
        self.REG_ACC_X_OFFSET_L = 0x07
        self.REG_ACC_Y_OFFSET_H = 0x08
        self.REG_ACC_Y_OFFSET_L = 0x09
        self.REG_ACC_Z_OFFSET_H = 0x0a
        self.REG_ACC_Z_OFFSET_L = 0x0b
        self.REG_ACCEL_XOUT_H = 0x3b
        self.REG_ACCEL_YOUT_H = 0x3d
        self.REG_ACCEL_ZOUT_H = 0x3f
        self.REG_ACCEL_CONFIG = 0x1c

        # other useful constants
        self.ACC_SCALE_LENGTH = 2
        self.ACC_SCALE_START_BIT = 4

        # offset constants
        self.X_OFFSET = 820
        self.Y_OFFSET = 2627
        self.Z_OFFSET = 1310

        # values
        self.accel_x = 0.0
        self.accel_y = 0.0
        self.accel_z = 0.0

    # merge two values to an 8-bit register
    @staticmethod
    def merge_bits(original, value, left_bit_start, length):
        left_shift = (left_bit_start - length + 1)
        # set mask
        mask = ((0x1 << length) - 1) << left_shift
        value <<= left_shift
        value &= mask  # zero the non-target bits in value
        original &= ~mask  # zero the target bits in original value of register
        return original | value  # puts target bits in the original register

    # writes some bits to a register in I2C bus 1, leaving the other bits unchanged
    def write_bits(self, register, value, left_bit_start, length):
        original = self.read_byte(register)
        # don't do anything if reading the byte has failed
        if original is None:
            return None
        new_value = self.merge_bits(original, value, left_bit_start, length)
        return self.write_byte(register, new_value)

    # writes a word to I2C
    def write_word(self, register, value):
        value_h = value >> 8
        value_l = value & 0xFF
        self.write_byte(register, value_h)
        return self.write_byte(register+1, value_l)

    # writes a byte to a register in I2C bus 1
    def write_byte(self, register, value):
        try:
            return self.bus.write_byte_data(self.MPU_ADDRESS, register, value)
        except IOError:
            return None

    # reads a byte from I2C bus 1
    def read_byte(self, register):
        try:
            return self.bus.read_byte_data(self.MPU_ADDRESS, register)
        except IOError:
            return None

    # reads a word from I2C bus 1
    def read_word(self, register):
        try:
            high = self.bus.read_byte_data(self.MPU_ADDRESS, register)
            low = self.bus.read_byte_data(self.MPU_ADDRESS, register + 1)
            val = (high << 8) + low
            return val
        except IOError:
            return None

    # converts word reading into complement of 2
    def read_word_2c(self, register):
        val = self.read_word(register)
        if val >= 0x8000:
            return -((65535 - val) + 1)
        else:
            return val

    # adjusts accelerometer offset
    def set_accelerometer_offset(self, axis, value):
        axis = axis.lower()
        if axis == 'x':
            return self.write_word(self.REG_ACC_X_OFFSET_H, value)
        elif axis == 'y':
            return self.write_word(self.REG_ACC_Y_OFFSET_H, value)
        elif axis == 'z':
            return self.write_word(self.REG_ACC_Z_OFFSET_H, value)
        else:
            return None

    # sets accelerometer scale. Options are: 2, 4, 8 or 16 (g)
    def set_accelerometer_scale(self, new_range):
        if new_range == 2:
            config_bits = 0b00
        elif new_range == 4:
            config_bits = 0b01
        elif new_range == 8:
            config_bits = 0b10
        elif new_range == 16:
            config_bits = 0b11
        else:
            return None

        ret = self.write_bits(self.REG_ACCEL_CONFIG, config_bits, self.ACC_SCALE_START_BIT,
                              self.ACC_SCALE_LENGTH)
        self.scale = new_range
        return ret

    def run(self):
        # get out of power saving mode
        self.bus.write_byte_data(self.MPU_ADDRESS, self.REG_PWR_MGMT_1, 0)
        # set accelerometer offsets
        self.set_accelerometer_offset('x', self.X_OFFSET)
        self.set_accelerometer_offset('y', self.Y_OFFSET)
        self.set_accelerometer_offset('z', self.Z_OFFSET)
        # set accelerometer scale
        self.set_accelerometer_scale(4)

        while self.run_event.is_set():
            try:
                self.accel_x = round(self.read_word_2c(self.REG_ACCEL_XOUT_H)*self.scale/32767., 5)
                self.accel_y = round(self.read_word_2c(self.REG_ACCEL_YOUT_H)*self.scale/32767., 5)
                self.accel_z = round(self.read_word_2c(self.REG_ACCEL_ZOUT_H)*self.scale/32767., 5)
            except TypeError:  # if failed reading an register, just keep going and try again
                pass

            time.sleep(0.01)
