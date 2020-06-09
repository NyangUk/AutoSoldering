import cv2 as cv


# 웹캠으로 사진찍기

Pcbimg = cv.VideoCapture(0)

while(True):
    ret,PcbColor = Pcbimg.read()

    if ret==False:
        continue


    PcbGray = cv.cvtColor(PcbColor,cv.IMREAD_COLOR)

    cv.imshow("gray", PcbGray)

    if cv.waitKey(1)&0xFF==32:
        cv.imwrite('PCB.jpg', PcbGray)
        break

    if cv.waitKey(1)&0xFF==27:
        break




Pcbimg.release()
cv.destroyAllWindows()