import numpy as np
import cv2

PATH_TO_OPENCV_CASCADES = "C:\\Users\\Sam Coope\\Documents\\Programming\\opencv\\sources\\data\\haarcascades\\"
SUBJECT_VIDEO_PATH = "D:\\HeartAV\\SensorData\\HeartAV_VideoFiles\\"


face_cascade = cv2.CascadeClassifier(PATH_TO_OPENCV_CASCADES + 'haarcascade_frontalface_alt2.xml')
eye_cascade = cv2.CascadeClassifier(PATH_TO_OPENCV_CASCADES + 'haarcascade_eye.xml')



video_capture = cv2.VideoCapture(SUBJECT_VIDEO_PATH + 'vp_035_01_00[2014][03][26][17][34]28.mp4')

# Moving averages for face position, starting values are typical in vidoes of subjects
(steadyX, steadyY) = (400, 185)
(steadyHeight, steadyWidth) = (250, 250)
alpha = 0.9
while True:
    # Capture frame-by-frame
    ret, frame = video_capture.read()
    if not ret or frame is None:
        print('no more frames from the video')
        break

    # print(str(frame.shape))
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    faces = face_cascade.detectMultiScale(gray, 1.3, 5)

    if len(faces) > 1:
        print('more than one face detected')
    elif len(faces) == 0:
        print('no faces detected')
    else:
        (x, y, w, h) = faces[0]
        (steadyX, steadyY) = (int(alpha*steadyX + (1-alpha)*x), int(alpha*steadyY + (1-alpha)*y))
        (steadyWidth, steadyHeight) = (int(alpha*steadyWidth + (1-alpha)*w), int(alpha*steadyHeight + (1-alpha)*h))
        # draw a rectangle
        cv2.rectangle(frame, (steadyX, steadyY), (steadyX+steadyWidth, steadyY+steadyHeight), (0, 255, 0), 2)

        # params for setecting the face

        half_width = (steadyWidth // 2)
        half_height = (steadyHeight // 2)

        center_x = steadyX + half_width
        center_y = steadyY + half_height

        from_middleX = 0.6
        from_middleY = 0.8

        top_right = (
            steadyX + int((1-from_middleX) * half_width),
            center_y
        )

        bottom_left = (
            center_x + int(half_width * from_middleX),
            center_y + int(half_height * from_middleY)
        )

        cv2.rectangle(frame, top_right, bottom_left, (255, 255, 0), 2)
        # cv2.rectangle(frame, top_right, (top_right[0] + 4, top_right[1] + 4), (255, 255, 0), 2)
        # cv2.rectangle(frame, (steadyX, steadyY), (steadyX + 4, steadyY + 4), (0, 0, 255), 2)



    # Display the resulting frame
    cv2.imshow('Video', frame)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# When everything is done, release the capture
video_capture.release()
cv2.destroyAllWindows()
