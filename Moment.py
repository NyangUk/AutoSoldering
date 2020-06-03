import cv2 as cv
import numpy as np

#contours center location dictionary
ccl = {}


img_color = cv.imread('AutoSolding/PCB1.jpg')

TestImg = img_color.copy()
img_gray = cv.cvtColor(img_color, cv.COLOR_BGR2GRAY)
ret, img_binary = cv.threshold(img_gray, 127, 255, 0)
contours, hierarchy = cv.findContours(img_binary, cv.RETR_LIST, cv.CHAIN_APPROX_SIMPLE)


for cnt in contours:
    area = cv.contourArea(cnt)
    print(area)
    if area> 50 and area<250:
        cv.drawContours(img_color, [cnt], 0, (255, 0, 0), 1)  # blue

        mmt = cv.moments(cnt)
        for key,value in mmt.items():
            try : 
                cx = int(mmt['m10']/mmt['m00']) 
                cy = int(mmt['m01']/mmt['m00'])
            except ZeroDivisionError:
                pass
            ccl[cx] = cy

        for key,value in ccl.items():
            cv.line(TestImg,(key,value),(key,value),(0,0,255),5)

            print('%d :\t %d' %(key,value))

cv.imshow("result", img_color)
cv.imshow("TestCenterLocation" ,TestImg)
cv.waitKey(0)