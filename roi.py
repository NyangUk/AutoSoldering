import cv2
import numpy as np 

# 클릭 이벤트 선언
ROIevents = [i for i in dir(cv2) if 'EVENT' in i] 

# 클릭이 되었을때 드래그 할것 이므로 Click flag 넘기기
OriginalImg = cv2.imread('PCB(0).jpg') 
H,W,C =OriginalImg.shape[:]
RoiImg = np.zeros((H,W,C),np.uint8)
mask = np.zeros((H,W,C),np.uint8)

# click = False     
x1,y1,x2,y2 = -1,-1,-1,-1



def CallMouse(event ,x,y,flags,param):
    global x1,y1,x2,y2,RoiImg,mask#,click
    RoiImg = OriginalImg
    if event == cv2.EVENT_LBUTTONDOWN:  # 마우스 누를때
        # click = True
        x1,y1 =x,y

    elif event == cv2.EVENT_LBUTTONUP: # 마우스 땔때
        # click =False
        x2,y2 =x,y
        cv2.rectangle(RoiImg,(x1,y1),(x2,y2),(0,0,0),-1)
    
def CropRoi():
    global RoiImg
    while True:
        cv2.imshow('img',OriginalImg)
        cv2.namedWindow('img')
        cv2.setMouseCallback('img',CallMouse)

        if cv2.waitKey(1)&0xFF == 27:
            print("roi 선택을 그만두셨습니다.")               
            break
        elif cv2.waitKey(1)&0xFF == ord('s'):
            cv2.imwrite('AppliedROI.jpg',RoiImg)
            print("roi 선택 완료")   
            break
        elif cv2.waitKey(1)&0xFF == ord('r'):
            RoiImg = OriginalImg
            cv2.imshow('img',OriginalImg)
            print("roi 선택을 다시합니다.")       

CropRoi()

