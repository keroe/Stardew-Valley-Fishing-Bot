import numpy as np
from matplotlib import pyplot as plt
from PIL import ImageGrab
import cv2
import time
from directkeys import ReleaseKey, PressKey, C
from matplotlib import pyplot as plt

upperBound = np.array([255, 250, 32])  # upper and lower bound for the color detection (the way I came up with to find the contour of the green rectangle)
lowerBound = np.array([0, 0, 0])

#img_YCrCb = cv2.cvtColor(img_rgb_little, cv2.COLOR_BGR2YCrCb)  # chose this color scheme because ir seemed to be one of the few who worked. BGR2Lab also seemed to work.
#img_green = cv2.inRange(img_YCrCb, lowerBound_s1, upperBound_s1)
fish_template = cv2.imread('Images\\black.png')

black1 = cv2.imread('Images\\black.png')
black2 = cv2.imread('Images\\black.png')


fish_template = cv2.imread('Images\\black 2.png')
test1 = cv2.imread('Images\\fish.png')
test2 = cv2.imread('Images\\test2.png')

test1R = cv2.inRange(test1, lowerBound, upperBound)
#test2R = cv2.inRange(test2, lowerBound, upperBound)
test2R = cv2.cvtColor(test2, cv2.COLOR_BGR2GRAY)
ret, test2R = cv2.threshold(test2R, 150, 255, cv2.THRESH_BINARY)


kernel = np.ones((3,3),np.uint8)
dilation1 = cv2.dilate(test1R,kernel,iterations = 1)
dilation2 = cv2.dilate(test2R,kernel,iterations = 1)

dilation1 = cv2.bitwise_not(test1R)


threshold = 0.2

res = cv2.matchTemplate(test2R, dilation1, cv2.TM_CCOEFF_NORMED)

loc = np.where( res >= threshold) 
for pt in zip(*loc[::-1]):  # This all is basically the same as trying to find the exc_point, but it also saves the fish center point
    fish_top = pt[1]
    fish_bot = pt[1] + 10

    fish_center_height = int(np.round((fish_top + fish_bot)/2, 0))

    fish_center_point = cv2.circle(test2R, (pt[0] + 10 + 5, fish_center_height), 17, (100, 0, 255), 2) # draws circle around fish's center
    print('F')

'''
_, conts, h = cv2.findContours(test1R, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)

for cnt in conts:
    area = cv2.contourArea(cnt)
    if area > 5:
        cv2.drawContours(black1, cnt, -1, (0,0,255),1)
        pass

_, conts, h = cv2.findContours(test2R, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)

for cnt in conts:
    area = cv2.contourArea(cnt)
    if area > 5:
        cv2.drawContours(black2, cnt, -1, (0,0,255),1)
        pass
'''
#cv2.imshow("fish_template", fish_template)
#cv2.imshow("test1", test1)
#cv2.imshow("test2", test2)
#cv2.imshow("test1R", test1R)
cv2.imshow("test2R", test2R)
cv2.imshow("dilation1", dilation1)
#cv2.imshow("dilation2", dilation2)
#cv2.imshow("black1", black1)
#cv2.imshow("black2", black2)



cv2.waitKey(0)
cv2.destroyAllWindows()