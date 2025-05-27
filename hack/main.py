import cv2
import pickle
import cvzone
import numpy as np

# This is video feed
vid=cv2.VideoCapture("carPark.mp4")

width,height=107,48

with open("myCarPark","rb") as f:
    posList=pickle.load(f)

def checkParkingSpace(imgProc):
    spaceCounter=0
    
    for pos in posList:
        x,y=pos
        
        imgCrop=imgProc[y:y+height,x:x+width]
        # cv2.imshow(str((x*y)),imgCrop)
        count=cv2.countNonZero(imgCrop)
        # cvzone.putTextRect(img,str(count),(x,y+height-5),scale=2,thickness=1,offset=0)

        if count<900:
            color=(0,255,0)
            thickness=6
            spaceCounter+=1
        else:
            color=(0,0,255)
            thickness=2
        
        cv2.rectangle(img,pos,(pos[0]+width,pos[1]+height),
                      color,thickness)
        cvzone.putTextRect(img,str(count),(x,y+height-3),scale=1,
                           thickness=2,offset=0,colorR=color)
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
    #for pos in posList:
    #   cv2.rectangle(img,pos,(pos[0]+width,pos[1]+height),(255,0,255),2)
        
    cv2.imshow("Image",img)
    #cv2.imshow("ImageBlur",imgBlur)
    #cv2.imshow("ImageThreshold",imgThreshold)
    cv2.waitKey(10)