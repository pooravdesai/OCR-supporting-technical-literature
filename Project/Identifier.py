import numpy as np
import cv2
from sklearn.neural_network import MLPClassifier
from sklearn.externals import joblib

class Identifier:
    
    def bbox_image_preprocess(self,bbox_image):
        padding_size = 10
        horizontal_padding = np.zeros((bbox_image.shape[0],padding_size),dtype = bbox_image.dtype)
        bbox_image = np.hstack((horizontal_padding,bbox_image,horizontal_padding))

        vertical_padding = np.zeros((padding_size,bbox_image.shape[1]),dtype = bbox_image.dtype)
        bbox_image = np.vstack((vertical_padding,bbox_image,vertical_padding))

        target_image_dim = (100,100)
        bbox_image = cv2.resize(bbox_image,target_image_dim)

        retval,bbox_image = cv2.threshold(bbox_image,127,255,cv2.THRESH_BINARY)
        return bbox_image 
    
    def prepareData(self,image,bbox):
        inputx = np.empty((len(bbox),10000),dtype = image.dtype)
        count = 0
        for boundary in bbox:
            left,top,right,bottom = boundary
            character_image = self.bbox_image_preprocess(image[top:bottom+1,left:right+1])
            #cv2.imwrite('image' + str(count) + '.png', character_image)
            inputx[count] = np.ravel(character_image)
            count += 1
        return inputx

    
    def predict(self,inputx):
        model = joblib.load('model.pkl')
        prediction = model.predict(inputx)
        return prediction
   
    
    def identify(self,image,bbox):	
        inputx = self.prepareData(image,bbox)
        prediction = self.predict(inputx)
        for x,y in zip(bbox,prediction):
            x.append(chr(y))
        return bbox


	


	

	
