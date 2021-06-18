import cv2
import numpy as np
import sqlite3
from imutils.video import WebcamVideoStream

class VideoCamera(object):
    def __init__(self):
        self.stream = WebcamVideoStream(src=0).start()
        global faceDetect, rec, font
        faceDetect=cv2.CascadeClassifier('haarcascade_frontalface_default.xml');
        
        rec= cv2.face.LBPHFaceRecognizer_create()
        rec.read("recognizer/trainner.yml")
        font = cv2.FONT_HERSHEY_SIMPLEX
        
    def __del__(self):
        self.stream.stop()
    
        

    def get_frame(self):
        image = self.stream.read()
        
        
        
        gray=cv2.cvtColor(image,cv2.COLOR_BGR2GRAY)
        faces=faceDetect.detectMultiScale(gray,1.1,5);
        for(x,y,w,h) in faces:
            cv2.rectangle(image,(x,y),(x+w,y+h),(0,255,0),2)
            id,conf=rec.predict(gray[y:y+h,x:x+w])
            
            conn=sqlite3.connect("facerecognition.db")
            cmd="SELECT * FROM People WHERE ID = "+str(id)
            cursor=conn.execute(cmd)
            profile=None
            for row in cursor:
                profile=row
            conn.close()
            

            
            if(conf<60):
                
                if(profile!=None):
                    cv2.putText(image,"Name : "+str(profile[1]),(x,y+h+30),font,1.5,(0,0,255));
                    cv2.putText(image,"Age : "+str(profile[2]),(x,y+h+55),font,1,(0,0,255));
                    cv2.putText(image,"Gender : "+str(profile[3]),(x,y+h+75),font,1,(0,0,255));
                    cv2.putText(image,"Location : "+str(profile[4]),(x,y+h+100),font,1,(0,0,255));
                    
            else:
                cv2.putText(image, str("unknown"), (x,y+h+30), font, 1.5, (255,255,255), 2)
                
        ret, jpeg = cv2.imencode('.jpg', image)
        data = []
        data.append(jpeg.tobytes())
        return data        
        





       
       
