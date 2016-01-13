import numpy as np
import pickle
from normalizer import premade_video_normalizer
from keras.models import model_from_json

def check_cache(cache_file):
    with open(cache_file,'rb') as f:
        data = pickle.load(f)
        return data

model = model_from_json(open('data_analysis/video_1D_CNN_RNN.json').read())
model.load_weights('data_analysis/video_1D_CNN_RNN.h5')

class VideoHeartrateGenerator(object):
    def __init__(self):
        self.frame_samples = []
        self.current_heartrate = None
        self.normalizer = premade_video_normalizer

    def add_sample(self, roi):
        sample = roi[:, :, 1].mean()
        self.frame_samples.append(sample)

        if len(self.frame_samples) % 30 == 0 and len(self.frame_samples) >= 120:
            normalized = self.normalizer.normalize_data(np.array(self.frame_samples[-120:]))
            self.current_heartrate = model.predict(np.reshape(normalized, (1,1,1,-1)))
            self.current_heartrate = self.normalizer.unnormalize_bpm(self.current_heartrate).mean()
            # self.current_heartrate = self.normalizer.normalize_data(np.array(self.frame_samples[-120:])).mean()


    def lost_face(self):
        self.frame_samples = []
        self.current_heartrate = None

    def get_heartrate(self):
        return self.current_heartrate
