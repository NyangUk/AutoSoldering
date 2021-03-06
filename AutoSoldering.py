import cv2 
import numpy as np 

capflag= True
roiflag= True
selectflag= True
findflag = False
checkflag = False

MainBoard = cv2.imread("MainBoard.jpg")

OriginalCcl = {}  # 원본영상의 모든 납땝가능한 홀의 좌표 
SelectedCcl = {}  # 납땜하고자하는 spot을 지정해둔 홀의 좌표

# DummyImg = cv2.imread('PCB(0).jpg') # 디폴트

H,W,C = 480,640,3
OriginalImg = np.zeros((H,W,C),np.uint8) 
RoiImg = np.zeros((H,W,C),np.uint8)
OnlyHoleImg = np.zeros((H,W,C),np.uint8)
FindedHoleImg = np.zeros((H,W,C),np.uint8)
ActiveHoleImg = np.zeros((H,W,C),np.uint8)
SelectPointImg = np.zeros((H,W,C),np.uint8)

     
events = [i for i in dir(cv2) if 'EVENT' in i] 
click = False       
x1,y1,x2,y2 = -1,-1,-1,-1
# 클릭이 되었을때 드래그 할것 이므로 Click flag 넘기기

# PCB기판 이미지 캡쳐
def CapturePCB():  
    global capflag,OriginalImg
    capture = cv2.VideoCapture(2)
    while (True):
        ret,PcbImg = capture.read()
        if ret == False:
            continue
        cv2.imshow("Capture Image", PcbImg)
        if cv2.waitKey(1)&0xFF==32:
            capflag = False
            cv2.imwrite('PCB(0).jpg', PcbImg)
            OriginalImg = PcbImg.copy() #이곳에서 갱신이 일어남
            print("캡쳐 완료.")
            break
        elif cv2.waitKey(1)&0xFF==27:
            print("캡쳐 취소.")
            break
    cv2.destroyWindow('Capture Image')
    capture.release()
# 불필요한 부분 제거 
def CallROIMouse(event ,x,y,flags,param):
    global x1,y1,x2,y2,RoiImg#,click
    if event == cv2.EVENT_LBUTTONDOWN:  # 마우스 누를때
        x1,y1 =x,y
    elif event == cv2.EVENT_LBUTTONUP: # 마우스 땔때
        x2,y2 =x,y
        cv2.rectangle(RoiImg,(x1,y1),(x2,y2),(0,0,0),-1)
        x1,y1,x2,y2 =-1,-1,-1,-1 #마우스 이벤트가 끝날땐 초기화시켜주기

def CropRoi():
    global roiflag,findflag ,RoiImg
    RoiImg =OriginalImg.copy()
    while True:
        cv2.imshow('Remove ROI',RoiImg)
        cv2.namedWindow('Remove ROI')
        cv2.setMouseCallback('Remove ROI',CallROIMouse)

        if cv2.waitKey(1)&0xFF == 32:
            cv2.imwrite('RemoveROI.jpg',RoiImg)
            roiflag =False
            findflag =True # roi이미지가 있어야만 납땜가능 구역을 찾을수있음
            print("roi 선택 완료했습니다.")  
            break
        elif cv2.waitKey(1)&0xFF == 27:
            print("roi 선택을 그만두셨습니다.")               
            break
    cv2.destroyWindow('Remove ROI')
# 납땜이 가능한 부분 추출
def FindHole(): 
    global RoiImg,findflag,FindedHoleImg,OnlyHoleImg

    def nothing(x):
        pass
    cv2.namedWindow('Find Soldering Point')

    cv2.createTrackbar('low', 'Find Soldering Point', 0, 255, nothing)
    cv2.createTrackbar('high', 'Find Soldering Point', 0, 255, nothing)

    cv2.setTrackbarPos('low', 'Find Soldering Point', 100)  #트랙바의 초기 value 설정
    cv2.setTrackbarPos('high', 'Find Soldering Point', 230)

    

    while(True):
        low = cv2.getTrackbarPos('low', 'Find Soldering Point')
        high = cv2.getTrackbarPos('high', 'Find Soldering Point')
        FindedHoleImg = RoiImg.copy()
        GrayImg = cv2.cvtColor(FindedHoleImg, cv2.COLOR_BGR2GRAY)
        OnlyHoleImg = np.zeros((H,W,C),np.uint8)
        ret, BinaryImg = cv2.threshold(GrayImg, low, high, 0)
        _,contours, hierarchy= cv2.findContours(BinaryImg, cv2.RETR_LIST, cv2.CHAIN_APPROX_SIMPLE)

        for cnt in contours:
            area = cv2.contourArea(cnt)
            if area> 65 and area<250:
                # 컨투어의 중심좌표구하기 
                mmt = cv2.moments(cnt)
                for key,value in mmt.items():
                    try : 
                        cx = int(mmt['m10']/mmt['m00']) 
                        cy = int(mmt['m01']/mmt['m00'])
                    except ZeroDivisionError:
                        pass
                    OriginalCcl[cx] = cy #  OriginalCcl딕션어리에 등록하기 
                for key,value in OriginalCcl.items():
                    cv2.line(OnlyHoleImg,(key,value),(key,value),(255,255,255),4)    # 원본이미지 위에  Hole그리기
                    cv2.line(FindedHoleImg,(key,value),(key,value),(0,0,255),4)      # Hole 만 그리기

        cv2.imshow("Find Soldering Point" ,FindedHoleImg)  
        cv2.imshow("OnlyHole",OnlyHoleImg)                
        if cv2.waitKey(1)&0xFF==32:
            print("납땜가능 Point을 찾았습니다.")
            findflag = True
            break
        elif cv2.waitKey(1)&0xFF== 27:
            print("납땜가능 Point 찾지 않았습니다.")
            break
    cv2.destroyWindow('Find Soldering Point')
    cv2.destroyWindow('OnlyHole')        
    cv2.imwrite('Hole(Checking).jpg',OnlyHoleImg)
    cv2.imwrite('Hole(Showing).jpg',FindedHoleImg)
    # cv2.waitKey(0)
# 납땜하고자 하는 부분 선택
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

def SelectPoint():
    global selectflag,checkflag,FindedHoleImg
    while True:
        cv2.imshow('Select Soldering Point',FindedHoleImg)
        cv2.namedWindow('Select Soldering Point')
        cv2.setMouseCallback('Select Soldering Point',CallPointMouse)
        cv2.imshow('Drawing...',SelectPointImg)

        if cv2.waitKey(1) & 0xFF == 32:               
            print("납땜 활성화 포인트 저장완료")
            cv2.destroyWindow("Select Soldering Point")
            cv2.destroyWindow("Drawing...")
            selectflag =False
            checkflag =True
            break
        elif cv2.waitKey(1) & 0xFF == 27:               
            cv2.destroyWindow("Select Soldering Point")
            cv2.destroyWindow("Drawing...")
            break
    CheckHole()
    # cv2.imwrite('SelectPoint.jpg',SelectPointImg)
# 선택된 부분이 납땜이 가능한 부분인지 확인
def CheckHole():
    global SelectPointImg,OnlyHoleImg,ActiveHoleImg
    mask = SelectPointImg.copy()
    img = OnlyHoleImg.copy()
    mask = cv2.cvtColor(mask, cv2.COLOR_BGR2GRAY)
    img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    ret, mask = cv2.threshold(mask ,10, 255, cv2.THRESH_BINARY)
    ActiveHoleImg =cv2.bitwise_and(img,mask,mask =mask)
    cv2.imwrite('CheckHole.jpg',ActiveHoleImg)

# 선택된 부분 활성분
def SoldingPoint():
    global ActiveHoleImg
    img =ActiveHoleImg.copy()
    ret, BinaryImg = cv2.threshold(img, 127, 255, 0)
    _,contours, hierarchy = cv2.findContours(BinaryImg, cv2.RETR_LIST, cv2.CHAIN_APPROX_SIMPLE)
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
                cv2.line(img,(key,value),(key,value),(255,0,0),13) # 중심좌표그리기
    cv2.imwrite('RESULT.jpg',img)
    while(True):
        cv2.imshow('RESULT',img)
        if cv2.waitKey(1) & 0xFF == 32:
            print("납땜을 실행합니다")
            cv2.destroyWindow("RESULT")
            break

        

 
if __name__ == "__main__":
    while True:
        
        cv2.imshow('Menu',MainBoard)
        k = cv2.waitKey(1) & 0xFF

        if k==ord('1'):
            if capflag:
                cv2.destroyWindow('Menu')
                print("이미지를 캡쳐합니다...")
                CapturePCB()
        elif k==ord('2'):
            if not capflag and roiflag:
                cv2.destroyWindow('Menu')
                print("Roi 설정합니다...")
                CropRoi()
        elif k==ord('3'):
            if findflag:
                cv2.destroyWindow('Menu')
                print("납땜 가능한 포인트를 찾습니다...")
                FindHole()                
        elif k==ord('4'):
            if not capflag and not roiflag and selectflag:
                cv2.destroyWindow('Menu')
                print("납땜 하고자 하는 포인트를 선택합니다...")
                SelectPoint()
        elif k==ord('5'):
            if not capflag and not roiflag and not selectflag and checkflag:
                cv2.destroyWindow('Menu')
                print("모든 준비 완료! 납땜 가능포인트을 활성화합니다...")
                SoldingPoint()
        elif k==ord('R'):
            cv2.destroyWindow('Menu')
            print("RESET 합니다...")
            capflag= True
            roiflag= True
            selectflag= True
            findflag = False
            checkflag = False
            SelectedCcl.clear()
            OriginalCcl.clear()
        elif k== ord('E'): # exit
            cv2.destroyWindow('Menu')
            print("프로그램을 종료합니다...")
            break