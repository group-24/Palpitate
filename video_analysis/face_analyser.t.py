import unittest
import sys
import numpy as np
from face_analyser import analyse_video
import os
import numpy as np

path_to_cascades = os.environ.get('CONTAINER_OPENCV')
if path_to_cascades is None:
    path_to_cascades = "C:\\Users\\Sam Coope\\Documents\\Programming\\opencv"

path_to_cascades = os.path.join(path_to_cascades, 'sources', 'data', 'haarcascades')

class HeartRateTests(unittest.TestCase):

    @classmethod
    def setUpClass(self):
        times = [(2,5), (5, 9), (2,6)]
        heartrates = {
            'test': {
                'heartrates': np.array([0,1,2,3,4,5,6,7,8,9])
            }
        }

        path_to_heartav = "test"
        (self.data, self.times) = analyse_video(
            'test',
            times,
            heartrates,
            path_to_opencv_cascades=path_to_cascades,
            path_to_heartav=path_to_heartav,
            gui=False
        )

    def test_one_failed(self):
        # the time (2,5) is to short
        self.assertEqual(len(self.times), 2)

    def test_data_has_same_length(self):
        self.assertEqual(len(self.data[0]), len(self.data[1]))
        self.assertEqual(len(self.data[0]), len(self.data[2]))

    def test_heartrates_correct(self):
        heartrates = self.data[1]
        np.testing.assert_array_equal(heartrates[0], np.array([5,6,7,8]))
        np.testing.assert_array_equal(heartrates[1], np.array([2,3,4,5]))

if __name__ == '__main__':
    unittest.main()
