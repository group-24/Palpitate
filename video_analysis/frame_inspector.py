import numpy as np
from scipy import signal

TIME_SECOND_WINDOW = 4
FRAME_RATE = 30


class FrameInspector(object):
    """This class inspects the frame of a video, then produces spectrograms of the
    desired features of the frame"""

    def __init__(self, heartrates):
        self.heartrates = heartrates
        self.frames_processed = 0
        self.data = None
        self.window = []

    def extract(self, frame):
        """frame is the sliced pixel of the face"""
        self.frames_processed += 1
        # get the greenpixels
        self.window.append(frame[:, :, 1].mean())

        if self.frames_processed == (FRAME_RATE * TIME_SECOND_WINDOW):
            print 'asdasdasdasdasdasdasd'
            self.process_data()
        else:
            print self.frames_processed
        # return the location of the smoothed face in the video

    def lost_frame(self):
        raise Error("NOT DONE YET")

    def done(self):
        """Called when processing of a video is finished, flushes the data"""
        self.frames_processed = 0
        self.window = None

    def flush(self):
        """flushed data"""
        self.data = None

    def get_data(self):
        return self.data

    def process_data(self):
        """makes the spectrigrams and adds it to data"""
        self.frames_processed = 0
        window = self.window
        self.window = []

        print window

        # normalise the time series
        total = 0
        mean = reduce(lambda acc, x: x + acc, window)/len(window)
        window = map(lambda x: x - mean, window)

        f, t, spectrogram = signal.spectrogram(window, 1.0, nperseg=30)
        if self.data is None:
            self.data = np.array([spectrogram])
        else:
            self.data = np.concatenate((self.data, [spectrogram]))
