#  These methods is responsible for getting the sppectrogram data for the facial anlaysis
import numpy as np
import cv2
from scipy import signal
import subprocess
import os
import sys
import pickle
import shlex

path = os.path.abspath(os.path.join(os.path.dirname(__file__), '../data_analysis'))
if not path in sys.path:
    sys.path.insert(1, path)
del path

from get_heartrates import get_heartrates
from frame_inspector import FrameInspector
from face_tracker import FaceTracker

PATH_TO_OPENCV_CASCADES = "C:\\Users\\Sam Coope\\Documents\\Programming\\opencv\\sources\\data\\haarcascades\\"
PATH_TO_HEARTAV =  "D:\\HeartAV\\"

FRAME_RATE = 30
WINDOW_SIZE = 4

def analyse_video(subject_state, times, subjects_heartrates,
 path_to_opencv_cascades=PATH_TO_OPENCV_CASCADES, path_to_heartav=PATH_TO_HEARTAV, gui=True):
    print('analysing: ' + subject_state)
    # getting path to video
    subject_video_path = os.path.join(path_to_heartav, "SensorData", "HeartAV_VideoFiles")
    path_to_video = maybe_get_unique_avi_from_subjectState_id(subject_state, subject_video_path)

    if path_to_video is None:
        return None
    def analyse_slice(start, end):
        # slice the subject video to the correct size
        command = 'ffmpeg -loglevel panic -y -an' + ' -ss ' + str(start - 2) + ' -i \"' + path_to_video +  '\" -to ' + str((end-start) + 2) + ' -c copy -avoid_negative_ts 1 slice.avi'
        print command
        subprocess.call(shlex.split(command))
        # setup video analysis
        tracker = FaceTracker(path_to_opencv_cascades, gui=gui)
        heartrates_for_slice = subjects_heartrates[subject_state]['heartrates'][start:end]
        inspector = FrameInspector(heartrates_for_slice)

        video_capture = cv2.VideoCapture('slice.avi')

        i = 0
        while True:
            i += 1
            ret, frame = video_capture.read()
            if not ret or frame is None:
                print(str((start, end)) + "processed successfuly")
                break

            roi = None

            try:
                roi = tracker.detect_face(frame)
            except RuntimeError as e:
                raise RuntimeError(e.args[0] +  " at time:" + str((start, end)))


            if roi is None:
                raise RuntimeError('face_tracker failed to find face at ' + str(start) + '-' + str(end))
            else:
                if (i > 2 * FRAME_RATE):
                    inspector.extract(roi)
                if cv2.waitKey(1) & 0xFF == ord('q'):
                    break

        inspector.done()

        # When everything is done, release the capture
        video_capture.release()
        if gui:
            cv2.destroyAllWindows()
        data = inspector.get_data()
        inspector.flush()
        return data

    analyses = []
    times_used = []
    analysis = None
    for start, end in times:
        try:
            analysis = analyse_slice(start, end)
        except RuntimeError as e:
            print str(e)
        else:
            if analysis!= None and len(analysis[0]) > 0:
                analyses.append(analysis)
                times_used.append((start, end))
            else:
                print "no data found"

    def merge_data(acc, x):
        (spectrograms, heartrates, time_series) = x
        (acc_spectrograms, acc_heartrates, acc_time_series) = acc
        acc_spectrograms = np.append(acc_spectrograms, spectrograms, axis=0)
        acc_heartrates = np.append(acc_heartrates, heartrates, axis=0)
        acc_time_series += time_series
        return (acc_spectrograms, acc_heartrates, acc_time_series)

    if len(analyses) > 0:
        analyses = reduce(merge_data , analyses)
    return (analyses, times_used)

# shamelessly copied from timotej
def maybe_get_unique_avi_from_subjectState_id(ss_id, path):
    candidates = []
    for f in os.listdir(path):
        if f.endswith(".avi") and ss_id in f:
            # candidates += [path + "\\" + f]
            candidates += [os.path.join(path, f)]
    if len(candidates) == 1:
        return candidates[0]
    else:
        return None

def write_cache(cache_file, data):
    with open(cache_file,'wb') as f:
        pickle.dump(data, f, protocol=pickle.HIGHEST_PROTOCOL)
