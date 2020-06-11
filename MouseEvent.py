import cv2
import numpy as np 

# 클릭 이벤트 선언
ROIevents = [i for i in dir(cv2) if 'EVENT' in i] 
# SelectEvents = [j for j in dir(cv2) if 'EVENT' in j] 

# 클릭이 되었을때 드래그 할것 이므로 Click flag 넘기기
OriginalImg = cv2.imread('PCB(0).jpg') 
H,W,C =OriginalImg.shape[:]
RoiImg = np.zeros((H,W,C),np.uint8)
mask = np.zeros((H,W,C),np.uint8)

# H,W,C = oriSP.shape

SelectPointImg = np.zeros((H,W,C),np.uint8)
click = False     
# click = False     
x1,y1,x2,y2 = -1,-1,-1,-1



def CallROIMouse(event ,x,y,flags,param):
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
        cv2.setMouseCallback('img',CallROIMouse)

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

def CallPointMouse(event ,x,y,flags,param):
    global x1,y1,x2,y2,click,SelectPointImg
    # SelectPointImg = oriSP
    if event == cv2.EVENT_LBUTTONDOWN:  # 마우스 누를때
        click = True
        cv2.circle(SelectPointImg,(x,y),7,(0,255,0),-1)

    elif event == cv2.EVENT_MOUSEMOVE: # 그냥 움직일때도 인식할수 있으므로 Click flag로 관리한다.                     
        if click:                                   
            cv2.circle(SelectPointImg,(x,y),7,(0,255,0),-1)
            # break

    elif event == cv2.EVENT_LBUTTONUP: # 마우스 땔때
        click =False
        

def Point():
    while True:
        cv2.imshow('simg',oriSP)
        cv2.namedWindow('simg')
        cv2.setMouseCallback('simg',CallPointMouse)
        cv2.imshow('result',SelectPointImg)
        

        # elif k ==ord('f'): 
        if cv2.waitKey(1) & 0xFF == ord('s'):               
            print("납땜 활성화 포인트 저장완료")
            break
    cv2.imwrite('SelectPoint.jpg',SelectPointImg)


def Cvt(holeImg,selectedholeImg):
    mask = cv2.imread("SelectPoint.jpg",cv2.IMREAD_GRAYSCALE)
    img = cv2.imread("Hole(Checking).jpg",cv2.IMREAD_GRAYSCALE)

    ret, mask = cv2.threshold(mask ,10, 255, cv2.THRESH_BINARY)
    result=cv2.bitwise_and(img,mask,mask =mask)
    cv2.imwrite('result.jpg',result)
    cv2.imshow('re',result)
    cv2.waitKey(0)
        

CropRoi()
oriSP = cv2.imread("AppliedROI.jpg")
Point()
Cvt(oriSP,SelectPointImg)


