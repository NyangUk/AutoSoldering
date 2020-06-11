import cv2 
import numpy as np 

capflag= True
roiflag= True
selectflag= True

MainBoard = cv2.imread("MainBoard.jpg")
DeleteBoard = cv2.imread("DeleteBoard.jpg")
# flag= Flase
OriginalCcl = {}  # 원본영상의 모든 납땝가능한 홀의 좌표
SelectedCcl = {}  # 납땜하고자하는 spot을 지정해둔 홀의 좌표

DummyImg = cv2.imread('PCB(0).jpg') # 디폴트로 이전영상의 이미지를 넣어둠 캡쳐를 통해 갱신할예정
H,W,C =DummyImg.shape
HoleImg = np.zeros((H,W,C),np.uint8)
OriginalImg = np.zeros((H,W,C),np.uint8)
oriSP = np.zeros((H,W,C),np.uint8)      # AppliedROI.jpg
RoiImg = np.zeros((H,W,C),np.uint8)     # PCB(0).jpg 또는 활성화 지역
RoiImg = np.zeros((H,W,C),np.uint8)
mask = np.zeros((H,W,C),np.uint8)


SelectPointImg = np.zeros((H,W,C),np.uint8)
click = False     

events = [i for i in dir(cv2) if 'EVENT' in i] 

# 클릭이 되었을때 드래그 할것 이므로 Click flag 넘기기
oriSP = np.zeros((H,W,C),np.uint8)      # AppliedROI.jpg
# RoiImg = np.zeros((H,W,C),np.uint8)     # PCB(0).jpg 또는 활성화 지역
RoiImg = np.zeros((H,W,C),np.uint8)
mask = np.zeros((H,W,C),np.uint8)

x1,y1,x2,y2 = -1,-1,-1,-1
# H,W,C = oriSP.shape

SelectPointImg = np.zeros((H,W,C),np.uint8)
click = False       
x1,y1,x2,y2 = -1,-1,-1,-1

def CapturePCB():  # PCB기판 이미지 캡쳐
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
            break
        if cv2.waitKey(1)&0xFF==27:
            capflag = True
            break
    cv2.destroyWindow('Capture Image')
    capture.release()

def FindHole():
    # global 
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

def SoldingPoint():
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

def CallROIMouse(event ,x,y,flags,param):
    global x1,y1,x2,y2,RoiImg#,click
    if event == cv2.EVENT_LBUTTONDOWN:  # 마우스 누를때
        x1,y1 =x,y
    elif event == cv2.EVENT_LBUTTONUP: # 마우스 땔때
        x2,y2 =x,y
        cv2.rectangle(RoiImg,(x1,y1),(x2,y2),(0,0,0),-1)
        x1,y1,x2,y2 =-1,-1,-1,-1 #마우스 이벤트가 끝날땐 초기화시켜주기


def CropRoi():
    global roiflag ,RoiImg
    RoiImg =OriginalImg.copy()
    while True:
        cv2.imshow('img',RoiImg)
        cv2.namedWindow('img')
        cv2.setMouseCallback('img',CallROIMouse)

        if cv2.waitKey(1)&0xFF == 27:
            print("roi 선택을 그만두셨습니다.")               
            break
        elif cv2.waitKey(1)&0xFF == ord('s'):
            cv2.imwrite('AppliedROI.jpg',RoiImg)
            roiflag =False
            print("roi 선택 완료")   
            break   

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
                

def DeleteImg():
    k = cv2.waitKey(1) & 0xFF

    if k==ord('1'):
        print("roi 이미지 삭제")
        print('2')
    elif k==ord('2'):
        print('3')
        print("납땜 선택된 Point 이미지 삭제.")
    elif k==ord('3'):
        print("모든 이미지 삭제. (리셋)")
        print('0')
    elif k==ord('0'):
        print("뒤로가기")
        print('0')

    


# cv.destroyWindow('dd')

def WaitKey():
    # global capflag,roiflag,selectflag
    while True:
        
        cv2.imshow('Menu',MainBoard)
        k = cv2.waitKey(1) & 0xFF

        if k==ord('1'):
            if capflag:
                cv2.destroyWindow('Menu')
                print("이미지를 캡쳐합니다.")
                CapturePCB()
        elif k==ord('2'):
            if roiflag:
                cv2.destroyWindow('Menu')
                print("Roi 설정합니다.")
                CropRoi()                
        elif k==ord('3'):
            if selectflag:
                cv2.destroyWindow('Menu')
                print("납땜 하고자하는 지역 선택")
                print('3')
                SelectPointImg()
        elif k==ord('4'):
            if capflag and roiflag and selectflag:
                cv2.destroyWindow('Menu')
                print("모든 준비 완료 납땜 가능지역을 활성화합니다")
                SoldingPoint()
        elif k== 27: # esc
            cv2.destroyWindow('Menu')
            print("프로그램을 종료합니다.")
            break

if __name__ == "__main__":
    WaitKey()