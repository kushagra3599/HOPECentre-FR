import cv2
import numpy as np
import sqlite3


def getProfile(id):
    conn=sqlite3.connect("facerecognition.db")
    cmd="SELECT * FROM People WHERE ID = "+str(id)
    cursor=conn.execute(cmd)
    profile=None
    for row in cursor:
        profile=row
    conn.close()
    return profile
def test():

    faceDetect=cv2.CascadeClassifier('haarcascade_frontalface_default.xml');
    cam=cv2.VideoCapture(0);
    rec= cv2.face.LBPHFaceRecognizer_create()
    rec.read("recognizer/trainner.yml")
    font = cv2.FONT_HERSHEY_SIMPLEX
    while(True):
        ret,img=cam.read();
        gray=cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
        faces=faceDetect.detectMultiScale(gray,1.1,10);
        for(x,y,w,h) in faces:
            cv2.rectangle(img,(x,y),(x+w,y+h),(0,255,0),2)
            id,conf=rec.predict(gray[y:y+h,x:x+w])
            profile=getProfile(id)
            if(conf<50):
            
                if(profile!=None):
                    cv2.putText(img,"Name : "+str(profile[1]),(x,y+h+30),font,1.5,(0,0,255));
                    cv2.putText(img,"Age : "+str(profile[2]),(x,y+h+55),font,1,(0,0,255));
                    cv2.putText(img,"Gender : "+str(profile[3]),(x,y+h+80),font,1,(0,0,255));
                    cv2.putText(img,"Confidence : "+str(100-int(conf)),(x,y+h+100),font,1,(0,0,255));
                    cv2.imshow("Face",img);
            else:
                #cv2.putText(img, str("unknown"), (x,y+h+30), font, 1.5, (255,255,255), 3)
                cv2.putText(img,"Confidence : "+str(100-int(conf)),(x,y+h+100),font,1,(0,0,255));
                cv2.imshow('Face',img)
            
            
        if(cv2.waitKey(1)==ord('q')):
            break;
    cam.release()
    cv2.destroyAllWindows()
