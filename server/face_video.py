import numpy as np
import cv2
import sys

videoPath = sys.argv[1]
opencvPath = sys.argv[2]

face_cascade = cv2.CascadeClassifier(opencvPath + 'data/haarcascades/haarcascade_frontalface_default.xml')
eye_cascade = cv2.CascadeClassifier(opencvPath + 'data/haarcascades/haarcascade_eye.xml')

cap = cv2.VideoCapture(videoPath)
w = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
h = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
fourcc = int(cap.get(cv2.CAP_PROP_FOURCC))
fps = int(cap.get(cv2.CAP_PROP_FPS))
print w, h, fourcc, fps
writer = cv2.VideoWriter('faces_' + videoPath, fourcc, fps, (w, h)) 

while True:
  ret, frame = cap.read()

  gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

  faces = face_cascade.detectMultiScale(gray, 1.3, 5)

  for (x,y,w,h) in faces:

    cv2.rectangle(frame, (x,y), (x+w,y+h), (0,0,255), 2)

  writer.write(frame)
	
  if cv2.waitKey(1) & 0xFF == ord('q'):
    break

cap.release()
cv2.destroyAllWindows()
