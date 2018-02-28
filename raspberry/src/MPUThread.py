from MPU6050 import MPU6050
from threading import Thread
import time

class MPUThread(Thread):
    def __init__(self, run_event):
        Thread.__init__(self)
        self.run_event = run_event
        self.mpu = MPU6050()

        # offset constants
        self.X_OFFSET = 820
        self.Y_OFFSET = 2627
        self.Z_OFFSET = 1310

        self.accel_x = 0.0
        self.accel_y = 0.0
        self.accel_z = 0.0
        self.gyro_x = 0.0
        self.gyro_y = 0.0
        self.gyro_z = 0.0
    
    def getAccelerationValue(self):
        return self.accel_x, self.accel_y, self.accel_z
    
    def getGyroscopeValue(self):
        return self.gyro_x, self.gyro_y, self.gyro_z

    def run(self):
        # get out of power saving mode
        self.mpu.set_psm_off()
        # set accelerometer offsets
        self.mpu.set_accelerometer_x_offset(self.X_OFFSET)
        self.mpu.set_accelerometer_y_offset(self.Y_OFFSET)
        self.mpu.set_accelerometer_z_offset(self.Z_OFFSET)
        # set accelerometer scale
        self.mpu.set_accelerometer_scale(16)
        self.mpu.set_gyro_scale(1000)

        while self.run_event.is_set():
            try:
                self.accel_x = self.mpu.get_accelerometer_x()
                self.accel_y = self.mpu.get_accelerometer_y()
                self.accel_z = self.mpu.get_accelerometer_z()
                self.gyro_x = self.mpu.get_gyro_x()
                self.gyro_y = self.mpu.get_gyro_y()
                self.gyro_z = self.mpu.get_gyro_z()
            except TypeError:  # if failed reading an register, just keep going and try again
                pass

            time.sleep(0.01)
