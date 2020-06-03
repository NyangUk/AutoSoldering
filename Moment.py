import cv2 as cv
import numpy as np

#contours center location dictionary
ccl = {}


img_color = cv.imread('AutoSolding/PCB1.jpg')
img_gray = cv.cvtColor(img_color, cv.COLOR_BGR2GRAY)
ret, img_binary = cv.threshold(img_gray, 127, 255, 0)
contours, hierarchy = cv.findContours(img_binary, cv.RETR_LIST, cv.CHAIN_APPROX_SIMPLE)


for cnt in contours:
    area = cv.contourArea(cnt)
    print(area)
    if area> 50 and area<250:
        cv.drawContours(img_color, [cnt], 0, (255, 0, 0), 1)  # blue

for cnt in contours:
    mmt = cv.moments(cnt)
    
    for key,value in mmt.items():
        cx = int(mmt['m10']/mmt['m00']) 
        cy = int(mmt['m01']/mmt['m00'])
        ccl[cx] = cy
    for key,value in ccl.items():
        print('%d :\t %d' %(key,value))
    


cv.imshow("result", img_color)

cv.waitKey(0)