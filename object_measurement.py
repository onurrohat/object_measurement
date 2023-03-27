import cv2
import numpy as np
import utils



cam= False

cap=cv2.VideoCapture(0)

path="test4.jpeg"

cap.set(10,160)
cap.set(3,1920)
cap.set(4,1080)
scale=3
wP=210 * scale
hP =297 *scale
scm= scale*10 # for mm to cm
fSpc=0

totalspc = 609


while True:
    if cam :success,img=cap.read()

    else: img=cv2.imread(path)

    imgContours, conts = utils.getContours(img,minArea=5000,filter=4)

    if len(conts)!=0:
        biggest = conts [0][2]
        
        imgWarp=utils.warpImg (img,biggest,wP,hP)
        
    
        imgContours2, conts2 = utils.getContours(imgWarp,minArea=2000,filter=4,threshold=[170,170],draw=False)
        

        if len(conts) !=0:
            for obj in conts2:
                cv2.polylines(imgContours2,[obj[2]],True,(0,255,0),2)
                nPoints=utils.reorder(obj[2])
                          
               
                e1=[nPoints[0],0] #also e3
                e2= [0,nPoints[1]] #also e5
                e4=[630,nPoints[1]] #also e8
                e6=[nPoints[0],891] #also e7
                

                fD1=utils.freeSpc(nPoints[0][0])
                fD2=utils.freeSpc(nPoints[1][0])
                fD3=utils.freeSpc(nPoints[2][0])
                fD4=utils.freeSpc(nPoints[3][0])

                #print(nPoints[1][0][1])
                #print(type(nPoints[1][0][1]))
                print(nPoints)
                allpoints = []

        

                allpoints.append(nPoints)


                #print(type(nPoints))
                #print(allpoints)

                pW=round(utils.findDis(nPoints[0][0]// scm, nPoints[1][0]//scm)/1,1) # width of product in cm
                pH=round(utils.findDis(nPoints[0][0]// scm, nPoints[2][0]//scm)/1 ,1) # height of product in cm
                

                
                #print(nPoints[3][0])
                
                
                #print(totalspc)
                fSpc= totalspc - (pW*pH) ## free space for another product in cm*2
                totalspc=fSpc
                #print(pW*pH)
              
              


                for x in range(len(nPoints)-1) :
                    if nPoints[x][0][1] >495 :
                        oPb=min(fD1[2],fD2[2],fD3[2],fD4[2])# free length  over the product at the bottom shelf
                        usop=[]
                        usop.append(oPb)
                        
                        rP=min(fD1[3],fD2[3],fD3[3],fD4[3])# max free length  to the right side of the products at the bottom shelf
                        urPall=[]
                        urPall.append(rP)
                        lP=min(fD1[1],fD2[1],fD3[1],fD4[1])# max free length to the left side of the products at the bottom shelf
                        ulPall=[]
                        ulPall.append(lP)
                    elif nPoints[x][0][1] < 495 :
                        oP=min(fD1[0],fD2[0],fD3[0],fD4[0])# max free length  over the product at the top shelf
                        tsop=[]
                        tsop.append(oP)
                        rP=min(fD1[3],fD2[3],fD3[3],fD4[3])# max free length  to the right side of the products
                        trPall=[]
                        trPall.append(rP)
                        lP=min(fD1[1],fD2[1],fD3[1],fD4[1])# max free length to the left side of the products
                        tlPall=[]
                        tlPall.append(lP)
                        
                
                
                rP=min(fD1[3],fD2[3],fD3[3],fD4[3])# max free length  to the right side of the product
                lP=min(fD1[1],fD2[1],fD3[1],fD4[1])# max free length to the left side of the product

                #print(" max free length  under the product : " ,uP,"\n"
                 #     " max free length over the product:",oP,"\n",
                  #     "max free length  to the right side of the product",rP,"\n",
                   #     "max free length to the left side of the product",lP)
                

                cv2.arrowedLine(imgContours2, (nPoints[0][0][0], nPoints[0][0][1]), (nPoints[1][0][0], nPoints[1][0][1]),
                                (255, 0, 255), 3, 8, 0, 0.05)
                cv2.arrowedLine(imgContours2, (nPoints[0][0][0], nPoints[0][0][1]), (nPoints[2][0][0], nPoints[2][0][1]),
                                (255, 0, 255), 3, 8, 0, 0.05)
                x, y, w, h = obj[3]
                cv2.putText(imgContours2, '{}cm'.format(pW), (x + 30, y - 10), cv2.FONT_HERSHEY_COMPLEX_SMALL, 1.5,
                            (255, 0, 255), 2)
                cv2.putText(imgContours2, '{}cm'.format(pH), (x - 70, y + h // 2), cv2.FONT_HERSHEY_COMPLEX_SMALL, 1.5,
                            (255, 0, 255), 2)

        cv2.imshow("Wrapped",imgContours2)
    imgContours2=cv2.resize(img,(0,0),None,0.5,0.5)

    
    print("max free length  over the product at the top shelf " ,min(tsop))
    print("max free length  right side of the product at the top shelf " ,min(trPall))
    print("max free length  left the product at the top shelf " ,min(tlPall))
    print("max free length  over the product at the bottom shelf ", min(usop))
    print("max free length  right the product at the bottom shelf " ,min(urPall))
    print("max free length  left the product at the bottom shelf " ,min(ulPall))
    
    
    #print( "You have ",fSpc," cm*2 free space" )
    #cv2.imshow("Original",img)
    cv2.waitKey(1)
    


 