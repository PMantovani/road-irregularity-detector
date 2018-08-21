import unittest
import sys
sys.path.append('../src/')
from continuous_transformer import ContinuousTransformer

class TestContinuousTransformer(unittest.TestCase):

    def test_correct_input_inserts_in_current_readings(self):
        cut = ContinuousTransformer()
        cut.add_reading([1, 2, 3, 4, 5, 6, 7, 8, 9, 60, 11])
        self.assertEquals(len(cut.continuous_readings), 1)

    def test_wrong_input_length_resets_current_readings(self):
        cut = ContinuousTransformer()
        cut.add_reading([1, 2, 3, 4, 5, 6, 7, 8, 9, 60])
        self.assertEquals(len(cut.continuous_readings), 0)

    def test_change_of_quality_resets_current_readings(self):
        cut = ContinuousTransformer()
        cut.add_reading([1, 2, 3, 4, 5, 6, 7, 8, 9, 60, 11])
        cut.add_reading([2, 2, 3, 4, 5, 6, 7, 8, 9, 60, 11])
        self.assertEquals(len(cut.continuous_readings), 0)

    def test_ten_seconds_difference_insert_in_summary_array(self):
        cut = ContinuousTransformer()
        cut.add_reading([1, 2, 3, 4, 5, 6, 7, 8, 9, 60, 11])
        cut.add_reading([1, 2, 3, 4, 5, 6, 7, 8, 9, 60, 21])
        self.assertEquals(len(cut.summary_array), 1)

    def test_insert_in_summary_array_resets_current_readings(self):
        cut = ContinuousTransformer()
        cut.add_reading([1, 2, 3, 4, 5, 6, 7, 8, 9, 60, 11])
        cut.add_reading([1, 2, 3, 4, 5, 6, 7, 8, 9, 60, 21])
        self.assertEquals(len(cut.continuous_readings), 0)

    def test_speeds_over_200_resets_current_readings(self):
        cut = ContinuousTransformer()
        cut.add_reading([1, 2, 3, 4, 5, 6, 7, 8, 9, 210, 11])
        self.assertEquals(len(cut.continuous_readings), 0)

    def test_speeds_under_15_resets_current_readings(self):
        cut = ContinuousTransformer()
        cut.add_reading([1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11])
        self.assertEquals(len(cut.continuous_readings), 0)

    def test_lat_over_90_reset_current_readings(self):
        cut = ContinuousTransformer()
        cut.add_reading([1, 2, 3, 4, 5, 6, 7, 100, 9, 60, 11])
        self.assertEquals(len(cut.continuous_readings), 0)

    def test_lat_under_minus_90_reset_current_readings(self):
        cut = ContinuousTransformer()
        cut.add_reading([1, 2, 3, 4, 5, 6, 7, -100, 9, 60, 11])
        self.assertEquals(len(cut.continuous_readings), 0)

    def test_lng_over_180_reset_current_readings(self):
        cut = ContinuousTransformer()
        cut.add_reading([1, 2, 3, 4, 5, 6, 7, 8, 200, 60, 11])
        self.assertEquals(len(cut.continuous_readings), 0)

    def test_lng_under_minus_180_reset_current_readings(self):
        cut = ContinuousTransformer()
        cut.add_reading([1, 2, 3, 4, 5, 6, 7, 8, -200, 60, 11])
        self.assertEquals(len(cut.continuous_readings), 0)



if __name__ == '__main__':
    unittest.main()
