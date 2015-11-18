from keras.models import model_from_json
from data_analysis.spectrogram import SubjectWav
import subprocess
import numpy as np
import os

pwd = '/home/'
print 'Loading model'
model = model_from_json(open(pwd + 'data_analysis/my_model_architecture18%.json').read())
model.load_weights(pwd + 'data_analysis/my_model_weights18%.h5')
print 'Loaded model'

class HeartRateGenerator(object):

    def __init__(self, avi_file=None, wav_file=None):
        if wav_file:
            self.wav_file = wav_file
        elif avi_file:
            self.avi_file = avi_file
            self.wav_file = avi_file.split('.')[0] + '.wav'
            subprocess.call(['ffmpeg', '-y', '-i', str(self.avi_file), '-ab', '160k', '-ac', '2', '-ar', '44100', '-vn', str(self.wav_file)])
        else:
            raise Exception()
            
        self.model = model
        self.subjectWav = SubjectWav(str(self.wav_file))

    # Yield and average heartrate over 4 seconds for every second in a audio
    # file except the first 4
    def gen_heartrates(self):
        window = []
        time = 0
        while True:
            try:
                spectrogram = self.subjectWav.get_spectrogram(time)
                spectrogram = spectrogram[2]
                spectrogram = np.array([[spectrogram]])
                heartrate = self.model.predict(spectrogram)[0][0]
                heartrate = heartrate if str(heartrate) != 'nan' else None

                window.append(heartrate)
                if len(window) is 5:
                    window = window[1:]

                if len(filter(lambda x: x, window)) is 4:
                    yield np.mean(window)
                else:
                    yield None
            except Exception:
                break
            time += 1
