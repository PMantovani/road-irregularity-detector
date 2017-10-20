import smbus
import time
bus = smbus.SMBus(1)
address = 0x68
power_mgmt_1 = 0x6b
scale = 2 # number of g's of accelerometer when reading is 16353

# reads a word from I2C bus 1. 
def read_word(addr):
  high = bus.read_byte_data(address, addr)
  low = bus.read_byte_data(address, addr+1)
  val = (high << 8) + low
  return val

# converts word reading into complement of 2
def read_word_2c(addr):
  val = read_word(addr)
  if (val >= 0x8000):
    return -((65535 - val) + 1)
  else:
    return val

# get out of power saving mode
bus.write_byte_data(address, power_mgmt_1, 0)

while True:
  accel_x = read_word_2c(0x3b)*scale/32767.
  accel_y = read_word_2c(0x3d)*scale/32767.
  accel_z = read_word_2c(0x3f)*scale/32767.
  print("x: " + str(accel_x))
  print("y: " + str(accel_y))
  print("z: " + str(accel_z))
  print()
  time.sleep(1)
