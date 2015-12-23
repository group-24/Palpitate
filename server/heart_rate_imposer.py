from data_analysis.heart_rate_generator import HeartRateGenerator
import numpy as np
import cv2
import sys
import subprocess
import random

class HeartRateImposer(object):

  def __init__(self, from_file, opencv_path):
    self.from_file = from_file
    self.opencv_path = opencv_path
    self.hrg = HeartRateGenerator(avi_file=self.from_file)

  def gen_heartrate_frames(self):
    face_cascade = cv2.CascadeClassifier(self.opencv_path +
                     'data/haarcascades/haarcascade_frontalface_default.xml')
    cap = cv2.VideoCapture(self.from_file)

    w = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    h = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
    fourcc = int(cap.get(cv2.CAP_PROP_FOURCC))
    fps = cap.get(cv2.CAP_PROP_FPS)

    frame_count = 0
    heartrate = None
    heartrate_time = 0
    heartrate_gen = self.hrg.gen_heartrates()

    while True:
      # Read frame from video capture
      ret, frame = cap.read()
      if not ret or frame is None:
        break

      # Only generate a new heartrate every second
      frame_count += 1
      time = int(frame_count / fps)

      # heartrates are cut off at the end of the video a there are not enough
      # readings to average them so if this occurs, just stop generating them
      if time > heartrate_time:
          heartrate = heartrate_gen.next()
          heartrate_time = time

      gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
      faces = face_cascade.detectMultiScale(gray, 1.3, 5)

      for (x,y,w,h) in faces:
        cv2.rectangle(frame, (x,y), (x+w,y+h), (0,0,255), 2)
        heartrate_text = round(heartrate, 1) if heartrate else '---'
        cv2.putText(frame, str(heartrate_text) + ' bpm', (x+(w*1)/4, y+h+20),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.75, (0, 0, 255), 2)

      ret, jpeg = cv2.imencode('.jpg', frame)
      yield jpeg.tobytes()

    cap.release()
    cv2.destroyAllWindows()

  def pipe_heartrate_frames(self):
    face_cascade = cv2.CascadeClassifier(self.opencv_path +
                     'data/haarcascades/haarcascade_frontalface_default.xml')
    cap = cv2.VideoCapture(self.from_file)

    w = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    h = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
    fourcc = int(cap.get(cv2.CAP_PROP_FOURCC))
    fps = cap.get(cv2.CAP_PROP_FPS)
    sys.stdout.write(str(w) + " " + str(h) + " " + str(fps) + '\n')

    frame_count = 0
    heartrate = None
    heartrate_time = 0
    heartrate_gen = self.hrg.gen_heartrates()

    while True:
      # Read frame from video capture
      ret, frame = cap.read()
      if not ret or frame is None:
        break

      # Only generate a new heartrate every second
      frame_count += 1
      time = int(frame_count / fps)

      # heartrates are cut off at the end of the video a there are not enough
      # readings to average them so if this occurs, just stop generating them
      if time > heartrate_time:
          heartrate = heartrate_gen.next()
          heartrate_time = time

      gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
      faces = face_cascade.detectMultiScale(gray, 1.3, 5)

      for (x,y,w,h) in faces:
        cv2.rectangle(frame, (x,y), (x+w,y+h), (0,0,255), 2)
        heartrate_text = round(heartrate, 1) if heartrate else '---'
        cv2.putText(frame, str(heartrate_text) + ' bpm', (x+(w*1)/4, y+h+20),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.75, (0, 0, 255), 2)

      sys.stdout.write(frame.tostring())

    cap.release()
    cv2.destroyAllWindows()

  def impose_heartrate(self, to_file):
    self._add_face_detection(to_file)
    self._copy_audio(self.from_file, to_file)

