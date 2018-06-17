import Recogniser
import Identifier
import Classifier
import Corrector
import EqnRec
import cv2
import numpy as np
import sys
from pylatex import Document, Math
from subprocess import call
from threading import Thread
from PyQt5.QtWidgets import *


class myThread(Thread):
    def __init__(self, str1, str2, status_field):
        super(myThread, self).__init__()
        self.image_loc = str1
        self.save_loc = str2
        self.status = status_field
        
    def run(self):
        self.status.append("Recogniser")
        recogniser = Recogniser.Recogniser()
        image, img, lines, words, characters = recogniser.recognise(self.image_loc)

        self.status.append("Identifier")
        identifier = Identifier.Identifier()
        characters = identifier.identify(image, characters)
        for i in range(0, len(words)):
            string = ''
            for j in range(words[i][4], words[i][5] + 1):
                string += characters[j][4]
            words[i].append(string)

        self.status.append("Classifier")
        words = Classifier.Classifier().classify(lines, words, characters)

        for i in range(0, len(words)):
            if type(words[i][-1]) is str:
                if words[i][-2].find('æ') != -1:
                    index  = words[i][-2].find('æ')
                    words[i][-2] = words[i][-2][0:index] + 'ae' + words[i][-2][index+1:]
                if words[i][-2].find('œ') != -1:
                    index  = words[i][-2].find('œ')
                    words[i][-2] = words[i][-2][0:index] + 'oe' + words[i][-2][index+1:]
                if words[i][-2].find('ﬀ') != -1:
                    index  = words[i][-2].find('ﬀ')
                    words[i][-2] = words[i][-2][0:index] + 'ff' + words[i][-2][index+1:]
                if words[i][-2].find('ﬁ') != -1:
                    index  = words[i][-2].find('ﬁ')
                    words[i][-2] = words[i][-2][0:index] + 'fi' + words[i][-2][index+1:]
                if words[i][-2].find('ﬂ') != -1:
                    index  = words[i][-2].find('ﬂ')
                    words[i][-2] = words[i][-2][0:index] + 'fl' + words[i][-2][index+1:]
                if words[i][-2].find('ﬃ') != -1:
                    index  = words[i][-2].find('ﬃ')
                    words[i][-2] = words[i][-2][0:index] + 'ffi' + words[i][-2][index+1:]
                if words[i][-2].find('ﬄ') != -1:
                    index  = words[i][-2].find('ﬄ')
                    words[i][-2] = words[i][-2][0:index] + 'ffl' + words[i][-2][index+1:]
                if words[i][-2].find('ﬅ') != -1:
                    index  = words[i][-2].find('ﬅ')
                    words[i][-2] = words[i][-2][0:index] + 'ft' + words[i][-2][index+1:]
        
        '''
        for w in words:
            if w[-1] == 'text':
                cv2.rectangle(img, (w[0], w[1]), (w[2], w[3]), (0, 0, 255), 3) 
            else:
                cv2.rectangle(img, (w[0], w[1]), (w[2], w[3]), (0, 255, 0), 3)
            
        cv2.imwrite('a8.png', img)
        '''

        self.status.append('Spell Corrector')
        words = Corrector.Corrector().correct(words)
        
        self.status.append('Equation Recognizer')
        indx = 0
        for w in words:
            if w[-1] == 'math':
                left, top, right, bottom = w[0], w[1], w[2], w[3]
                top -= 10
                bottom += 10
                tmp = image[top:bottom+1,left:right+1]
                H, W = tmp.shape
                top = np.zeros((10, W), dtype = 'uint8')
                bottom = np.zeros((10, W), dtype = 'uint8')
                tmp = np.vstack((np.vstack((top, tmp)), bottom))
                H = tmp.shape[0]
                left = np.zeros((H,10), dtype = 'uint8')
                right = np.zeros((H,10), dtype = 'uint8')
                tmp = np.hstack((left, np.hstack((tmp, right))))
                indx+=1
                w[-2] = EqnRec.EqnRec().eqnRec(tmp, tmp)
                
        self.status.append('Generating Output')
        
        for i in range(0, len(words)):
            if words[i][-1] is not None:
                if words[i][-2].find('æ') != -1:
                    index  = words[i][-2].find('æ')
                    words[i][-2] = words[i][-2][0:index] + 'ae' + words[i][-2][index+1:]
                if words[i][-2].find('œ') != -1:
                    index  = words[i][-2].find('œ')
                    words[i][-2] = words[i][-2][0:index] + 'oe' + words[i][-2][index+1:]
                if words[i][-2].find('ﬀ') != -1:
                    index  = words[i][-2].find('ﬀ')
                    words[i][-2] = words[i][-2][0:index] + 'ff' + words[i][-2][index+1:]
                if words[i][-2].find('ﬁ') != -1:
                    index  = words[i][-2].find('ﬁ')
                    words[i][-2] = words[i][-2][0:index] + 'fi' + words[i][-2][index+1:]
                if words[i][-2].find('ﬂ') != -1:
                    index  = words[i][-2].find('ﬂ')
                    words[i][-2] = words[i][-2][0:index] + 'fl' + words[i][-2][index+1:]
                if words[i][-2].find('ﬃ') != -1:
                    index  = words[i][-2].find('ﬃ')
                    words[i][-2] = words[i][-2][0:index] + 'ffi' + words[i][-2][index+1:]
                if words[i][-2].find('ﬄ') != -1:
                    index  = words[i][-2].find('ﬄ')
                    words[i][-2] = words[i][-2][0:index] + 'ffl' + words[i][-2][index+1:]
                if words[i][-2].find('ﬅ') != -1:
                    index  = words[i][-2].find('ﬅ')
                    words[i][-2] = words[i][-2][0:index] + 'ft' + words[i][-2][index+1:]
                
        
        
        for l in lines:
            count = sum([words[i][-1] == 'math' for i in range(l[3], l[4]+1)])    
            if count == l[4] - l[3] + 1:
                for i in range(l[3], l[4]+1):
                    words[i][-1] = 'mathDisplay'
            else:
                for i in range(l[3], l[4]+1):
                   if words[i][-1] == 'math':
                       words[i][-1] = 'mathInline'
        
        try:
            doc = Document()
            textString = ""
            mathString = ""
            count = 0
            lengthOfArray = len(words)
            while count < lengthOfArray:
                while count < lengthOfArray and (words[count][-1] == 'text' or words[count][-1] == 'mathInline'):
                    if words[count][-1] == 'mathInline':
                        textString += '$' + words[count][-2] + '$' + ' ' 
                    else:
                        textString += words[count][-2] + ' '    
                    count += 1
                doc.append(textString)
                textString = ""
                while count < lengthOfArray and words[count][-1]== 'mathDisplay':
                    mathString += words[count][-2] + ' '
                    count += 1
                    doc.append(Math(data = mathString, escape = False))
                    mathString = ""
            
            if sys.platform.startswith('win'):
                imageNameStartIndex = self.image_loc.rfind('\\')
            elif sys.platform.startswith('linux'):
                imageNameStartIndex = self.image_loc.rfind('/')

            imageNameEndIndex = self.image_loc.rfind('.')
            
            doc.generate_pdf(self.save_loc + self.image_loc[imageNameStartIndex:imageNameEndIndex],\
                             clean_tex=False,compiler='pdflatex')
        
        except:
            pass
        
        
        try:
            call(['C:/Program Files (x86)/latex2rtf/latex2rt.exe', \
                  self.save_loc + self.image_loc[imageNameStartIndex:imageNameEndIndex] + '.tex'])
        except:
            pass
        self.status.append("Output Generated")
        
        print ('\n')
    

def started(str1, str2, status_field):
    thread1 = myThread(str1, str2, status_field).start()
   

'''
if __name__ == '__main__':
    start('00_000.png')
'''
