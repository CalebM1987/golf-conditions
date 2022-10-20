import unittest
from app.routers.weather.ratings import get_dew_rating, get_temp_rating, get_wind_rating, get_precip_rating

class TestDewRating(unittest.TestCase):
    def test_dew_zero_rating(self):
        actual = get_dew_rating(65, 85)
        self.assertEqual(actual, 0, 'the dew rating is 0 when temp is >= 85 and dew point >= 65')
    
    def test_dew_high_rating(self):
        actual = get_dew_rating(40, 75)
        self.assertGreaterEqual(actual, .9, 'the dew rating good when temp is 75 and dew point is 50')
    
    def test_dew_fair_rating(self):
        actual = get_dew_rating(55, 80)
        self.assertEqual(actual, .5, 'the dew rating is fair when temp is 80 and dew point is 55')

class TestTempRating(unittest.TestCase):
    def test_temp_zero_rating(self):
        actual = get_temp_rating(45)
        self.assertEqual(actual, 0, 'the temp rating is 0 when temp is <= 45')
    
    def test_temp_high_rating(self):
        actual = get_temp_rating(75)
        self.assertGreaterEqual(actual, .9, 'the temp rating good when temp is 75 (ideal)')
    
    def test_dew_fair_rating(self):
        actual = get_temp_rating(60)
        self.assertEqual(actual, .5, 'the temp rating is fair when temp is 60 (a little chilli for golf)')

class TestWindRating(unittest.TestCase):
    def test_wind_zero_rating(self):
        actual = get_wind_rating(25, 70)
        self.assertEqual(actual, 0, 'the wind rating is 0 when wind speed is >= 25')
    
    def test_wind_high_rating(self):
        actual = get_wind_rating(5, 75)
        self.assertGreaterEqual(actual, .9, 'the wind speed rating good when wind speed is 5 (ideal)')
    
    def test_wind_fair_rating(self):
        actual = get_wind_rating(10, 75)
        self.assertGreaterEqual(actual, .6, 'the wind speed rating is fair when temp is 75 and wind speed is 10')
    
    def test_hot_day_higher_wind_good_rating(self):
        actual = get_wind_rating(10, 90)
        self.assertEqual(actual, 1, 'but the 10 mph wind feels better when it is 90')

class TestPrecipRating(unittest.TestCase):
    def test_precip_zero_rating(self):
        actual = get_precip_rating(4)
        self.assertEqual(actual, 0, 'the precip rating is 0 when it is raining 4mm/hr')
    
    def test_precip_high_rating(self):
        actual = get_precip_rating(0.09)
        self.assertGreaterEqual(actual, .09, 'the precip rating good when there is little to no rain')
    
    def test_precip_fair_rating(self):
        actual = get_precip_rating(2)
        self.assertEqual(actual, .5, 'the precip rating is fair when temp is 80 and dew point is 55')

