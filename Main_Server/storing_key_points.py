# -*- coding: utf-8 -*-
"""
Created on Fri Mar  9 09:17:24 2018

@author: DELL
"""

import numpy as np
import cv2
import math
import _pickle as pickle

  
# cap = cv2.VideoCapture('v2.mp4')
count=0
while(count<1):
    # ret1, img1 = cap.read()
    # ret2, img2 = cap.read()
    train_img = []
    for i in range(0,110):
        fp = "Main_Database/SIT1stfloor/"+str(i)+".jpg"
        frame = cv2.imread(fp)
        train_img.append(frame)
        
    print("All images read")   
          
    # find the keypoints and descriptors with SIFT
    #********changed *******
    sift = cv2.xfeatures2d.SIFT_create()
    # orb = cv2.ORB_create(nfeatures = 100)
    

    count+=1
    # find the keypoints and descriptors with SIFT
    keypt_vector=[]
    
    for img in train_img :
        i=0
        kp ,des = sift.detectAndCompute(img,None)
        img_keypt = []
        for point in kp:
            temp = (point.pt, point.size, point.angle, point.response, point.octave,point.class_id, des[i])
            i+=1     
            img_keypt.append(temp)           
    
        keypt_vector.append(img_keypt)
    pickle.dump(keypt_vector,open("keypoint_database.p","wb"))     
        


