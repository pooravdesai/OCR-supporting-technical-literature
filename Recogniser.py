import numpy as np
import cv2
import math
import matplotlib.pyplot as plt


class Recogniser:
    K = 12
    

####################################################################################################    
    def reshape1(self, img):
        H, W = img.shape
        top = np.zeros((10, W), dtype = 'uint8')
        bottom = np.zeros((10, W), dtype = 'uint8')
        img = np.vstack((np.vstack((top, img)), bottom))
        H = img.shape[0]
        left = np.zeros((H,10), dtype = 'uint8')
        right = np.zeros((H,10), dtype = 'uint8')
        img = np.hstack((left, np.hstack((img, right))))
        return img 
    
####################################################################################################    
    def reshape2(self, img, K):
        H, W = img.shape
        h = (H // K + 1)*(K) - H
        w = (W // K + 1)*(K) - W
        t = int(math.ceil(h/2))
        b = int(math.floor(h/2))
        l = int(math.ceil(w/2))
        r = int(math.floor(w/2))        
        top = np.zeros((t,W), dtype = 'uint8')
        bottom = np.zeros((b,W), dtype = 'uint8')
        img = np.vstack((top, np.vstack((img, bottom))))
        H = img.shape[0]
        left = np.zeros((H,l), dtype = 'uint8')
        right = np.zeros((H,r), dtype = 'uint8')
        img = np.hstack((left, np.hstack((img, right))))
        return img 
    

####################################################################################################    
    def deskew(self, img):
        pts = np.column_stack(np.where(img > 0))
        ang = cv2.minAreaRect(pts)[-1]
        #print(ang)

        if ang < -45:
            ang = -(90 + ang)
        else:
            ang = -ang
    
        (H, W) = img.shape[:2]
        center = (W / 2, H / 2)    
        M = cv2.getRotationMatrix2D(center, ang, 1.0)
        rotated = cv2.warpAffine(img, M, (img.shape[1], img.shape[0]))
        cv2.imwrite("deskwed2.png", rotated)
        return rotated
 
    
####################################################################################################
    def detectLines(self):
        img = np.copy(self.imgBinInvDeskwed)
        hist = cv2.reduce(img, 1, cv2.REDUCE_AVG).reshape(-1)
        
        avg = sum(hist) / len(hist)
        th = avg*.10
        #print(avg, th)
        H,W = img.shape[:2]
        uppers = [y for y in range(H-1) if hist[y]<=th and hist[y+1]>th]
        lowers = [y for y in range(H-1) if hist[y]>th and hist[y+1]<=th]
        
        lines = [list((uppers[i], lowers[i], lowers[i] - uppers[i])) for i in range(0,len(uppers))]
        
        sm = 0
        for i in range(0,len(lines)):
            sm += lines[i][2]
        avg = sm / len(lines)
        th = avg*.25
        #print(avg, th)

        final_lines = []
        all_done = False
        while not all_done:
            all_done = True
            flag_prev = False
            flag = False
            for i in range(0,len(lines)):
                if lines[i][2] < th:
                    all_done = False
                    if i == 0:                 #update for only 1 line in a page
                        flag = True
                        final_lines.append(list((lines[i][0], lines[i+1][1], \
                                                 lines[i+1][1] - lines[i][0])))
                    elif i == len(lines) - 1:
                        a,b,c = final_lines[-1]
                        final_lines.pop()
                        final_lines.append(list((a, lines[i][1], lines[i][1] - a)))
                    elif lines[i][0] - lines[i-1][1] < lines[i+1][0] - lines[i][1]:
                        a,b,c = final_lines[-1]
                        final_lines.pop()
                        final_lines.append(list((a, lines[i][1], lines[i][1] - a)))
                    else:
                        flag = True
                        final_lines.append(list((lines[i][0], lines[i+1][1], \
                                                 lines[i+1][1] - lines[i][0])))
                elif not flag_prev:
                    final_lines.append(lines[i])   
                flag_prev = flag
                flag = False
            lines = list(final_lines)
            final_lines = []
    
        return lines

####################################################################################################
    def computeGrads(self, img, k):               #k is even
        H, W = img.shape
        cells = [np.hsplit(row, W//k) for row in np.vsplit(img, H//k)]
        cells = np.array(cells)
        m1 = np.ones((k,k), dtype='int32')
        m2 = np.ones((k,k), dtype='int32')
        m3 = np.ones((k,k), dtype='int32')
        
        for i in range(0, k):               #1 -1
            for j in range(k//2, k):         #1 -1
                m1[i][j] = -1
                
        for i in range(k//2, k):             # 1  1
            for j in range(0, k):           #-1 -1
                m2[i][j] = -1
            
        for i in range(0,k//2):              # 1 -1
            for j in range(k//2, k):         #-1  1
                m3[i][j] = -1
            
        for i in range(k//2, k):
            for j in range(0, k//2):
                m3[i][j] = -1
            
        grads = []
        for i in range(0, cells.shape[0]):
            for j in range(0, cells.shape[1]):
                d1 = abs(2*sum(np.multiply(cells[i,j,:,:], m1).ravel())/(k*k))
                d2 = abs(2*sum(np.multiply(cells[i,j,:,:], m2).ravel())/(k*k))
                d3 = abs(2*sum(np.multiply(cells[i,j,:,:], m3).ravel())/(k*k))
                grads.append((d1, d2, d3))
                
        return grads, cells


####################################################################################################    
    def binarise(self, norms, threshold):
        img = np.zeros(self.imgBinDeskwed.shape, dtype = 'uint8')
        for i in range(0, norms.shape[0]):
            for j in range(0, norms.shape[1]):
                if norms[i][j] <= threshold and \
                ((j!=0 and norms[i][j-1] <= threshold) \
                 or (i!= 0 and norms[i-1][j] <= threshold)  \
                 or (j != norms.shape[1]-1 and norms[i][j+1] <= threshold) \
                 or (i != norms.shape[0]-1 and norms[i+1][j] <= threshold)):     #left, above, right, below
                     for m in range(0, self.K):
                         for n in range(0, self.K):
                             img[i*self.K+m][j*self.K+n] = 0
                else:
                    for m in range(0, self.K):
                        for n in range(0, self.K):
                            img[i*self.K+m][j*self.K+n] = 255
        return img

####################################################################################################    
    
    def blur(self, img, k):
        grads, cells = self.computeGrads(img, k) 
        norms = np.array([sum(g) for g in grads])
        threshold = np.mean(norms)*.5 
        norms = norms.reshape((cells.shape[0], cells.shape[1]))
        imgNew = self.binarise(norms, threshold)
        return imgNew
    
    
####################################################################################################    
    def getBoxes(self, img):
        imgNew, contours, hierarchy = cv2.findContours(img, cv2.RETR_EXTERNAL, \
                                                     cv2.CHAIN_APPROX_SIMPLE)
        boxes = []
        for c in contours:
            a, b, c, d = cv2.boundingRect(c)
            boxes.append(list((a,b,a+c,b+d)))
            
        return boxes
    
####################################################################################################    
    def getWords(self, img, lines):
        l = []
        r = []
        for i in range(0, len(lines)):
            temp = np.copy(img[lines[i][0]:lines[i][1]][:]) 
            hist = cv2.reduce(temp,0, cv2.REDUCE_AVG).reshape(-1)
            avg = sum(hist) / len(hist)
            th = avg*.10
            H, W = temp.shape
            lefts = [y for y in range(W-1) if hist[y]<=th and hist[y+1]>th]
            rights = [y for y in range(W-1) if hist[y]>th and hist[y+1]<=th]
            l.append(lefts)
            r.append(rights)
        return l, r

####################################################################################################    
    def recognise(self, imgPath):
        self.imgPath = imgPath
        imgOrig = cv2.imread(imgPath)
        #print("read")
        imgGray = cv2.cvtColor(imgOrig, cv2.COLOR_BGR2GRAY)
        #print('grayed')
        #imgGray = cv2.fastNlMeansDenoising(imgGray,10,7,21)  #factor, template size, search size
        #print("denoised")
        imgBinInv = cv2.threshold(imgGray, 127, 255, cv2.THRESH_BINARY_INV)[-1]
        #print('binarised')
                
        imgBinInvMod = self.reshape1(imgBinInv)
        #print('mod1')
        imgBinInvMod = self.reshape2(imgBinInvMod, self.K)
        #print('mod2')
        self.imgBinInvDeskwed = self.deskew(imgBinInvMod)
        #print('deskwed')
        self.imgBinDeskwed = cv2.bitwise_not(self.imgBinInvDeskwed)
        #print('deskewinv')
        self.imgOrigDeskwed = cv2.cvtColor(self.imgBinDeskwed, cv2.COLOR_GRAY2BGR)
        #print('modcolor')
        
        self.lines = self.detectLines()
        #print(self.lines)
        
        self.imgBinInvBlur = self.blur(self.imgBinDeskwed, self.K)
        lefts,rights = self.getWords(self.imgBinInvBlur, self.lines)
        
        indx = 0
        for i in range(0, len(self.lines)):
            self.lines[i].append(list((indx, indx+len(lefts[i])-1)))
            indx += len(lefts[i])
            
        self.words = []
        for i in range(0, len(lefts)):
            for j in range(0, len(lefts[i])):
                self.words.append(list((lefts[i][j], self.lines[i][0], \
                                        rights[i][j], self.lines[i][1])))
        
        charBoxes = self.getBoxes(self.imgBinInvDeskwed)
        self.characters = []
        for i in range(0,len(self.words)):
            chars = []
            for c in charBoxes:
                cx, cy = (c[0] + c[2])/2, (c[1] + c[3])/2
                if self.words[i][0] <= cx <= self.words[i][2] \
                and self.words[i][1] <= cy <= self.words[i][3]:
                    chars.append(c)
            chars = sorted(chars,key=lambda l:l[0])
            f = len(self.characters)
            self.characters = self.characters + chars
            l = len(self.characters) - 1
            self.words[i].append(f)
            self.words[i].append(l)
            
        
        img1 = np.copy(self.imgOrigDeskwed)
        img2 = np.copy(self.imgOrigDeskwed)
        img3 = np.copy(self.imgOrigDeskwed)
        
        for i in range(0, len(self.lines)):
            cv2.line(img1, (0,self.lines[i][0]), (img1.shape[1], self.lines[i][0]), (255,0,0), 1)
            cv2.line(img1, (0,self.lines[i][1]), (img1.shape[1], self.lines[i][1]), (0,255,0), 1)
    
            
        for w in self.words:
           cv2.rectangle(img2, (w[0], w[1]), (w[2], w[3]), (0, 0, 255), 1)     
            
        for c in self.characters:
            cv2.rectangle(img3, (c[0], c[1]), (c[2], c[3]), \
                          (0, 255, 0), 1)
        
        cv2.imwrite('a1.png', self.imgBinInvDeskwed)
        cv2.imwrite('a2.png', self.imgBinDeskwed)
        cv2.imwrite('a3.png', self.imgOrigDeskwed)
        cv2.imwrite('a4.png', self.imgBinInvBlur)
        cv2.imwrite('a5.png', img1)
        cv2.imwrite('a6.png', img2)
        cv2.imwrite('a7.png', img3)
    
        
        
####################################################################################################        
r = Recogniser()
r.recognise('00_001.png') 
            
        
    
        