import cv2
import numpy as np
 
img = cv2.imread('00_000.png')
gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
gray = cv2.fastNlMeansDenoising(gray,10,7,21)  #factor, template size, search size

ret, thresh = cv2.threshold(gray, 127, 255, cv2.THRESH_BINARY_INV)
cv2.imwrite('bin1.png', thresh)
height = thresh.shape[0]
width = thresh.shape[1]

line_present = True
line_top = []
line_bottom = []
x = 0
y = 0

def findNextLine(image, y, x):
    if y >= height:
        return -1
    while image[y][x] == 0:                 #not a character pixel
        x += 1
        if x == width:
            x = 0
            y += 1
        if y >= height:
            break
    if y < height:
        return y
    else: 
        return -1
        
def findLineBottom(image, top):
    x0 = 0
    no_white_pixel = False
    while no_white_pixel == False:
        top += 1
        no_white_pixel = True
        x0 = 0
        while x0 < width and top < height and no_white_pixel:
            if image[top][x0] != 0:           #character pixel
                no_white_pixel = False
            x0 += 1
    return top

while line_present:   
    x = 0
    y = findNextLine(thresh, y, x)
    if y == -1:
        break
    if y > height:
        line_present = False
    if line_present:
        line_top.append(y)
        y = findLineBottom(thresh, y)
        line_bottom.append(y)
        
for i in range(0, len(line_top)):
    cv2.rectangle(img, (0, line_top[i]), (width, line_bottom[i]),
                  (0, 255, 0), 1)
    
cv2.imwrite('lines.png', img)


    