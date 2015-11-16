from spectrogram import full_bpm_to_data, HEART_AV_ROOT
from get_heartrates import get_interesting_heartrates
from keras.models import Sequential
from keras.layers.core import Dense, Activation, Dropout, Flatten
from keras.layers.convolutional import Convolution2D, MaxPooling2D
from keras.callbacks import EarlyStopping
from scipy.stats import pearsonr
from math import sqrt
from sklearn.metrics import mean_squared_error
from sklearn.cross_validation import train_test_split
from kbhit import KBHit

import numpy as np
import code
import itertools

kb = KBHit()
(X_train, y_train), (X_test, y_test) = full_bpm_to_data(get_interesting_heartrates(HEART_AV_ROOT))

MAX_BPM = 250
def normalize_bpm(bpm):
    return bpm / MAX_BPM
def unnormalize_bpm(bpm):
    return bpm * MAX_BPM

#so it fits into memory without paging
reduce_to = int(X_train.shape[0] * 0.7)
X_train = X_train[:reduce_to]
y_train = y_train[:reduce_to]

#Y_train = np.array(y_train)
#Y_test = np.array(y_test)
Y_test = y_test
#X_train = np.array(X_train)
#X_test = np.array(X_test)

print(X_train.shape)

def get_model_and_score( X_train, Y_train,
              nb_hidden=50, drop1=0.1, drop2=0.1, drop3=0.5,
              nb_filter=10, nb_pool=2, nb_rows = 2, nb_coloumns = 2):
    model = Sequential()

    row_num = X_train.shape[2]
    model.add(Convolution2D(nb_filter,nb_rows,nb_coloumns, input_shape=(X_train[0].shape)))
    model.add(Activation('relu'))
    model.add(MaxPooling2D(pool_size=(nb_pool, nb_pool), ignore_border=False))
    #1D convolutions

    row_num = (row_num // nb_rows) // nb_pool
    nb_rows1 = max(1,   min(nb_rows, row_num))
    model.add(Convolution2D(nb_filter*4,nb_rows1,nb_coloumns))
    model.add(Activation('relu'))
    model.add(MaxPooling2D(pool_size=(nb_pool, nb_pool), ignore_border=False))
    model.add(Dropout(drop1))

    row_num = (row_num // nb_rows1) // nb_pool
    nb_rows1 = max(1,   min(nb_rows, row_num))
    model.add(Convolution2D(nb_filter*8, nb_rows1,nb_coloumns))
    model.add(Activation('relu'))
    model.add(MaxPooling2D(pool_size=(nb_pool, nb_pool), ignore_border=False))
    model.add(Dropout(drop2))

    model.add(Flatten())
    model.add(Dense(nb_hidden))
    model.add(Activation('relu'))
    model.add(Dropout(drop3))
    model.add(Dense(1))
    model.add(Activation('linear'))

    model.compile(loss='mse', optimizer='adam')

    early_stopping = EarlyStopping(monitor='val_loss', patience=2)
    history = model.fit(X_train, Y_train, batch_size=100, nb_epoch=15,
            verbose=1, validation_split=0.1, callbacks=[early_stopping])

    return history, model

def assess_model(model, X_test, Y_test):
    predictions = model.predict(X_test)
    r = pearsonr(predictions[:,0], Y_test)
    rmse = sqrt(mean_squared_error(predictions, Y_test))
    return r, rmse, predictions

def shuffle_in_unison_scary(a, b):
    rng_state = np.random.get_state()
    np.random.shuffle(a)
    np.random.set_state(rng_state)
    np.random.shuffle(b)

nb_pools = [2]
nb_rows = [X_train.shape[2]] #if set to lower numbers seems to masivelly overfit
nb_columns = [3,6]
nb_filters = [32,16,64]
drop1s = [0.5]
drop2s = [0.5]
drop3s = [0.5]
nb_hiddens = [200,300]

print("Model: nb_hiddens, drop1s, drop2s, drop3s, nb_filters, nb_pools, nb_rows, nb_columns")


#X_train, X_validate, Y_train, Y_validate = train_test_split(X_train, Y_train, test_size=0.25, random_state=4)

split_at = X_train.shape[0] // 4

X_validate = np.array(X_train[:split_at])
Y_validate = np.array(list(map(normalize_bpm, y_train[:split_at])))
print(split_at)

Y_train = np.array(list(map(normalize_bpm, y_train[split_at:])))
X_train = np.array(X_train[split_at:])
shuffle_in_unison_scary(X_train, Y_train)

prevLoss = 223942309
maxModel = None
stop = False
for args in itertools.product(nb_hiddens, drop1s, drop2s, drop3s, nb_filters, nb_pools, nb_rows, nb_columns):
    print("Model: ", args)
    hist , model = get_model_and_score(X_train, Y_train, *args)
    # most recent loss hist.history["loss"][-1]
    r, rmse, _ = assess_model(model, X_validate, Y_validate)
    print("Model r: ", r)
    print("Model rmse: ", rmse)
    if r[0] < prevLoss:
        prevLoss =  r[0]
        maxModel = model
    while kb.kbhit():
        try:
            if "q" in kb.getch():
                print("quiting due to user pressing q")
                stop = True
        except UnicodeDecodeError:
            pass

    if stop:
        break

del X_train

X_test = np.array(X_test)
Y_test_norm = np.array(list(map(normalize_bpm, Y_test)))

r, rmse, preds = assess_model(maxModel, X_test, Y_test_norm)
predicted_bpm = np.array(list(map(unnormalize_bpm, preds)))
print("Model r: ", r)
print("Model rmse: ", rmse)
code.interact(local=locals())
