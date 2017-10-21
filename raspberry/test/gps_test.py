import unittest
import sys
sys.path.insert(1, '../src')
import gps


class GPSTest(unittest.TestCase):
    def setUp(self):
        self.gps_test = gps.GPS(None)

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
        expected = -25.39049, -49.22087, 2.97
        self.assertEqual(self.gps_test.parse_gprmc(msg), expected)

unittest.main()