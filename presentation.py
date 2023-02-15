import cv2 as cv
import os
from cvzone.HandTrackingModule import HandDetector
from sqlalchemy import false
import numpy as np

width,height=1280,720
folder_path='pic'




#camera setup
cap=cv.VideoCapture(0)
cap.set(3,width)
cap.set(4,height)

#Getting list of images
pathImages=sorted(os.listdir(folder_path),key=len)#sort the img no 1 to n
print(pathImages)

#variable for image number
imgNum=0
hs,ws=int(120*1),int(213*1)



buttonPress=False
buttonCount=0
buttonDelay=15

#Hand Detect
detect=HandDetector(detectionCon=0.8,maxHands=1)

#Annotation to draw on slide frame by point to point
#annotation
annotations=[[]]
annotationNum=0
annotationStart=False


while True:

    istrue,img=cap.read()
    img=cv.flip(img,1)
    #importing images
    imgPath=os.path.join(folder_path,pathImages[imgNum])
    imgCurr=cv.imread(imgPath)

    #line so that we can adjust our hand as per convience


    #hand detect
    hands,img = detect.findHands(img)
    if hands and buttonPress is False:
        hand=hands[0]
        fingers=detect.fingersUp(hand)
        lmList=hand['lmList']
        indexFinger=lmList[8][0],lmList[8][1]

        print(fingers)

        #left and right moving slide
        if fingers==[1,0,0,0,0]: #left
            print("left")
            if imgNum>0:
                buttonPress=True
                annotations=[[]]
                annotationNum=0
                annotationStart=False
                imgNum-=1
        if fingers==[0,0,0,0,1]: #right
            print("right")
            if imgNum<len(pathImages)-1:
                buttonPress=True
                annotations=[[]]
                annotationNum=0
                annotationStart=False
                imgNum+=1   
         # close the ppt       
        if fingers==[0,0,1,1,1]:#rock on symbol
            cv.destroyAllWindows()  
            break       

        #circle point on slide using index and middle finger
        if fingers==[0,1,1,0,0]:
            cv.circle(imgCurr,indexFinger,12,(0,0,255),cv.FILLED)


        #to draw on slide
        if fingers==[0,1,0,0,0]:
            if annotationStart is False:
                annotationStart=True
                annotationNum+=1
                annotations.append([])
            cv.circle(imgCurr,indexFinger,12,(0,0,255),cv.FILLED)
            annotations[annotationNum].append(indexFinger)
        else:
            annotationStart=False


        #eraser
        if fingers==[0,1,1,1,1]:
            if annotations:
                annotations.pop(-1)
                annotationNum-=1
                buttonPress=True    
        
        print(annotationNum)


    #button press iteration slow down the slide speed
    if buttonPress:
        buttonCount+=1
        if buttonCount>buttonDelay:
            buttonCount=0
            buttonPress=False



    #drawing on slide to append annotations
    for i in range(len(annotations)):
        for j in range(len(annotations[i])):
            if j!=0:
                cv.line(imgCurr,annotations[i][j-1],annotations[i][j],(0,0,255),12)       

    #Adding Webcam on top of the image
    imgSmall=cv.resize(img,(ws,hs))
    h, w, _ =imgCurr.shape
    imgCurr[0:hs,w-ws:w]=imgSmall







    # cv.imshow("images",imgCurr)
    # cv.imshow("vdo",img)
    if cv.waitKey(4) &  0xFF==ord('q'):
        break