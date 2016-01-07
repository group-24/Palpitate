import numpy as np

class VideoHeartrateGenerator(object):
    def __init__(self):
        self.frame_samples = np.array([])
        self.current_heartrate = None

    def add_sample(self, roi):
        sample = roi[:, :, 1].mean()
        np.append(self.frame_samples, sample)
        if self.current_heartrate == None:
            self.current_heartrate = 1
        else:
            self.current_heartrate += 1

    def get_heartrate(self):
        return self.current_heartrate
