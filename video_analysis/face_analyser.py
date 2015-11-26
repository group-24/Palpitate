
#  This script is responsible for getting the sppectrogram data for the facial anlaysis

import numpy as np
import cv2
from scipy import signal
from frame_inspector import FrameInspector
import matplotlib.pyplot as plt
import subprocess
import os

PATH_TO_OPENCV_CASCADES = "C:\\Users\\Sam Coope\\Documents\\Programming\\opencv\\sources\\data\\haarcascades\\"
SUBJECT_VIDEO_PATH = "D:\\HeartAV\\SensorData\\HeartAV_VideoFiles\\"

FRAME_RATE = 30
WINDOW_SIZE = 4

# this is fucking magic
# 'ffmpeg -y -ss 3 -i vp_035_01_00[2014][03][26][17][34]28.avi -to 10 -c copy -avoid_negative_ts 1 test.avi'
def analyse_video(subject_state, times):

    # getting path to video
    path_to_video = maybe_get_unique_avi_from_subjectState_id(subject_state, SUBJECT_VIDEO_PATH)
    if path_to_video is None:
        return None

    print path_to_video

    def analyse_slices(acc, x):
        (start, end) = x
        (acc_spectrograms, acc_heartrates) = acc
        (spectrograms, heartrates) = analyse_slice(start, end)
        acc_spectrograms = np.concatenate(acc_spectrograms, spectrograms)
        acc_heartrates += heartrates
        return (acc_spectrograms, acc_heartrates)

    def merge_data(acc, x):
        (spectrograms, heartrates) = x
        (acc_spectrograms, acc_heartrates) = acc
        # (spectrograms, heartrates) = analyse_slice(start, end)
        acc_spectrograms = np.concatenate(acc_spectrograms, spectrograms)
        acc_heartrates += heartrates
        return (acc_spectrograms, acc_heartrates)

    def analyse_slice(start, end):
        command = 'ffmpeg -y ' + ' -i ' + path_to_video + ' -ss ' + str(start) + ' -to ' + str(end) + ' -c copy -avoid_negative_ts 1 slice.avi'
        print command
        subprocess.call(command)

        # setup video analysis
        face_cascade = cv2.CascadeClassifier(PATH_TO_OPENCV_CASCADES + 'haarcascade_frontalface_alt2.xml')
        eye_cascade = cv2.CascadeClassifier(PATH_TO_OPENCV_CASCADES + 'haarcascade_eye.xml')

        video_capture = cv2.VideoCapture('slice.avi')

        inspector = FrameInspector(None)

        def analyse_segment():
            """some comment about what this does"""
            # Moving averages for face position, starting values are typical in vidoes of subjects
            (steadyX, steadyY) = (400, 185)
            (steadyHeight, steadyWidth) = (250, 250)
            alpha_movement = 0.9
            alpha_face_size = 0.999

            for i in range(FRAME_RATE*WINDOW_SIZE):
                # Capture frame-by-frame
                ret, frame = video_capture.read()
                if not ret or frame is None:
                    raise ValueError('video finished before analysing was complete')
                    break

                gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

                faces = face_cascade.detectMultiScale(gray, 1.3, 5)

                if len(faces) > 1:
                    print('more than one face detected')
                elif len(faces) == 0:
                    print('no faces detected')
                else:
                    (x, y, w, h) = faces[0]
                    (steadyX, steadyY) = (
                        int(alpha_movement*steadyX + (1-alpha_movement)*x),
                        int(alpha_movement*steadyY + (1-alpha_movement)*y)
                    )

                    (steadyWidth, steadyHeight) = (
                        int(alpha_face_size*steadyWidth + (1-alpha_face_size)*w),
                        int(alpha_face_size*steadyHeight + (1-alpha_face_size)*h)
                    )
                    # draw a rectangle
                    cv2.rectangle(frame, (steadyX, steadyY), (steadyX+steadyWidth, steadyY+steadyHeight), (0, 255, 0), 2)

                    # params for setecting the face

                    half_width = (steadyWidth // 2)
                    half_height = (steadyHeight // 2)

                    center_x = steadyX + half_width
                    center_y = steadyY + half_height

                    from_middleX = 0.6
                    from_middleY = 0.7

                    top_right = (
                        steadyX + int((1-from_middleX) * half_width),
                        center_y
                    )

                    bottom_left = (
                        center_x + int(half_width * from_middleX),
                        center_y + int(half_height * from_middleY)
                    )

                    # draw a rectangle
                    cv2.rectangle(frame, (steadyX, steadyY), (steadyX+steadyWidth, steadyY+steadyHeight), (0, 255, 0), 2)
                    cv2.rectangle(frame, top_right, bottom_left, (255, 255, 0), 2)

                    # just get the green color
                    interesting_pixels = frame[top_right[1]:bottom_left[1], top_right[0]:bottom_left[0]]
                    inspector.extract(frame)

                    # cv2.imshow('sdas', interesting_pixels)


                # Display the resulting frame
                cv2.imshow('Video', frame)

                if cv2.waitKey(1) & 0xFF == ord('q'):
                    break

            # When everything is done, release the capture
            cv2.destroyAllWindows()

            # g = plt.plot(range(len(l)), l)
            # plt.show(g)

            # f, t, spectrogram = signal.spectrogram(l, 1.0, nperseg=30)
            # plt.pcolormesh(t, f, spectrogram)
            # plt.ylabel('Frequency [Hz]')
            # plt.xlabel('Time [sec]')
            # plt.show()

        for i in range(start, end - WINDOW_SIZE, WINDOW_SIZE):
            analyse_segment()

        video_capture.release()
        return inspector.get_data()

    data = map(lambda x: analyse_slice(x[0], x[1]) , times)
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


sps = analyse_video('43_01', [(200, 210), (500, 540)])
