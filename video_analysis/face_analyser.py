
#  This script is responsible for getting the sppectrogram data for the facial anlaysis

import numpy as np
import cv2
from scipy import signal
import matplotlib.pyplot as plt
import subprocess
import os
import sys
import pickle

path = os.path.abspath(os.path.join(os.path.dirname(__file__), '../data_analysis'))
if not path in sys.path:
    sys.path.insert(1, path)
del path

from get_heartrates import get_heartrates
from frame_inspector import FrameInspector
from face_tracker import FaceTracker

PATH_TO_OPENCV_CASCADES = "C:\\Users\\Sam Coope\\Documents\\Programming\\opencv\\sources\\data\\haarcascades\\"
PATH_TO_HEARTAV =  "D:\\HeartAV\\"
# SUBJECT_VIDEO_PATH = "D:\\HeartAV\\SensorData\\HeartAV_VideoFiles\\"
SUBJECT_VIDEO_PATH = os.path.join(PATH_TO_HEARTAV, "SensorData", "HeartAV_VideoFiles")

FRAME_RATE = 30
WINDOW_SIZE = 4

gui = True
subjects_heartrates = get_heartrates(PATH_TO_HEARTAV, window=4)

def analyse_video(subject_state, times):

    # getting path to video
    path_to_video = maybe_get_unique_avi_from_subjectState_id(subject_state, SUBJECT_VIDEO_PATH)
    if path_to_video is None:
        return None

    print path_to_video

    def merge_data(acc, x):
        (spectrograms, heartrates) = x
        (acc_spectrograms, acc_heartrates) = acc
        # (spectrograms, heartrates) = analyse_slice(start, end)
        acc_spectrograms = np.concatenate((acc_spectrograms, spectrograms))
        acc_heartrates = np.append(acc_heartrates, heartrates)
        return (acc_spectrograms, acc_heartrates)

    def analyse_slice(start, end):
        command = 'ffmpeg -y ' + ' -i ' + path_to_video + ' -ss ' + str(start) + ' -to ' + str(end) + ' -c copy -avoid_negative_ts 1 slice.avi'
        print command
        subprocess.call(command)

        # setup video analysis
        tracker = FaceTracker(PATH_TO_OPENCV_CASCADES, gui=gui)
        heartrates_for_slice = subjects_heartrates[subject_state]['heartrates'][start:end]
        inspector = FrameInspector(heartrates_for_slice)

        video_capture = cv2.VideoCapture('slice.avi')

        while True:
            ret, frame = video_capture.read()
            if not ret or frame is None:
                # raise ValueError('video finished before analysing was complete')
                print 'video finished'
                break

            roi = tracker.detect_face(frame)

            if roi is None:
                # panic
                print('face_tracker failed to find face')
            else:
                inspector.extract(frame)

                if cv2.waitKey(1) & 0xFF == ord('q'):
                    break

        inspector.done()

        video_capture.release()
        # When everything is done, release the capture
        if gui:
            cv2.destroyAllWindows()
        data = inspector.get_data()
        inspector.flush()
        return data


    data = map(lambda x: analyse_slice(x[0], x[1]), times)
    data_from_video = reduce(merge_data , data)
    return data_from_video

# shamelessly copied from timotej
def maybe_get_unique_avi_from_subjectState_id(ss_id, path):
    candidates = []
    for f in os.listdir(path):
        if f.endswith(".avi") and ss_id in f:
            candidates += [path + "\\" + f]
    if len(candidates) == 1:
        return candidates[0]
    else:
        return None

def write_cache(cache_file, data):
    with open(cache_file,'wb') as f:
        pickle.dump(data, f, protocol=pickle.HIGHEST_PROTOCOL)



sps = analyse_video('43_01', [(200, 210), (500, 540)])
# sps = analyse_video('43_01', [(200, 210)])
write_cache('video_analysis.pickle',sps)





# stuff that i might need later
# g = plt.plot(range(len(l)), l)
# plt.show(g)

# f, t, spectrogram = signal.spectrogram(l, 1.0, nperseg=30)
# plt.pcolormesh(t, f, spectrogram)
# plt.ylabel('Frequency [Hz]')
# plt.xlabel('Time [sec]')
# plt.show()
