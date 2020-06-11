# 이미지로 부터 납땜가능지역을 활성화하기

import cv2 
import numpy as np 

#contours center location dictionary
ccl = {} 
SelectedCcl = {}
img_color = cv2.imread('PCB.jpg')
h,w,c =img_color.shape[:]

# np.ones((3,3),np.uint8)
zeroImg = np.zeros((w,h),np.uint8)


def capturePCB():
    def nothing(x):
        pass


    cv2.namedWindow('Canny')

    cv2.createTrackbar('low threshold', 'Canny', 0, 1000, nothing)
    cv2.createTrackbar('high threshold', 'Canny', 0, 1000, nothing)

    cv2.setTrackbarPos('low threshold', 'Canny', 50)
    cv2.setTrackbarPos('high threshold', 'Canny', 150)

    # img_gray = cv2.imread('1.jpg', cv2.IMREAD_GRAYSCALE)

    Pcbimg = cv2.VideoCapture(2)

    while (1):
        ret,PcbColor = Pcbimg.read()

        if ret==False:
            continue
        img_gray = cv2.cvtColor(PcbColor,cv2.IMREAD_COLOR)
        img_gray = cv2.GaussianBlur(img_gray,(3,3),0)
        cv2.imshow("gray", img_gray)
        img_colors =img_gray
        FindHole(img_colors)
        if cv2.waitKey(1)&0xFF==32:
            cv2.imwrite('PCB.jpg', img_gray)
            # img_color =img_gray
            break
        if cv2.waitKey(1)&0xFF==27:
            break
        

        low = cv2.getTrackbarPos('low threshold', 'Canny')
        high = cv2.getTrackbarPos('high threshold', 'Canny')



    Pcbimg.release()

def FindHole(OriginalImg):
    ImgColor = OriginalImg.copy()
    zeroImg = np.zeros((w,h),np.uint8)

    ImgGray = cv2.cvtColor(ImgColor, cv2.COLOR_BGR2GRAY)
    # ImgGray = cv2.GaussianBlur(ImgGray,(3,3),0)
    ret, img_binary = cv2.threshold(ImgGray, 100, 230, 0)
    _,contours, hierarchy= cv2.findContours(img_binary, cv2.RETR_LIST, cv2.CHAIN_APPROX_SIMPLE)


    for cnt in contours:
        area = cv2.contourArea(cnt)
        
        if area> 60 and area<250:
            cv2.drawContours(ImgColor, [cnt], 0, (255, 0, 255), 1)  # 컨투어 그리기
            # 컨투어의 중심좌표구하기 
            mmt = cv2.moments(cnt)
            for key,value in mmt.items():
                try : 
                    cx = int(mmt['m10']/mmt['m00']) 
                    cy = int(mmt['m01']/mmt['m00'])
                except ZeroDivisionError:
                    pass
                ccl[cx] = cy
            for key,value in ccl.items():
                cv2.line(zeroImg,(key,value),(key,value),(255,0,0),4) # 중심좌표그리기
                cv2.line(ImgColor,(key,value),(key,value),(255,0,0),4)
                # print('%d :\t %d' %(key,value))

      
    cv2.imshow("result" ,ImgColor) # 보여주기용
    cv2.imshow("hole",zeroImg)
    cv2.imwrite('findhole.jpg',zeroImg)
    cv2.imwrite('availablepoint.jpg',ImgColor)
    cv2.waitKey(0)

def SoldingArea():
    img =  cv2.imread("AutoSolding/result.jpg",cv2.IMREAD_GRAYSCALE)
    zero = zeroImg.copy()
    ret, img_binary = cv2.threshold(img, 127, 255, 0)
    _,contours, hierarchy = cv2.findContours(img_binary, cv2.RETR_LIST, cv2.CHAIN_APPROX_SIMPLE)
    for cnt in contours:
        mmt = cv2.moments(cnt)
        for key,value in mmt.items():
            try : 
                cx = int(mmt['m10']/mmt['m00']) 
                cy = int(mmt['m01']/mmt['m00'])
            except ZeroDivisionError:
                pass
            SelectedCcl[cx] = cy
        for key,value in SelectedCcl.items():
            if ccl.get(key):
                cv2.line(zero,(key,value),(key,value),(255,0,0),13) # 중심좌표그리기
                # cv2.circle(zeroImg,(key,value),7,(0,255,0),-1)
    # zero = cv2.cvtColor(zero, cv2.COLOR_GRAY2RGB)
    cv2.imshow('final',zero)
    cv2.waitKey(0)

                
while(True):
    capturePCB()
    # FindHole(img_color)
    # SoldingArea()

