from flask import Flask, request, Response, abort, send_file, jsonify
import os, subprocess, re, sys

app = Flask(__name__)

video_file = sys.argv[1]
opencv_path = sys.argv[2]

# pipe testavi.avi to output
# change this to input pipe
# cmd = ['ffmpeg', '-i', u'/home/server/Bill_Clinton.avi', '-an', '-ss', '0', '-f', 'ogg', '-acodec', 'libvorbis', '-qscale:v', '10', 'pipe:1']
# cmd = ['ffmpeg', '-f', 'rawvideo', '-pix_fmt', 'bgr24', '-r', '30', '-i', '-', '-an', '-f', 'avi', '-r', '30', 'pipe:1']
# cmd = 'ffmpeg -f rawvideo -pix_fmt bgr24 -ss 0 -s 480x360 -r 30 -i - -f ogg -an -r 30 -qscale:v 10 pipe:1'.split(' ')
# cmd = 'ffmpeg -f rawvideo -pix_fmt bgr24 -ss 0 -s 480x360 -r 30 -i - -ss 0 -f avi -an -qscale:v 10 pipe:1'.split(' ')
# cmd = 'ffmpeg -f rawvideo -pix_fmt bgr24 -s 480x360 -r 30 -i - -f ogg -acodec libvorbis -qscale:v 10 pipe:1'.split(' ')
# raw_cmd = 'ffmpeg -f rawvideo -pix_fmt bgr24 -ss 0 -s 480x360 -r 30 -i - -ss 0 -f avi -an -qscale:v 10 pipe:1'.split(' ')
# avi_cmd = 'ffmpeg -f rawvideo -pix_fmt bgr24 -s 480x360 -r 30 -i - -an -ss 0 -f ogg -acodec libvorbis -qscale:v 10 pipe:1'.split(' ')
# MP4 does not support unseekable output

cmd = 'ffmpeg -f rawvideo -pix_fmt bgr24 -s 480x360 -r 30 -i - -f ogg -an -qscale:v 10 pipe:1'.split(' ')

@app.route('/')
def index():
    return "Hello world"

@app.route('/video')
def video():
    FNULL = open(os.devnull, 'w')

    hri_cmd = ['python', 'heart_rate_imposer.py', video_file, opencv_path]
    opencv_ps = subprocess.Popen(hri_cmd, stdout=subprocess.PIPE, stderr = FNULL)

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
