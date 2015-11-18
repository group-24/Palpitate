from spectrogram import full_bpm_to_data, HEART_AV_ROOT, NormalizedSpectrograms
from get_heartrates import get_interesting_heartrates
from keras.callbacks import EarlyStopping
from kbhit import KBHit

import numpy as np
import code
import random
import learnLib

kb = KBHit()
#(X_train, y_train), (X_test, y_test) = full_bpm_to_data(get_interesting_heartrates(HEART_AV_ROOT))

ns = NormalizedSpectrograms()

def sliceToTimeSeries(X):
    divisibleTime = X[:,0,:,:150]
    slicedTime = np.reshape(divisibleTime, (-1, X.shape[2], 30, 5))
    swappedAxes = np.swapaxes(slicedTime, 1, 2)
    flattenLastTwo = np.reshape(swappedAxes,(X.shape[0],30 , -1))
    return flattenLastTwo


(X_train, Y_train) , (X_val, Y_val) = ns.getTrainAndValidationData()

#slice the spectrogram
X_train = sliceToTimeSeries(X_train)
print(X_train.shape)
#Y_train = np.repeat(np.reshape(-1,1), X_train.shape[1], axis=1)
print(Y_train.shape)

print("Model: lstm outdim, nb_hiddens, drop1, drop2")


prevLoss =  34534645735673
maxModel = None
stop = False
models = {}
X_val = sliceToTimeSeries(X_val)

for args in learnLib.RandomRnnParameters(): #itertools.product(nb_hiddens, drop1s):
    print("Model: ", args)
    model = learnLib.get_RNN_model(X_train[0].shape, *args)
    early_stopping = EarlyStopping(monitor='val_loss', patience=3)
    history = model.fit(X_train, Y_train, batch_size=100, nb_epoch=20,
            verbose=1, validation_data=(X_val,Y_val), callbacks=[early_stopping])


    # most recent loss hist.history["loss"][-1]
    r, rmse, _ = learnLib.assess_model(model, X_val, Y_val)
    models[args]  = r,rmse
    print("Model r: ", r)
    print("Model rmse: ", rmse)
    if rmse < prevLoss:
        prevLoss = rmse
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

X_test, Y_test = ns.getTestData()
X_test = sliceToTimeSeries(X_test)

learnLib.printModels(models)

r, rmse, preds = learnLib.assess_model(maxModel, X_test, Y_test)
predicted_bpm = np.array(list(map(ns.unnormalize_bpm, preds)))
print("Model r: ", r)
print("Model rmse: ", rmse)
code.interact(local=locals())
