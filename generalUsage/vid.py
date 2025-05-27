import cv2
import pickle
import cvzone
import numpy as np
from PIL import Image

# This is video feed

car1=Image.open("carFar1.png")

width,height=car1.size

def lotIdentify(video):
    vid=cv2.VideoCapture(video)

    with open("genPark","rb") as f:
        posList=pickle.load(f)

    def checkParkingSpace(imgProc):
        spaceCounter=0
        
        for pos in posList:
            x,y=pos
            
            imgCrop=imgProc[y:y+height,x:x+width]
            count=cv2.countNonZero(imgCrop)

            if count<900:   # no car
                color=(0,255,0)     # green
                thickness=5     # more thickness for visibility 
                spaceCounter+=1
            else:   # car
                color=(0,0,255)     # red
                thickness=2
            
            # add suitable rectangle as per the space availability
            cv2.rectangle(img,pos,(pos[0]+width,pos[1]+height),
                        color,thickness)
            cvzone.putTextRect(img, f'Free: {spaceCounter}/{len(posList)}', (100, 50), scale=3,
                            thickness=5, offset=20, colorR=(0,200,0))
            
    while True:
        
        if vid.get(cv2.CAP_PROP_POS_FRAMES)== vid.get(cv2.CAP_PROP_FRAME_COUNT):
            vid.set(cv2.CAP_PROP_POS_FRAMES,0)
        sucess,img = vid.read()
        
        imgGray=cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
        imgBlur=cv2.GaussianBlur(imgGray,(3,3),1)
        imgThreshold=cv2.adaptiveThreshold(imgBlur,255,cv2.ADAPTIVE_THRESH_GAUSSIAN_C,
                                        cv2.THRESH_BINARY_INV,25,16)
        imgMedian=cv2.medianBlur(imgThreshold,5)
        kernel=np.ones((3,3),np.int8)
        imgDilate=cv2.dilate(imgMedian,kernel,iterations=1)
        
        checkParkingSpace(imgDilate)
        
        cv2.imshow("Image",img)
        cv2.waitKey(10)
        
lotIdentify("carFar2.mp4")