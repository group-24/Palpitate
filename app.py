from flask import Flask, request, Response, abort, send_file, jsonify, render_template, url_for, redirect, send_from_directory
from werkzeug import secure_filename
import os, subprocess, re, sys, difflib

app = Flask(__name__)

video_file = sys.argv[1]

@app.route('/')
def index():
    return render_template('homepage.html');

@app.route('/<path:filename>')
def uploaded_file(filename):
    return send_from_directory('/', filename)

@app.route("/upload", methods=['POST'])
def upload():
    print "Video request"
    age = request.form['age']
    gender = request.form['gender']

    if age and gender:
        print "Medical use case: Age " + age + ", " + gender

    file = request.files['file']
    if file:
        filename = secure_filename(file.filename)
        file.save(os.path.join('/', filename))

        client_proc_cmd = 'python heart_rate_client.py ' + url_for('uploaded_file', filename=filename) + ' ' + str(age) + ' ' + str(gender)
        client_proc = subprocess.Popen(client_proc_cmd.split(' '), stdout=subprocess.PIPE)

        header = client_proc.stdout.readline()
        print header
        [width, height, fps] = header.split(' ')

        cmd = 'ffmpeg -f rawvideo -pix_fmt bgr24 -s WIDTHxHEIGHT -r 30 -i - -i ' + url_for('uploaded_file', filename=filename) + ' -f ogg -qscale:v 10 pipe:1'
        cmd = cmd.replace('WIDTH', width).replace('HEIGHT', height)
        cmd = cmd.split(' ')
        
        # lets you skip forward
        start = request.args.get("start") or 0
        def generate():
            proc = subprocess.Popen(cmd, stdout=subprocess.PIPE, stdin=client_proc.stdout)
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