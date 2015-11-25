
#  This script is responsible for getting the sppectrogram data for the facial anlaysis

import numpy as np
import cv2
from scipy import signal
from frame_inspector import FrameInspector
import matplotlib.pyplot as plt

PATH_TO_OPENCV_CASCADES = "C:\\Users\\Sam Coope\\Documents\\Programming\\opencv\\sources\\data\\haarcascades\\"
SUBJECT_VIDEO_PATH = "D:\\HeartAV\\SensorData\\HeartAV_VideoFiles\\"

FRAME_RATE = 30
WINDOW_SIZE = 4

face_cascade = cv2.CascadeClassifier(PATH_TO_OPENCV_CASCADES + 'haarcascade_frontalface_alt2.xml')
eye_cascade = cv2.CascadeClassifier(PATH_TO_OPENCV_CASCADES + 'haarcascade_eye.xml')

video_capture = cv2.VideoCapture(SUBJECT_VIDEO_PATH + 'vp_035_01_00[2014][03][26][17][34]28.avi')

inspector = FrameInspector(None)

def analyse_segment():
    """some comment about what this does"""

    # Moving averages for face position, starting values are typical in vidoes of subjects
    (steadyX, steadyY) = (400, 185)
    (steadyHeight, steadyWidth) = (250, 250)
    alpha_movement = 0.9
    alpha_face_size = 0.999

    for i in range(FRAME_RATE*WINDOW_SIZE + 100):
        # Capture frame-by-frame
        ret, frame = video_capture.read()
        if not ret or frame is None:
            raise Error('video finished before analysing was complete')
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
    video_capture.release()
    cv2.destroyAllWindows()

    # g = plt.plot(range(len(l)), l)
    # plt.show(g)

    # f, t, spectrogram = signal.spectrogram(l, 1.0, nperseg=30)
    # plt.pcolormesh(t, f, spectrogram)
    # plt.ylabel('Frequency [Hz]')
    # plt.xlabel('Time [sec]')
    # plt.show()
    spectrograms = inspector.get_data()
    inspector.done()
    return spectrograms


sps = analyse_segment()
