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

  def gen_heartrate_frames(self, age, gender):
    return self.heartrate_frames(age, gender, False)

  def pipe_heartrate_frames(self, age, gender):
    self.heartrate_frames(age, gender, True)

  def heartrate_frames(self, age, gender, pipe):
    face_cascade = cv2.CascadeClassifier(self.opencv_path +
                     'data/haarcascades/haarcascade_frontalface_default.xml')
    cap = cv2.VideoCapture(self.from_file)

    w = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    h = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
    fourcc = int(cap.get(cv2.CAP_PROP_FOURCC))
    fps = cap.get(cv2.CAP_PROP_FPS)

    if pipe:
        sys.stdout.write(str(w) + " " + str(h) + " " + str(fps) + '\n')
    else:
        yield str(w) + " " + str(h) + " " + str(fps) + '\n'

    frame_count = 0
    heartrate = None
    heartrate_time = 0
    heartrate_gen = self.hrg.gen_heartrates()

    # will not be lower or higher (if not rip)
    current_max = -1.0
    current_min = 300.0

    if age and gender:
        print "Imposing medical information"
        age = int(age)
        mhr = round(float(self.calculate_max_heartrate(age, gender)), 1)

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

      if heartrate > 0: 
          if heartrate > current_max:
             current_max = heartrate
          elif heartrate < current_min:
             current_min = heartrate

      gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
      faces = face_cascade.detectMultiScale(gray, 1.3, 5)

      for (x,y,w,h) in faces:
        cv2.rectangle(frame, (x,y), (x+w,y+h), (0,0,255), 2)
        heartrate_text = round(heartrate, 1) if heartrate else '---'
        cv2.putText(frame, str(heartrate_text) + ' bpm', (x+(w*1)/4, y+h+20),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.75, (0, 0, 255), 2)

        if age and gender:
            intensity = round(float(self.calculate_exercise_intensity(heartrate, mhr)), 1)
            if intensity < 0:
                intensity = '---'
            intensity = str(intensity)

            cmax = str(round(float(current_max), 1)) if current_max != -1.0 else '---'
            cmin = str(round(float(current_min), 1)) if current_min != 300.0 else '---'

            cv2.putText(frame, 'Max. Heart Rate: ' + str(mhr) + ' bpm',
                        (10, 20), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 255), 1)
            cv2.putText(frame, 'Intensity: ' + str(intensity) + '%',
                        (10, 40), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 255), 1)
            cv2.putText(frame, 'Current Max. Heart Rate: ' + cmax + ' bpm',
                        (10, 60), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 255), 1)
            cv2.putText(frame, 'Current Min. Heart Rate: ' + cmin + ' bpm',
                        (10, 80), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 255), 1)

      if pipe:
        sys.stdout.write(frame.tostring())
      else:
        yield frame.tostring()

    cap.release()
    cv2.destroyAllWindows()

  def calculate_max_heartrate(self, age, gender):
    if gender == 'male': 
        return 203.7 / (1 + pow(2.718282, 0.033 * (age - 104.3)))
    else:
        return 190.2 / (1 + pow(2.718282, 0.0453 * (age - 107.5)))

  def calculate_exercise_intensity(self, heartrate, max_heartrate):
    if heartrate:
      return heartrate / max_heartrate
    return -1

