import cv2
import numpy as np 

# 클릭 이벤트 선언
events = [i for i in dir(cv2) if 'EVENT' in i] 

# 클릭이 되었을때 드래그 할것 이므로 Click flag 넘기기
OriginalImg = np.zeros((640,600,3),np.uint8)
result1 = np.zeros((640,600,3),np.uint8)
mask = np.zeros((640,600,3),np.uint8)

click = False     
x1,y1,x2,y2 = -1,-1,-1,-1



def CallMouse(event ,x,y,flags,param):
    global x1,y1,x2,y2,click,result1,mask
    result1 = OriginalImg
    if event == cv2.EVENT_LBUTTONDOWN:  # 마우스 누를때
        click = True
        x1,y1 =x,y

    elif event == cv2.EVENT_LBUTTONUP: # 마우스 땔때
        click ==False
        x2,y2 =x,y
        cv2.rectangle(result1,(x1,y1),(x2,y2),(255,255,255),-1)
        

def CropRoi():
    while True:
        # cv2.imshow('img',mask)   
        # cv2.imshow('result1',result1) 

        k = cv2.waitKey(1) & 0xFF  # 입력을 기다리기
        cv2.imshow('img',OriginalImg)
        cv2.namedWindow('img')
        cv2.setMouseCallback('img',CallMouse)

        # elif k ==ord('f'): 
        if k == 27:               
            break

OriginalImg = cv2.imread("AutoSolding/PCB1.jpg")
OriginalImg = cv2.resize(OriginalImg ,(640,600))
CropRoi()

