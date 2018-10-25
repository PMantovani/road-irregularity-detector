# noinspection PyUnresolvedReferences
import unittest
# noinspection PyUnresolvedReferences
import sys
# noinspection PyUnresolvedReferences
from src.I2CDevice import I2CDevice


class I2CDeviceTest(unittest.TestCase):

    def test_merge_bits(self):
        res = I2CDevice.merge_bits(0b10101110, 0b001, 3, 3)
        self.assertEqual(res, 0b10100010)

        res = I2CDevice.merge_bits(0b00000000, 0b1111, 7, 4)
        self.assertEqual(res, 0b11110000)

        # tests overflow in new value
        res = I2CDevice.merge_bits(0b00000000, 0b111111, 2, 2)
        self.assertEqual(res, 0b00000110)
