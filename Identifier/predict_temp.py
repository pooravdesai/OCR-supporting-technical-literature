import numpy as np
import cv2
from sklearn.externals import joblib


image = '40.png'
#inputx_test = np.load('inputx_test.npy')
#targety_test = np.load('targety_test.npy')

inputx = cv2.imread(image,0)

mlp = joblib.load('model.pkl')
output = mlp.predict(inputx.reshape(1,-1))

print(chr(output))

