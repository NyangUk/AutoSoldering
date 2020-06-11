# 이미지로 부터 납땜가능지역을 활성화하기

import cv2 
import numpy as np 

OriginalCcl = {}  # 원본영상의 모든 납땝가능한 홀의 좌표
SelectedCcl = {}  # 납땜하고자하는 spot을 지정해둔 홀의 좌표

DummyImg = cv2.imread('PCB(0).jpg') # 디폴트로 이전영상의 이미지를 넣어둠 캡쳐를 통해 갱신할예정
H,W,C =DummyImg.shape[:]
HoleImg = np.zeros((H,W,C),np.uint8)
OriginalImg = np.zeros((H,W,C),np.uint8)

def CapturePCB():  # PCB기판 이미지 캡쳐
    capture = cv2.VideoCapture(2)
    # print("Press the space bar")

    while (True):
        ret,PcbImg = capture.read()
        if ret == False:
            continue
        cv2.imshow("Press the space bar", PcbImg)
        if cv2.waitKey(1)&0xFF==32:
            cv2.imwrite('PCB(0).jpg', PcbImg)
            OriginalImg = PcbImg #이곳에서 갱신이 일어남
            break
        if cv2.waitKey(1)&0xFF==27:
            break
    capture.release()

def FindHole():

    def nothing(x):
        pass
    cv2.namedWindow('FindHole')

    cv2.createTrackbar('low threshold', 'FindHole', 0, 1000, nothing)
    cv2.createTrackbar('high threshold', 'FindHole', 0, 1000, nothing)

    cv2.setTrackbarPos('low threshold', 'FindHole', 100)
    cv2.setTrackbarPos('high threshold', 'FindHole', 230)

    CapturedImg = cv2.imread('PCB(0).jpg') 
    HoleImg = np.zeros((H,W,C),np.uint8)

    ImgGray = cv2.cvtColor(CapturedImg, cv2.COLOR_BGR2GRAY)

    while(True):
        low = cv2.getTrackbarPos('low threshold', 'FindHole')
        high = cv2.getTrackbarPos('high threshold', 'FindHole')

        ret, img_binary = cv2.threshold(ImgGray, low, high, 0)
        _,contours, hierarchy= cv2.findContours(img_binary, cv2.RETR_LIST, cv2.CHAIN_APPROX_SIMPLE)

        for cnt in contours:
            area = cv2.contourArea(cnt)

            if area> 60 and area<250:
                # cv2.drawContours(CapturedImg, [cnt], 0, (255, 0, 255), 1)  # 컨투어 그리기
                # 컨투어의 중심좌표구하기 
                mmt = cv2.moments(cnt)
                for key,value in mmt.items():
                    try : 
                        cx = int(mmt['m10']/mmt['m00']) 
                        cy = int(mmt['m01']/mmt['m00'])
                    except ZeroDivisionError:
                        pass
                    OriginalCcl[cx] = cy
                for key,value in OriginalCcl.items():
                    cv2.line(HoleImg,(key,value),(key,value),(255,255,255),4) # 중심좌표그리기
                    cv2.line(CapturedImg,(key,value),(key,value),(0,0,255),4)
        cv2.imshow("FindHole" ,CapturedImg)  # 원본이미지 위에  Hole
        cv2.imshow("hole",HoleImg)          # Hole 만 활성화 
        if cv2.waitKey(1)&0xFF==32:
            break

    cv2.imwrite('Hole(Checking).jpg',HoleImg)
    cv2.imwrite('Hole(Showing).jpg',CapturedImg)
    cv2.waitKey(0)

def SoldingArea():
    img =  cv2.imread("AutoSolding/result.jpg",cv2.IMREAD_GRAYSCALE)
    zero = HoleImg.copy()
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
            if OriginalCcl.get(key):
                cv2.line(zero,(key,value),(key,value),(255,0,0),13) # 중심좌표그리기
                # cv2.circle(HoleImg,(key,value),7,(0,255,0),-1)
    cv2.imshow('final',zero)
    cv2.waitKey(0)

                

CapturePCB()
FindHole()
    # SoldingArea()

