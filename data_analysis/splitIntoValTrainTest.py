import pickle
import random

spec = pickle.load(open( "spec.pickle", "rb" ))
keys = spec.keys()
val = 0.3
test = 0.3
train = 0.4
split = {'train':[], 'test':[], 'validation':[]}
for k in keys:
    r = random.random()
    if r < val:
        split['validation'].append(k)
    elif r < val + test:
        split['test'].append(k)
    else:
        split['train'].append(k)

pickle.dump(split, open("testTrainValidation.pickle", "wb"))
print(split)

