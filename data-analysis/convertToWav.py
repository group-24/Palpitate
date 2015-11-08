import os
import subprocess



VIDEO_ROOT = "C:\\Uni\\HeartAV\\SensorData\\HeartAV_VideoFiles"
if __name__ == "__main__":
	for avi in os.listdir(VIDEO_ROOT):
		if avi.endswith(".avi"):
			full_path = VIDEO_ROOT + "\\" + avi
			command = "ffmpeg -i " + full_path + " -ab 160k -ac 2 -ar 44100 -vn " + full_path[:-4] + ".wav"
			print("Proccessing:")
			print(full_path)
			subprocess.call(command)
	print("done")
