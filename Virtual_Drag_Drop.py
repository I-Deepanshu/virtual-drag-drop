#Virtual Drag Drop project 
#cvzone model used 1.4.1

import cv2
import cvzone
from cvzone.HandTrackingModule import HandDetector
import numpy as np 

cap = cv2.VideoCapture(0)
cap.set(3,1280)
cap.set(4,720)

detector=HandDetector(detectionCon=1)
color=(255,0,255)

cx,cy,w,h=100,100,200,200

class DragRect():
    def __init__(self,posCenter,size=[200,200]):
        self.posCenter=posCenter
        self.size=size
    def update(self,cursor):
        cx,cy=self.posCenter
        w,h=self.size

        #If the index fingure tip is in the rectangle region 
        if cx-w//2<cursor[0]<cx+w//2 and cy-h//2<cursor[1]<cy+h//2:
                color = 0,255,0
                self.posCenter=cursor

#for multiple rectangles
rectList=[]
for x in range(5):
    rectList.append(DragRect([x*250+150,150]))

while True:
    success, img = cap.read()
    img=cv2.flip(img,1)
    img= detector.findHands(img)
    lmsList, _ = detector.findPosition(img)
    
    if lmsList:

        len,_,_=detector.findDistance(8,12,img,draw=False)

        #print(len) #it helps us in finding the minimum value which is required 
        #for value which we will put in the findDistance

        if len < 40:
            cursor=lmsList[8] #index finger tip landmark
            for rect in rectList:
                #print(1)
                rect.update(cursor) 
                #print(2)
                #print(1) and print(2) is to crossverify that the update command is working

    #to draw  solid 
    # for rect in rectList:
    #     cx,cy=rect.posCenter
    #     w,h = rect.size
    #     cv2.rectangle(img,(cx-w//2,cy-h//2),(cx+w//2,cy+h//2),color,cv2.FILLED)
        
    #     #cvzone.cornerRect(img,(cx-w//2,cy-h//2,w,h),20,rt=0) 
    #     #this is used to provide the corner lines in a shape of rectangles 
    
    # cv2.imshow("Image",img)
    # cv2.waitKey(1)

    
    #to draw transparent
    imgNew=np.zeros_like(img,np.uint8)
    for rect in rectList:
        cx,cy=rect.posCenter
        w,h = rect.size
        cv2.rectangle(imgNew,(cx-w//2,cy-h//2),(cx+w//2,cy+h//2),color,cv2.FILLED)
        cvzone.cornerRect(imgNew,(cx-w//2,cy-h//2,w,h),20,rt=0) 
    out=img.copy()
    alpha=.5
    mask=imgNew.astype(bool)
    out[mask]=cv2.addWeighted(img,alpha,imgNew,1-alpha,0)[mask]

    cv2.imshow("Image",out)
    cv2.waitKey(1)
