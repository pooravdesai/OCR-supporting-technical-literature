#import bbox_image_preprocessing as bip
import numpy as np
#import pandas as pd
import cv2
import string
def getData(data,number_of_tuples,start = 0):
	numeric = ['zero','one','two','three','four','five','six','seven','eight','nine']
	l = list(string.ascii_lowercase) + list(string.ascii_uppercase) + numeric
	dataset = np.empty((0,data.shape[1]),dtype = data.values.dtype)
	for i in l:
		entity = data.loc[data['Entity'].isin([i])]
		dataset = np.vstack((dataset,entity.values[start:start + number_of_tuples]))
	return dataset

def prepareData(dataset):
	path = 'Images/'
	image = None
	inputx = None
	l = list(string.ascii_lowercase)+list(string.ascii_uppercase)
	numeric = ['zero','one','two','three','four','five','six','seven','eight','nine']
	digit = list(string.digits)
	numeric_to_digit = dict(zip(numeric,digit))
	for index in dataset:
		if image is not index[2]:
			image = cv2.imread(path+index[2],0)
			#print(path+index[2])
			retval,image = cv2.threshold(image,127,255,cv2.THRESH_BINARY_INV)
		#image =	bip.bbox_image_preprocess(image)
		image = bbox_image_preprocess(image)
		image.resize((1,np.size(image)))	#reshape it into a row vector
		if inputx is None:
			inputx = np.empty((0,image.shape[1]),dtype = image.dtype)
			targety = np.empty((0,1),dtype = type(ord(index[1])))
		inputx = np.vstack((inputx,image))
		if index[1] in l:
			targety = np.vstack((targety,ord(index[1])))
		else:
			targety = np.vstack((targety,ord(numeric_to_digit[index[1]])))
	return inputx,targety


def bbox_image_preprocess(bbox_image):
	padding_size = 10
	#print(type(bbox_image))
	horizontal_padding = np.zeros((bbox_image.shape[0],padding_size),dtype = bbox_image.dtype)
	bbox_image = np.hstack((horizontal_padding,bbox_image,horizontal_padding))

	vertical_padding = np.zeros((padding_size,bbox_image.shape[1]),dtype = bbox_image.dtype)
	bbox_image = np.vstack((vertical_padding,bbox_image,vertical_padding))

	target_image_dim = (100,100)
	bbox_image = cv2.resize(bbox_image,target_image_dim)

	retval,bbox_image = cv2.threshold(bbox_image,127,255,cv2.THRESH_BINARY)
	#print(type(bbox_image))

	return bbox_image



#data = pd.read_csv('In3.csv',header = 0,usecols = ['ImageName','Rect','Rect.1','Rect.2','Rect.3','Code','Entity'])	#edit this path
#training_data = getData(data,1)
#print(training_data.shape)
