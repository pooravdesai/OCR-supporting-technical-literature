import numpy as np
import pandas as pd
import cv2
import string
import bbox_image_train as bit
from sklearn.neural_network import MLPClassifier 

inputx = np.load('inputx.npy')
targety = np.load('targety.npy')
inputx_test = np.load('inputx_test.npy')
targety_test = np.load('targety_test.npy')

bias = np.ones((inputx.shape[0],1),dtype = inputx.dtype)
inputx = np.hstack((bias,inputx))/1.
bias_test = np.ones((inputx_test.shape[0],1),dtype = inputx_test.dtype)
inputx_test = np.hstack((bias_test,inputx_test))/1.
#targety = targety.T
#targety_test = targety_test.T

mlp = MLPClassifier(hidden_layer_sizes = (400,400,),activation = 'logistic',learning_rate_init = 0.003,verbose = True,random_state = 1)
print("enter fit")
mlp.fit(inputx,targety)
print("exit fit")
#np.save('model',mlp)

res = mlp.predict(inputx) == targety
mean = np.mean(res)*100
print("training data accuracy: %f"%mean)
res = mlp.predict(inputx_test) == targety_test
mean = np.mean(res)*100
print("testing data accuracy: %f"%mean)