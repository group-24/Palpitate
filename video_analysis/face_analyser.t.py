import unittest
import sys
import numpy as np
from face_analyser import analyse_video

path_to_cascades = "C:\\Users\\Sam Coope\\Documents\\Programming\\opencv\\sources\\data\\haarcascades\\"
if len(sys.argv) > 1:
    path_to_cascades = sys.argv[1]

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
        self.assertEqual(heartrates[0], 6.5)
        self.assertEqual(heartrates[1], 3.5)

if __name__ == '__main__':
    unittest.main()
