from spectrogram import bpm_to_data
from get_heartrates import get_interesting_heartrates
from convertToWav import VIDEO_ROOT
from keras.models import Sequential  
from keras.layers.core import Dense, Activation, Dropout, Flatten
from keras.layers.convolutional import Convolution2D, MaxPooling2D
from keras.optimizers import SGD
from keras.utils import np_utils

import random
import numpy as np
import code
#dumy_data_subject1 = [(i*5 + 1, random.randint(lowest_bpm, highest_bpm)) for i in range(1,200)]
#dumy_data = {35 : dumy_data_subject1}

(X_train, y_train), (X_test, y_test) = bpm_to_data(get_interesting_heartrates("C:\\Uni\\HeartAV"))

lowest_bpm = min(min(y_train) , min(y_test))
highest_bpm = max(max(y_train) , max(y_test))
nb_classes = highest_bpm - lowest_bpm + 1
nb_filters = 32
nb_conv = 3 
nb_pool = 2




y_train = list(map(lambda x : x - lowest_bpm, y_train))
y_test = list(map(lambda x : x - lowest_bpm, y_test))
# convert class vectors to binary class matrices
# converts a number to unary so 4 is 0001
Y_train = np_utils.to_categorical(y_train, nb_classes)
Y_test = np_utils.to_categorical(y_test, nb_classes)

print(X_train[0].shape)
model = Sequential()
model.add(Convolution2D(nb_filters, 3,3, input_shape=(X_train[0].shape)))
model.add(Activation('sigmoid'))
model.add(Convolution2D(nb_filters, 3,3))
model.add(Activation('relu'))
model.add(MaxPooling2D(pool_size=(nb_pool, nb_pool)))
model.add(Dropout(0.25))

model.add(Flatten())
model.add(Dense(512))
model.add(Activation('tanh'))
model.add(Dropout(0.5))
model.add(Dense(nb_classes))
model.add(Activation('softmax'))

model.compile(loss='categorical_crossentropy', optimizer='adadelta')

model.fit(X_train, Y_train, batch_size=50, nb_epoch=5, show_accuracy=True, verbose=1, validation_data=(X_test, Y_test))
score = model.evaluate(X_test, Y_test, show_accuracy=True, verbose=0)
print('Test score:', score[0])
print('Test accuracy:', score[1])
