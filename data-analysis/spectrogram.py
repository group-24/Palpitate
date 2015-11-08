import convertToWav
import numpy as np
import os
from scipy.io import wavfile
from scipy import signal
from get_heartrates import check_cache, write_cache

import matplotlib.pyplot as plt
import pylab
import re
import random
import code


class SubjectWav:
	def __init__(self, wav_file):
		self.wav_file = wav_file
		self.sample_rate = None
		self.freqency_resolution = 1300 #uknown measure of frequency resolution, higher number, larger resolution
	def __load_data__(self):
		if self.sample_rate is None:
			fs, frames = wavfile.read(self.wav_file)
			self.sample_rate = fs
			self.audio_data = frames
	def get_spectrogram(self, at_second, for_seconds=4,channel=0):
		self.__load_data__()
		at_second = int(at_second)
		window_start = at_second * self.sample_rate	
		window_size = for_seconds * self.sample_rate
#		code.interact(local=locals())
		f, t, Sxx = signal.spectrogram(self.audio_data[window_start:window_start + window_size,channel],
					  self.sample_rate,
					  nperseg = self.freqency_resolution,
					  ) 
				#to decibel
		return f, t, 20.*np.log10(np.abs(Sxx)/10e-6)
	


def plotSubjectWav(sw, at_second,for_seconds=4):
	f, t, Sxx = sw.get_spectrogram(at_second,for_seconds)
	plt.pcolormesh(t, f[0:300], Sxx[0:300])
	plt.ylabel('Frequency [Hz]')
	plt.xlabel('Time [sec]')
	plt.show()

"""
	itearates through all wav files, executing func and passing it the path to wav file
"""
def iterateThroughWav():
	for wav in os.listdir(convertToWav.VIDEO_ROOT):
		if wav.endswith(".wav"):
			full_path = convertToWav.VIDEO_ROOT + "\\" + wav
			yield full_path

SPECTROGRAM_CACHE = "spectrogramCache.dat"
def bpm_to_data(data, train_split=0.9):
	try:
		return check_cache(SPECTROGRAM_CACHE)
	except FileNotFoundError:
		pass
	pattern = re.compile(".*vp_(\\d+)_(\\d+)_.*")
	X_train = []
	Y_train = []
	X_test = []
	Y_test = []
	prevElem = None
	for wavFile in iterateThroughWav():
		m = pattern.match(wavFile)
		subjectId = int(m.group(1))
		stateId = int(m.group(2))
		sw = SubjectWav(wavFile)
		subjectStateId = str(subjectId) + "_" + str(stateId).zfill(2)
		try:
			for _,timestamp,bpm in data[subjectStateId]:
				timestamp = int(timestamp)
				bpm = round(float(bpm))
				_,_,Sxx0 = sw.get_spectrogram(timestamp,4,0)
				_,_,Sxx1 = sw.get_spectrogram(timestamp,4,1)
				elem = np.array([Sxx0[0:100],Sxx1[0:100]])
				if prevElem is not None and elem.shape != prevElem.shape:
					print("skipping " + str(wavFile) + " " + subjectStateId + 
							" due to incorrect shape")
					continue
				prevElem = elem
				if random.uniform(0,1) < 0.9:
					X_train.append(elem)
					Y_train.append(bpm)
				else:
					X_test.append(elem)
					Y_test.append(bpm)
		except KeyError:
			print("can not find: " + subjectStateId + ".")
			pass
		print("converted " + str(wavFile))
	#Could not broadcast error means that not all elemnt of X_train have the same shape
	#usually meaning there is something wrong with files
	data = (np.array(X_train), np.array(Y_train)) , (np.array(X_test), np.array(Y_test))
	write_cache(SPECTROGRAM_CACHE,data)
	return data



if __name__ == "__main__":
	sw = None
	for p in iterateThroughWav():
		sw = SubjectWav(p)
	plotSubjectWav(sw, 31*60+17)


