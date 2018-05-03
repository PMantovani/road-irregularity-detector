from I2CDevice import I2CDevice

class MPU6050(I2CDevice):
    def __init__(self):
        # register constants
        self.BUS_LINE = 1
        self.MPU_ADDRESS = 0x68  # I2C accelerometer address
        self.PWR_MGMT_1 = 0x6b  # register of power management 1

        ### ACCELEROMETER REGISTERS ###
        self.ACCEL_CONFIG = 0x1c # register for acc config
        self.ACCEL_SCALE_START_BIT = 4 # first bit of the scale part of the configuration
        self.ACCEL_SCALE_LENGTH = 2 # length in bits of scale configuration 
        self.ACC_X_OFFSET_H = 0x06  # registers for offset
        self.ACC_X_OFFSET_L = 0x07
        self.ACC_Y_OFFSET_H = 0x08
        self.ACC_Y_OFFSET_L = 0x09
        self.ACC_Z_OFFSET_H = 0x0a
        self.ACC_Z_OFFSET_L = 0x0b
        self.ACCEL_XOUT_H = 0x3b # registers for acc measurements
        self.ACCEL_YOUT_H = 0x3d
        self.ACCEL_ZOUT_H = 0x3f

        ### GYROSCOPE REGISTERS ###
        self.GYRO_CONFIG = 0x1b # register for gyro config
        self.GYRO_SCALE_START_BIT = 4 # first bit of the scale part of the configuration
        self.GYRO_SCALE_LENGTH = 2 # length in bits of scale configuration 
        self.GYRO_XOUT_H = 0x43 # registers for gyro measurements
        self.GYRO_YOUT_H = 0x45
        self.GYRO_ZOUT_H = 0x47

        ### CLASS VARIABLES ###
        self.accel_scale = 0.0
        self.gyro_scale = 0.0

        super(MPU6050, self).__init__(self.MPU_ADDRESS, self.BUS_LINE)

    def set_psm_off(self):
        self.bus.write_byte_data(self.MPU_ADDRESS, self.PWR_MGMT_1, 0)

    # set accelerometer scale to: 2g, 4g, 8g or 16g
    def set_accelerometer_scale(self, scale):
        if scale == 2:
            config_bits = 0b00
        elif scale == 4:
            config_bits = 0b01
        elif scale == 8:
            config_bits = 0b10
        elif scale == 16:
            config_bits = 0b11
        else:
            return -1

        ret = self.write_bits(self.ACCEL_CONFIG, config_bits, self.ACCEL_SCALE_START_BIT,
                              self.ACCEL_SCALE_LENGTH)
        self.accel_scale = scale
        return ret

    def set_accelerometer_x_offset(self, offset):
        return self.write_word(self.ACC_X_OFFSET_H, offset)

    def set_accelerometer_y_offset(self, offset):
        return self.write_word(self.ACC_Y_OFFSET_H, offset)

    def set_accelerometer_z_offset(self, offset):
        return self.write_word(self.ACC_Z_OFFSET_H, offset)

    def get_accelerometer_x(self):
        return round(self.read_word_2c(self.ACCEL_XOUT_H)*self.accel_scale/32767., 5)

    def get_accelerometer_y(self):
        return round(self.read_word_2c(self.ACCEL_YOUT_H)*self.accel_scale/32767., 5)

    def get_accelerometer_z(self):
        return round(self.read_word_2c(self.ACCEL_ZOUT_H)*self.accel_scale/32767., 5)

    # set gyro scale to: 250deg/s, 500deg/s, 1000deg/s or 2000deg/s
    def set_gyro_scale(self, scale):
        if scale == 250:
            config_bits = 0b00
        elif scale == 500:
            config_bits = 0b01
        elif scale == 1000:
            config_bits = 0b10
        elif scale == 2000:
            config_bits = 0b11
        else:
            return -1

        ret = self.write_bits(self.GYRO_CONFIG, config_bits, self.GYRO_SCALE_START_BIT,
                              self.GYRO_SCALE_LENGTH)
        self.gyro_scale = scale
        return ret

    def get_gyro_x(self):
        return round(self.read_word_2c(self.GYRO_XOUT_H)*self.gyro_scale/32767., 5)

    def get_gyro_y(self):
        return round(self.read_word_2c(self.GYRO_YOUT_H)*self.gyro_scale/32767., 5)
        
    def get_gyro_z(self):
        return round(self.read_word_2c(self.GYRO_ZOUT_H)*self.gyro_scale/32767., 5)
