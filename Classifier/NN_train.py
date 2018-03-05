import numpy as np
import pandas as pd
import cv2
import string
import bbox_image_train as bit
from sklearn.neural_network import MLPClassifier 

data = pd.read_csv('In3.csv',header = 0,usecols = ['ImageName','Rect','Rect.1','Rect.2','Rect.3','Code','Entity'])

print('getData in')
dataset = bit.getData(data,200)
print('getData out')
dataset_test = bit.getData(data,50,201)

print('prepareData in')
inputx,targety = bit.prepareData(dataset)
np.save('inputx',inputx)
np.save('targety',targety)
inputx_test,targety_test = bit.prepareData(dataset_test)
np.save('inputx_test',inputx_test)
np.save('targety_test',targety_test)
print('prepareData out')

bias = np.ones((inputx.shape[0],1),dtype = inputx.dtype)
inputx = np.hstack((bias,inputx))/1.

bias_test = np.ones((inputx_test.shape[0],1),dtype = inputx_test.dtype)
inputx_test = np.hstack((bias_test,inputx_test))/1.

print('before')
mlp = MLPClassifier(hidden_layer_sizes = (160,))
print('after before')
mlp.fit(inputx,targety)
print('after')

res = mlp.predict(inputx_test) == targety_test
print(res)
print("training set score : %f"%mlp.score(inputx,targety))
print("test set score : %f"%mlp.score(inputx_test,targety_test))
#print("prediction:")
#print(mlp.predict(inputx_test))
#print("target:")
#print(targety_test)




