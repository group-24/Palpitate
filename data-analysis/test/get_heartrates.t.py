import sys
sys.path.append('..')

import unittest
import get_heartrates as gh

DATAPATH = 'dummyAV'

class HeartRateTests(unittest.TestCase):

    @classmethod
    def setUpClass(self):
        self.heartrate_info = gh.get_heartrates(DATAPATH)


    def test_seconds_difference(self):
        start = (17,45,29)
        end = (19, 15, 27)
        difference = gh.seconds_differece(start, end)
        expected = 1 * 3600 + 29 * 60 + 58
        self.assertEqual(difference, expected)
        self.assertEqual(gh.seconds_differece(start, start), 0)

    def test_get_heartrates_contains_keys(self):
        try:
            self.heartrate_info['40_01']
            self.heartrate_info['53_02']
            self.heartrate_info['78_01']
        except Exception as e:
            self.fail('Keys not founf in get_heartrates')

    def test_get_heartrates(self):
        subject_40 = self.heartrate_info['40_01']
        first_average = subject_40['heartrates'][0]
        second_average = subject_40['heartrates'][1]
        self.assertAlmostEqual(84.5795354364, first_average)
        self.assertAlmostEqual(82.929966298695, second_average)
        self.assertEqual(len(subject_40['heartrates']), 4)


if __name__ == '__main__':
    unittest.main()
