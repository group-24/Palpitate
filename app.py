from flask import Flask, render_template, Response
import sys
import random
from server.heart_rate_imposer import HeartRateImposer
from keras.models import model_from_json

app = Flask(__name__)

video_file = sys.argv[1]
opencv_path = sys.argv[2]

def gen_http_frame(gen_frames):
    for frame in gen_frames():
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')

@app.route('/')
def index():
    return "Hello World"

# @app.route('/video/<youtube_extension>')
# def stream(youtube_extension):
#     url = 'www.youtube.com/' + youtube_extension
#     hri = HeartRateImposer(video_file, opencv_path)
#     return Response(gen_http_frame(hri.gen_heartrate_frames),
#                     mimetype='multipart/x-mixed-replace; boundary=frame')

@app.route('/video')
def stream():
    hri = HeartRateImposer(video_file, opencv_path)
    return Response(gen_http_frame(hri.gen_heartrate_frames),
                    mimetype='multipart/x-mixed-replace; boundary=frame')


if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True)
