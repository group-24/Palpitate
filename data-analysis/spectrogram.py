import convertToWav
import numpy as np
import tables as tb
import os
from scipy.io import wavfile
from scipy import signal
from get_heartrates import check_cache, write_cache

import matplotlib.pyplot as plt
import pylab
import re
import random
import code
import errno


class SubjectWav:
    def __init__(self, wav_file):
        self.wav_file = wav_file
        self.sample_rate = None
    def __load_data__(self):
        if self.sample_rate is None:
            fs, frames = wavfile.read(self.wav_file)
            self.sample_rate = fs
            self.audio_data = frames
    def get_spectrogram(self, at_second, for_seconds=4,channel=0, window_length=0.2, max_freqency=4000):
        """
            Gets the spectrogram for the file. With window_length in seconds and
            0-max_freqency Hz range. The shorter the window_length the smaller
            freqency resolution
        """
        self.__load_data__()
        at_second = int(at_second)
        fs = max_freqency * 2
        nfft = int(fs*window_length)
        noverlap = nfft/ 2

        window_start = at_second * self.sample_rate
        window_size = for_seconds * self.sample_rate
#       code.interact(local=locals())
        f, t, Sxx = signal.spectrogram(self.audio_data[window_start:window_start + window_size,channel],
                      fs,
                      nperseg = nfft, #self.freqency_resolution,
                      noverlap = noverlap,
                      nfft = nfft
                      )
                #to decibel
        return f, t, 20.*np.log10(np.abs(Sxx)/10e-6)



def plotSubjectWav(sw, at_second,for_seconds=4):
    f, t, Sxx = sw.get_spectrogram(at_second,for_seconds)
    plt.pcolormesh(t, f, Sxx)
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
        return readh5File()
    except IOError:
        pass
    pattern = re.compile(".*vp_(\\d+)_(\\d+)_.*")
    prevElem = None
   # limit = 250
    h5file = tb.openFile('spectrograms.h5', mode='w', title="All the data")
    root = h5file.root
    first = True
    X_train = None
    Y_train = None
    X_test = None
    Y_test = None


    for wavFile in iterateThroughWav():
        m = pattern.match(wavFile)
        subjectId = int(m.group(1))
        stateId = int(m.group(2))
        sw = SubjectWav(wavFile)
        subjectStateId = str(subjectId) + "_" + str(stateId).zfill(2)
        try:
            for _,timestamp,bpm in data[subjectStateId]:
                #reduces the memory used
             #   if random.uniform(0,1) < 0.9:
             #       continue
                timestamp = int(timestamp)
                bpm = round(float(bpm))
                _,_,Sxx0 = sw.get_spectrogram(timestamp,4,0)
                _,_,Sxx1 = sw.get_spectrogram(timestamp,4,1)
               # print(Sxx0.shape) #(651,154) (801,219)
                elem = np.array([Sxx0,Sxx1])
                if prevElem is not None and elem.shape != prevElem.shape:
                    print("skipping " + str(wavFile) + " " + subjectStateId +
                            " due to incorrect shape")
                    continue
                prevElem = elem
                #store the elem to disk
                if first:
                    first = False
                    a = tb.Atom.from_dtype(np.dtype('Float32'))
                    data_shape = tuple([0] + list(elem.shape))
                    X_train = h5file.create_earray(root,'X_train',a,data_shape ,"X_train")
                    X_test = h5file.create_earray(root,'X_test',a, data_shape,"X_test")
                    Y_train = h5file.create_earray(root,'Y_train',tb.IntAtom(), (0,),"Y_train")
               #     code.interact(local=locals())
                    Y_test = h5file.create_earray(root,'Y_test',tb.IntAtom(), (0,),"Y_test")
                if random.uniform(0,1) < 0.9:
                    X_train.append(np.array([elem]))
                    Y_train.append([bpm])
                else:
                    X_test.append(np.array([elem]))
                    Y_test.append([bpm])
            h5file.flush()
        except KeyError:
            print("can not find: " + subjectStateId + ".")
            pass
        print("converted " + str(wavFile))
    #Could not broadcast error means that not all elemnt of X_train have the same shape
    #usually meaning there is something wrong with files
    h5file.close()
#    data = (X_train, Y_train) , (X_test, Y_test)
#    write_cache(SPECTROGRAM_CACHE,data)
    return readh5File()


def readh5File():
    h5file = tb.openFile('spectrograms.h5', mode='r', title="All the data")
    return ((h5file.root.X_train , h5file.root.Y_train),
            (h5file.root.X_test, h5file.root.Y_test))

def make_sure_path_exists(path):
    try:
        os.makedirs(path)
    except OSError as exception:
        if exception.errno != errno.EEXIST:
            raise


if __name__ == "__main__":
    sw = None
    for p in iterateThroughWav():
        sw = SubjectWav(p)
    plotSubjectWav(sw, 31*60+17)

# make_sure_path_exists("dat")
#                filename = os.path.join("dat", subjectStateId + "_" + str(timestamp))
#                memmap_elem = np.memmap(filename,dtype='float32',mode='w+', shape=(elem.shape))
#                memmap_elem[:] = elem[:]
#                del memmap_elem #flushes to disk
#                #make a ro version of it that goes into the list
#                ro_elem = np.memmap(filename,dtype='float32',mode='r', shape=elem.shape)
#
