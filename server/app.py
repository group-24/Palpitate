from flask import Flask, render_template, Response
import sys
import random
from face_video import HeartRateImposer

app = Flask(__name__)

video_file = sys.argv[1]
opencv_path = sys.argv[2]

@app.route('/')
def index():
    return "Hello World"

def gen(gen_frames):
    for frame in gen_frames(): 
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')

@app.route('/video')
def video():
    hri = HeartRateImposer(video_file, opencv_path, 
            (i / 100 + random.random() % 5 for i in range(6500, 1000000, 2)))
    return Response(gen(hri.gen_heartrate_frames),
                    mimetype='multipart/x-mixed-replace; boundary=frame')

if __name__ == '__main__':
    app.run(host='0.0.0.0')
