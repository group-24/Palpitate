from spectrogram import full_bpm_to_data, HEART_AV_ROOT, NormalizedSpectrograms, NormalizedSubjectSplitSpectrograms
from get_heartrates import get_interesting_heartrates
from keras.callbacks import EarlyStopping
from kbhit import KBHit

import numpy as np
import code
import random
import learnLib

kb = KBHit()
#(X_train, y_train), (X_test, y_test) = full_bpm_to_data(get_interesting_heartrates(HEART_AV_ROOT))

ns = NormalizedSubjectSplitSpectrograms()

(X_train, Y_train) = ns.getTrainData()
valTuple = ns.getValidationData()

print(X_train.shape)


print("Model: nb_hiddens, drop1s")


prevLoss =  34534645735673
maxModel = None
stop = False
models = {}
X_validate, Y_validate = valTuple
for args in learnLib.RandomMlpParameters(): #itertools.product(nb_hiddens, drop1s):
    print("Model: ", args)
    model = learnLib.get_2_layer_MLP_model(X_train[0].shape, *args)
    early_stopping = EarlyStopping(monitor='val_loss', patience=2)
    history = model.fit(X_train, Y_train, batch_size=100, nb_epoch=10,
            verbose=1, validation_data=valTuple, callbacks=[early_stopping])


    # most recent loss hist.history["loss"][-1]
    r, rmse, _ = learnLib.assess_model(model, X_validate, Y_validate)
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

learnLib.printModels(models)

r, rmse, preds = learnLib.assess_model(maxModel, X_test, Y_test)
predicted_bpm = np.array(list(map(ns.unnormalize_bpm, preds)))
print("Model r: ", r)
print("Model rmse: ", rmse)
code.interact(local=locals())
