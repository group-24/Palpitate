import os
import subprocess

VIDEO_ROOT = "D:\HeartAV\SensorData\HeartAV_VideoFiles"

for avi in os.listdir(VIDEO_ROOT):
    if avi.endswith(".avi"):
        full_path = VIDEO_ROOT + "\\" + avi
        command = "ffmpeg -i " + full_path + " -c:v libx264 -crf 19 -preset superfast -an " + full_path[:-4] + ".mp4"
        print("Proccessing:")
        print(full_path)
        subprocess.call(command)
print("done")

# full_path = VIDEO_ROOT + "\\" + 'vp_035_01_00[2014][03][26][17][34]28.avi'
# command = "ffmpeg -i " + full_path + " -c:v libx264 -crf 19 -preset superfast -an " + full_path[:-4] + ".mp4"
# print("Proccessing:")
# print(full_path)
# subprocess.call(command)
