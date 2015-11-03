import numpy as np
import cv2
import sys
import subprocess

def add_face_detection(from_file, to_file, opencv_path):
  face_cascade = cv2.CascadeClassifier(opencv_path + 
                   'data/haarcascades/haarcascade_frontalface_default.xml')
  eye_cascade = cv2.CascadeClassifier(opencv_path + 
                   'data/haarcascades/haarcascade_eye.xml')
  
  cap = cv2.VideoCapture(from_file)

  w = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
  h = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
  fourcc = int(cap.get(cv2.CAP_PROP_FOURCC))
  fps = cap.get(cv2.CAP_PROP_FPS)

  writer = cv2.VideoWriter(to_file, fourcc, fps, (w, h)) 

  while True:
    ret, frame = cap.read()

    if not ret or frame is None:
      break

    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    faces = face_cascade.detectMultiScale(gray, 1.3, 5)
  
    for (x,y,w,h) in faces:
      cv2.rectangle(frame, (x,y), (x+w,y+h), (0,0,255), 2)
      cv2.putText(frame, "68 bpm", (x+(w*1)/4, y+h+20), cv2.FONT_HERSHEY_SIMPLEX, 0.75, (0, 0, 255), 2)  

    writer.write(frame)
  
  cap.release()
  cv2.destroyAllWindows()

def copy_audio(from_file, to_file):
  temp_audio_file = 'audio_' + to_file
  subprocess.call(['ffmpeg', '-i', to_file, '-i', from_file, '-c', 'copy',
                   '-map', '0:0', '-map', '1:1', '-shortest', temp_audio_file])
  subprocess.call(['mv', temp_audio_file, to_file])

video_file = sys.argv[1]
new_video_file = 'face_' + video_file
opencv_path = sys.argv[2]

add_face_detection(video_file, new_video_file, opencv_path)
copy_audio(video_file, new_video_file)

print "Done"
