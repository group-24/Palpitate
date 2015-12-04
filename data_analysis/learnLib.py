from keras.models import Sequential
from keras.layers.core import Dense, Activation, Dropout, Flatten, TimeDistributedDense, Reshape, Permute
from keras.layers.convolutional import Convolution2D, MaxPooling2D
from keras.layers.recurrent import LSTM, GRU, SimpleDeepRNN
from keras.layers.noise import GaussianNoise
from keras.regularizers import l2
from keras.callbacks import EarlyStopping
from scipy.stats import pearsonr
from sklearn.metrics import mean_squared_error
from math import sqrt

import random
import numpy as np
import code

class RandomMlpParameters():
    def __init__(self):
        self.__cnt = 0

    def __iter__(self):
        return self

    def __next__(self):
        self.__cnt += 1
        if self.__cnt > 100:
            raise StopIteration
        return random.randrange(100,1000,500), random.uniform(0.2,0.8)

def printModels(models):
    for key, value in models.items():
        print("Model: " + str(key) + " r: " + str(value[0][0]) + " rmse: " + str(value[1]))

def get_2_layer_MLP_model(in_shape, nb_hidden=50, drop1=0.1):
    model = Sequential()

    model.add(GaussianNoise(0.05, input_shape=in_shape))
    model.add(Flatten(input_shape=in_shape))
    model.add(Dense(nb_hidden))
    model.add(Activation('relu'))
    model.add(Dropout(drop1))

    model.add(Dense(1))
    model.add(Activation('linear'))

    model.compile(loss='mse', optimizer='adam')
    return model

def assess_2dmodel(model, X_test, Y_test):
    predictions = model.predict(X_test)
    minDim = min(Y_test.shape[1], predictions.shape[1])
    r = pearsonr(np.mean(predictions[:,0:minDim,0],axis=0), np.mean(Y_test[:,0:minDim,0],axis=0))
    rmse = sqrt(mean_squared_error(predictions[:,0:minDim,0], Y_test[:,0:minDim,0]))
    return r, rmse, predictions

def assess_model(model, X_test, Y_test):
    predictions = model.predict(X_test)
    r = pearsonr(predictions[:,0], Y_test[:,0])
    rmse = sqrt(mean_squared_error(predictions, Y_test))
    return r, rmse, predictions



def shuffle_in_unison(a, b):
    rng_state = np.random.get_state()
    np.random.shuffle(a)
    np.random.set_state(rng_state)
    np.random.shuffle(b)

class RandomRnnParameters():
    def __init__(self):
        self.__cnt = 0

    def __iter__(self):
        return self

    def __next__(self):
        self.__cnt += 1
        if self.__cnt > 100:
            raise StopIteration
        return  random.randrange(300,600,50), \
                random.randrange(100,400,20), \
                random.randrange(200,300,20), \
                random.uniform(0.3,0.7), \
                random.uniform(0.3,0.7)


def get_RNN_model(in_shape,td_num=512, ltsm_out_dim = 256,nb_hidden=100, drop1=0.5, drop2=0.5):
    model = Sequential()

    model.add(GaussianNoise(0.05, input_shape=in_shape))
    model.add(LSTM(ltsm_out_dim, return_sequences=True))
    reg = l2(0.05)
    model.add(TimeDistributedDense(td_num, W_regularizer=l2(0.03)))
    #reg.set_param(model.layers[3].get_params()[0][0])
    #model.layers[3].regularizers = [reg]
    model.add(Dropout(drop1))

    model.add(LSTM(ltsm_out_dim))
  #  reg = l2(0.05)
  #  reg.set_param(model.layers[3].get_params()[0][0])
  #  model.layers[3].regularizers = [reg]
    model.add(Dropout(drop1))
#    model.regularizers = [l2(0.05)]
    #model.add(Activation('relu'))

    model.add(Flatten())
    model.add(Dense(nb_hidden, W_regularizer=l2(0.05)))
    model.add(Activation('relu'))
    model.add(Dropout(drop2))

    model.add(Dense(1))
    model.add(Activation('linear'))

    model.compile(loss='mse', optimizer='rmsprop')
    return model



class RandomCnnRnnParameters():
    def __init__(self):
        self.__cnt = 0

    def __iter__(self):
        return self

    def __next__(self):
        self.__cnt += 1
        if self.__cnt > 100:
            raise StopIteration
        return  random.randrange(16,32,2), \
                random.randrange(3,15,2), \
                random.randrange(32,256,6), \
                random.randrange(5,15,2), \
                random.randrange(50,300,30), \
                random.uniform(0.3,0.7), \
                random.uniform(0.3,0.7)

def get_CNN_RNN_model(in_shape, nb_filters1 = 32,nb_col1=5,
                                nb_filters2 = 64,nb_col2=10,
                                ltsm_out_dim = 256, drop1=0.5, drop2=0.5):
    model = Sequential()

    # shape (n_images, frequencies, time)
    # shape (1,200,158)
    model.add(GaussianNoise(0.05, input_shape=in_shape))
    #Convolution2D(nb_filter, nb_row, nb_col)

    model.add(Convolution2D(nb_filters1,in_shape[1],nb_col1, W_regularizer=l2(0.05)))
    model.add(Activation('relu'))
#    model.add(MaxPooling2D((1,2)))
    model.add(Dropout(drop2))

    # shape (16,1,77)
    model.add(Convolution2D(nb_filters2,1,nb_col2,W_regularizer=l2(0.05)))
    model.add(Activation('relu'))
#    model.add(MaxPooling2D((1,2)))
    model.add(Dropout(drop2))


    # shape (32,1,68)
    shape = model.layers[-1].input_shape
    model.add(Reshape(dims=(shape[1],shape[3])))
    #shape (32,68)
    model.add(Permute((2,1)))
    model.add(LSTM(ltsm_out_dim,return_sequences=True))
    model.add(Dropout(drop1))

    model.add(TimeDistributedDense(1, W_regularizer=l2(0.05)))
    model.add(Activation('linear'))
    print("Model output " + str(model.layers[-1].input_shape))

    model.compile(loss='mse', optimizer='adam')
    return model
