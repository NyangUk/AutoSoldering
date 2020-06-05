import cv2
import numpy as np 

# 클릭 이벤트 선언
events = [i for i in dir(cv2) if 'EVENT' in i] 

# 클릭이 되었을때 드래그 할것 이므로 Click flag 넘기기
RemoveImg =False
SelectedImg = np.zeros((640,480,3),np.uint8)
ShowImg = np.zeros((640,480,3),np.uint8)
StartProcess =True
click = False     
x1,y1,x2,y2 = -1,-1,-1,-1

def SelectRoi(event ,x,y,flags,param):
    global x1,y1,x2,y2,click,SelectedImg,ShowImg

    if event == cv2.EVENT_LBUTTONDOWN:  # 마우스 누를때
        click = True
        x1,y1 =x,y
        
    # elif event == cv2.cv2.EVENT_MOUSEMOVE: # 마우스 드래그시
    #     # if click ==True:
            
    elif event == cv2.EVENT_LBUTTONUP: # 마우스 땔때
        click ==False
        x2,y2 =x,y
        cv2.rectangle(ShowImg,(x1,y1),(x2,y2),(255,255,255),-1)

        k = cv2.waitKey(1) & 0xFF
        if k== ord('t'):
            SelectedImg =ShowImg
        elif k==ord('f'):
            ShowImg =OriginalImg
            pass




OriginalImg = cv2.imread("AutoSolding/PCB1.jpg")
OriginalImg = cv2.resize(OriginalImg ,(640,480))


while True:

    if StartProcess ==True:
        ShowImg = OriginalImg
        SelectedImg =OriginalImg
        StartProcess =False

    cv2.imshow('img',ShowImg)   
    cv2.imshow('selectedImg',SelectedImg) 
    
    k = cv2.waitKey(1) & 0xFF  # 입력을 기다리기

    if k ==ord('r'): # 이미지가 마음에 안들때 처음으로 돌아가기 
        SelectedImg = OriginalImg
    elif k == ord('s'): # 이미지에서 없앨부분 선택
        cv2.namedWindow('img')
        cv2.setMouseCallback('img',SelectRoi)

    # elif k ==ord('f'): 
    elif k == 27:               
        break

cv2.destroyAllWindows()
