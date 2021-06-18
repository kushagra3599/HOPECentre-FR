import cv2
import numpy as np
import sqlite3


def insertOrUpdate(Name,Age,Gen,Loc):
    conn=sqlite3.connect("facerecognition.db")
    cursor= conn.execute('SELECT max(Id) from People')
    Id = cursor.fetchone()[0]
    if(Id == None):
        Id=0
    Id+=1
    cmd="SELECT * FROM People WHERE ID = "+str(Id)
    cursor=conn.execute(cmd)
    isRecordExist=0
    for row in cursor:
        isRecordExist=1
    if(isRecordExist==1):
        conn.execute("UPDATE People SET Name =? WHERE ID =?",(Name,Id))
        conn.execute("UPDATE People SET Age =? WHERE ID =?",(Age,Id))
        conn.execute("UPDATE People SET Gender =? WHERE ID =?",(Gen,Id))
        conn.execute("UPDATE People SET Location =? WHERE ID =?",(Loc,Id))
       
    else:
        params= (Id, Name, Age, Gen, Loc)
        conn.execute("INSERT INTO People Values(?, ?, ?, ?, ?)",params)
        cmd2=""
        cmd3=""
       
    
    
    conn.commit()
    conn.close()
    return Id
def test(form_name, form_age, form_gen, form_loc):
    
    faceDetect=cv2.CascadeClassifier('haarcascade_frontalface_default.xml');
    cam=cv2.VideoCapture(0);
    
    name = str(form_name)
    age = int(form_age)
    gen = form_gen
    loc = str(form_loc)
    

    Id=insertOrUpdate(name,age,gen,loc)
    sampleNum=0
    while(True):
        ret,img=cam.read();
        gray=cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
        faces=faceDetect.detectMultiScale(gray,1.1,5);
        for(x,y,w,h) in faces:
            sampleNum=sampleNum+1;
            cv2.imwrite("dataSet/User."+str(Id)+"."+str(sampleNum)+".jpg",gray[y:y+h,x:x+w])
            cv2.rectangle(img,(x,y),(x+w,y+h),(0,255,0),2)
            cv2.waitKey(50);
        cv2.imshow("Face",img);
        if(sampleNum>30):
            break;
    cam.release()
    cv2.destroyAllWindows()
