import unittest
from datetime import date
from tockchecker import find_fridays_and_saturdays

class TestTockChecker(unittest.TestCase):

    def test_find_fridays_and_saturdays(self):
        start_date = date(2022, 1, 1)
        end_date = date(2022, 1, 31)
        expected_result = [
            date(2022, 1, 7), date(2022, 1, 8),
            date(2022, 1, 14), date(2022, 1, 15),
            date(2022, 1, 21), date(2022, 1, 22),
            date(2022, 1, 28), date(2022, 1, 29)
        ]
        result = find_fridays_and_saturdays(start_date, end_date)
        self.assertEqual(result, expected_result)

if __name__ == '__main__':
    unittest.main()