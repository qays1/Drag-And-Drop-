import cv2
from cvzone.HandTrackingModule import HandDetector
import cvzone
import os
#import webbrowser
#import pyttsx3
#webbrowser.open("https://youtube.com")
#engine = pyttsx3.init()
#voices = engine.getProperty('voices')

# changing index changes voices but only
# 0 and 1 are working here
#engine.setProperty('voice', voices[1].id)
#engine.runAndWait()

cap = cv2.VideoCapture(0)
cap.set(4, 1920)
cap.set(3, 1280)

detector = HandDetector(detectionCon=0.65)

class DragImg():
    def __init__(self, path, posOrigin, imgType):

        self.posOrigin = posOrigin
        self.imgType = imgType
        self.path = path

        if self.imgType == 'png':
            self.img = cv2.imread(self.path, cv2.IMREAD_UNCHANGED)

        else:
            self.img = cv2.imread(self.path)

            self.img = cv2.resize(self.img, (200,200),None,0.4,0.4)

        self.size = self.img.shape[:2]

    def update(self, cursor):
        ox, oy = self.posOrigin
        h, w = self.size

        cvzone.cornerRect(img, (ox - w // 64, oy - h // 64, w, h), 5, rt=5)

      # Check if in region
        if ox < cursor[0] < ox + w and oy < cursor[1] < oy + h:
            self.posOrigin = cursor[0] - w // 2 +50, cursor[1] - h // 2+50
 #            for i in range (0,1):
 #                #os.startfile ("C:/Users/GTS/Desktop/New Text Document.txt")
 #                pyttsx3.speak("Opening T. T. U. Website  ")
 #                webbrowser.open("https://onedrive.live.com/edit.aspx?cid=dc1f4b44908e26e4&page=view&resid=DC1F4B44908E26E4!524&parId=DC1F4B44908E26E4!232&app=PowerPoint")
 #                webbrowser.open("http://www.ttu.edu.jo/")
 #                break


path = "C:/Users/GTS/PycharmProjects/DragNdROP/Images"
myList = os.listdir(path)
print(myList)

listImg = []
for x, pathImg in enumerate(myList):
    if 'png' in pathImg:
        imgType = 'png'
    else:
        imgType = 'jpg'
    listImg.append(DragImg(f'{path}/{pathImg}', [50 + x * 300, 50], imgType))

while True:
    success, img = cap.read()
    img = cv2.flip(img, 1)
    hands, img = detector.findHands(img, flipType=False)

    if hands:
        lmList = hands[0]['lmList']
        print(lmList)
        # Check if clicked
        length, info, img = detector.findDistance(lmList[8], lmList[12], img)
        print(length)
        if length <50 :
            cursor = lmList[8]
            for imgObject in listImg:
                imgObject.update(cursor)
    try:

        for imgObject in listImg:
            print (hands)
            # Draw for JPG image
            h, w = imgObject.size
            ox, oy = imgObject.posOrigin
            if imgObject.imgType == "png":
                # Draw for PNG Images
                img = cvzone.overlayPNG(img, imgObject.img, [ox, oy])
            else:
                img[oy:oy + h, ox:ox + w] = imgObject.img
    except:
        pass

    # if hands == ox and oy:
    #     os.startfile("C:/Users/GTS/Desktop/New Text Document.txt")

    cv2.imshow("Image", img)
    cv2.waitKey(1)