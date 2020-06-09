# 마우스로 클릭한다음 그건 bitand연산을 통해 색을 뽑아낸뒤 그안의 색이있다면 그 자표의 색을 활성화하기 !

import cv2
import numpy as np 

# 클릭 이벤트 선언
SelectEvents = [j for j in dir(cv2) if 'EVENT' in j] 

OriginalImg = cv2.imread("AutoSolding/availablepoint.jpg")
H,W,C = OriginalImg.shape
# 클릭이 되었을때 드래그 할것 이므로 Click flag 넘기기
# OriginalImg = np.zeros((640,600,3),np.uint8)
zeroImg = np.zeros((H,W,C),np.uint8)
click = False     
x1,y1,x2,y2 = -1,-1,-1,-1

# OriginalImg = cv2.imread("AutoSolding/availablepoint.jpg")
# OriginalImg = cv2.resize(OriginalImg ,(640,600))

def CallPointMouse(event ,x,y,flags,param):
    global x1,y1,x2,y2,click,result1,mask
    result1 = OriginalImg
    if event == cv2.EVENT_LBUTTONDOWN:  # 마우스 누를때
        click = True
        cv2.circle(zeroImg,(x,y),7,(0,255,0),-1)

    elif event == cv2.EVENT_MOUSEMOVE: # 그냥 움직일때도 인식할수 있으므로 Click flag로 관리한다.                     
        if click:                                   
            cv2.circle(zeroImg,(x,y),7,(0,255,0),-1)
            # break

    elif event == cv2.EVENT_LBUTTONUP: # 마우스 땔때
        click =False
        

def Point():
    while True:
        k = cv2.waitKey(1) & 0xFF  # 입력을 기다리기
        cv2.imshow('img',OriginalImg)
        cv2.namedWindow('img')
        cv2.setMouseCallback('img',CallPointMouse)
        cv2.imshow('result',zeroImg)
        

        # elif k ==ord('f'): 
        if k == 27:               
            break
    cv2.imwrite('selectpoint.jpg' ,zeroImg)


def Cvt(holeImg,selectedholeImg):
    mask = cv2.imread("AutoSolding/selectpoint.jpg",cv2.IMREAD_GRAYSCALE)
    img = cv2.imread("AutoSolding/findhole.jpg",cv2.IMREAD_GRAYSCALE)
    
    ret, mask = cv2.threshold(mask ,10, 255, cv2.THRESH_BINARY)
    result=cv2.bitwise_and(img,mask,mask =mask)
    
    cv2.imshow('1',img)
    cv2.imshow('2',mask)
    
    cv2.imshow('re',result)
    cv2.waitKey(0)

Point()
Cvt(OriginalImg,zeroImg)


