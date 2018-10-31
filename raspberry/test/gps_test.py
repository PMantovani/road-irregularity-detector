# noinspection PyUnresolvedReferences
import unittest
# noinspection PyUnresolvedReferences
import sys
# noinspection PyUnresolvedReferences
from src import gps


class TestGPS(unittest.TestCase):
    # noinspection PyPep8Naming,PyAttributeOutsideInit
    def setUp(self):
        self.gps_test = gps.GPS(None, None)

    def test_convert_degrees(self):
        res = self.gps_test.convert_degrees(57, 23.451)
        self.assertEqual(res, 57.39085)

    def test_calculate_decimal(self):
        res = self.gps_test.calculate_decimal(4913.21079, 'S')
        self.assertEqual(round(res, 5), -49.22018)
        res = self.gps_test.calculate_decimal(4913.21079, 'W')
        self.assertEqual(round(res, 5), -49.22018)
        res = self.gps_test.calculate_decimal(2523.4332, 'N')
        self.assertEqual(round(res, 5), 25.39055)
        res = self.gps_test.calculate_decimal(2523.4332, 'E')
        self.assertEqual(round(res, 5), 25.39055)

    def test_parse_gprmc(self):
        msg = "$GPRMC,005517.00,A,2523.42932,S,04913.25209,W,1.604,,211017,,,A*75"
        expected = -25.3904887, -49.2208682, 2.97
        self.assertEqual(self.gps_test.parse_gprmc(msg), expected)

    def test_current_time_2018(self):
        msg = "$GPRMC,005517.00,A,2523.42932,S,04913.25209,W,1.604,,211018,,,A*75"
        expected = 21, 10, 2018
        self.gps_test.parse_gprmc(msg)
        result = self.gps_test.get_current_time()
        self.assertEqual((result.day, result.month, result.year), expected)

    def test_current_time_1999(self):
        msg = "$GPRMC,005517.00,A,2523.42932,S,04913.25209,W,1.604,,211099,,,A*75"
        expected = 21, 10, 1999
        self.gps_test.parse_gprmc(msg)
        result = self.gps_test.get_current_time()
        self.assertEqual((result.day, result.month, result.year), expected)

if __name__ == '__main__':
    unittest.main()