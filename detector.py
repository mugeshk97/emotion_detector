from tensorflow.keras.models import load_model
from time import sleep
import tensorflow as tf
from tensorflow.keras.preprocessing import image
import cv2
import numpy as np


face_classifier=cv2.CascadeClassifier('haarcascade_frontalface_default.xml')
model=load_model('emotionv1.0.h5')

class_labels = ['Angry','Disgust','Fear','Happy','Sad','Surprise','Neutral']

cap=cv2.VideoCapture(0)

while True:
    # Grab a single frame of video
    ret, frame = cap.read()
    labels = []
    gray = cv2.cvtColor(frame,cv2.COLOR_BGR2GRAY)
    faces = face_classifier.detectMultiScale(gray,1.3,5)

    for (x,y,w,h) in faces:
        cv2.rectangle(frame,(x,y),(x+w,y+h),(255,0,0),2)
        roi_gray = gray[y:y+h,x:x+w]
        roi_gray=np.expand_dims(roi_gray,2)
        roi_gray = np.resize(roi_gray,(48,48,1))
        
        

        if np.sum([roi_gray])!=0:
            roi = roi_gray.astype('float')/255.0
            roi = np.array(roi)
            roi = np.expand_dims(roi,axis=0)

        
            preds = model.predict(roi)[0]
            label=class_labels[preds.argmax()]
            label_position = (x,y)
            cv2.putText(frame,label,label_position,cv2.FONT_HERSHEY_SIMPLEX,2,(0,255,0),3)
        else:
            cv2.putText(frame,'No Face Found',(20,60),cv2.FONT_HERSHEY_SIMPLEX,2,(0,255,0),3)
    cv2.imshow('Emotion Detector',frame)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
