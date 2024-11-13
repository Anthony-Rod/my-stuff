import cv2 as cv
import numpy as np
from matplotlib import pyplot as plt
import os
import time

img = cv.imread("opencv_image/images/eminem.jpg")
img2 = img
W_SIZE = 4
H_SIZE = 4

height, width, channels = img.shape

for ih in range(H_SIZE ):
   for iw in range(W_SIZE ):
   
      x = width/W_SIZE * iw 
      y = height/H_SIZE * ih
      h = (height / H_SIZE)
      w = (width / W_SIZE )
      print(x,y,h,w)
      img = img[int(y):int(y+h), int(x):int(x+w)]
      NAME = str(time.time()) 
      cv.imwrite("opencv_image/" + str(ih)+str(iw) +  ".jpg", img)
      img = img2
      cv.imshow("img", img2)
#gray = cv.cvtColor(img, cv.COLOR_BGR2GRAY)

#ret, thresh = cv.threshold(gray, 127, 255, 0)

#contours, hierarchy = cv.findContours(thresh, cv.RETR_TREE, cv.CHAIN_APPROX_SIMPLE)

cv.waitKey(0)

cv.destroyAllWindows()
