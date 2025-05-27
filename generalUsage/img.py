import cv2
import pickle
from PIL import Image

# This is for image

car1=Image.open("carFar1.png")

def imageMarks(imgInput):

    width,height=car1.size

    try: 
        with open("genPark","rb") as f:
            posList=pickle.load(f)
    except:
        posList=[]
        
    def mouseClick(events,x,y,flags,params):
        if events==cv2.EVENT_LBUTTONDOWN:
            posList.append((x,y))
        if events==cv2.EVENT_RBUTTONDOWN:
            for i,pos in enumerate(posList):
                x1,y1=pos
                if x1<x<x1+width and y1<y<y+height:
                    posList.pop(i)
                    
        with open("genPark","wb") as f:
            pickle.dump(posList,f)
            
    while True:
        img=cv2.imread(imgInput)
        
        for pos in posList:
            cv2.rectangle(img, pos, (pos[0] + width, pos[1] + height), (255, 0, 255), 2)
            
        cv2.imshow("Image", img)
        cv2.setMouseCallback("Image", mouseClick)
        cv2.waitKey(1)
        
imageMarks("carFarImg.png")