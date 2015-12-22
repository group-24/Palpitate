from flask import Flask, request, Response, abort, send_file, jsonify
import os, subprocess, re, sys

app = Flask(__name__)

video_file = sys.argv[1]
opencv_path = sys.argv[2]

@app.route('/')
def index():
    return 'Hello World'

@app.route('/video')
def video():
    FNULL = open(os.devnull, 'w')

    hri_cmd = ['python', 'heart_rate_imposer.py', video_file, opencv_path]
    opencv_ps = subprocess.Popen(hri_cmd, stdout=subprocess.PIPE, stderr=FNULL)

    line = opencv_ps.stdout.readline()
    [width, height, fps] = line.split(' ')

    cmd = 'ffmpeg -f rawvideo -pix_fmt bgr24 -s WIDTHxHEIGHT -r 30 -i - -f ogg -an -qscale:v 10 pipe:1'
    cmd = cmd.replace('WIDTH', width).replace('HEIGHT', height)
    cmd = cmd.split(' ')
    
    # lets you skip forward
    start = request.args.get("start") or 0
    def generate():
        proc = subprocess.Popen(cmd, stdout=subprocess.PIPE, stdin=opencv_ps.stdout)
        try:
            f = proc.stdout
            byte = f.read(512)
            while byte:
                yield byte
                byte = f.read(512)
        finally:
            proc.kill()

    return Response(response=generate(),
                    status=200,
                    mimetype='video/ogg',
                    headers={'Access-Control-Allow-Origin': '*',
                             "Content-Type": "video/ogg",
                             "Content-Disposition": "inline",
                             "Content-Transfer-Enconding": "binary"})

if __name__ == '__main__':
    app.run(host='0.0.0.0', threaded=True, debug=True)