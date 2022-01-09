"""
python code to detect hands , and make drag and drop virtuality using computer vision.
by : Qays Abu Mahfouz & Laith Yahya
The HandTracking Module from : https://www.computervision.zone/

"""

import cv2
from cvzone.HandTrackingModule import HandDetector
import cvzone
import numpy as np
import webbrowser


cap = cv2.VideoCapture(0) # to open camera
cap.set(3, 1280)
cap.set(4, 720) # make cam size bigger
detector = HandDetector(detectionCon=0.8) # miniumum detect factor
colorR = (25,0,10) #color of dots
#cv2.destroyAllWindows()

cx,cy,w,h=100,100,200,200 # the center for the rectangle (x,y) , and the width & height about screen


class dragrec():# Class for specify center and size for each rect

    def __init__(self,poscenter, size= [200,200]): #For (x & y)
        self.poscenter = poscenter
        self.size = size

    def update(self,cursor): #for update the cursor after each rect draw
        cx,cy=self.poscenter
        w,h=self.size

        if cx - w // 2 < cursor[0] < cx + w // 2 and cy - h // 2 < cursor[1] < cy + h // 2:
            self.poscenter = cursor

rectList = [] # List to add rects in it

for i in range (3): # to add how many rects i want
    rectList.append (dragrec([i*250+150,150])) # specify every rect distance from the next


while True:
    success, img = cap.read() # To read frames fom cam
    #img = cv2.flip(img, 1)
    img = detector.findHands(img) # to find hands
    lmList, _ = detector.findPosition(img)

    if lmList:

        l,_,_= detector.findDistance(8,12,img) # To find the dis between two points

        if l <50: # if distance less than 100 it will considred as click (drag) , and if not it will do (drop)
            cursor = lmList[12] # tip of second finger
            print(l)

            webbrowser.open("https://google.com")
            for rect in rectList:
                rect.update(cursor)


# for rect in rectList: # update values for each rectangle
    #     cx,cy=rect.poscenter
    #     w,h= rect.size
    #     cv2.rectangle(img, (cx-w//2, cy-h//2), (cx+w//2, cy+h//2), (0, 0, 255), cv2.FILLED)
    #     cvzone.cornerRect(img, (cx - w // 2 , cy -h // 2 , w, h ), 10,rt=0)

    imgnew = np.zeros_like(img,np.uint8)

    for rect in rectList: # update values for each rectangle
        cx,cy=rect.poscenter
        w,h= rect.size
        cv2.rectangle(imgnew, (cx-w//2, cy-h//2), (cx+w//2, cy+h//2), (0, 0, 255), cv2.FILLED)
        cvzone.cornerRect(imgnew, (cx - w // 2 , cy -h // 2 , w, h ), 10,rt=0)

    out= img.copy()
    alpha = 0.1
    mask = imgnew.astype(bool)
    out[mask] = cv2.addWeighted(img,alpha, imgnew , 2-alpha , 0 )[mask]

    cv2.imshow("Image",out) # show us the cam!
    cv2.waitKey(1) # wait time after one click (in ms)
