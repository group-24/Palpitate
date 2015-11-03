import numpy as np
import cv2
import sys
import subprocess
import random

class HeartRateImposer(object):

  def __init__(self, from_file, opencv_path, heartrates):
    self.from_file = from_file
    self.opencv_path = opencv_path
    self.heartrates = heartrates

  def impose_heartrate(self, to_file):
    self._add_face_detection(to_file)
    self._copy_audio(self.from_file, to_file)

  def _add_face_detection(self, to_file):
    face_cascade = cv2.CascadeClassifier(self.opencv_path + 
                     'data/haarcascades/haarcascade_frontalface_default.xml')
    eye_cascade = cv2.CascadeClassifier(self.opencv_path + 
                     'data/haarcascades/haarcascade_eye.xml')
    
    cap = cv2.VideoCapture(self.from_file)
  
    w = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    h = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
    fourcc = int(cap.get(cv2.CAP_PROP_FOURCC))
    fps = cap.get(cv2.CAP_PROP_FPS)
  
    writer = cv2.VideoWriter(to_file, fourcc, fps, (w, h)) 
  
    for heartrate in self.heartrates: 
      ret, frame = cap.read()
  
      if not ret or frame is None:
        break
  
      gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
      faces = face_cascade.detectMultiScale(gray, 1.3, 5)
    
      for (x,y,w,h) in faces:
        cv2.rectangle(frame, (x,y), (x+w,y+h), (0,0,255), 2)
        cv2.putText(frame, str(int(heartrate)) + ' bpm', (x+(w*1)/4, y+h+20), 
                    cv2.FONT_HERSHEY_SIMPLEX, 0.75, (0, 0, 255), 2)  
  
      writer.write(frame)
    
    cap.release()
    cv2.destroyAllWindows()
  
  def _copy_audio(self, from_file, to_file):
    temp_audio_file = 'audio_' + to_file
    subprocess.call(['ffmpeg', '-i', to_file, '-i', from_file, '-c', 'copy',
                     '-map', '0:0', '-map', '1:1', '-shortest', temp_audio_file])
    subprocess.call(['mv', temp_audio_file, to_file])


if len(sys.argv) < 3:
  print 'usage: python ' + sys.argv[0] + ' VIDEO_FILE OPENCV_DIR'
  exit()

video_file = sys.argv[1]
opencv_path = sys.argv[2]

hri = HeartRateImposer(video_file, opencv_path, (i / 100 + random.random() % 5 for i in range(6500, 1000000, 2)))
hri.impose_heartrate('faces_' + video_file)

print "Done"
