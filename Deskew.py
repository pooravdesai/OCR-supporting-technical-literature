import cv2
import numpy as np

img = cv2.imread("sample1.tif.jpg")

gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
ret, thresh = cv2.threshold(gray, 127, 255, cv2.THRESH_BINARY_INV)

pts = cv2.findNonZero(thresh)
rect = cv2.minAreaRect(pts)
print(rect)

(cx,cy), (w,h), ang = rect

M = cv2.getRotationMatrix2D((cx,cy), ang, 1.0)
rotated = cv2.warpAffine(thresh, M, (img.shape[1], img.shape[0]))
rot = cv2.bitwise_not(rotated)
cv2.imwrite("result.png", rot)




