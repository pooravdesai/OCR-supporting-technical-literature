import numpy as np
import cv2
import Identifier
import EqnParseLatex

class EqnRec:

    
#######################################################################################################
    def eqnRec(self, img, img2):
        l, r, u, l, d, c = self.getEqnLayout(img, img2)
        c = self.ocr(img, c)
        pseudoResult = self.identifyEqn(img, l, r, u, l, d, c)
        #print(pseudoResult)
        out = EqnParseLatex.EqnParser().parse(pseudoResult)
        #print(out)
        return out
#######################################################################################################
    
    def getEqnLayout(self, thresh, img):
        H,W = thresh.shape[:2]
        hist = cv2.reduce(thresh, 0, cv2.REDUCE_AVG).reshape(-1)
        th = 0
        lefts = [y for y in range(W-1) if hist[y]<=th and hist[y+1]>th]
        rights = [y for y in range(W-1) if hist[y]>th and hist[y+1]<=th]

        uppers = []
        lowers = []
        for i in range(0,len(lefts)):
            temp = np.copy(thresh[:, lefts[i]:rights[i] + 1])
            H,W = temp.shape[:2]
            hist = cv2.reduce(temp, 1, cv2.REDUCE_AVG).reshape(-1)
            th = 0
            uppers.append([y for y in range(H-1) if hist[y]<=th and hist[y+1]>th])
            lowers.append([y for y in range(H-1) if hist[y]>th and hist[y+1]<=th])

        chars = []
        numOfClumps = {}
        for i in range(0, len(lefts)):
            for j in range(0, len(uppers[i])):
                numOfClumps[(i,j)] = 0
                temp = np.copy(thresh[uppers[i][j]:lowers[i][j]+1, lefts[i]:rights[i]+1])
                contours= cv2.findContours(temp, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)[1]
                rects = [cv2.boundingRect(c) for c in contours]
                rects = sorted(rects,key=lambda l:l[0])
                
                for k in range(0, len(rects)):
                    rects[k] = rects[k][0], rects[k][1], rects[k][0]+rects[k][2],\
                                rects[k][1]+rects[k][3]
                
                k = 0
                while k < len(rects)-1:
                    xmin1, xmax1 = rects[k][1], rects[k][3]
                    xmin2, xmax2 = rects[k+1][1], rects[k+1][3]
                    ymin1, ymax1 = rects[k][0], rects[k][2]
                    ymin2, ymax2 = rects[k+1][0], rects[k+1][2]
                    #print(xmin1, xmax1, xmin2, xmax2, ymin1, ymax1, ymin2, ymax2)
                    if (ymin1 <= ymin2 and ymax2 <= ymax1 or ymin2 <= ymin1 and ymax1 <= ymax2) and \
                         (abs(max(xmin1,xmin2) - min(xmax1,xmax2)) / \
                         abs(max(xmax1, xmax2) - min(xmin1,xmin2)) < 0.50) and \
                          ((xmax1-xmin1 <= 25 and ymax1-ymin1 <= 25) or \
                           (xmax2-xmin2 <= 25 and ymax2-ymin2 <= 25)):####:  
                             
                            rects[k] = list((min(ymin1, ymin2), min(xmin1, xmin2),
                                              max(ymax1,ymax2), max(xmax1, xmax2)))
                            del rects[k+1]
                    k += 1
                
                for cnt in range(0, len(rects)):
                    numOfClumps[(i,j)] += 1
                    chars.append(list(((i,j,cnt), lefts[i]+rects[cnt][0], uppers[i][j]+rects[cnt][1],\
                                      lefts[i]+rects[cnt][2], uppers[i][j]+rects[cnt][3])))   #doubt
                    '''cv2.rectangle(img, (chars[-1][1], chars[-1][2]), (chars[-1][3], chars[-1][4]), \
                          (0, 0, 255), 1)
                     
                cv2.imwrite('ltx/z0.png', img) '''          
                            
                                       
        return lefts, rights, uppers, lowers, numOfClumps, chars

#######################################################################################################

    def identifyEqn(self, img, lefts, rights, uppers, lowers, numOfClumps, chars):
        isPow = 0
        canBePow = 0
        lastBottom = -1
        lastTop = 99999
        numOfOpenParens = 0
        inSqrt = 0
        startOfSumOrProductOrIntegral = 0
        sumOrProductOrIntegralBody = 0
        needRightParen = 0
        sumOrProductOrIntegralParenNum = 0
        checkIntegralRange = 0
        inIntegral = 0
        inIntegralLimits = 0
        intTop = -1
        intBottom = -1
        closeIntegral = 0
        word = ''
        col = -1
        row = -1
        charIndex = 0
        addNewLine = False
        ans = []

        for col in range(0, len(lefts)):
            numOfRows = 0
            pos = img.shape[0]
            for row in range(0, len(uppers[col])):
                numOfRows += 1
                if row != len(uppers[col]) - 1:
                    canBePow = 0          #base and exponenet not form different columns
                for i in range(charIndex, charIndex + numOfClumps[(col, row)]):
                    if chars[i][0][0] != col or chars[i][0][1] != row:
                        break

                    letter = chars[i][-1]
                    #print()
                    #print(letter, end = '')
                    if letter == '(':
                        #print('1 ', end = '')
                        numOfOpenParens += 1
                    if letter == ')':
                        #print('2 ', end = '')
                        numOfOpenParens -= 1                       

                    if inIntegral and letter == 'd':                #don't close if /
                        #print('3 ', end = '')
                        closeIntegral = 1
                    maxr = chars[i][-2]
                    minr = chars[i][-4]
                    maxc = chars[i][-3]
                    minc = chars[i][-5]
                    top = pos - minr
                    bottom = pos - maxr
                    '''bottom = pos + lowers[col][row] - uppers[col][row] - maxr  #
                    top = bottom + maxr - minr'''
                    
                    #print(letter, top, bottom, lastTop, lastBottom, minc, maxc, minr, maxr)
                    
                    if inIntegralLimits:
                        #print(chars[i][-1], top, bottom, intTop, intBottom)
                        if intTop - (intTop - intBottom)*0.25 <= bottom: 
                            #print("Yes1")
                            letter = '~' + letter
                        elif intBottom + (intTop - intBottom)*0.25 >= top:
                             #print("Yes2")
                             letter = '_' + letter
                        else:
                            inIntegralLimits = 0
                            intTop = -1
                            intBottom = -1

                    if letter == '-':
                        #print('4 ', end = '')
                        diff = maxr - minr                #maxc = minc
                        bottom -= diff
                        top += diff

                    if (isPow and '''letter != '/''') and (bottom + (maxr - minr + 1)/2 <= lastBottom or\
                    (letter == '(' and bottom + (maxr - minr + 1)/4 <= lastBottom)):
                        #print('5 ', end = '')
                        isPow = 0
                        word += ')'
                        numOfOpenParens -= 1

                    if (2*lastTop - lastBottom >= bottom) and canBePow and \
                    ((self.isLetterOrNum(letter) and (lastBottom + (lastTop-lastBottom)*0.4) <= bottom)\
                     or (not self.isLetterOrNum(letter) and letter !="''" and letter !="." and lastBottom + (lastTop - lastBottom) <= bottom) \
                     or (letter == '' and (lastBottom + (lastTop-lastBottom)*0.4 <= bottom))):      #Redesign
                        #print('6 ')
                        isPow = 1
                        word += '^'
                        word += '('
                        lastBottom = bottom
                        lastTop = top
                        #print(letter, lastTop, lastBottom)
                        numOfOpenParens += 1
                    elif (not self.isSign(letter) and (self.isLetterOrNum(letter) or letter == ')')):
                        #print('7 ')
                        canBePow = 1
                        lastBottom = bottom
                        lastTop = top
                        #print(letter, lastTop, lastBottom)
                    else:
                       # print('8 ', end = '')
                        canBePow = 0

                    if checkIntegralRange:
                        #print('9 ', end = '')
                        checkIntegralRange = 0
                        word += '('
                        sumOrProductOrIntegralParenNum = numOfOpenParens
                        numOfOpenParens += 1
                        needRightParen = 1

                    if sumOrProductOrIntegralBody:
                        #print('10 ', end = '')
                        sumOrProductOrIntegralBody = 0
                        #word += '('
                        sumOrProductOrIntegralParenNum = numOfOpenParens
                        numOfOpenParens += 1
                        needRightParen = 1

                    if (closeIntegral and not self.isLetterOrNum(letter) and not isPow) or needRightParen \
                        and (letter == '+' or letter == '-' and numOfRows == 1 and numOfClumps[(col,row)] == 1 \
                        and sumOrProductOrIntegralParenNum == numOfOpenParens - 1 and not isPow):
                        #print('11 ', end = '')
                        closeIntegral = 0
                        #word += ')'
                        word += ':'          #add \n to file
                        addNewLine = True
                        numOfOpenParens -= 1
                        needRightParen = 0

                    if (startOfSumOrProductOrIntegral and row == len(uppers[col]) - 1 and i == charIndex + numOfClumps[(col, row)]):
                        #print('12 ', end = '')
                        startOfSumOrProductOrIntegral = 0
                        sumOrProductOrIntegralBody = 1

                    if isPow:
                        #print('13 ', end = '')
                        canBePow = 0

                    word = word + letter

                    if letter == '√(':               ###############
                        #print('14 ', end = '')
                        inSqrt = len(cv2.findContours(img[minr:maxr+1, minc:maxc+1],
                        cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)[1])
                        #print(inSqrt)

                    if (letter == '∑' or letter == '∏' or letter == '∫') \
                    and row != len(uppers[col]) - 1:
                        #print('15 ', end = '')
                        startOfSumOrProductOrIntegral = 1
                        
                    if letter == '∫':
                        #print('16 ', end = '')
                        inIntegral = 1
                        inIntegralLimits = 1
                        intTop = top
                        intBottom = bottom
                        if not startOfSumOrProductOrIntegral:
                            checkIntegralRange = 1
                    
                    if inSqrt == 1:
                        #print('17 ', end = '')
                        word += ')'
                    
                    if inSqrt > 0:
                        inSqrt -= 1
                    charIndex += 1
                    
                word += ':'
                
                '''this if is used in order not to create pow in which
                the base is the last line for some column and the
                exponent is taken from the next column - see TEST_12'''
                if row == len(uppers[col]) - 1 and len(uppers[col]) != 1:
                    #print('18 ', end = '')
                    canBePow = 0
                    
            ans.append(word)
            if addNewLine:
                ans.append('')

            word = ''
        
        while numOfOpenParens > 0:
            numOfOpenParens -= 1
            ans.append('):')
                            
        return ans                            
    
#####################################################################################
            
    def isLetterOrNum(self, letter):
        s = 0
        for l in letter:
            if (letter >='0' and letter <= '9') or (letter >='A' and \
               letter <= 'Z') or(letter >='a' and letter <= 'z') or \
               (len(letter) == 1 and (0x03B1 <= int(hex(ord(letter)), 16) \
                    and int(hex(ord(letter)), 16) <= 0x3c9)) or \
               (len(letter) == 1 and (0x0391 <= int(hex(ord(letter)), 16) \
                    and int(hex(ord(letter)), 16) <= 0x3a9)):     #add greek
                s += 1
        return s == len(letter)
    
#####################################################################################

    def isSign(self, letter):
        return letter == '∑' or letter == '∫' or letter == '√' or \
        letter == '∏' or letter == 'arrow'
        
#####################################################################################

    def ocr(self, img, chars):
        #print(chars)
        #print(len(chars))
        chars = Identifier.Identifier().identifyMath(img, chars)
        for i in range(0, len(chars)):
            c = chars[i][-1] #chr(int(chars[i][-1][2:], 16))     
            if (c == '−' or c == '-' or c == '—') and \
            (i != 0 and chars[i][0][0] == chars[i-1][0][0] and chars[i][0][1] != chars[i-1][0][1]) and \
            (i != len(chars) - 1 and chars[i][0][0] == chars[i+1][0][0] and chars[i][0][1] != chars[i+1][0][1]):
                c = '/'
            if c == '√':
                c = '√('
            chars[i][-1] = c
        
        return chars        
        
#####################################################################################
'''
if __name__ == '__main__':
    img = cv2.imread('C:\\Users\\Dell\\Documents\\College\\Sem 8\\Project\\src\\1.png')
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    thresh = cv2.threshold(gray, 127, 255, cv2.THRESH_BINARY_INV|cv2.THRESH_OTSU)[-1]
    eqnRec = EqnRec()
    print(eqnRec.eqnRec(thresh, img))                   
'''    
#write for i and !
#add seperator for upper and lower limits of integrate
             














