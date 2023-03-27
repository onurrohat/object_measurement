import cv2
import numpy as np


def getContours(img,threshold=[100,100],showCanny=False, minArea=1000 ,filter = 0, draw = False):

    imgGray=cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
    cv2.imshow("Blurrd",imgGray)
    imgBlur = cv2.GaussianBlur(imgGray,(5,5),1)
    cv2.imshow("Blurred",imgBlur)
    imgCanny=cv2.Canny(imgBlur,threshold[0],threshold[1])
    cv2.imshow("Canny",imgCanny)
    kernel=np.ones((5,5))
    imgDial=cv2.dilate(imgCanny,kernel,iterations=3)
    imgErod=cv2.erode(imgDial,kernel,iterations=2 )
    
  

    if showCanny :cv2.imshow("Canny",imgErod)

    contours,hiearchy=cv2.findContours(imgErod,cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_NONE)
    finalContours =[]

    for i in contours:
        area=cv2.contourArea(i)
        if area >minArea:
            peri= cv2.arcLength(i,True)
            approx=cv2.approxPolyDP(i,0.02*peri,True)
            bbox=cv2.boundingRect(approx)
            if filter > 0:
                if len(approx) ==filter :
                    finalContours.append([len(approx),area,approx,bbox,i])
            else:
                finalContours.append([len(approx),area,approx,bbox,i])
    finalContours=sorted(finalContours,key = lambda x:x[1],reverse=True)

    if draw :
        for con in finalContours:
            cv2.drawContours(img,con[4],-1,(0,0,255),3)

    return img,finalContours

def reorder(myPoints):
    #print(myPoints.shape)
    newPoints=np.zeros_like(myPoints)
    myPoints=myPoints.reshape((4,2))
    add = myPoints.sum(1)


    newPoints[0]=myPoints[np.argmin(add)]
    newPoints[3] = myPoints[np.argmax(add)]

    diff =np.diff(myPoints,axis=1)


    newPoints[1]=myPoints[np.argmin(diff)]
    newPoints[2] = myPoints[np.argmax(diff)]

    return newPoints

    

def warpImg (img,points,w,h,pad=5):
    points=reorder(points)
    pts1 = np.float32(points)
    pts2 = np.float32([[0,0],[w,0],[0,h],[w,h]])
   
    matrix= cv2.getPerspectiveTransform(pts1,pts2)
    imgWarp =cv2.warpPerspective(img,matrix,(w,h))
    imgWarp = imgWarp[pad:imgWarp.shape[0]-pad,pad:imgWarp.shape[1]-pad]
 

    return imgWarp

def findDis(pts1,pts2):
    #print(pts1.shape)
    
    return ((pts2[0]-pts1[0])**2+(pts2[1]-pts1[1])**2)**0.5

def freeSpc(pts):
    #print(pts.shape)
    e1=[pts[0],0]#also e3  free space for Y axis in points 1,2
    e2=[0,pts[1]]#also e5 free space for X axis in points 1,3
    e6=[pts[0],495]#also e7  free space Y axis in points 3,4
    e4=[630,pts[1]]#also e8 free space X axis  in points 2,4
    
    


    
    d1 =(pts[1]-e1[1]) #also d3
    d1=abs(d1)
    d2=(pts[0]-e2[0]) #also d5
    d2=abs(d2)
    d6 =(pts[1]-e6[1]) # also d7
    d6=abs(d6)
    d4=(pts[0]-e4[0]) #also d8 
    d4=abs(d4)

    lst=[d1,d2,d6,d4]
    lst=[int(x) for x in lst]
    


    
    return lst


    




    
    




