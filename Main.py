import cv2 as cv
import numpy as np 

SelectedImg = np.zeros((640,480,3),np.uint8)
ShowImg = np.zeros((640,480,3),np.uint8)

def WaitKey():
    OriginalImg = cv.imread("AutoSolding/PCB1.jpg")
    OriginalImg = cv.resize(OriginalImg ,(640,480))

    while True:
        cv.imshow('img',OriginalImg)
        k = cv.waitKey(1) & 0xFF

        if k==ord('0'):
            cv.imshow('dd',ShowImg)
        elif k==ord('1'):
            cv.destroyWindow('dd')
            print('1')
        elif k==ord('2'):
            print('2')
        elif k==ord('3'):
            print('3')
        elif k==ord('4'):
            print('4')
        elif k== 27: # esc
            break

if __name__ == "__main__":
    WaitKey()