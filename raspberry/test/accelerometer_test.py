# noinspection PyUnresolvedReferences
import unittest
# noinspection PyUnresolvedReferences
import sys
sys.path.insert(1, '../src')
# noinspection PyUnresolvedReferences
import accelerometer


class AccelerometerTest(unittest.TestCase):

    def test_merge_bits(self):
        res = accelerometer.Accelerometer.merge_bits(0b10101110, 0b001, 3, 3)
        self.assertEqual(res, 0b10100010)

        res = accelerometer.Accelerometer.merge_bits(0b00000000, 0b1111, 7, 4)
        self.assertEqual(res, 0b11110000)

        # tests overflow in new value
        res = accelerometer.Accelerometer.merge_bits(0b00000000, 0b111111, 2, 2)
        self.assertEqual(res, 0b00000110)

unittest.main()
