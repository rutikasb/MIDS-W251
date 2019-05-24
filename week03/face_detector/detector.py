#!/usr/bin/env python

import numpy as np
import cv2
import paho.mqtt.client as mqtt
import time

# 1 should correspond to /dev/video1, the USB camera. The 0 is reserved for the TX2 onboard camera
cap = cv2.VideoCapture(1)
print("Is cap opened:", cap.isOpened())

# create mqtt client for publishing
mqttc = mqtt.Client()
mqttc.connect("broker", port=1883)

# pre-trained frontal face HAAR Cascade Classifier 
face_cascade = cv2.CascadeClassifier('/opt/opencv/data/haarcascades/haarcascade_frontalface_default.xml')
print("Loaded model")

while(True):
    # capture frame-by-frame
    ret, frame = cap.read()

    time.sleep(1)
    # if frame is captured correctly
    if ret == True:
        print("captured image")
        # convert image to gray scale
        gray_img = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

        # face detection
        faces = face_cascade.detectMultiScale(gray_img, 1.3, 5)
        for (x, y, w, h) in faces:
            # create a rectangle around the face
            cv2.rectangle(gray_img, (x,y), (x+w,y+h), (255,0,0), 2)

            rc, jpg = cv2.imencode('.png', gray_img)
            msg = jpg.tobytes()
            # forward to mqtt broker on jetson
            print("publishing message")
            mqttc.publish("faces", msg)
            # cv2.imshow('img', gray_img)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
