# 이미지로 부터 납땜가능지역을 활성화하기

import cv2 as cv
import numpy as np 

#contours center location dictionary
ccl = {} 
SelectedCcl = {}
img_color = cv.imread('AutoSolding/PCB1.jpg')
h,w,c =img_color.shape[:]

# np.ones((3,3),np.uint8)
zeroImg = np.zeros((w,h),np.uint8)

def FindHole(OriginalImg):
    ImgColor = OriginalImg.copy()

    ImgGray = cv.cvtColor(ImgColor, cv.COLOR_BGR2GRAY)
    ret, img_binary = cv.threshold(ImgGray, 127, 255, 0)
    _,contours, hierarchy= cv.findContours(img_binary, cv.RETR_LIST, cv.CHAIN_APPROX_SIMPLE)


    for cnt in contours:
        area = cv.contourArea(cnt)
        
        if area> 100 and area<250:
            # cv.drawContours(ImgColor, [cnt], 0, (255, 0, 255), 1)  # 컨투어 그리기
            # 컨투어의 중심좌표구하기 
            mmt = cv.moments(cnt)
            for key,value in mmt.items():
                try : 
                    cx = int(mmt['m10']/mmt['m00']) 
                    cy = int(mmt['m01']/mmt['m00'])
                except ZeroDivisionError:
                    pass
                ccl[cx] = cy
            for key,value in ccl.items():
                cv.line(zeroImg,(key,value),(key,value),(255,0,0),4) # 중심좌표그리기
                cv.line(ImgColor,(key,value),(key,value),(255,0,0),4)
                # print('%d :\t %d' %(key,value))

      
    cv.imshow("result" ,ImgColor) # 보여주기용
    cv.imshow("hole",zeroImg)
    cv.imwrite('findhole.jpg',zeroImg)
    cv.imwrite('availablepoint.jpg',ImgColor)
    cv.waitKey(0)

def SoldingArea():
    img =  cv.imread("AutoSolding/result.jpg",cv.IMREAD_GRAYSCALE)
    zero = zeroImg.copy()
    ret, img_binary = cv.threshold(img, 127, 255, 0)
    _,contours, hierarchy = cv.findContours(img_binary, cv.RETR_LIST, cv.CHAIN_APPROX_SIMPLE)
    for cnt in contours:
        mmt = cv.moments(cnt)
        for key,value in mmt.items():
            try : 
                cx = int(mmt['m10']/mmt['m00']) 
                cy = int(mmt['m01']/mmt['m00'])
            except ZeroDivisionError:
                pass
            SelectedCcl[cx] = cy
        for key,value in SelectedCcl.items():
            if ccl.get(key):
                cv.line(zero,(key,value),(key,value),(255,0,0),13) # 중심좌표그리기
                # cv.circle(zeroImg,(key,value),7,(0,255,0),-1)
    # zero = cv.cvtColor(zero, cv.COLOR_GRAY2RGB)
    cv.imshow('final',zero)
    cv.waitKey(0)

                

FindHole(img_color)
SoldingArea()

