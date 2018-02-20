import cv2
import numpy as np
 
img = cv2.imread('00_000.png')
gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
gray = cv2.fastNlMeansDenoising(gray,10,7,21)  #factor, template size, search size

ret, thresh = cv2.threshold(gray, 127, 255, cv2.THRESH_BINARY_INV)
cv2.imwrite('bin.png', thresh)

img2, contours, hierarchy = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

for c in contours:
    rect = cv2.boundingRect(c)
    cv2.rectangle(img, (rect[0], rect[1]), (rect[0]+rect[2], rect[1]+rect[3]),
                  (0, 255, 0), 1)

cv2.imwrite('bboxes.png', img)