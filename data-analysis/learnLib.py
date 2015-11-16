from keras.models import Sequential
from keras.layers.core import Dense, Activation, Dropout, Flatten
from keras.layers.convolutional import Convolution2D, MaxPooling2D
from keras.callbacks import EarlyStopping
from scipy.stats import pearsonr
from sklearn.metrics import mean_squared_error
from math import sqrt



import random
import numpy as np

class RandomMlpParameters():
    def __init__(self):
        self.__cnt = 0
    def __iter__(self):
        return self
    def __next__(self):
        self.__cnt += 1
        if self.__cnt > 100:
            raise StopIteration
        return random.randrange(100,1000,100), random.uniform(0.2,0.8)

def printModels(models):
    for key, value in models.items():
        print("Model: " + str(key) + " r: " + str(value[0][0]) + " rmse: " + str(value[1]))

def get_2_layer_MLP_model(in_shape, nb_hidden=50, drop1=0.1):
    model = Sequential()

    model.add(Flatten(input_shape=in_shape))
    model.add(Dense(nb_hidden))
    model.add(Activation('relu'))
    model.add(Dropout(drop1))

    model.add(Dense(1))
    model.add(Activation('linear'))

    model.compile(loss='mse', optimizer='adam')
    return model

def assess_model(model, X_test, Y_test):
    predictions = model.predict(X_test)
    r = pearsonr(predictions[:,0], Y_test)
    rmse = sqrt(mean_squared_error(predictions, Y_test))
    return r, rmse, predictions

def shuffle_in_unison(a, b):
    rng_state = np.random.get_state()
    np.random.shuffle(a)
    np.random.set_state(rng_state)
    np.random.shuffle(b)
