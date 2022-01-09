import cv2
from cvzone.HandTrackingModule import HandDetector
import cvzone
import os
import webbrowser
import pyttsx3


engine = pyttsx3.init()
voices = engine.getProperty('voices')

# changing index changes voices but only
# 0 and 1 are working here
engine.setProperty('voice', voices[1].id)
engine.runAndWait()

cap = cv2.VideoCapture(0)
cap.set(4, 1920)
cap.set(3, 1280)

detector = HandDetector(detectionCon=0.65)

img1 = cv2.imread("C:/Users/GTS/PycharmProjects/DragNdROP/Images/ttu100.png")
#img2 = cv2.imread("C:/Users/GTS/PycharmProjects/DragNdROP/Images/OIP.jpg")
pyttsx3.speak("system loading ...  ")
pyttsx3.speak("GOOD Morning sir ,"
              "what you want to do today?  ")
ox, oy = 500,200

while True:
    success, img = cap.read()
    #img = cv2.flip(img, 1)
    hands, img = detector.findHands(img, flipType= False)

    if hands:
        lmList= hands[0]["lmList"]

        cursor = lmList[8]

        if ox < cursor[0] < ox +w and oy < cursor[1] <oy +h :
            pyttsx3.speak("Opening T T U wbsite  ")
            webbrowser.open("http://www.ttu.edu.jo/")
        #
        # elif ox < cursor[0] < ox +213 and oy < cursor[1] <oy +198 :
        #     pyttsx3.speak("Opening YouTube website  ")
        #     webbrowser.open("https://www.youtube.com/")



    h , w , _ = img1.shape
    img[oy:oy + h , ox:ox + w ] = img1

    # img[oy:oy + 198  , ox:ox + 213  ] = img2

    cv2.imshow('image',img)
    cv2.waitKey(1)